---
name: pr278-revmux-progress
description: "State of revmux review of PR #278 (SEC.a OIDC login): round 01-initial findings, which are fixed, which remain"
metadata:
  type: project
---

2026-10-28: revmux `pr-278/01-initial` (profile `code`, run from main checkout because `.revmux/` config lives on main; PR fetched into a temp worktree via `--workdir`). 5/5 sources, 6 findings = 5 distinct points:

1. [major] cross-site `<img>` on /start, /callback exhausts per-IP throttle → **fixed** in 79574eb (unbound callbacks not counted; non-navigation `Sec-Fetch-Dest ≠ document` rejected without counters/cookies; api.md + operations-runtime §2.7). Local commit, not pushed yet.
2. **fixed** caf2081 — [minor] ROTATED `AUTH_SESSION_REVOKED` event carries new session's user/binding/privilege with old sessionId.
3. **fixed** c78a4fd (expiry by state before cookie check, expired rows kept 24h, not counted) — [minor] `AUTH_OIDC_ATTEMPT_EXPIRED` unreachable (cookie Max-Age = attempt TTL; start deletes expired rows) — two findings, same symptom.
4. **fixed** (local placeholders) — [config, minor] `.env.example` empty `AUTH_OIDC_CLIENT_ID` breaks README local start for api and worker.
5. **fixed** — [tests, minor] fake IdP `tokenRequests()` counts only issued tokens → "refused before code exchange" test proves nothing.

**How to apply:** continue point by point from the first unfixed one ([[review-findings-one-by-one]]); work on branch `feat/sec-internal-auth` in the main checkout; re-run revmux (profile `final`, new round on task pr-278, from main checkout) only after all points are closed. Related: [[sec-implementation-progress]].
- Sweep after point 3: same shape for session — cookie Max-Age = absoluteExpiresAt so browser never gets AUTH_SESSION_EXPIRED (gets AUTH_REQUIRED); §3.8 forbids longer cookie. Raised with user.
- User agreed: AUTH_SESSION_EXPIRED unreachable in browser stays as is in #278; handle in PR (c) — SPA login page uses expires_at from /auth/session to show 'session ended'.
- Round 02-after-fix (no codex → `--profile code --lenses bugs,impl,adversarial`): 1 major — Speculation Rules prefetch passes Sec-Fetch-Dest gate → fixed dd715ed (Sec-Purpose/Purpose prefetch → 403, not redirect, so browser can't serve it to the real click). All 6 commits pushed 2026-10-28, PR description updated. No further round agreed.
- `final` profile needs codex (missing here); use `code --lenses …` for narrow re-reviews.
