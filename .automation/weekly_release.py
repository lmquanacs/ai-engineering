#!/usr/bin/env python3
"""Write release notes for a weekly GitHub release that rolls up the past 7 days of digests.

  python3 .automation/weekly_release.py [--today YYYY-MM-DD] [--out notes.md]

Prints `tag=...` and `title=...` lines (for $GITHUB_OUTPUT) and writes the notes to --out.
Exits 0 with `skip=true` when there are no digests in the window.
Used by .github/workflows/weekly-release.yml; people who "Watch → Custom → Releases"
get one notification a week instead of one per daily commit.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/lmquanacs/ai-engineering"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", help="YYYY-MM-DD (default: today in Australia/Brisbane)")
    ap.add_argument("--out", default="release-notes.md")
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(ZoneInfo("Australia/Brisbane")).date()
    start = today - dt.timedelta(days=7)

    week = []
    for p in (ROOT / "daily").glob("*/*/*.md"):
        try:
            d = dt.date.fromisoformat(p.stem)
        except ValueError:
            continue
        if start < d <= today:
            week.append((d, p))
    week.sort(reverse=True)

    if not week:
        print("skip=true")
        return

    lines = [
        f"Everything that changed for engineers building with AI, {week[-1][0]:%d %b} – {week[0][0]:%d %b %Y}.",
        "",
        "## Daily digests",
        "",
    ]
    for d, p in week:
        text = p.read_text(encoding="utf-8")
        m = re.search(r"<!-- summary: (.*?) -->", text)
        summary = f": {m.group(1)}" if m else ""
        lines.append(f"- [{d:%a %d %b}]({REPO_URL}/blob/main/{p.relative_to(ROOT).as_posix()}){summary}")
    lines += [
        "",
        "---",
        f"⭐ Star the repo · 👀 **Watch → Custom → Releases** to get this roll-up weekly · "
        f"📡 [Atom feed](https://raw.githubusercontent.com/lmquanacs/ai-engineering/main/feed.xml) for every daily edition · "
        f"[Contribute]({REPO_URL}/blob/main/CONTRIBUTING.md)",
    ]
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"tag=week-{today.isoformat()}")
    print(f"title=Week of {today:%d %b %Y}")


if __name__ == "__main__":
    main()
