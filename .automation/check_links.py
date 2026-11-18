#!/usr/bin/env python3
"""Check relative markdown links (files and #anchors) across the repo.

Usage: python3 .automation/check_links.py   (exit code 1 if any link is broken)
External http(s) links are not fetched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^\s*```")


def github_slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)          # inline code -> text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)  # drop punctuation/emoji
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    result: set[str] = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        slug = github_slug(m.group(2))
        n = seen.get(slug, 0)
        result.add(slug if n == 0 else f"{slug}-{n}")
        seen[slug] = n + 1
    return result


def main() -> int:
    errors: list[str] = []
    cache: dict[Path, set[str]] = {}
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        in_fence = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK_RE.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                path_part, _, anchor = target.partition("#")
                if path_part.startswith("../../issues"):
                    continue  # GitHub UI route, not a file
                dest = (md.parent / path_part).resolve() if path_part else md
                if not dest.exists():
                    errors.append(f"{md.relative_to(ROOT)}:{lineno}: missing {target}")
                    continue
                if anchor and dest.is_file() and dest.suffix == ".md":
                    if dest not in cache:
                        cache[dest] = anchors(dest)
                    if anchor not in cache[dest]:
                        errors.append(f"{md.relative_to(ROOT)}:{lineno}: bad anchor {target}")
    for e in errors:
        print(e)
    print(f"{'FAIL' if errors else 'OK'}: {len(errors)} broken link(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
