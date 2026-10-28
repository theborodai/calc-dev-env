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
