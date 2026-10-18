Review this feature spec before we start implementing it.

---

# Spec: Password reset by email

## Context
Users who forget their password currently have to email support. This feature lets them reset it themselves.

## Flow
1. On the login page, the user clicks "Forgot password" and enters their email address.
2. If the email belongs to an account, the system sends an email with a reset link. If it does not, the page shows "No account found for this email" so the user can try another address.
3. The reset link has the form `https://app.example.com/reset?token=<token>`, where `<token>` is a random 32-byte value, base64url-encoded. The token is stored in the `password_reset_tokens` table (`user_id`, `token_hash`, `created_at`, `used_at`).
4. The user opens the link and enters a new password twice. Passwords must be at least 12 characters.
5. On submit, the server looks up the token hash, checks that it is less than 30 minutes old, sets the new password (bcrypt, cost 12), and redirects to the login page with the message "Password updated".

## Acceptance criteria
- AC1: Given a registered email, when the user requests a reset, then an email with a link arrives within 2 minutes.
- AC2: Given a valid token less than 30 minutes old, when the user submits a 12+ character password twice, then the password is updated and the user is redirected to login.
- AC3: Given a token older than 30 minutes, when the user submits, then they see "This link has expired" and the password is unchanged.
- AC4: Given a password shorter than 12 characters, when the user submits, then they see "Password must be at least 12 characters".

## Out of scope
- SMS reset.
- Changing the email address.
