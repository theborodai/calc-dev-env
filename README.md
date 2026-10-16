# calc-dev-env

Приватне робоче середовище для роботи над `baranchuk/cost-calculator` з Claude Code:

- **облік часу** по днях, гілках і задачах (`worklog/`);
- **пам'ять Claude Code** для проєкту (`memory/cost-calculator/`);
- **Codespaces dotfiles**: `install.sh` налаштовує все в новому codespace.

Репозиторій приватний і окремий від репозиторію PO, тому PO не бачить ні обліку часу, ні пам'яті. Дані комітяться
й пушаться автоматично, тож не зникають разом з codespace.

---

## Зміст

1. [Як це влаштовано](#1-як-це-влаштовано)
2. [Структура репозиторію](#2-структура-репозиторію)
3. [Одноразове налаштування в GitHub](#3-одноразове-налаштування-в-github)
4. [Налаштування codespace](#4-налаштування-codespace)
5. [Перевірка](#5-перевірка)
6. [Щоденне використання](#6-щоденне-використання)
7. [Як рахується час](#7-як-рахується-час)
8. [Задачі: tasks.json](#8-задачі-tasksjson)
9. [Конфігурація: config.json](#9-конфігурація-configjson)
10. [Безпека](#10-безпека)
11. [Перенесення зі старого трекера (гілка `worklog`)](#11-перенесення-зі-старого-трекера-гілка-worklog)
12. [Усунення проблем](#12-усунення-проблем)
13. [Поточний стан](#13-поточний-стан)

---

## 1. Як це влаштовано

```
Claude Code ──пише──▶ ~/.claude/projects/-workspaces-cost-calculator/*.jsonl   (транскрипти)
     │                         │
     │ хуки                    │ читає лише мітки часу й гілку
     ▼                         ▼
worklog.py hook ──фон──▶ worklog.py sync ──▶ worklog/data/, worklog/REPORT.md
                                   │
                                   └──▶ git commit (worklog/ + memory/) → git push origin main

~/.claude/projects/-workspaces-cost-calculator/memory ──symlink──▶ /workspaces/calc-dev-env/memory/cost-calculator
```

- Транскрипти Claude Code лежать у `~/.claude`, тобто в домашньому каталозі контейнера. Перезапуск codespace
  (stop/start) їх зберігає, а **rebuild або новий codespace — ні**. Крім того, Claude Code сам видаляє транскрипти
  через 30 днів. Тому інтервали часу регулярно витягуються з транскриптів і комітяться сюди.
- `/workspaces` переживає перезапуск, тому клон лежить у `/workspaces/calc-dev-env`.
- Пам'ять Claude Code живе прямо в клоні через symlink, тому кожен `sync` комітить і її.

Хуки (у `~/.claude/settings.json`, рівень користувача):

| Подія | Що робить |
|---|---|
| `SessionStart` | запускає `sync` у фоні, щоб дозаписати попередні сесії, навіть якщо вони закрились без `SessionEnd` |
| `Stop` (кінець кожного ходу агента) | запускає `sync` у фоні, але не частіше ніж раз на `stop_throttle_minutes` (10 хв) |
| `SessionEnd` | фіксує момент закриття сесії й запускає `sync` у фоні |

`SessionEnd` ненадійний: якщо закрити вкладку або codespace зупиниться, він не спрацює. Тому `Stop` і
`SessionStart` страхують його, і втратити можна щонайбільше ~10 хв даних, які дозапишуться наступним `SessionStart`.

Хуки глобальні, тобто спрацьовують у будь-якому проєкті, але `sync` рахує лише транскрипти `cost-calculator`.

## 2. Структура репозиторію

```
calc-dev-env/
├── README.md                 ← ця інструкція
├── install.sh                ← ідемпотентне налаштування (dotfiles-точка входу)
├── worklog/
│   ├── worklog.py            ← збір, звіт, git, хуки
│   ├── REPORT.md             ← звіт, оновлюється автоматично
│   ├── tasks.json            ← відповідність гілка → задача
│   ├── config.json           ← (необов'язково) перевизначення налаштувань
│   ├── data/<автор>/sessions/<id сесії>.json   ← інтервали по сесіях
│   ├── .sync.log             ← лог фонових запусків (не комітиться)
│   ├── .sync.lock            ← блокування паралельних sync (не комітиться)
│   └── .last-sync            ← мітка для тротлінгу Stop (не комітиться)
└── memory/
    └── cost-calculator/      ← пам'ять Claude Code (MEMORY.md + файли фактів)
```

## 3. Одноразове налаштування в GitHub

Робиться один раз, а не в кожному codespace.

### 3.1. Репозиторій

Створіть **приватний** репозиторій `theborodai/calc-dev-env`. Гілка за замовчуванням — `main`.

### 3.2. Fine-grained Personal Access Token

Codespace за замовчуванням має доступ лише до свого репозиторію (`baranchuk/cost-calculator`), тому для push у
`calc-dev-env` потрібен окремий токен з мінімальними правами.

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. **Token name:** `calc-dev-env codespaces`.
3. **Expiration:** на ваш вибір. Запишіть дату, бо після неї sync тихо перестане пушити (див. [§12](#12-усунення-проблем)).
4. **Resource owner:** `theborodai`.
5. **Repository access → Only select repositories →** `theborodai/calc-dev-env`. Лише його.
6. **Permissions → Repository permissions → Contents: Read and write.** `Metadata: Read-only` додасться
   автоматично. Більше нічого не вмикайте.
7. **Generate token** і скопіюйте значення. Його покажуть лише один раз, і ніде крім наступного кроку його не
   зберігайте.

### 3.3. Секрет Codespaces

1. GitHub → **Settings → Codespaces → Secrets → New secret**.
2. **Name:** `DEV_ENV_TOKEN`.
3. **Value:** токен з попереднього кроку.
4. **Repository access:** `baranchuk/cost-calculator`, тобто codespaces, у яких цей секрет буде доступний.

Секрет потрапляє в змінну середовища `$DEV_ENV_TOKEN` лише в codespaces, **створених або перезапущених після**
додавання секрету. Уже запущений codespace треба перезапустити (див. [§4.1](#41-новий-codespace-автоматично)).

### 3.4. Dotfiles

1. GitHub → **Settings → Codespaces → Dotfiles**.
2. Увімкніть **Automatically install dotfiles** і виберіть `theborodai/calc-dev-env`.

GitHub клонує dotfiles-репозиторій у `/workspaces/.codespaces/.persistedshare/dotfiles` і запускає з нього
`install.sh`. Це відбувається **лише під час створення codespace**, а не під час перезапуску. Для вже наявного
codespace `install.sh` запускається вручну (§4.2).

## 4. Налаштування codespace

### 4.1. Новий codespace (автоматично)

Якщо §3 виконано, у новому codespace нічого робити не треба: `install.sh` запуститься сам. Перевірте результат
за [§5](#5-перевірка).

### 4.2. Наявний codespace (вручну)

**Крок 1. Перезапустіть codespace**, якщо секрет додано після його старту: Command Palette →
`Codespaces: Stop Current Codespace`, потім відкрийте його знову. Перевірте:

```bash
[ -n "$DEV_ENV_TOKEN" ] && echo "токен є" || echo "токена немає"
```

Не виводьте сам токен (`echo $DEV_ENV_TOKEN`) і не читайте `/workspaces/.codespaces/shared/.env-secrets`.

**Крок 2. Склонуйте репозиторій** з credential helper, який бере токен зі змінної середовища в момент запиту, тож
на диск токен не потрапляє:

```bash
HELPER='!f() { echo username=x-access-token; echo "password=$DEV_ENV_TOKEN"; }; f'
git -c credential.helper= -c credential.helper="$HELPER" \
    clone https://github.com/theborodai/calc-dev-env.git /workspaces/calc-dev-env
git -C /workspaces/calc-dev-env config credential.helper ''
git -C /workspaces/calc-dev-env config --add credential.helper "$HELPER"
```

Порожній `credential.helper ''` скидає глобальний helper Codespaces, який для цього репозиторію не має прав.

**Крок 3. Запустіть установку:**

```bash
bash /workspaces/calc-dev-env/install.sh
```

`install.sh` ідемпотентний, тож його можна запускати скільки завгодно разів. Він:

1. склонує репозиторій у `/workspaces/calc-dev-env`, якщо його немає, і налаштує credential helper (кроки 2);
2. перенаправить пам'ять: `~/.claude/projects/-workspaces-cost-calculator/memory` →
   `/workspaces/calc-dev-env/memory/cost-calculator`. Якщо там уже лежить звичайний каталог з файлами, спершу
   скопіює їх у репозиторій без перезапису наявних;
3. пропише хуки в `~/.claude/settings.json` (`worklog.py install-hook`), зберігши решту налаштувань;
4. запустить перший `sync`.

#### Якщо треба вручну, без install.sh

Пам'ять:

```bash
P=~/.claude/projects/-workspaces-cost-calculator
mkdir -p "$P"
[ -d "$P/memory" ] && [ ! -L "$P/memory" ] && cp -n "$P/memory/"* /workspaces/calc-dev-env/memory/cost-calculator/ && mv "$P/memory" "$P/memory.bak"
ln -sfn /workspaces/calc-dev-env/memory/cost-calculator "$P/memory"
```

Хуки — додайте в `~/.claude/settings.json` (зберігши інші ключі, наприклад `theme`):

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "python3 /workspaces/calc-dev-env/worklog/worklog.py hook" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "python3 /workspaces/calc-dev-env/worklog/worklog.py hook" }] }
    ],
    "SessionEnd": [
      { "hooks": [{ "type": "command", "command": "python3 /workspaces/calc-dev-env/worklog/worklog.py hook" }] }
    ]
  }
}
```

Хуки підхоплюються в **нових** сесіях Claude Code. Поточну сесію треба перезапустити або перевірити через `/hooks`.

### 4.3. Режим дозволів Claude Code

Автоматичний режим (auto mode) Claude Code блокує зміни, які стосуються самого Claude Code: хуки в
`~/.claude/settings.json`, код, який хуки запускають, роботу з токенами. Це навмисно. Налаштування й зміни
`worklog.py` робіть або самі, або попросіть Claude, перемкнувши режим на ручні підтвердження (**Shift+Tab**). Після
налаштування можна повернутись в auto mode, бо фонові `sync` запускаються хуками й класифікатора не потребують.

## 5. Перевірка

```bash
# 1. Доступ до репозиторію (має вивести хеш і refs/heads/main)
git -C /workspaces/calc-dev-env ls-remote origin

# 2. Пам'ять — symlink у репозиторій
ls -l ~/.claude/projects/-workspaces-cost-calculator/memory

# 3. Хуки прописані
python3 -c 'import json,pathlib; print(list(json.loads((pathlib.Path.home()/".claude/settings.json").read_text()).get("hooks",{})))'
# очікувано: ['SessionStart', 'Stop', 'SessionEnd']

# 4. Звіт рахується (без git)
python3 /workspaces/calc-dev-env/worklog/worklog.py report | head -20

# 5. Повний sync без push, перевірити коміт
python3 /workspaces/calc-dev-env/worklog/worklog.py sync --no-push
git -C /workspaces/calc-dev-env log --oneline -3

# 6. Після наступної сесії Claude Code — лог фонових запусків
tail /workspaces/calc-dev-env/worklog/.sync.log
```

## 6. Щоденне використання

Нічого робити не треба: працюйте в Claude Code як завжди, і хуки самі оновлюватимуть `worklog/REPORT.md` та
пушитимуть його в `main`. Звіт зручно дивитись прямо на GitHub.

Ручні команди:

```bash
cd /workspaces/calc-dev-env/worklog
python3 worklog.py report             # надрукувати звіт за поточними транскриптами
python3 worklog.py sync               # те саме, що хук: дані → коміт → push
python3 worklog.py sync --no-push     # закомітити без push
python3 worklog.py sync --no-commit   # лише оновити data/ і REPORT.md
python3 worklog.py install-hook       # (пере)записати хуки в ~/.claude/settings.json
```

Перед зупинкою або видаленням codespace варто один раз виконати `python3 worklog.py sync`, щоб не залежати від
хуків.

## 7. Як рахується час

`worklog.py` бере з транскриптів **лише мітки часу подій і назву гілки**, без змісту повідомлень. Стрічка подій
сесії ділиться на проміжки між сусідніми подіями:

| Проміжок | Тип |
|---|---|
| довший за поріг `pause_minutes` (15 хв) | **пауза**, не рахується ніде |
| закінчується вашим промптом, слеш-командою, перериванням або закриттям сесії | **ваш хід** (`user`) |
| інший, тобто агент працює | **хід агента**: `agent+`, якщо ви відповіли без паузи, інакше `agent` |

Робота фонових субагентів теж вважається ходом агента.

- **Загальний** = об'єднання `user` + `agent+` + `agent`.
- **Мій** = об'єднання `user` + `agent+`, тобто ваші ходи й ходи агента, під час яких ви були поруч.
- **з них мої ходи** = лише `user`: ви читаєте, думаєте й пишете.

Інтервали з паралельних сесій об'єднуються, тож одна хвилина рахується один раз. Дні рахуються в часовому поясі
`timezone` (Europe/Kyiv); інтервал через північ ділиться між днями.

Обмеження:

- робота поза Claude Code (рев'ю в GitHub, читання в редакторі, дзвінки) не потрапляє в облік;
- якщо після паузи ви повернулись і 3 хв писали промпт, ці 3 хв теж ідуть у паузу, бо проміжок один;
- у звіті «По гілках» паралельні сесії на різних гілках рахуються в кожній, тож сума може бути більшою за
  загальний час.

## 8. Задачі: tasks.json

Розділ «По задачах» у звіті групує гілки за правилами з `worklog/tasks.json`: це список пар
`[glob-шаблон гілки, назва задачі]`, і спрацьовує **перше** правило, що підходить. Гілка без правила показується
як є.

```json
[
  ["feat/a1-*",              "A1"],
  ["feat/a2-persistence",    "A2.1"],
  ["feat/a2-jobs",           "A2.2"],
  ["feat/a2-object-storage", "A2.3"],
  ["main",                   "обговорення"]
]
```

Коли починаєте нову задачу, додайте рядок для її гілки. Звіт перерахується з усієї історії за наступного `sync`.

## 9. Конфігурація: config.json

Необов'язковий `worklog/config.json` перевизначає значення за замовчуванням:

| Ключ | За замовчуванням | Значення |
|---|---|---|
| `pause_minutes` | `15` | проміжок без подій, довший за цей, вважається паузою |
| `timezone` | `"Europe/Kyiv"` | часовий пояс для розбивки по днях |
| `repo` | `"/workspaces/cost-calculator"` | робочий репозиторій, чиї транскрипти рахуються |
| `stop_throttle_minutes` | `10` | мінімальний інтервал між sync, запущеними хуком `Stop` |

Приклад: `{"pause_minutes": 20}`.

## 10. Безпека

- Токен має доступ **лише** до `calc-dev-env` і лише до вмісту (Contents). Навіть якщо він витече, решта
  репозиторіїв і акаунт залишаться недоступними.
- Токен не записується на диск: credential helper читає `$DEV_ENV_TOKEN` у момент запиту, а в `.git/config`
  лежить лише сам helper без значення.
- Не виводьте токен у термінал і не читайте файли секретів Codespaces. Перевіряйте лише наявність змінної (§4.2).
- `worklog/data/` містить лише мітки часу, ID сесій і назви гілок. Пам'ять (`memory/`) може містити робочий
  контекст проєкту, тому репозиторій має залишатися **приватним**.
- Хуки виконують лише `worklog.py` з цього репозиторію. Перед `git pull` чужих змін (якщо колись з'являться)
  переглядайте `worklog.py`, бо він виконується автоматично.

## 11. Перенесення зі старого трекера (гілка `worklog`)

Раніше облік вівся в orphan-гілці `worklog` репозиторію PO (`baranchuk/cost-calculator`), у worktree
`/workspaces/cost-calculator.worklog`, з хуком `SessionEnd` у `/workspaces/cost-calculator/.claude/settings.local.json`.

Перенесення:

1. Скопіювати дані: `cp -a /workspaces/cost-calculator.worklog/data/. /workspaces/calc-dev-env/worklog/data/`.
2. Запустити `python3 /workspaces/calc-dev-env/worklog/worklog.py sync`. Він перечитає наявні транскрипти й
   доповнить дані.
3. Видалити старий хук: прибрати `SessionEnd` з `/workspaces/cost-calculator/.claude/settings.local.json`. Інакше
   старий трекер і далі комітитиме в гілку PO.
4. Прибрати worktree: `git -C /workspaces/cost-calculator worktree remove /workspaces/cost-calculator.worklog`.
5. За бажанням видалити гілку `worklog` у репозиторії PO (`git push origin --delete worklog`). Це видно PO, тож
   робіть свідомо.

## 12. Усунення проблем

| Симптом | Причина / що робити |
|---|---|
| `$DEV_ENV_TOKEN` порожній | секрет додано після старту codespace → перезапустіть; або в секреті не вибрано `baranchuk/cost-calculator` |
| `Repository not found` під час clone/push | у токені не вибрано `calc-dev-env`, бракує `Contents: Read and write` або токен прострочено. Перевірте токен на GitHub, оновіть секрет і перезапустіть codespace |
| `REPORT.md` на GitHub не оновлюється | дивіться `worklog/.sync.log`; у `git -C /workspaces/calc-dev-env status` можуть бути незапушені коміти. Виконайте `git push` вручну |
| хуки не спрацьовують | `/hooks` у Claude Code; перевірте `~/.claude/settings.json` (§5, крок 3); хуки діють лише в нових сесіях |
| конфлікт під час `pull --rebase` | один codespace на одного автора конфліктів не дає. Якщо сталось: `git -C /workspaces/calc-dev-env status`, розв'язати, `git rebase --continue` |
| пам'ять «зникла» | symlink зламався після rebuild → `bash /workspaces/calc-dev-env/install.sh` |
| сесія без `ended_at` у `data/` | `SessionEnd` не спрацював; кінець сесії береться з останньої події, втрата ≤ одного ходу |

## 13. Поточний стан

Станом на 2026-10-16:

- [x] Репозиторій, токен, секрет і dotfiles налаштовано (§3).
- [x] Клон у `/workspaces/calc-dev-env`, дані старого трекера й пам'ять скопійовано.
- [ ] `worklog.py` адаптовано під цей репозиторій (корінь git, гілка `main`, коміт `memory/`, хуки
      `SessionStart`/`Stop`/`SessionEnd`, розділ «По задачах»).
- [ ] `install.sh`, `tasks.json`, `.gitignore`.
- [ ] Хуки в `~/.claude/settings.json`, symlink пам'яті, перший `sync`.
- [ ] Старий трекер прибрано (§11).

Після завершення цей розділ треба видалити.
