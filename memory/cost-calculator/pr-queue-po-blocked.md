---
name: pr-queue-po-blocked
description: "PRs deliberately held until PO answers (as of 2026-10-28): #267 waits #269, so #263 waits too"
metadata:
  type: project
---

2026-10-28: user decided **PR #267 (DEC.054) is not merged until PO answers #269**, even though it is green and rebased onto main (9519576). PR #263 (plans 006/007) depends on #267's IDs, so it waits as well. #266 (DEC.053) was merged with open PO questions in #268; when PO answers, close them via a new PR that adds an "Уточнення <date> (#268 п.N)" section to DEC.053 (precedent: DEC.041 / #243).

**Why:** user prefers not to merge a team interpretation of PO's model before PO confirms it.
**How to apply:** at session start check #269 for a PO answer before touching #267/#263. Related: [[adr007-review-progress]], [[po-questions-separate-issues]].
