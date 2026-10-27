---
name: reminder-deps-audit-undici
description: "REMIND USER at session start if today >= 2026-10-29: close undici high advisory via pnpm.overrides; fast-uri from 2026-11-02"
metadata:
  node_type: memory
  type: project
  originSessionId: a27288f3-56d7-4a49-8f36-94c158f92f69
  modified: 2026-10-27T17:59:59.750Z
---

User asked (2026-10-27) to be reminded proactively. At the start of any session on/after the dates below, raise it before other work:

- **From 2026-10-29**: separate PR — `pnpm.overrides` undici `>=8.12.2` (GHSA-xjj6-f33q-929c high + 2 moderate; dev-only via testcontainers, jsdom). No `minimumReleaseAgeExclude` — user chose to wait rather than make a policy exception. Then `pnpm audit --audit-level high` must be green; rebase #278.
- **From 2026-11-02**: fast-uri 3.1.9 / 4.2.3 (moderate/low, via fastify) — same approach, can be in the same PR if done after 11-02.

Context: PR #279 (zod/vite/fastify bumps) already closes the other highs. Delete this memory once both are merged.

**Why:** `minimumReleaseAge` 14 days (dependency-management.md §1.11) blocks the patches until those dates; high SCA findings block PRs (§3.6).
**How to apply:** check today's date vs. above; if due, remind first. Related: [[sec-implementation-progress]].
