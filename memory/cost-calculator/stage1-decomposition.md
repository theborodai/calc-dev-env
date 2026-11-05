---
name: stage1-decomposition
description: Stage-1 (sourcing loop for employees) decomposition — DONE 2026-11-05: plan 008 (blocks 0, A–G + approximate estimate ≈29–52 days) merged via PR.329 + PR.330
metadata:
  type: project
---

2026-11-05 user: build the decomposition of development stage 1; PR.281 finalization and issue triage are parked ([[adr007-review-progress]]). Stage vocabulary per plan 006 (stage 0 skeleton, stage 1 = sourcing loop, parts 1.1 BOM / 1.2 catalog & params / 1.3 search & selection) — see [[pr-queue-po-blocked]]. Plan 007 = part 1.1 (steps A1–A10); plan 008 (1.2–1.3) not written.

**User's format (decided):** blocks that can be implemented separately and are understandable to a PM; max 2 levels (block → items); NO estimates yet (PO/CISO clarifications pending); for each item mark open questions / Issue / whether discussion is going. Legend used: ✅ no questions; 🟡 PO/CISO answered but not formalized in docs (no DEC/PR); 🔴 waiting external answer/data; ⚪ Issue exists, discussion not started.

**Draft v1 given in chat 2026-11-05 (~13:50 Kyiv):**
- 0 Prerequisites: SEC b/c (#193) ✅; infra/stand #282/#276 🔴 (I write IT request); accesses #217 🔴; monitoring #328 ⚪.
- A Projects & files: project/BOM revisions ✅; upload with checks — limits #218 🔴 CISO, archive sizes #298 🟡; jobs + isolated parser ✅.
- B BOM parsing: real samples #216 🔴; table reading/libs ✅; column recognition + customer profile #293 🟡; value normalization ✅; packages #288 ⚪; row classification #286 🟡 (+#289 formalize); MPN-only → manufacturer #290 🟡; problem rows + suitability report ✅; ambiguity resolution by Engineering #291 🟡; ProductionQty ✅.
- C Catalog: catalog + Engineer additions ✅; SRC-* param registry, values from Purchasing #216 🔴; supplier curation (trust class, maxFreshness, enable) #284 🟡, supplier lists #308/#310 🔴 CISO.
- D Inventory: fixed snapshot #216 🔴; Odoo read #217 🔴.
- E Supplier data: gateway (cache, freshness, single-flight) PR.281 🟡; request process/queues #327 ⚪; API adapters DigiKey/Mouser/TME keys #217 🔴; FEED price file #321 🔴 CISO + #310; background refresh ✅ (in PR.281, metrics-gated); fixed offers for tests/demo #216 🔴.
- F Source selection: parametric candidates #326 ⚪ (key open question); NRND/EOL #287 ⚪; algorithm + MOQ/currencies, supplier priority/LCSC #322 🔴 PO no answer; "supplier didn't respond" warning #285 🟡; plan-with-explanation screen ✅; freshness horizon #325 🔴 optional.
- G Comparison & calibration: calibration cases #292 🟡 + data #216 🔴; purchaser decision + discrepancies #292 🟡, technical comparison model (plan 006 §6.5) not written; Admin arbitration ✅ DEC.054.
- Demos after B, after C+D, after E+F+G; one acceptance at end; needs stand #282.

**Key findings:** 7 PO answers (#284/285/286/290/291/292/293) not formalized in any DEC — 1–2 PRs, no one to wait for. Not discussed yet: #287, #288, #326, #327. External blockers: #216, #217, #282, #322 (PO), #308/#310/#321 (CISO). Can start now: A, B core, C without values, E gateway on fixed data.

**Done 2026-11-05 (~14:30 Kyiv):** user accepted the split as is and asked to save it in the repo WITHOUT conclusions (only blocks 0, A–G + legend + demos) to hand to the PM for organizing work and understanding the process. File `docs/_plans/008-stage-1-work-breakdown.md` (status `planned`, non-normative, statuses as of 11-05, refs `Issue.NNN (#NNN)`; one line maps A–B → 1.1, C–D → 1.2 + inventory, E–G → 1.3). Branch `docs/plan-008-stage-1-breakdown` from main, commit 7396e5c, pushed; **PR.329 opened** (body: blocks, legend, no req/DEC/tests/security impact; check-doc-ids clean). Number 008 chosen because plan 007 refers to "plan 008" for parts 1.2–1.3; offered rename to 009 if 008 should stay for a detailed 1.2–1.3 plan — no answer.

**PR.329 MERGED** by user (~15:00, merge 2a1de09) — plan 008 without estimates is on main.

**Estimate (decided 11-05 ~15:10):** user asked for estimates; I gave per-block working days of the team (user + Claude, no parallelism) based on [[estimate-calibration-a]] (code takes hours; discussions/design/post-review fixes dominate — e.g. SEC.a 20 min code + 2 days fixes, ADR.007 ≈ 8 session days with no code): 0 = 2–3, A = 1, B = 6–10, C = 2–4, D = 1–3, E = 5–9, F = 6–12 (biggest uncertainty, #326), G = 3–5, demos + fixes 3–5 → **≈ 29–52 days ≈ 6–10 weeks**. User required notes: approximate; valid only if plant data #216, accesses #217, stand #282 arrive on time and PO/CISO questions are agreed without delay; waiting, plant calibration (≈2–4 weeks after first full run) and scope changes NOT included; re-estimate after block B. Added as section «Орієнтовна оцінка» in plan 008 (intro line points to it), commit 1ad1733 on branch `docs/plan-008-stage-1-estimate` → **PR.330 open**. PR.329 body was briefly edited by mistake after merge, then restored to original.

**Stopped at (2026-11-05 15:23 Kyiv):** PR.330 open, awaiting user review/merge. Local branch `docs/plan-008-stage-1-estimate`, clean. Stale remote branch `docs/plan-008-stage-1-breakdown` (recreated by my push after merge) — deletion blocked by auto-mode classifier; user should delete it (`! git push origin --delete docs/plan-008-stage-1-breakdown`).

**Next step on resume:** ask whether PR.330 is merged / needs edits and whether the stale branch is deleted. Possible follow-ups (not agreed yet): GitHub milestone + Issues per block; keep statuses in plan 008 updated; formalize the 7 PO answers in DEC (#284/285/286/290/291/292/293). Rename 008→009 is moot (008 merged). After decomposition — return to the parked list in [[adr007-review-progress]] (PR.281 overview, DEC #284/#285, triage all open issues).
**DONE 2026-11-05 17:52 Kyiv:** PR.330 merged — plan 008 (blocks + approximate estimate) is on main; stale remote branch deleted by user; local branches cleaned; local main at 689ea3c. User moved back to PR.281 — see [[adr007-review-progress]]. Possible later follow-ups (not agreed): GitHub milestone + Issues per block; keep plan 008 statuses updated; DEC for the 7 PO answers (#284/285/286/290/291/292/293).
