---
name: estimate-calibration-a
description: "Calibration of Claude's effort estimates vs actual session time for backlog items A1–A2 (Oct 2026)"
metadata:
  node_type: memory
  type: project
  originSessionId: 493d1179-bb5b-4bf3-803b-23f526e3e9b9
  modified: 2026-10-16T19:38:48.085Z
---

Actual time reconstructed from session transcripts (message timestamps) and git/PR times.

| Item | Estimate (person-days, 1 day ≈ 8 h) | Actual wall-clock with user |
|---|---|---|
| A1 skeleton (15.10) | 6–8 (orig. 1.5–2 person-weeks) | ~17 min generation + ~15–30 min look/merge (16.10) ≈ 0.5–0.75 h |
| A2.1 Postgres+migrations+stand (16.10) | 2–3 + stand 2–3 | 15:21→16:33 ≈ 1.2 h (18 min gen, rest Q&A, TLS + secrets docs) |
| A2.2 Job runtime | 3–5 | 16:33→17:55 ≈ 1.4 h (14 min gen, ~40 min design talk, progress feature) |
| A2.3 object storage | (was moved to stage 1, ~1 day implied) | 17:55→18:08 gen 13 min, + ~20 min infra questions; PR #275 merged 16.10 |
| A2 total | revised 16.10: 1–1.5 person-weeks (4–6 days, incl. audit not yet done) | ≈ 3 h |

Ratio: ~10–15× faster than the revised (16.10) estimate, ~20–30× vs the original (15.10) one.

**Caveats:** no deep human review was done (PRs merged within ~15–60 min); all items were well-specified infrastructure with no external dependencies; the user's thinking time outside sessions isn't captured.

**How to apply:** for well-specified infra/CRUD, estimate in hours of joint session time, not days; keep separate buffers for review debt, PO decisions, access (#217, #231) and real data (#216), which code speed does not compress. Record estimate at start and actual at finish of each next item to extend this table. Related: [[team-is-user-plus-claude]].

**Re-estimate 16.10 evening (full doc: calc-dev-env `notes/cost-calculator/estimate-2026-10-16.md`, internal only — NOT for PO, revisit later) (after A2 merged), stages 0–3 (PO contour), one person + Claude:** code-heavy parts in session hours; uncompressible parts (algorithm design on real data, UI iterations, review, PO #269, plant calibration, access #217/#231, data #216) kept in days. Result ≈ 17–32 working days + 25% overhead ≈ 4–8 weeks to first full sourcing run, + calibration 2–4 weeks (plant pace) → **≈ 6–12 weeks** total (was 29 person-weeks / 7–7.5 months on 16.10 afternoon). Next check: SEC (first security-logic item) — if it also takes ~hours, the factor holds for spec-driven work.
