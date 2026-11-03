---
name: pr-queue-po-blocked
description: "Project state at pause 2026-10-28 ~24:00 Kyiv: merged PRs, plan 006/007 structure, open PO issues, agreed next-work order"
metadata:
  type: project
---

**Merged 2026-10-28:** #266 (DEC.053), #267 (DEC.054 + #269 answers: Admin arbitrates, SRC.BEN.004/006, ROLE.005), #278 (SEC a, OIDC login), #263 (plans 006/007).

**Plan vocabulary (renumbered to PO's, user-approved):** stage 0 skeleton (in_progress: SEC b, c left); **stage 1 = PO's first stage "sourcing-контур для співробітників"** with parts 1.1 BOM (plan 007), 1.2 catalog & sourcing params, 1.3 supplier/stock search + purchase algorithm + comparison (plan 008, not yet written); then 2 PCB/POS, 3 pricing/Estimate, 4 production, 5 customer/order, 6 pilot. Demo after each part, one acceptance for stage 1. No customers in stage 1.

**Plan 007 (part 1.1) key points:** BOM → per-line technical requirement or explained problem; suitability report; classification per #286 (MPN vs parameters by class), PackageAlias #288; two dimensions — requirement completeness (1.1) vs candidate result (1.3); `sourcing-selection.md` §2.42 allows only exact MPN/approved alts → parametric search needs change (1.3); default values (power per package etc.) have no numbers/owner yet.

**Plan 008 (next, separate PR):** parts 1.2–1.3 — parametric candidate search (#286) vs §2.42, candidate source (local catalog vs supplier parametric search; CISO #231 covers MPN queries only), #287 lifecycle, #284/#285, comparison model SRC.BEN + #292, SRC-* values (#216), Odoo stock.

**Open PO issues:** #291 (who reviews BOM analysis), #292 (calibration baseline / does purchaser buy per system decision), #293 (BOM column mapping profile). #282: Ivan (user) must write infra spec for IT head.

**Agreed next-work order:** plan 008 → DEC.053 «Уточнення» for #268 (stricter Q3: missing/conflicting coordinate reference blocks Engineering review/VERIFIED_QUOTE) → #284/#285 DEC + continue #281 review from finding 4 → #282 infra spec → #288 → #286 (→ #287 with 008). SEC (b) also pending.

Force-push after rebase is blocked by auto-mode classifier → ask user to run `! git push --force-with-lease=<branch>:<sha> ...`.

**How to apply:** at session start check #291/#292/#293 answers and remind undici override (due 2026-10-29 after 15:05 UTC). Related: [[adr007-review-progress]], [[sec-implementation-progress]], [[reminder-deps-audit-undici]], [[reminder-db-request-metrics]].

**Update 2026-11-03 — CISO docs PRs:** merge order agreed: #314 → #312 → #313 → #316 (rebase, manual merge §3.13/SEC.AUTH.002 with #313) → #315 (rebase on #312) → #281. Edits pushed to 312/314/315/316. User accepted «3 years then delete within 24h». New CISO issue #319 (retention of project files with no CalculationRun; proposal: configurable period then delete). Gap marked in #315 (sourcing spec after SRC.SUP.001): no supplier priority logic (what is «insufficient» at preferred, is cheaper LCSC rejected) — LCSC not enabled until defined; belongs to plan 008 (offer PO issue). SEC (b) should start after #313 (grant expiresAt ≤12m).

**Update 2026-11-03 (later):** CISO PRs PR.314, PR.312, PR.313, PR.316, PR.315 + PR.320 (deps) + PR.323 (DEC.026 retention fix) MERGED. Closed issues: 318, 231, 294, 295, 299–305, 264. PR.324 merged; Issue.152 and Issue.208 closed. Still open on purpose: Issue.218 (п.9 not in docs: disable Customer access after contract, delete account after its data; depends on Issue.317), Issue.309 (CISO discussion thread), Issue.284/285/291–293 (PO answered, not yet formalized — PO did answer 291–293 on 10-29). Unchecked stale candidates: Issue.192 (held by Issue.254), Issue.261 (PO answered 10-06, check if formalized). Next: PR.281 merge main, then findings 4, 6–11 one by one.
