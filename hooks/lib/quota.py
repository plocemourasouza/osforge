#!/usr/bin/env python3
"""
hooks/lib/quota.py — quota-window state: read, record, and decide what to tell the model (B-027,
SPEC-L01 Parte A). Stdlib only; every public function is tolerant of missing/malformed input and
never raises.

The file `~/.osforge/quota.json` (override: OSFORGE_QUOTA_FILE) is the single source of truth,
schema `osforge.quota.v1`:

    {"schema": "osforge.quota.v1", "at": 1790000000, "source": "statusline",
     "five_hour": {"pct": 83.0, "resets_at": 1790012345},
     "seven_day": {"pct": 41.0, "resets_at": 1790500000},
     "rejected": null}

Two writers feed it, both defined here:
  - `record_statusline(payload)` — A1, called by hooks/quota-record.py with the statusline's
    stdin JSON. No-op (keeps the existing file untouched) when `rate_limits` is missing or null
    (EV-C01: happens for API-key/Bedrock/Vertex auth).
  - `record_rejection(quota_limits)` — A2, called by hooks/session-save.py when the transcript's
    tail holds a rate-limit rejection line (EV-C04). `source` becomes "transcript"; independent
    of the statusline.

One reader feeds the warning and, later, the eval harness (Part B, not implemented here):
  - `read_state(now)` — parsed dict if the file is schema-valid AND fresh (`at` within
    STALE_SECONDS), else None. "Fresh-or-None": callers never see a stale record.

One decision function drives A3, called from hooks/context-threshold.py:
  - `pending_warning(now)` — the message to inject via additionalContext, or None. Warns once per
    band per WINDOW (keyed by `five_hour.resets_at`, not by session — the window crosses
    sessions) and once per rejection (keyed by `rejected.resets_at`). State for "already warned"
    lives in a sibling file (`<quota file>.warned`), so the kill-switch and the `at` staleness
    rule apply only to the underlying data, not to whether a given band/rejection was already
    surfaced.

`read_state`'s staleness gate exempts `rejected` (B-026, SPEC-L01 Part B, item 4): the overall
`at`-based staleness check still hides stale usage numbers (`five_hour`/`seven_day`), but a
`rejected` fact does not go stale just because nothing refreshed quota.json since the Stop event
that recorded it — it is still true that the last window ended in rejection, and the rejection's
own `resets_at` still tells a caller (A3's warning, or the eval harness's B3 preflight) whether
that window is still closed. Previously the uniform gate discarded `rejected` too whenever `at`
aged past STALE_SECONDS, blinding both callers to a rejection whose reset was still in the
future or had passed recently.

Kill-switch: OSFORGE_QUOTA_THRESHOLD=off (independent of OSFORGE_CONTEXT_THRESHOLD).
Bands: OSFORGE_QUOTA_BANDS="80,95" (default), same overlapping-band idiom as context-threshold.py.
"""
import json
import os
import time

SCHEMA = "osforge.quota.v1"
STALE_SECONDS = 15 * 60
MAX_FILE_BYTES = 1024 * 1024          # same cap as the recorder's stdin (defense in depth)
DEFAULT_BANDS = (80, 95)

BAND_MESSAGES = {
    1: ("Janela de 5h em {pct:.0f}% (reseta {reset_hhmm} local): termine o passo atual; "
        "não abra ondas paralelas nem subagentes novos."),
    2: ("Janela de 5h em {pct:.0f}%: PARE e grave o handoff agora "
        "(`osforge-db set-resume <slug> \"…\"` ou plano). Você pode ser cortado no próximo turno."),
}
REJECTED_MESSAGE = "A janela anterior foi rejeitada às {rej_hhmm} local; confira o handoff antes de retomar."
SEVEN_DAY_NOTE = " (janela de 7 dias em {pct:.0f}%)"


# ── paths ────────────────────────────────────────────────────────────────────

def quota_path():
    return os.environ.get("OSFORGE_QUOTA_FILE") or os.path.expanduser("~/.osforge/quota.json")


def _warned_path():
    return quota_path() + ".warned"


def _is_off():
    return os.environ.get("OSFORGE_QUOTA_THRESHOLD", "").strip().lower() in ("off", "0", "false")


def _bands():
    raw = os.environ.get("OSFORGE_QUOTA_BANDS", "")
    try:
        vals = tuple(sorted(int(x) for x in raw.split(",") if x.strip()))
        return vals if len(vals) == 2 else DEFAULT_BANDS
    except ValueError:
        return DEFAULT_BANDS


def _band_for(pct, bands):
    if pct >= bands[1]:
        return 2
    if pct >= bands[0]:
        return 1
    return 0


def _hhmm(epoch):
    try:
        return time.strftime("%H:%M", time.localtime(epoch))
    except Exception:
        return "?"


# ── low-level read/write ────────────────────────────────────────────────────

def _read_json(path):
    """Tolerant JSON read capped at MAX_FILE_BYTES. None on anything wrong."""
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return None
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def _atomic_write(path, data):
    try:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def _read_warned():
    return _read_json(_warned_path()) or {}


def _write_warned(state):
    _atomic_write(_warned_path(), state)


# ── A1 + A2: writers ─────────────────────────────────────────────────────────

def record_statusline(payload, now=None):
    """A1. `payload` is the FULL statusline stdin object. Merges `rate_limits.five_hour` /
    `.seven_day` (renaming `used_percentage` -> `pct`) into quota.json. Never writes when
    `rate_limits` is missing or null (keeps the existing file intact). Returns True on write."""
    try:
        if not isinstance(payload, dict):
            return False
        rl = payload.get("rate_limits")
        if not isinstance(rl, dict):
            return False
        now = now if now is not None else time.time()
        existing = _read_json(quota_path()) or {}
        record = dict(existing)
        wrote_any = False
        for key in ("five_hour", "seven_day"):
            sub = rl.get(key)
            if not isinstance(sub, dict):
                continue
            entry = {}
            pct = sub.get("used_percentage")
            resets_at = sub.get("resets_at")
            if isinstance(pct, (int, float)):
                entry["pct"] = pct
            if isinstance(resets_at, (int, float)):
                entry["resets_at"] = resets_at
            if entry:
                record[key] = entry
                wrote_any = True
        if not wrote_any:
            return False
        record["schema"] = SCHEMA
        record["at"] = now
        record["source"] = "statusline"
        record.setdefault("rejected", existing.get("rejected"))
        return _atomic_write(quota_path(), record)
    except Exception:
        return False


def record_rejection(quota_limits, now=None):
    """A2. `quota_limits` is the transcript line's `quotaLimits` object (EV-C04). No-op unless
    `status == "rejected"` and a numeric `resetsAt` is present. `source` becomes "transcript"."""
    try:
        if not isinstance(quota_limits, dict) or quota_limits.get("status") != "rejected":
            return False
        resets_at = quota_limits.get("resetsAt")
        if not isinstance(resets_at, (int, float)):
            return False
        now = now if now is not None else time.time()
        existing = _read_json(quota_path()) or {}
        record = dict(existing)
        record["schema"] = SCHEMA
        record["at"] = now
        record["source"] = "transcript"
        record["rejected"] = {
            "type": quota_limits.get("rateLimitType"),
            "resets_at": resets_at,
            "at": now,
        }
        return _atomic_write(quota_path(), record)
    except Exception:
        return False


# ── reader ───────────────────────────────────────────────────────────────────

def read_state(now=None):
    """Parsed quota.json if schema-valid, else None. When `at` is fresh (within STALE_SECONDS of
    `now`), returns the full record. When `at` is stale, returns None UNLESS `rejected` is
    present -- in that case returns a minimal record carrying only `rejected` (usage numbers are
    dropped: they really are stale). Used by A3 here, and by the eval harness's B3 preflight
    (Part B)."""
    now = now if now is not None else time.time()
    data = _read_json(quota_path())
    if data is None or data.get("schema") != SCHEMA:
        return None
    at = data.get("at")
    if not isinstance(at, (int, float)):
        return None
    if now - at <= STALE_SECONDS:
        return data
    rejected = data.get("rejected")
    if isinstance(rejected, dict):
        return {"schema": SCHEMA, "at": at, "source": data.get("source"), "rejected": rejected}
    return None


# ── A3: the decision ─────────────────────────────────────────────────────────

def pending_warning(now=None):
    """The additionalContext text for A3, or None. Applies its own kill-switch
    (OSFORGE_QUOTA_THRESHOLD=off). Warns once per band per window (keyed by
    `five_hour.resets_at`) and once per rejection (keyed by `rejected.resets_at`); state is
    global (not per-session) because the window crosses sessions."""
    if _is_off():
        return None
    try:
        now = now if now is not None else time.time()
        state = read_state(now)
        if state is None:
            return None
        warned = _read_warned()
        parts = []
        changed = False

        five = state.get("five_hour")
        if isinstance(five, dict):
            pct = five.get("pct")
            resets_at = five.get("resets_at")
            if (isinstance(pct, (int, float)) and isinstance(resets_at, (int, float))
                    and resets_at > now):
                band = _band_for(pct, _bands())
                prev_band = warned.get("band", 0) if warned.get("resets_at") == resets_at else 0
                if band > 0 and band > prev_band:
                    parts.append(BAND_MESSAGES[band].format(pct=pct, reset_hhmm=_hhmm(resets_at)))
                    warned["resets_at"] = resets_at
                    warned["band"] = band
                    changed = True

        rejected = state.get("rejected")
        if isinstance(rejected, dict):
            r_reset = rejected.get("resets_at")
            if (isinstance(r_reset, (int, float)) and now >= r_reset
                    and warned.get("rejected_resets_at") != r_reset):
                parts.append(REJECTED_MESSAGE.format(rej_hhmm=_hhmm(r_reset)))
                warned["rejected_resets_at"] = r_reset
                changed = True

        if not parts:
            return None

        seven = state.get("seven_day")
        if isinstance(seven, dict):
            pct7 = seven.get("pct")
            if isinstance(pct7, (int, float)) and pct7 >= 90:
                parts.append(SEVEN_DAY_NOTE.format(pct=pct7))

        if changed:
            _write_warned(warned)
        return "[OSForge quota-guard] " + " ".join(parts)
    except Exception:
        return None
