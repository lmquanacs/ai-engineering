#!/usr/bin/env python3
"""Render a 1200x630 share card (PNG) for a daily digest, for social posts.

  python3 .automation/make_card.py daily/YYYY/MM/YYYY-MM-DD.md   # writes daily/YYYY/MM/YYYY-MM-DD.png

Headline: the digest's `<!-- hook: ... -->` line, else its `<!-- summary: ... -->` line.
Bullets: the first three TL;DR items, with markdown stripped.
Needs Pillow (`pip install pillow`). Uses DejaVu Sans if installed, else Pillow's default font.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, FG, MUTED, ACCENT, PANEL = "#0b1220", "#f8fafc", "#94a3b8", "#38bdf8", "#111a2e"
FONT_DIRS = [Path("/usr/share/fonts/truetype/dejavu"), Path("/Library/Fonts"), Path("/System/Library/Fonts/Supplemental")]


def font(bold: bool, size: int) -> ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for d in FONT_DIRS:
        if (d / name).exists():
            return ImageFont.truetype(str(d / name), size)
    return ImageFont.load_default(size=size)


def plain(md: str) -> str:
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)   # links -> text
    md = re.sub(r"[*_`]+", "", md)                      # emphasis / code
    md = re.sub(r"[\U00010000-\U0010FFFF☀-➿️]", "", md)  # emoji the font can't draw
    return re.sub(r"\s+", " ", md).strip()


def clip(text: str, n: int) -> str:
    return text if len(text) <= n else text[: n - 1].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def first_sentence(text: str) -> str:
    return re.split(r"(?<=[.!?])\s+(?=[A-Z])", text, maxsplit=1)[0]


def main() -> None:
    src = Path(sys.argv[1])
    text = src.read_text(encoding="utf-8")
    date = dt.date.fromisoformat(src.stem)
    m = re.search(r"<!-- hook: (.*?) -->", text) or re.search(r"<!-- summary: (.*?) -->", text)
    headline = plain(m.group(1)) if m else "Today in AI engineering"
    tl = re.search(r"^## TL;DR\n(.*?)(?=^---|^## )", text, re.S | re.M)
    items = re.findall(r"^\d+\.\s+(.*)$", tl.group(1), re.M) if tl else []
    bullets = [clip(first_sentence(plain(i)), 140) for i in items[:3]]

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 12, H], fill=ACCENT)
    d.text((60, 44), "AI ENGINEERING · DAILY", font=font(True, 26), fill=ACCENT)
    d.text((W - 60, 44), date.strftime("%a %d %b %Y"), font=font(False, 26), fill=MUTED, anchor="ra")

    y = 104
    for line in textwrap.wrap(clip(headline, 150), 40)[:3]:
        d.text((60, y), line, font=font(True, 46), fill=FG)
        y += 58

    y += 18
    d.rounded_rectangle([48, y, W - 48, H - 96], radius=16, fill=PANEL)
    y += 22
    for b in bullets:
        lines = textwrap.wrap(b, 74)[:2]
        d.text((76, y), "›", font=font(True, 26), fill=ACCENT)
        for ln in lines:
            d.text((104, y), ln, font=font(False, 24), fill=FG)
            y += 32
        y += 12
        if y > H - 140:
            break

    d.text((60, H - 64), "github.com/lmquanacs/ai-engineering", font=font(True, 26), fill=FG)
    d.text((W - 60, H - 64), "Free · updated every morning", font=font(False, 24), fill=MUTED, anchor="ra")

    out = src.with_suffix(".png")
    img.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
