---
name: reminder-db-request-metrics
description: "REMIND USER every session until decided: plan observability/metrics (DB writes like last_seen_at/throttle/attempts, external calls, heavy jobs) to find bottlenecks"
metadata:
  type: project
---

Raised by user 2026-10-28 while reviewing PR #278 (temporary rows in DB, `last_seen_at` touches, throttle counters). Want observability of where the system bottlenecks: DB query count/latency, external calls (Google OIDC, suppliers, Odoo), heavy processes (Jobs, parsing, calculation). Initial idea: in DEBUG mode log or emit a metric of request count and processing time per operation. User: "питання метрік треба підняти і запланувати", not ready to decide yet — **remind at the start of each session until a decision is made**; delete this memory once decided (issue/ADR/plan).

Context already established: HTTP requests are logged per request (`onResponse` hook in `server.ts`: route template, method, status, durationMs, referenceId at info). No DB query timing in `platform/database/postgres.ts`, no metrics/transport. Spec `operations-runtime.md` §7 `OPS.MET.001` requires low-cardinality metrics (HTTP latency by route, Job duration, adapter latency, DB capacity…), labels without UUID/email/customer; metric transport/aggregator is a platform adapter, depends on infra choice (#217, #282).

**How to apply:** briefly remind; if user wants to proceed, natural first step is a team-internal technical GitHub issue (not a PO question) scoping metrics + transport, possibly an ADR. Related: [[sec-implementation-progress]].
