---
name: pr278-revmux-progress
description: "State of revmux review of PR #278 (SEC.a OIDC login): round 01-initial findings, which are fixed, which remain"
metadata:
  type: project
---

2026-10-28: revmux `pr-278/01-initial` (profile `code`, run from main checkout because `.revmux/` config lives on main; PR fetched into a temp worktree via `--workdir`). 5/5 sources, 6 findings = 5 distinct points:

1. [major] cross-site `<img>` on /start, /callback exhausts per-IP throttle → **fixed** in 79574eb (unbound callbacks not counted; non-navigation `Sec-Fetch-Dest ≠ document` rejected without counters/cookies; api.md + operations-runtime §2.7). Local commit, not pushed yet.
2. [minor] ROTATED `AUTH_SESSION_REVOKED` event carries new session's user/binding/privilege with old sessionId.
3. [minor] `AUTH_OIDC_ATTEMPT_EXPIRED` unreachable (cookie Max-Age = attempt TTL; start deletes expired rows) — two findings, same symptom.
4. [config, minor] `.env.example` empty `AUTH_OIDC_CLIENT_ID` breaks README local start for api and worker.
5. [tests, minor] fake IdP `tokenRequests()` counts only issued tokens → "refused before code exchange" test proves nothing.

**How to apply:** continue point by point from the first unfixed one ([[review-findings-one-by-one]]); work on branch `feat/sec-internal-auth` in the main checkout; re-run revmux (profile `final`, new round on task pr-278, from main checkout) only after all points are closed. Related: [[sec-implementation-progress]].
