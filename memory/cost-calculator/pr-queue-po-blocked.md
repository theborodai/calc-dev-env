---
name: pr-queue-po-blocked
description: "PR/PO queue as of 2026-10-28 evening: #266/#267/#278 merged; #263 plan updated and ready; open PO issues #291/#292; formalization backlog"
metadata:
  type: project
---

2026-10-28: #266 (DEC.053), #267 (DEC.054 with #269 answers), #278 (SEC a) merged by user. #263 (plans 006/007) rebased, updated with PO's "first result = stages 0–3, employees only" (§1.1, 21f2b04), CI doc-ids green — awaiting user merge.

PO answered on 10-28: #268 (stricter Q3: missing/conflicting coordinate reference blocks Engineering review / VERIFIED_QUOTE), #269, #284 (Purchasing owns freshness per SupplierSource × data class), #285 (supplier failure + full coverage → Purchasing warning, blocks VERIFIED_QUOTE until recalc/accept), #282 (user/Ivan must write infra spec for IT head), #286 finished (policy for all component classes).

Open PO questions created 10-28: #291 (who reviews BOM analysis in stage 1), #292 (calibration baseline: purchaser decision vs actual purchase; does purchaser buy per system decision). Still to create: plan 007 §3 BOM mapping-profile reuse question.

Formalization backlog agreed order: DEC.053 «Уточнення» for #268 → #284/#285 DEC + continue #281 review from finding 4 → #282 infra spec → #288 → #287 → #286.

Force-push after rebase is blocked by auto-mode classifier → ask user to run `! git push --force-with-lease=<branch>:<sha> ...` themselves.

**How to apply:** at session start check #291/#292 answers. Related: [[adr007-review-progress]], [[po-questions-separate-issues]].
