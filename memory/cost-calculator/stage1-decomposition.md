---
name: stage1-decomposition
description: Stage-1 (sourcing loop for employees) decomposition — 2026-11-05 first 2-level draft (blocks 0, A–G + demos) given in chat, awaiting user feedback; priority over PR.281/issue triage
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

**Stopped at (2026-11-05 ~14:15 Kyiv):** asked user whether the block split fits (merge/split items?) and offered: after fixing structure → publish as PM page (artifact) or GitHub milestone + Issues. User went idle; no answer yet. Nothing written to repo.

**Next step on resume:** re-show draft v1 briefly (or ask if they saw it), get feedback on blocks, then decide where it lives (PM page / docs/_plans/008 / milestone). When decomposition is done, return to the parked list in [[adr007-review-progress]].
**11-05 saved:** docs/_plans/008-stage-1-work-breakdown.md on branch docs/plan-008-stage-1-breakdown (commit 7396e5c) → PR.329 opened 11-05. Blocks 0, A–G only, no conclusions; for the PM. Took number 008 (plan 007 refers to 008 for parts 1.2–1.3).
