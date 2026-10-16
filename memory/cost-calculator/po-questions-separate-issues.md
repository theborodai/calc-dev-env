---
name: po-questions-separate-issues
description: Every new question to PO/business is a separate labeled issue, never a comment
metadata:
  type: feedback
---

Every new question to the business (PO, CISO, завод) — including follow-ups after a decision — is filed as a separate issue in the §11 format (title `PO: …`, label `потрібне рішення PO`, assignee, numeric example, options, `<details>Для команди`), not as a comment on an existing issue/PR.

**Why:** the user noted the PO (or their agent) may not recognise a team comment as a decision request; codified in docs/_meta/documentation-rules.md §11 п.7 (PR #270, 2026-10-13).

**How to apply:** before asking PO anything, also check whether the question is really the PO's (product semantics) or the team's (interpretation of an accepted decision, technical). Related: [[github-accounts-and-po]].
