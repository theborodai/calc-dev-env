#!/usr/bin/env bash
# Щоденна актуалізація міток Issue cost-calculator (documentation-rules.md §11 п.8).
#   daily.sh hook — SessionStart: якщо сьогодні запуску ще не було, просить Claude
#                   оголосити й запустити актуалізацію у фоні (additionalContext).
#   daily.sh run  — виконує scripts/issue-labels-sync.py; після успіху пише дату.
set -euo pipefail

REPO_DIR=/workspaces/cost-calculator
TEAM=theborodai,iBorodai
STATE_DIR="$HOME/.local/state/issue-labels"
STAMP="$STATE_DIR/last-run"
TODAY=$(date +%F)
SELF=$(readlink -f "$0")

case "${1:-}" in
  hook)
    [ -n "${IDLE_SAVE_CHILD:-}" ] && exit 0
    input=$(cat || true)
    cwd=$(printf '%s' "$input" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("cwd",""))
except Exception: print("")')
    case "$cwd" in "$REPO_DIR"|"$REPO_DIR"/*) ;; *) exit 0 ;; esac
    [ "$(cat "$STAMP" 2>/dev/null || true)" = "$TODAY" ] && exit 0
    python3 - "$SELF" <<'PY'
import json, sys
msg = ("Сьогодні ще не було щоденної актуалізації міток Issue (documentation-rules.md §11 п.8). "
       "Першим реченням відповіді явно скажи користувачу: «Потрібна щоденна актуалізація міток Issue — запускаю у фоні». "
       f"Потім запусти у фоні (Bash, run_in_background): bash {sys.argv[1]} run . "
       "Коли завершиться — коротко перекажи звіт: які Issue перейшли в «стан: є відповідь» і попередження щодо міток.")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg}}, ensure_ascii=False))
PY
    ;;
  run)
    mkdir -p "$STATE_DIR"
    script="$REPO_DIR/scripts/issue-labels-sync.py"
    cd "$REPO_DIR"
    if [ -f "$script" ]; then
      python3 -I "$script" --team "$TEAM"
    else
      # Скрипт ще не в поточній гілці — беремо з origin/main.
      git fetch -q origin main
      git show origin/main:scripts/issue-labels-sync.py | python3 -I - --team "$TEAM"
    fi
    echo "$TODAY" > "$STAMP"
    ;;
  *)
    echo "usage: $0 hook|run" >&2; exit 2 ;;
esac
