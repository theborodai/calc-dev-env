---
name: dev-env-migration-pending
description: "Time tracking + Claude memory live in private repo theborodai/calc-dev-env (/workspaces/calc-dev-env); setup done 2026-10-16, 2 cleanup items left"
metadata:
  node_type: memory
  type: project
  originSessionId: ef0490b9-055d-49a9-bb5f-02f5fd3a28bf
  modified: 2026-10-16T20:38:20.544Z
---

Private repo **`theborodai/calc-dev-env`** (NOT `dev-env`), clone `/workspaces/calc-dev-env`, also the Codespaces dotfiles repo. Full instruction in its README.md (§13 = status).

- `worklog/worklog.py` — hooks SessionStart/Stop(throttled 10 min)/SessionEnd in `~/.claude/settings.json` run background `sync`: commits `worklog/` + `memory/` and pushes `main`. Report `worklog/REPORT.md` incl. «По задачах» via `worklog/tasks.json` — add a row when a new task branch starts.
- This memory dir is a symlink → `/workspaces/calc-dev-env/memory/cost-calculator`.
- Token: env `$DEV_ENV_TOKEN` via credential helper; never print it or read `/workspaces/.codespaces/shared/.env-secrets`.
- Auto-mode classifier blocks edits to hooks/settings/worklog.py and deletions — ask the user to switch to manual mode (Shift+Tab) for those.

**Left (as of 2026-10-16):** (1) user to clear old `SessionEnd` hook in `/workspaces/cost-calculator/.claude/settings.local.json` (points to removed `/workspaces/cost-calculator.worklog`); (2) user's decision on deleting branch `worklog` in PO repo (local has 1 unpushed commit; data already copied). Old memory copy `/workspaces/.claude-persist/` can be removed after.

Related: [[estimate-calibration-a]], [[team-is-user-plus-claude]].
