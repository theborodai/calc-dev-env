---
name: review-findings-one-by-one
description: "User wants review findings discussed one by one in plain language before fixing; don't batch-fix or re-run review mid-list"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a27288f3-56d7-4a49-8f36-94c158f92f69
  modified: 2026-10-27T22:38:03.211Z
---

When a review (revmux or agent) returns findings, present them in plain language with a little context, then go through them **one point at a time** with the user; fix each only after discussing it. Don't batch-fix everything at once and don't re-run the review until the whole list is done.

**Why:** on 2026-10-27 the user stopped a revmux re-run ("рано, ми ще не дійшли до кінця списку"), asked for a simpler explanation of all findings, then repeatedly corrected the direction per point (e.g. no MPN-only supplier queries, metrics only from real API calls, PostgreSQL instead of Redis) — batch fixes would have been wrong.

**How to apply:** after a review, give a short simple list; ask which point to start; per point explain the problem, the options and a recommendation; implement after agreement; re-run the review only when all points are closed. Related: [[adr007-review-progress]].
