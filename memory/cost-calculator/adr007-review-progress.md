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
