---
name: issue-labels-scheme
description: Issue labels (type + стан) introduced 2026-11-05; I keep them current; daily SessionStart sync via calc-dev-env
metadata:
  type: project
---

2026-11-05: every open Issue has one type label (PO, CISO, дані/доступи, технічне, реалізація) and, except реалізація, one state label: стан: чекаємо відповіді / є відповідь / обговорення / робота за нами / готово до DEC / заблоковано. Rule — documentation-rules.md §11 п.8 (PR.336). Script scripts/issue-labels-sync.py (PR.336) flips «чекаємо відповіді» → «є відповідь» when a non-team comment appears after the label (timeline keeps label name at event time).

Daily trigger: calc-dev-env/issue-labels/daily.sh (commit bb15236) — SessionStart hook prints additionalContext once per day (stamp ~/.local/state/issue-labels/last-run); I must say «Потрібна щоденна актуалізація міток Issue — запускаю у фоні» and run `bash .../daily.sh run` in background, then summarize. Hook registration in ~/.claude/settings.json was blocked by auto mode — pending user (manual mode or `!` command).

**How to apply:** set labels when creating Issues; change state when we answer/decide; GitHub milestones not used (user: manager doesn't use GitHub, it's the user's tool for PO/CISO). Related: [[po-questions-separate-issues]].
