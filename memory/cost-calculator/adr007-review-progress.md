---
name: adr007-review-progress
description: "State 2026-10-27 of PR #281 (ADR.007 supplier data acquisition) review via revmux: round-2 findings done/remaining, decisions taken, open PO issues"
metadata:
  node_type: memory
  type: project
  originSessionId: a27288f3-56d7-4a49-8f36-94c158f92f69
  modified: 2026-10-27T22:38:03.145Z
---

PR #281 branch `docs/adr-007-supplier-data-acquisition`. Reviewed with revmux (profile `spec`), task `pr-281` in `.revmux/tasks/` (gitignored). `.revmux/` exists only on branch `chore/revmux-review-standard` (PR #283) until merged — run revmux from that branch; scope.md tells agents to read PR files via `git show origin/<branch>:<path>`; goal.md lists team decisions so agents don't re-litigate them.

**Round 2 findings (11):** done — 1 (tracked list "eternal wait"), 2 (feed file must pass all SEC.UPLOAD.001 incl. antivirus), 3 (lookup carries canonical manufacturerId). Remaining, to go one by one with the user:
- 4: idempotency `(providerId, sourceVersion)` + lastConfirmedAt — after FAILED import same file never re-imported; supplier reverting to old file looks "confirmed". Proposed: confirm only if that version is the current PUBLISHED; re-import allowed after FAILED; revert = new import.
- 5: TEST.SUP.001 still says stale by "maxFreshness provider" → "технічний строк придатності".
- minors: 6 `LIVE_IF_SUPPORTED` — frozen run context lacks "created by Recalculate" flag; 7 reasons NOT_YET_FETCHED/STALE missing in gateway result model, sourcing providerFailures[], api.md; 8 transaction advisory lock holds DB connection during upstream call → in-process single-flight or lease row; 9 ADR p.6 wording "фон не передає нічого понад запит на вимогу" imprecise; 10 decisions README says "контракт sourcing незмінний"; 11 PR #281 description outdated.
Then run revmux round 3.

**Decisions taken this session (user):** tracked list only from calculation lookups, only full pair canonical manufacturer+MPN; no supplier query until manufacturer and MPN are resolved (sourcing-selection §2.53); freshness from our fetch/confirm time (not supplier's date inside file); file feed = system input of isolated parser reusing BOM tabular extractor, only if such a supplier exists; provider error metrics only from actual API calls; all supplier data in PostgreSQL, no Redis; finding "background refresh of suspended suppliers" skipped; Purchasing edits all supplier fields, Admin is superuser except business sign-offs.

**Open PO issues created:** #282 (stage-1 minimal infra, AWS vs corporate VM), #284 (owner of SRC-13 maxFreshness — proposal Purchasing per supplier; blocks VERIFIED_QUOTE per DEC.046), #285 (one supplier failed but all lines covered → WAIVABLE warning listing failed suppliers, blocks VERIFIED_QUOTE until recalc/accept). User said on 2026-10-27 they need a dialogue with PO before continuing.

**How to apply:** on resume, check PO answers on #282/#284/#285, then continue #281 from finding 4. Related: [[sec-implementation-progress]], [[po-questions-separate-issues]], [[review-findings-one-by-one]].

**Update 2026-11-03:** PO answered #284 (Purchasing owns maxFreshness per SupplierSource × data class) and #285 (WAIVABLE warning, recalc or audited risk acceptance before VERIFIED_QUOTE) — still need a DEC (separate PR). #281 merged with main (no force-push) + commit 2b9e9de: aligned with CISO #231 (option A): option-B bullet removed; file from supplier site only if it is the only official channel of an approved supplier (user's rule); LCSC fallback has no TRACKED_REFRESH; allowlist SRC.SUP.001; finding 5 fixed. Findings 4, 6–11 still open. #281 merges LAST (after #312–#316).

**Finding 7 DONE** (error.reason, providerFailures[] structure). **Finding 6 DONE** (CalculationContext.supplierFreshnessRequirement). **Update 2026-11-03 (later):** main merged into PR.281 (2d8e86e, no conflicts). Finding 4 DONE (65ccfc2), user's model: file is "accepted" only after successful atomic publish; `SupplierFeedState.acceptedImportId` per provider; fetched source compared only with last accepted (same → bump lastConfirmedAt; different incl. older → new import); FAILED/REJECTED never block re-import. Remaining: 6–11, then revmux round 3; DEC for Issue.284/285 before merging PR.281.

**PAUSE 2026-11-03 — resume here.** Branch `docs/adr-007-supplier-data-acquisition` (local + pushed, last commit 0c1b85f). Done this session: 4 (65ccfc2), 6 (7e5443b), 7 (0c1b85f). **Finding 8 presented, awaiting user's yes:** `supplier-gateway.md` §2.12 uses transaction-scoped advisory lock → holds DB connection during upstream call (slow DigiKey exhausts pool). Proposal: invariant "no open transaction/DB connection during provider call"; MVP = in-process single-flight (option A); lease row (option B) allowed later if metrics show cross-process duplicates; add TEST.SUP.001 check. Then 9 (ADR p.6 wording "фон не передає нічого понад запит на вимогу"), 10 (decisions README "контракт sourcing незмінний" — false now: context field, providerFailures structure, reason), 11 (PR.281 description outdated — rewrite incl. findings 4/6/7/8 changes), then revmux round 3 (run from branch with `.revmux/`, task `pr-281`), DEC for Issue.284/285 before merging PR.281.

**Update 2026-11-04:** Finding 8 DONE (a1682d5): §2.12 — no TX/DB connection during provider call, in-process single-flight, lease row only if metrics show cross-process dups; TEST.SUP.001 extended. Next: 9, 10, 11, revmux round 3, DEC 284/285.
**Update 2026-11-04 (later):** Finding 9 DONE (with option A, user): API provider default = ON_DEMAND + cache; TRACKED_REFRESH enabled per provider only when gateway metrics show rate-limit/quota pressure (it doesn't reduce total requests, only removes calc-time peaks + outage resilience). p.6 now says refresh repeats pairs from past calcs on schedule → demand profile → off for fallback. Next: 10, 11, revmux r3.
**Finding 10 DONE** (README decisions row). Next: 11 (PR description), revmux r3.
**Finding 11 DONE** (PR body rewritten 11-04). All round-2 findings closed. Next: revmux round 3 (task pr-281), then DEC for Issue.284/285 before merge.
**Update 2026-11-04 (round 3):** revmux 03-final ran (profile spec, 3/3 sources): 3 major (retry loses LIVE; LIVE on every Recalculate vs option A + open q estimate-lifecycle §3.39; feed compare ignores mapping/parser version), 5 minor (lastConfirmedAt on publish, provenance fields, STALE vs stale-not-usable, ADR p.2/traceability, PR desc TEST.CAL.001). Report .revmux/tasks/pr-281/03-final/report.md. None fixed yet.
