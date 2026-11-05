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

**Idle auto-save (IN PROGRESS 2026-11-05 ~13:30 Kyiv).** User rule: if user is inactive 25 min, save dialog state to memory (codespace stops after 30 min idle). Implementation: `/workspaces/calc-dev-env/idle-save/idle-save.sh` (untracked, not committed yet): `arm` (Stop hook) starts setsid timer `IDLE_SAVE_SECONDS` (default 1500) → `claude -p --resume <sid> --fork-session --no-session-persistence --add-dir <memdir> --permission-mode acceptEdits --allowedTools Read,Write,Edit,Glob,Grep` with prompt via stdin (variadic flags swallowed positional prompt — bug found in 1st test, fixed), then `worklog.py sync`; `cancel` (UserPromptSubmit) kills timer's process group; env `IDLE_SAVE_CHILD=1` makes the child's own hooks no-op. State in `/tmp/claude-idle-save/<sid>.{pid,log}`. arm/cancel tested OK; 2nd end-to-end test (3 s delay) ran when session ended — headless save could NOT edit memory: memory dir is a symlink to calc-dev-env, and edits via the symlink are refused as "sensitive file"; real path is outside --add-dir. **Fix:** pass `--add-dir` with the resolved path (`readlink -f` of memdir) or `--add-dir /workspaces/calc-dev-env/memory/cost-calculator`.
**Next:** fix add-dir, retest; register hooks idempotently (extend `worklog.py install-hook` or install.sh: Stop → `idle-save.sh arm`, UserPromptSubmit → `idle-save.sh cancel`) in `~/.claude/settings.json` (auto-mode may block settings edits → ask user for manual mode); commit + push calc-dev-env; then return to stage-1 decomposition ([[stage1-decomposition]]).

Related: [[estimate-calibration-a]], [[team-is-user-plus-claude]].
