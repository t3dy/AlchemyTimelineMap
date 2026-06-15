#!/usr/bin/env python3
"""
Load long-form figure essays (3,000-5,000 words) into persons.bio_html.

Each figure's single timeline index card links to the person page, whose
bio_html is rendered as the full essay. Essays live as one HTML fragment per
figure under staging/figure_essays/<person-slug>.html and are loaded here.

The HTML fragment uses [LINK:slug] markup (converted at site-build time) and
<p>/<h2>/<i> tags only. This loader validates word count (3,000-5,000) and that
every [LINK:slug] resolves to a real entity before writing.

Idempotent. Usage:
    python scripts/load_figure_essays.py
"""

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "db" / "alchemy_timeline.db"
ESSAY_DIR = ROOT / "staging" / "figure_essays"

MIN_WORDS, MAX_WORDS = 3000, 5000


def word_count(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def valid_slugs(cur):
    slugs = set()
    for t in ("persons", "texts"):
        cur.execute(f"SELECT slug FROM {t}")
        slugs |= {r[0] for r in cur.fetchall()}
    cur.execute("SELECT slug FROM concepts")
    slugs |= {r[0] for r in cur.fetchall()}
    return slugs


def main():
    if not ESSAY_DIR.exists():
        print(f"  [skip] no essay dir at {ESSAY_DIR}")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT slug FROM persons")
    person_slugs = {r[0] for r in cur.fetchall()}
    slugs = valid_slugs(cur)

    loaded, skipped = 0, 0
    for path in sorted(ESSAY_DIR.glob("*.html")):
        pslug = path.stem
        html = path.read_text(encoding="utf-8").strip()
        if pslug not in person_slugs:
            print(f"  [WARN] {pslug}: no such person, skipping")
            skipped += 1
            continue
        wc = word_count(html)
        if not (MIN_WORDS <= wc <= MAX_WORDS):
            print(f"  [WARN] {pslug}: {wc} words out of range {MIN_WORDS}-{MAX_WORDS}, skipping")
            skipped += 1
            continue
        bad = [m for m in re.findall(r"\[LINK:([^\]]+)\]", html) if m.strip() not in slugs]
        if bad:
            print(f"  [WARN] {pslug}: unknown link slugs {sorted(set(bad))}, skipping")
            skipped += 1
            continue
        cur.execute(
            "UPDATE persons SET bio_html = ?, review_status = 'REVIEWED' WHERE slug = ?",
            (html, pslug))
        loaded += 1
        print(f"  [OK] {pslug}: {wc} words loaded")

    conn.commit()
    conn.close()
    print(f"\n  Loaded {loaded} essays, skipped {skipped}.")


if __name__ == "__main__":
    main()
