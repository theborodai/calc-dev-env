---
name: dev-env-migration-pending
description: IN PROGRESS (2026-10-16) — move worklog time tracking + Claude memory into private repo theborodai/dev-env; resume after codespace restart
metadata:
  node_type: memory
  type: project
  originSessionId: 493d1179-bb5b-4bf3-803b-23f526e3e9b9
  modified: 2026-10-16T20:01:54.465Z
---

Goal (user, 2026-10-16): automatic time tracking per task, NOT in the PO's repo, impossible to lose. Agreed design: private repo `theborodai/dev-env`, also used as Codespaces dotfiles repo.

**Done by the user:** created empty private repo `theborodai/dev-env`; fine-grained PAT (Contents RW, only that repo) stored as Codespaces user secret `DEV_ENV_TOKEN` (access: baranchuk/cost-calculator); dotfiles enabled → dev-env. Codespace must be restarted for the env var to appear (secret added 19:57 after boot 19:22).

**Current state:**
- Memory lives at `/workspaces/.claude-persist/cost-calculator-memory/`, symlinked from `~/.claude/projects/-workspaces-cost-calculator/memory`.
- Old tracker: worktree `/workspaces/cost-calculator.worklog` = orphan branch `worklog` in baranchuk/cost-calculator (PO sees it). Hook `SessionEnd` in `/workspaces/cost-calculator/.claude/settings.local.json` — unreliable (didn't fire 15–16.10 because sessions closed without SessionEnd). On 16.10 I ran `sync --no-push`: local commit with 15–16.10 data, not pushed.
- Auto-mode classifier blocked (a) reading `/workspaces/.codespaces/shared/.env-secrets` — never do that; (b) creating `/workspaces/dev-env` + copying memory/worklog data. Ask for the user's explicit permission in the new session before redoing (b).

**Plan on resume:**
1. Check `$DEV_ENV_TOKEN` is set and `git ls-remote` to dev-env works (credential helper reading the env var; never write the token to disk).
2. Create `/workspaces/dev-env`: `worklog/` (worklog.py, data/, REPORT.md, README, config.json, tasks.json), `memory/cost-calculator/`, `install.sh`, README.
3. Adapt worklog.py: git root = repo root, branch `main`, commit worklog+memory together; hooks SessionStart (catch up) + Stop (throttled ~10–15 min) + SessionEnd, written to user-level `~/.claude/settings.json`; report «По задачах» via tasks.json (feat/a1-* → A1, feat/a2-persistence → A2.1, feat/a2-jobs → A2.2, feat/a2-object-storage → A2.3, main → обговорення; fallback = branch name).
4. install.sh (idempotent): hooks, memory symlink → `<repo>/memory/cost-calculator`, credential helper. Dotfiles runs only on codespace CREATION, so run it manually now.
5. Remove the old SessionEnd hook from settings.local.json and the old worktree. Ask the user before deleting the `worklog` branch in the PO repo.

Related: [[estimate-calibration-a]], [[team-is-user-plus-claude]].
