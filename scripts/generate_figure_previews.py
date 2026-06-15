#!/usr/bin/env python3
"""
Generate the 3-5 sentence index-card preview for each canonical figure event.

The preview is the timeline card a reader sees before clicking through to the
full essay. We derive it from the opening paragraph of the person's biography
(already scholarly, peer-reviewed prose), trimming to 3-5 sentences / ~90 words
of plain text so cards stay scannable.

Idempotent. Usage:
    python scripts/generate_figure_previews.py
"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

MAX_SENTENCES = 5
MIN_SENTENCES = 3
TARGET_WORDS = 110


def strip_html(html):
    text = re.sub(r"<[^>]+>", "", html or "")
    text = text.replace("*", "")  # drop stray markdown italic markers
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(html):
    m = re.search(r"<p>(.*?)</p>", html or "", re.DOTALL | re.IGNORECASE)
    return strip_html(m.group(1)) if m else strip_html(html)[:1200]


def split_sentences(text):
    # split on sentence-final punctuation followed by space + capital/quote
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", text)
    return [p.strip() for p in parts if p.strip()]


def build_preview(bio_html):
    para = first_paragraph(bio_html)
    sents = split_sentences(para)
    if not sents:
        return None
    chosen, words = [], 0
    for s in sents:
        chosen.append(s)
        words += len(s.split())
        if len(chosen) >= MIN_SENTENCES and words >= TARGET_WORDS:
            break
        if len(chosen) >= MAX_SENTENCES:
            break
    return " ".join(chosen)


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT slug, bio_html FROM persons")
    bios = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute("SELECT slug, primary_person_slug FROM timeline_events WHERE is_figure = 1")
    figs = cur.fetchall()

    n = 0
    for fig_slug, pslug in figs:
        preview = build_preview(bios.get(pslug, ""))
        if preview:
            cur.execute("UPDATE timeline_events SET card_preview = ? WHERE slug = ?",
                        (preview, fig_slug))
            n += 1
    conn.commit()
    conn.close()
    print(f"  [OK] previews generated for {n}/{len(figs)} figure events")


if __name__ == "__main__":
    main()
