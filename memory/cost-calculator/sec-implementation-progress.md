---
name: sec-implementation-progress
description: "State of SEC (stage-0 internal auth, #193) implementation as of 2026-10-26: PR #278 open, plan for PRs (b) and (c)"
metadata:
  node_type: memory
  type: project
  originSessionId: 11a28623-d98e-4c1e-8f30-84fd00932fbd
  modified: 2026-10-26T17:02:43.231Z
---

Last item of stage-0 skeleton (plan 006) = SEC #193, split into 3 PRs (agreed with user 2026-10-26):

- **(a) PR #278** `feat/sec-internal-auth` — OPEN, awaiting user review (2 commits: 775404b login+sessions, 85399b4 throttling). Module `src/modules/access` (first domain module), schema `m_access` (app_user, identity_binding, oidc_attempt, auth_session, auth_throttle), Google OIDC via `openid-client` 6.8.8, routes `/api/v1/auth/internal/start|callback`, `/auth/session`, `/auth/logout`, CSRF `X-CSRF-Token` + Origin, `RuntimeConfig.auth`, fake IdP `test/support/fake-oidc-provider.ts` (jose).
- **(b) next**: `platform/audit` (AuditRecorder in same UnitOfWork, append-only), roles/permissions/grants + `AuthorizationContext` (TX.09), `registerInternalIdentity` (§3.66), revoke binding (§3.69), CLI first Administrator (§3.71, ops §3.6), last-admin confirmation (§3.72). Audit moved here from (a) because registration/grants must audit in the same transaction.
- **(c)**: admin UI «Користувачі й ролі» (TX.17), SPA `/login` page (shows `?error=<code>`; AUTH_SESSION_EXPIRED never reaches browser — cookie dies with session — so SPA shows "session ended" itself from `expires_at`), dev fake IdP with browser /authorize for local login.

Decisions made in (a), user-approved: throttling counters in **PostgreSQL** (not memory); `API_TRUSTED_PROXIES` (IP/CIDR, empty = ignore X-Forwarded-For); thresholds only in config `AUTH_THROTTLE_*`; after N failures in a window further attempts blocked. Technical choices: openid-client needs `enableNonRepudiationChecks` or it skips ID-token signature check (documented in application-structure.md §1.4); PKCE verifier/nonce derived from browser-bound attempt secret cookie, not stored; new API codes `AUTH_PROVIDER_UNAVAILABLE`, `AUTH_CSRF_INVALID`; 401 codes now `AUTH_REQUIRED/SESSION_EXPIRED/SESSION_REVOKED` (was UNAUTHENTICATED).

External dependency: Google Workspace OAuth client registration — #276 (assigned to PO). Until (b), nobody can log in except via bindings inserted directly in DB.

**How to apply:** on resume, check #278 review/merge status first; if merged, branch (b) from main. Time calibration row for SEC.a is in [[estimate-calibration-a]]. Related: [[team-is-user-plus-claude]].

**Update 2026-10-27:** job `dependencies` (pnpm audit) red on main and #278 due to new advisories. PR #279 `fix/deps-audit` bumps zod/vite/fastify (closes 2 high). User chose to WAIT: on/after **2026-10-29** add `pnpm.overrides` undici>=8.12.2 (last high, dev-only; blocked by minimumReleaseAge 14d — no exceptions), fast-uri patches available from **2026-11-02**. Then rebase #278.
- 2026-10-27: #279 and #280 merged; #278 rebased onto main (19954ec), check green 262+12 tests. Only undici high remains in audit.
- 2026-10-27 later: security-requirements review of #278 (subagent) → fixes commit 5ca8478 (API_TRUSTED_PROXIES required in prod, access_denied not a failure, OIDC secret checked at startup, https origin, ASCII return path, session revoked event, tests) + doc commit on TLS termination at reverse proxy (operations-runtime §3.7). #283 = revmux review standard (.revmux/).
- **2026-10-28: PR #278 (a) merged by user** (with red dependencies job). Next: branch (b) from main.
