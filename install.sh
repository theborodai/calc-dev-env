#!/usr/bin/env bash
# Ідемпотентне налаштування calc-dev-env у codespace. Інструкція — README.md, §4.
# Запускається автоматично як Codespaces dotfiles (лише під час створення codespace) або вручну:
#   bash /workspaces/calc-dev-env/install.sh
set -euo pipefail

DIR=/workspaces/calc-dev-env
URL=https://github.com/theborodai/calc-dev-env.git
MEM_LINK="$HOME/.claude/projects/-workspaces-cost-calculator/memory"
MEM_DIR="$DIR/memory/cost-calculator"
# Токен читається з $DEV_ENV_TOKEN у момент запиту й не записується на диск.
HELPER='!f() { echo username=x-access-token; echo "password=$DEV_ENV_TOKEN"; }; f'

if [ -z "${DEV_ENV_TOKEN:-}" ]; then
  echo "calc-dev-env: \$DEV_ENV_TOKEN не задано — перезапустіть codespace або перевірте секрет (README §3.3)" >&2
  exit 1
fi

# 1. Клон у /workspaces (переживає перезапуск codespace) і credential helper.
if [ ! -d "$DIR/.git" ]; then
  git -c credential.helper= -c credential.helper="$HELPER" clone -q "$URL" "$DIR"
fi
git -C "$DIR" config --unset-all credential.helper || true
git -C "$DIR" config credential.helper ''
git -C "$DIR" config --add credential.helper "$HELPER"

# 2. Пам'ять Claude Code → репозиторій. Наявні файли переносяться без перезапису.
mkdir -p "$MEM_DIR" "$(dirname "$MEM_LINK")"
if [ "$(readlink -f "$MEM_LINK" 2>/dev/null)" != "$MEM_DIR" ]; then
  if [ -d "$MEM_LINK" ]; then
    cp -rn "$MEM_LINK/." "$MEM_DIR/"
  fi
  if [ -L "$MEM_LINK" ]; then
    rm "$MEM_LINK"
  elif [ -e "$MEM_LINK" ]; then
    mv "$MEM_LINK" "$MEM_LINK.bak.$(date +%s)"
  fi
  ln -s "$MEM_DIR" "$MEM_LINK"
fi

# 3. Хуки в ~/.claude/settings.json.
python3 "$DIR/worklog/worklog.py" install-hook

# 4. Перший sync: дані з наявних транскриптів → коміт → push.
python3 "$DIR/worklog/worklog.py" sync

echo "calc-dev-env: готово. Перевірка — README §5."
