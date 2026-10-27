---
name: po-questions-separate-issues
description: "Every new question to PO/business is a separate labeled issue, never a comment"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 94c947aa-db60-42f7-963c-facb575a70b6
  modified: 2026-10-26T13:20:46.179Z
---

Every new question to the business (PO, CISO, завод) — including follow-ups after a decision — is filed as a separate issue in the §11 format (title `PO: …`, label `потрібне рішення PO`, assignee, numeric example, options, `<details>Для команди`), not as a comment on an existing issue/PR.

**Why:** the user noted the PO (or their agent) may not recognise a team comment as a decision request; codified in docs/_meta/documentation-rules.md §11 п.7 (PR #270, 2026-10-13).

**Don't over-escalate:** on 2026-10-26 the user rejected a PO issue for an audit-log viewer in the admin UI ("очевидно потрібний"; admin sees it since there's no security role). Internal admin/ops features that don't change customer-visible price/term/rights and need no business knowledge are the team's call (§11) — record them as a team decision in a PR, not as a question to PO.

Also 2026-10-27: user rejected PO issues on (a) which suppliers to start with — "не обмежені послідовністю; головне принцип", connect whoever business has agreed; (b) manual price-list upload — all supplier data acquisition is automatic on behalf of the system (ADR.007, PR #281), no manual import; email-only suppliers are discussed if they ever appear.

**How to apply:** before asking PO anything, also check whether the question is really the PO's (product semantics) or the team's (interpretation of an accepted decision, technical). Related: [[github-accounts-and-po]].
