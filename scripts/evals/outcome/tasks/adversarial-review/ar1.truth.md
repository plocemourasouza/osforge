Seeded defects (ground truth, 3):
D1. Account enumeration: step 2 tells the user "No account found for this email", revealing which emails are registered. Fix: same neutral message for both cases.
D2. Token is never invalidated after use: step 5 checks only age; `used_at` exists in the table but is never set or checked, so a reset link can be replayed within 30 minutes (e.g. from email history / shared machine). No AC covers single use. Fix: check `used_at IS NULL`, set it on success, invalidate other outstanding tokens.
D3. Existing sessions are not revoked after a password reset: an attacker who already holds a session (the reason the user is resetting) stays logged in. Fix: revoke all sessions / refresh tokens for the user on reset.
Not defects (do not count as manufactured if raised as low-severity improvements, but they are not seeded): rate limiting of reset requests, email deliverability details.
