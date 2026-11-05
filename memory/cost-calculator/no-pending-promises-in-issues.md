---
name: no-pending-promises-in-issues
description: Don't leave an issue open/pending on a promise of future work; state "not needed now, a new issue if needed"
metadata:
  type: feedback
---

When answering an issue (CISO/PO), don't keep it blocked with "we'll come back here later / leave NEEDS_REVIEW until we decide". Close the question with the current answer and say that a future need gets its own new Issue — especially when that topic is already tracked separately (e.g. aggregators for parametric search → Issue.326).

**Why:** 2026-11-05, reply draft for Issue.308 kept aggregators as NEEDS_REVIEW pending Issue.326; user: "не подобається блокувати ішью обіцянкою майбутніх змін".

**How to apply:** replies resolve the issue as of now; future possibilities = "якщо знадобиться — окреме обговорення/Issue". Related: [[po-questions-separate-issues]].
