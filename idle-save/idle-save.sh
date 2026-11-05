#!/usr/bin/env bash
# Автозбереження стану діалогу перед зупинкою codespace (зупиняється після 30 хв бездіяльності).
#   idle-save.sh arm     — хук Stop: (пере)запустити таймер на IDLE_SAVE_SECONDS (типово 20 хв)
#   idle-save.sh cancel  — хук UserPromptSubmit: користувач активний — скасувати таймер
# Коли таймер спрацьовує, головна сесія відновлюється в headless-форку (--fork-session,
# без запису транскрипту) і зберігає поточний стан у пам'ять; потім worklog sync комітить і пушить пам'ять.
set -u

# Дочірній headless-процес сам викликає хуки — ігнорувати їх, щоб не було циклу й самоскасування.
[ -n "${IDLE_SAVE_CHILD:-}" ] && exit 0

mode=${1:-}
payload=$(cat)
sid=$(jq -r '.session_id // empty' <<<"$payload")
cwd=$(jq -r '.cwd // empty' <<<"$payload")
[ -z "$sid" ] && exit 0

STATE=/tmp/claude-idle-save
mkdir -p "$STATE"
pidfile="$STATE/$sid.pid"
log="$STATE/$sid.log"

if [ -f "$pidfile" ]; then
  kill -- "-$(cat "$pidfile")" 2>/dev/null || true
  rm -f "$pidfile"
fi
[ "$mode" = arm ] || exit 0

delay=${IDLE_SAVE_SECONDS:-1200}
mem="$HOME/.claude/projects/$(sed 's#[^A-Za-z0-9]#-#g' <<<"${cwd:-$PWD}")/memory"
# Пам'ять може бути symlink (на calc-dev-env) — дозволяємо реальний шлях, інакше запис блокується.
mem=$(readlink -f "$mem")
prompt="Користувач неактивний ${delay}s; codespace скоро зупиниться. Збережи поточний стан цієї сесії в пам'ять \
за правилами memory (онови наявний project-файл, а не дублюй): що зроблено, що вирішено, на чому зупинились, \
наступний крок для відновлення, з датою $(date +%F) і часом. Нічого не роби, крім оновлення файлів пам'яті."

IDLE_SAVE_CHILD=1 setsid bash -c '
  sleep "$1"
  cd "$2" || exit 1
  # Промпт — через stdin: --add-dir і --allowedTools варіадичні й поглинули б позиційний аргумент.
  printf "%s" "$5" | claude -p --resume "$3" --fork-session --no-session-persistence \
    --add-dir "$4" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep"
  python3 /workspaces/calc-dev-env/worklog/worklog.py sync
  rm -f "$6"
' _ "$delay" "${cwd:-$PWD}" "$sid" "$mem" "$prompt" "$pidfile" </dev/null >>"$log" 2>&1 &
echo $! >"$pidfile"
exit 0
