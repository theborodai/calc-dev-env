---
name: dev-env-migration-pending
description: "Time tracking + Claude memory live in private repo theborodai/calc-dev-env (/workspaces/calc-dev-env); setup done 2026-10-16, cleanup done"
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

**Left:** (1) done 2026-10-27 — stale `SessionEnd` hook removed by user. (2) done 2026-10-27 — branch `worklog` deleted from PO repo (local and origin); data had been copied to calc-dev-env. Old memory copy `/workspaces/.claude-persist/` can be removed after.

**Idle auto-save DONE 2026-11-05** (calc-dev-env 61491a1, README §6 «Автозбереження»). User rule: after 20 min of user inactivity (was 25; lowered for long-reply margin) save dialog state to memory (codespace stops at 30 min idle). `idle-save/idle-save.sh`: Stop hook `arm` → setsid timer → headless `claude -p --resume <sid> --fork-session --no-session-persistence` (prompt via stdin; `--add-dir` = `readlink -f` of memory symlink) → `worklog.py sync`; UserPromptSubmit hook `cancel`; `IDLE_SAVE_CHILD=1` makes the child's hooks no-op. Hooks registered by install.sh step 3. Logs `/tmp/claude-idle-save/<sid>.log`. Tested end-to-end.
**How to apply:** at a natural pause I don't need to save state manually just because of idle — the hook does it; still update memory at milestones. If an auto-saved note appears in memory, treat it as the latest state.

Related: [[estimate-calibration-a]], [[team-is-user-plus-claude]].
