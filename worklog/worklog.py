#!/usr/bin/env python3
"""Облік часу роботи над cost-calculator за транскриптами Claude Code.

Команди:
  sync    зібрати інтервали з транскриптів, оновити REPORT.md, закомітити worklog і memory, запушити main
  report  надрукувати звіт (без git)
  hook    точка входу для хуків SessionStart / Stop / SessionEnd: запускає sync у фоні
  install-hook  прописати хуки в ~/.claude/settings.json

Визначення метрик — у README.md.
"""
import argparse
import datetime as dt
import fcntl
import fnmatch
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
DEFAULTS = {"pause_minutes": 15, "timezone": "Europe/Kyiv", "repo": "/workspaces/cost-calculator",
            "stop_throttle_minutes": 10}
HOOK_EVENTS = ("SessionStart", "Stop", "SessionEnd")


def load_config():
    cfg = dict(DEFAULTS)
    path = ROOT / "config.json"
    if path.exists():
        cfg.update(json.loads(path.read_text(encoding="utf-8")))
    return cfg


def git(*args, cwd=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()


def author(cfg):
    return git("config", "user.name", cwd=cfg["repo"]) or "unknown"


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def fmt_ts(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- Транскрипти --------------------------------------------------------------

def project_dirs(repo):
    """Каталоги транскриптів цього репо, включно з сесіями у .claude/worktrees."""
    slug = re.sub(r"[^A-Za-z0-9]", "-", repo)
    base = Path.home() / ".claude" / "projects"
    if not base.exists():
        return []
    return [d for d in base.iterdir() if d.is_dir() and (d.name == slug or d.name.startswith(slug + "--claude-worktrees-"))]


def is_human(e):
    """Подія, яку створив сам користувач: промпт, слеш-команда або переривання."""
    if e.get("type") != "user" or e.get("isMeta"):
        return False
    origin = e.get("origin")
    if isinstance(origin, dict):
        return origin.get("kind") == "human"
    content = e.get("message", {}).get("content")
    if isinstance(content, list):
        texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        if not texts:
            return False  # tool_result
        content = texts[0]
    return isinstance(content, str) and (not content.startswith("<") or content.startswith("<command-name>"))


def load_events(path):
    """[(час, чи_дія_користувача, гілка)] — лише події, що означають активність."""
    events = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            ts, kind = e.get("timestamp"), e.get("type")
            if not ts or kind not in ("user", "assistant", "system"):
                continue
            if kind == "system" and e.get("subtype") == "away_summary":
                continue  # генерується саме тоді, коли користувача немає
            events.append((parse_ts(ts), is_human(e), e.get("gitBranch") or ""))
    events.sort(key=lambda x: x[0])
    return events


def main_intervals(events, pause, ended_at):
    """Розкладає основну стрічку сесії на інтервали user / agent+ / agent і паузи.

    user   — від попередньої події до промпту користувача (читає, думає, пише);
    agent+ — хід агента, після якого користувач відповів без паузи (був присутній);
    agent  — хід агента, після якого була пауза (користувача не було).
    Будь-який проміжок між подіями, довший за pause, — пауза і не рахується.
    """
    if ended_at and events and ended_at > events[-1][0]:
        events = events + [(ended_at, True, events[-1][2])]  # закриття сесії — теж дія користувача
    intervals, pauses, turn = [], [], []
    for (a, _, branch_a), (b, human_b, branch_b) in zip(events, events[1:]):
        gap = b - a
        branch = branch_b or branch_a
        if gap > pause:
            pauses.append([a, b])
        elif gap.total_seconds() > 0:
            (intervals if human_b else turn).append([a, b, "user" if human_b else "agent", branch])
        if human_b:
            present = gap <= pause
            for iv in turn:
                iv[2] = "agent+" if present else "agent"
            intervals += turn
            turn = []
    intervals += turn
    return intervals, pauses


def side_intervals(events, pause):
    """Фонові субагенти: суцільна робота агента без пауз."""
    return [[a, b, "agent", bb or ba] for (a, _, ba), (b, _, bb) in zip(events, events[1:])
            if dt.timedelta(0) < b - a <= pause]


def collect(cfg, ended=None):
    """Оновлює data/<автор>/sessions/<id>.json для всіх наявних транскриптів."""
    ended = ended or {}
    pause = dt.timedelta(minutes=cfg["pause_minutes"])
    out_dir = ROOT / "data" / author(cfg) / "sessions"
    out_dir.mkdir(parents=True, exist_ok=True)
    for pdir in project_dirs(cfg["repo"]):
        for transcript in pdir.glob("*.jsonl"):
            sid = transcript.stem
            out = out_dir / f"{sid}.json"
            prev = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
            ended_at = ended.get(sid) or (parse_ts(prev["ended_at"]) if prev.get("ended_at") else None)
            events = load_events(transcript)
            if not events:
                continue
            intervals, pauses = main_intervals(events, pause, ended_at)
            for side in (pdir / sid / "subagents").glob("*.jsonl"):
                intervals += side_intervals(load_events(side), pause)
            record = {
                "session": sid,
                "start": fmt_ts(events[0][0]),
                "end": fmt_ts(max(events[-1][0], ended_at or events[-1][0])),
                "ended_at": fmt_ts(ended_at) if ended_at else None,
                "intervals": [[fmt_ts(a), fmt_ts(b), k, br] for a, b, k, br in sorted(intervals)],
                "pauses": [[fmt_ts(a), fmt_ts(b)] for a, b in pauses],
            }
            out.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# --- Звіт ---------------------------------------------------------------------

def union_seconds(intervals):
    total, cur_a, cur_b = 0.0, None, None
    for a, b in sorted(intervals):
        if cur_b is None or a > cur_b:
            if cur_b is not None:
                total += (cur_b - cur_a).total_seconds()
            cur_a, cur_b = a, b
        else:
            cur_b = max(cur_b, b)
    if cur_b is not None:
        total += (cur_b - cur_a).total_seconds()
    return total


def split_by_day(a, b, tz):
    """Ділить інтервал по локальній півночі."""
    a, b = a.astimezone(tz), b.astimezone(tz)
    while a.date() < b.date():
        midnight = dt.datetime.combine(a.date() + dt.timedelta(days=1), dt.time(), tz)
        yield a.date(), a, midnight
        a = midnight
    yield a.date(), a, b


def hm(seconds):
    m = int(round(seconds / 60))
    return f"{m // 60}:{m % 60:02d}"


METRICS = {
    "total": ("user", "agent+", "agent"),
    "mine": ("user", "agent+"),
    "own": ("user",),
}


def metrics(intervals):
    return {name: union_seconds([(a, b) for a, b, k, _ in intervals if k in kinds]) for name, kinds in METRICS.items()}


def build_report(cfg):
    tz = ZoneInfo(cfg["timezone"])
    who = author(cfg)
    by_day, by_branch = defaultdict(list), defaultdict(list)
    sessions_by_day, pauses_by_day = defaultdict(set), defaultdict(int)
    for f in sorted((ROOT / "data" / who / "sessions").glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        for a, b, kind, branch in rec["intervals"]:
            for day, da, db in split_by_day(parse_ts(a), parse_ts(b), tz):
                by_day[day].append((da, db, kind, branch))
                by_branch[branch or "—"].append((da, db, kind, branch))
                sessions_by_day[day].add(rec["session"])
        for a, _ in rec["pauses"]:
            pauses_by_day[parse_ts(a).astimezone(tz).date()] += 1

    today = dt.datetime.now(tz).date()
    week_start = today - dt.timedelta(days=today.weekday())
    periods = [
        ("Сьогодні", lambda d: d == today),
        ("Цей тиждень", lambda d: d >= week_start),
        ("Цей місяць", lambda d: (d.year, d.month) == (today.year, today.month)),
        ("Усього", lambda d: True),
    ]
    lines = [
        f"# Облік часу — {who}",
        "",
        f"Оновлено: {dt.datetime.now(tz):%Y-%m-%d %H:%M} ({cfg['timezone']}). "
        f"Поріг паузи: {cfg['pause_minutes']} хв. Формат — год:хв. Визначення — у [README.md](README.md).",
        "",
        "| Період | Загальний | Мій | з них мої ходи |",
        "|---|---:|---:|---:|",
    ]
    for title, pred in periods:
        m = metrics([iv for day, ivs in by_day.items() if pred(day) for iv in ivs])
        lines.append(f"| {title} | {hm(m['total'])} | {hm(m['mine'])} | {hm(m['own'])} |")

    lines += ["", "## По днях", "", "| Дата | Загальний | Мій | з них мої ходи | Сесій | Пауз |", "|---|---:|---:|---:|---:|---:|"]
    for day in sorted(by_day, reverse=True):
        m = metrics(by_day[day])
        lines.append(f"| {day} | {hm(m['total'])} | {hm(m['mine'])} | {hm(m['own'])} "
                     f"| {len(sessions_by_day[day])} | {pauses_by_day[day]} |")

    lines += ["", "## По гілках (усього)", "",
              "Паралельні сесії на різних гілках рахуються в кожній, тому сума може перевищувати загальний час.", "",
              "| Гілка | Загальний | Мій |", "|---|---:|---:|"]
    rows = sorted(((b, metrics(ivs)) for b, ivs in by_branch.items()), key=lambda x: -x[1]["total"])
    for branch, m in rows:
        lines.append(f"| `{branch}` | {hm(m['total'])} | {hm(m['mine'])} |")

    by_task = defaultdict(list)
    for branch, ivs in by_branch.items():
        by_task[task_of(branch)] += ivs
    lines += ["", "## По задачах (усього)", "",
              "Гілка → задача за [tasks.json](tasks.json); гілка без відповідності показується як є.", "",
              "| Задача | Загальний | Мій | з них мої ходи |", "|---|---:|---:|---:|"]
    rows = sorted(((t, metrics(ivs)) for t, ivs in by_task.items()), key=lambda x: -x[1]["total"])
    for task, m in rows:
        lines.append(f"| {task} | {hm(m['total'])} | {hm(m['mine'])} | {hm(m['own'])} |")
    return "\n".join(lines) + "\n"


def task_of(branch, _rules=[]):
    """Назва задачі для гілки: перше правило з tasks.json, чий glob-шаблон підходить."""
    if not _rules:
        path = ROOT / "tasks.json"
        _rules += json.loads(path.read_text(encoding="utf-8")) if path.exists() else [["*", None]]
    return next((task for pattern, task in _rules if fnmatch.fnmatchcase(branch, pattern) and task), branch)


# --- Git і хук -----------------------------------------------------------------

def publish(cfg, push=True):
    git("add", "-A", "worklog/data", "worklog/REPORT.md", "memory", cwd=REPO_ROOT)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT).returncode == 0:
        return
    git("commit", "-q", "-m", f"sync {dt.datetime.now(ZoneInfo(cfg['timezone'])):%Y-%m-%d %H:%M}", cwd=REPO_ROOT)
    if push:
        git("push", "-q", "origin", "main", cwd=REPO_ROOT, check=False)


def cmd_sync(args, cfg):
    with open(ROOT / ".sync.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not args.no_push:
            git("pull", "-q", "--rebase", "--autostash", "origin", "main", cwd=REPO_ROOT, check=False)
        ended = {args.session: parse_ts(args.ended_at)} if args.session and args.ended_at else None
        collect(cfg, ended)
        (ROOT / "REPORT.md").write_text(build_report(cfg), encoding="utf-8")
        if not args.no_commit:
            publish(cfg, push=not args.no_push)


def cmd_hook(args, cfg):
    """SessionStart — наздогнати попередні сесії; Stop — не частіше ніж раз на stop_throttle_minutes;
    SessionEnd — ще й зафіксувати момент закриття сесії."""
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    event = payload.get("hook_event_name")
    last = ROOT / ".last-sync"
    if event == "Stop" and last.exists() and time.time() - last.stat().st_mtime < cfg["stop_throttle_minutes"] * 60:
        return
    last.touch()
    cmd = [sys.executable, str(ROOT / "worklog.py"), "sync"]
    if event == "SessionEnd" and payload.get("session_id"):
        cmd += ["--session", payload["session_id"], "--ended-at", fmt_ts(dt.datetime.now(dt.timezone.utc))]
    log = open(ROOT / ".sync.log", "a")
    subprocess.Popen(cmd, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)


def cmd_install_hook(args, cfg):
    settings_path = Path.home() / ".claude" / "settings.json"
    settings_path.parent.mkdir(exist_ok=True)
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    command = f"python3 {ROOT / 'worklog.py'} hook"
    for event in HOOK_EVENTS:
        entries = settings.setdefault("hooks", {}).setdefault(event, [])
        if not any(h.get("command") == command for e in entries for h in e.get("hooks", [])):
            entries.append({"hooks": [{"type": "command", "command": command}]})
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Хуки {', '.join(HOOK_EVENTS)} записано в {settings_path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync")
    s.add_argument("--session")
    s.add_argument("--ended-at")
    s.add_argument("--no-push", action="store_true")
    s.add_argument("--no-commit", action="store_true")
    sub.add_parser("report")
    sub.add_parser("hook")
    sub.add_parser("install-hook")
    args = p.parse_args()
    cfg = load_config()
    if args.cmd == "report":
        collect(cfg)
        print(build_report(cfg), end="")
    else:
        {"sync": cmd_sync, "hook": cmd_hook, "install-hook": cmd_install_hook}[args.cmd](args, cfg)


if __name__ == "__main__":
    main()
