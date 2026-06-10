/**
 * OSForge Canvas — single-file Bun server (viewer SPA host + artifact feedback loop).
 *
 * ┌─────────────────────────────────────────────────────────────────────────┐
 * │ SECURITY MODEL: LOCAL-ONLY BY DESIGN.                                     │
 * │                                                                          │
 * │ This server binds explicitly to 127.0.0.1 and has NO authentication.     │
 * │ That is intentional, not an oversight. The threat model is "another      │
 * │ machine / another user on the network", and we neutralize it by removing │
 * │ the network vector entirely (loopback bind) rather than by bolting auth   │
 * │ onto a dev tool. Per skills/security/insecure-defaults.md, fail-secure    │
 * │ means closing the attack surface — here the surface is the listener, so   │
 * │ we close it. DO NOT bind 0.0.0.0 or add a public route without revisiting │
 * │ this: it would expose unauthenticated read/write of local artifacts.     │
 * │                                                                          │
 * │ Defenses still applied (defense in depth):                               │
 * │  - :id sanitized to [a-z0-9_-] to block path traversal.                  │
 * │  - Writes are confined to outputs/canvas/feedback/ via basename only.    │
 * │  - POST feedback is structurally validated before it touches disk.       │
 * └─────────────────────────────────────────────────────────────────────────┘
 *
 * Run:  bun scripts/canvas/server.ts [--dir=<path>]
 * Env:  CANVAS_PORT (default 4242)
 *
 * Zero npm dependencies. Bun + node:fs only.
 */

import { watch, type FSWatcher } from "node:fs";
import { mkdir } from "node:fs/promises";
import { resolve, join } from "node:path";

// ── Constants ───────────────────────────────────────────────────────────────

const SERVICE = "osforge-canvas";
const API_VERSION = 1;
const DEFAULT_PORT = 4242;
const ID_PATTERN = /^[a-z0-9_-]+$/;
const SSE_DEBOUNCE_MS = 150;
const SSE_HEARTBEAT_MS = 25_000;
const READ_RETRY_MS = 100;

// ── Config resolution ─────────────────────────────────────────────────────────

function resolveDataDir(): string {
  const flag = Bun.argv.find((arg) => arg.startsWith("--dir="));
  const raw = flag ? flag.slice("--dir=".length) : join(process.cwd(), "outputs", "canvas");
  return resolve(raw);
}

function resolvePort(): number {
  const raw = process.env["CANVAS_PORT"];
  if (!raw) return DEFAULT_PORT;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > 65535) {
    console.error(`CANVAS_PORT inválido: "${raw}". Use um inteiro 1-65535.`);
    process.exit(1);
  }
  return parsed;
}

const DATA_DIR = resolveDataDir();
const ARTIFACTS_DIR = join(DATA_DIR, "artifacts");
const FEEDBACK_DIR = join(DATA_DIR, "feedback");
const VIEWER_HTML = join(import.meta.dir, "viewer.html");
const PORT = resolvePort();

// ── Helpers ───────────────────────────────────────────────────────────────────

function jsonError(message: string, status: number): Response {
  return Response.json({ error: message }, { status });
}

/** True when `id` is safe to interpolate into a filesystem path. */
function isSafeId(id: string): boolean {
  return id.length > 0 && id.length <= 200 && ID_PATTERN.test(id);
}

/**
 * Read+parse a JSON file. The Claude Write tool is NOT atomic, so a file may be
 * observed mid-write (truncated / partial JSON) during an fs.watch event. We
 * retry once after a short delay before giving up. Returns null if the file is
 * absent or still unparseable after the retry.
 */
async function readJsonResilient(path: string): Promise<unknown | null> {
  const file = Bun.file(path);
  if (!(await file.exists())) return null;
  try {
    return JSON.parse(await file.text());
  } catch {
    await Bun.sleep(READ_RETRY_MS);
    try {
      const retryFile = Bun.file(path);
      if (!(await retryFile.exists())) return null;
      return JSON.parse(await retryFile.text());
    } catch {
      return null;
    }
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// ── Route handlers ─────────────────────────────────────────────────────────────

async function handleRoot(): Promise<Response> {
  const file = Bun.file(VIEWER_HTML);
  if (!(await file.exists())) {
    return new Response("viewer.html not found (T3.3 pending)", {
      status: 503,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
  return new Response(file, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}

function handleHealth(): Response {
  return Response.json({ ok: true, service: SERVICE, version: API_VERSION, dir: DATA_DIR });
}

interface ArtifactSummary {
  id: string;
  title: string;
  createdAt: string;
  revision: number;
  hasFeedback: boolean;
}

async function handleListArtifacts(): Promise<Response> {
  const glob = new Bun.Glob("*.json");
  const entries: Array<{ summary: ArtifactSummary; mtime: number }> = [];

  for await (const name of glob.scan({ cwd: ARTIFACTS_DIR, onlyFiles: true })) {
    const id = name.replace(/\.json$/, "");
    if (!isSafeId(id)) continue; // skip files we'd refuse to serve anyway

    const path = join(ARTIFACTS_DIR, name);
    const parsed = await readJsonResilient(path);
    if (!isRecord(parsed)) continue; // invalid JSON → skipped silently

    const stat = await Bun.file(path).stat().catch(() => null);
    const mtime = stat ? stat.mtimeMs : 0;
    const hasFeedback = await Bun.file(join(FEEDBACK_DIR, `${id}.json`)).exists();

    entries.push({
      summary: {
        id,
        title: typeof parsed["title"] === "string" ? (parsed["title"] as string) : id,
        createdAt: typeof parsed["createdAt"] === "string" ? (parsed["createdAt"] as string) : "",
        revision: typeof parsed["revision"] === "number" ? (parsed["revision"] as number) : 0,
        hasFeedback,
      },
      mtime,
    });
  }

  entries.sort((a, b) => b.mtime - a.mtime); // newest first
  return Response.json(entries.map((e) => e.summary));
}

async function handleGetArtifact(id: string): Promise<Response> {
  if (!isSafeId(id)) return jsonError("invalid id", 400);
  const parsed = await readJsonResilient(join(ARTIFACTS_DIR, `${id}.json`));
  if (parsed === null) return jsonError("artifact not found", 404);
  return Response.json(parsed);
}

async function handleGetFeedback(id: string): Promise<Response> {
  if (!isSafeId(id)) return jsonError("invalid id", 400);
  const parsed = await readJsonResilient(join(FEEDBACK_DIR, `${id}.json`));
  if (parsed === null) return jsonError("feedback not found", 404);
  return Response.json(parsed);
}

async function handlePostFeedback(id: string, request: Request): Promise<Response> {
  if (!isSafeId(id)) return jsonError("invalid id", 400);

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return jsonError("body must be valid JSON", 400);
  }

  if (!isRecord(body)) return jsonError("body must be a JSON object", 400);
  if (body["artifactId"] !== id) {
    return jsonError(`body.artifactId must equal ":id" ("${id}")`, 400);
  }
  if (typeof body["revision"] !== "number") {
    return jsonError("body.revision must be a number", 400);
  }

  await Bun.write(join(FEEDBACK_DIR, `${id}.json`), JSON.stringify(body, null, 2));
  return Response.json({ ok: true });
}

// ── SSE: filesystem change stream ───────────────────────────────────────────────

interface SseEvent {
  kind: "artifact" | "feedback";
  id: string;
}

function handleEvents(request: Request): Response {
  const encoder = new TextEncoder();
  let watchers: FSWatcher[] = [];
  let heartbeat: ReturnType<typeof setInterval> | null = null;
  let debounceTimers = new Map<string, ReturnType<typeof setTimeout>>();
  let closed = false;

  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      const emit = (event: SseEvent): void => {
        if (closed) return;
        try {
          controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
        } catch {
          cleanup(); // controller already torn down
        }
      };

      // Debounce per-file so a burst of write events collapses into one emit.
      const schedule = (kind: SseEvent["kind"], filename: string | null): void => {
        if (!filename || !filename.endsWith(".json")) return;
        const id = filename.replace(/\.json$/, "");
        if (!isSafeId(id)) return;
        const key = `${kind}:${id}`;
        const existing = debounceTimers.get(key);
        if (existing) clearTimeout(existing);
        debounceTimers.set(
          key,
          setTimeout(() => {
            debounceTimers.delete(key);
            emit({ kind, id });
          }, SSE_DEBOUNCE_MS),
        );
      };

      watchers.push(watch(ARTIFACTS_DIR, (_evt, filename) => schedule("artifact", filename)));
      watchers.push(watch(FEEDBACK_DIR, (_evt, filename) => schedule("feedback", filename)));

      heartbeat = setInterval(() => {
        if (closed) return;
        try {
          controller.enqueue(encoder.encode(`: ping\n\n`));
        } catch {
          cleanup();
        }
      }, SSE_HEARTBEAT_MS);

      const cleanup = (): void => {
        if (closed) return;
        closed = true;
        if (heartbeat) clearInterval(heartbeat);
        for (const timer of debounceTimers.values()) clearTimeout(timer);
        debounceTimers.clear();
        for (const w of watchers) w.close();
        watchers = [];
        try {
          controller.close();
        } catch {
          /* already closed */
        }
      };

      // Client disconnect (curl Ctrl-C, browser navigate away) → tear everything down.
      request.signal.addEventListener("abort", cleanup);
    },
    cancel() {
      closed = true;
      if (heartbeat) clearInterval(heartbeat);
      for (const timer of debounceTimers.values()) clearTimeout(timer);
      debounceTimers.clear();
      for (const w of watchers) w.close();
      watchers = [];
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}

// ── Router ────────────────────────────────────────────────────────────────────

async function route(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const { pathname } = url;
  const method = request.method;

  if (pathname === "/" && method === "GET") return handleRoot();
  if (pathname === "/api/health" && method === "GET") return handleHealth();
  if (pathname === "/api/artifacts" && method === "GET") return handleListArtifacts();
  if (pathname === "/api/events" && method === "GET") return handleEvents(request);

  const artifactMatch = pathname.match(/^\/api\/artifacts\/([^/]+)$/);
  if (artifactMatch && method === "GET") {
    return handleGetArtifact(decodeURIComponent(artifactMatch[1]!));
  }

  const feedbackMatch = pathname.match(/^\/api\/feedback\/([^/]+)$/);
  if (feedbackMatch) {
    const id = decodeURIComponent(feedbackMatch[1]!);
    if (method === "GET") return handleGetFeedback(id);
    if (method === "POST") return handlePostFeedback(id, request);
  }

  return jsonError("not found", 404);
}

// ── Boot ──────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  await mkdir(ARTIFACTS_DIR, { recursive: true });
  await mkdir(FEEDBACK_DIR, { recursive: true });

  try {
    Bun.serve({
      port: PORT,
      hostname: "127.0.0.1",
      idleTimeout: 0, // SSE connections must not be killed by idle timeout
      fetch: route,
      error(err: Error): Response {
        // Generic message to the wire; full detail to server logs only.
        console.error("[canvas] request error:", err);
        return jsonError("internal error", 500);
      },
    });
  } catch (err) {
    const code = isRecord(err) ? err["code"] : undefined;
    if (code === "EADDRINUSE") {
      console.error(
        `Porta ${PORT} em uso. Se for outro canvas, ok; senão use CANVAS_PORT=<outra porta>.`,
      );
      process.exit(1);
    }
    throw err;
  }

  console.log(`OSForge Canvas → http://127.0.0.1:${PORT}`);
  console.log(`data dir       → ${DATA_DIR}`);
}

await main();
