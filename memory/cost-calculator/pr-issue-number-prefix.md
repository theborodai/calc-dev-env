---
name: pr-issue-number-prefix
description: "Never write bare #NNN — always prefix: PR.312 for pull requests, Issue.319 for issues"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1cc03a87-9b87-4e73-a772-2af0df2bbe03
  modified: 2026-11-03T11:53:32.268Z
---

When mentioning GitHub numbers, always use a prefix that says what it is: `PR.312` for a pull request, `Issue.319` for an issue. Never a bare `#312`.

**Why:** on 2026-11-03 the user asked for this — in mixed lists of PRs and issues (e.g. CISO merge queue PR.314/PR.312 next to Issue.319/Issue.322) bare numbers don't show what is what.

**How to apply:** in messages to the user and in memory files — `PR.312`, `Issue.319`. In GitHub texts (PR bodies, issue comments, commit messages, docs in the repo) — `PR.312 (#312)`, `Issue.319 (#319)` so the autolink still works (user confirmed 2026-11-03). Existing texts are not rewritten in bulk; apply when editing them anyway. Related: [[pr-queue-po-blocked]].
