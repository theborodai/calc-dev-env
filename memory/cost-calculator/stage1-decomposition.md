---
name: stage1-decomposition
description: Stage-1 (sourcing loop for employees) decomposition — 2026-11-05 blocks 0, A–G saved as docs/_plans/008, PR.329 open for the PM; priority over PR.281/issue triage
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

**Stopped at (2026-11-05 ~14:50 Kyiv):** PR.329 open, awaiting user/PM feedback and merge. Working tree on branch `docs/plan-008-stage-1-breakdown`, clean.

**Next step on resume:** ask whether PR.329 needs edits / PM feedback, then merge (user merges). Possible follow-ups (not agreed yet): GitHub milestone + Issues per block; keep statuses in plan 008 updated; formalize the 7 PO answers in DEC (#284/285/286/290/291/292/293). After decomposition — return to the parked list in [[adr007-review-progress]] (PR.281 overview, DEC #284/#285, triage all open issues).
**11-05:** PR.329 merged by user. Estimate section (≈29–52 working days, conditional, approximate) → PR.330 (branch docs/plan-008-stage-1-estimate). Stale remote branch docs/plan-008-stage-1-breakdown recreated by my push — deletion was blocked; user can delete it.
