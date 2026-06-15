#!/usr/bin/env python3
"""
Consolidate duplicate per-figure timeline events into a single canonical
"figure event" per historical person.

Problem: the timeline carried up to 14 near-identical events per figure
(Zosimos alone had 14), generated on arbitrary date intervals. The editorial
goal is ONE event per historical figure: an index-card preview on the timeline
that links to a single long-form essay (the person page).

Source of truth: the `persons_involved` JSON column (what the site actually
uses for cards and filtering). The legacy `person_event_refs` table is polluted
with spurious cross-links and is rebuilt from scratch here.

This script:
  1. Adds bookkeeping columns to timeline_events (idempotent):
       is_figure, primary_person_slug, card_preview
  2. For every person appearing in single-person events, collapses those events
     into ONE canonical figure event:
       slug   = figure-<person-slug>
       date   = the person's floruit (median of their event years)
       persons/texts/concepts_involved = union across the merged events
     and deletes the redundant source events.
  3. Multi-person events (collaborations) and non-person events (text
     publications, institutions) are left untouched.
  4. Rebuilds person_event_refs to match the final persons_involved JSON.

Idempotent. Usage:
    python scripts/consolidate_figure_events.py
"""

import json
import re
import sqlite3
import statistics
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"


def floruit_from_bio(bio_html):
    """Derive a historically accurate placement year and date label from the
    documented dates in the biography opening. Returns (year, label) or None.

    Handles: 'fl. c. 300 CE', '(c. 250–c. 330 CE)', '(1493/94–1541)',
    '(c. 722–815)', '(c. 460 – c. 370 BCE)'.
    """
    head = re.sub(r"<[^>]+>", " ", bio_html or "")[:400]
    bce = bool(re.search(r"\bB\.?C\.?E\.?\b|\bB\.?C\.?\b", head))
    sign = -1 if bce else 1

    m = re.search(r"\bfl\.?\s*c?\.?\s*(\d{3,4})", head)
    if m:
        y = sign * int(m.group(1))
        return y, f"fl. c. {int(m.group(1))} {'BCE' if bce else 'CE'}"

    m = re.search(r"(c\.?\s*)?(\d{3,4})(?:/\d+)?\s*[–\-—]\s*(?:c\.?\s*)?(\d{3,4})", head)
    if m:
        b, d = int(m.group(2)), int(m.group(3))
        approx = "c. " if m.group(1) else ""
        return sign * b, f"{approx}{b}–{d} {'BCE' if bce else 'CE'}"

    return None


def ensure_columns(cur):
    cur.execute("PRAGMA table_info(timeline_events)")
    cols = {r[1] for r in cur.fetchall()}
    for name, decl in [
        ("is_figure", "INTEGER DEFAULT 0"),
        ("primary_person_slug", "TEXT"),
        ("card_preview", "TEXT"),
    ]:
        if name not in cols:
            cur.execute(f"ALTER TABLE timeline_events ADD COLUMN {name} {decl}")
            print(f"  [migrate] added column {name}")


def load_json(val):
    try:
        out = json.loads(val or "[]")
        return out if isinstance(out, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def ensure_raw_snapshot(cur):
    """Snapshot the pristine event table once so consolidation is idempotent.

    The live timeline_events table is rebuilt from this immutable snapshot on
    every run, so the script can be run repeatedly without losing data.
    """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='raw_timeline_events'")
    if not cur.fetchone():
        cur.execute("CREATE TABLE raw_timeline_events AS SELECT * FROM timeline_events")
        print("  [migrate] created raw_timeline_events snapshot")


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ensure_columns(cur)
    ensure_raw_snapshot(cur)

    # Rebuild the live event table deterministically from the raw snapshot.
    cur.execute("DELETE FROM timeline_events")
    cur.execute("""INSERT INTO timeline_events
        SELECT * FROM raw_timeline_events""")

    cur.execute("""SELECT slug, date_start_year, location_slug, persons_involved,
                          texts_involved, concepts_involved, scholarly_grounding
                   FROM timeline_events""")
    rows = cur.fetchall()

    cur.execute("SELECT slug, name, bio_html FROM persons")
    persons = {r[0]: {"name": r[1], "bio": r[2]} for r in cur.fetchall()}

    # Group single-person events by their figure (persons_involved JSON).
    figure_events = {}  # person_slug -> [row,...]
    for row in rows:
        plist = load_json(row[3])
        if len(plist) == 1 and plist[0] in persons:
            figure_events.setdefault(plist[0], []).append(row)

    consolidated, deleted = 0, 0
    for pslug, evs in sorted(figure_events.items()):
        years, texts, concepts, locations, ground = [], [], [], [], None
        for r in evs:
            if r[1] is not None:
                years.append(r[1])
            if r[2]:
                locations.append(r[2])
            texts += load_json(r[4])
            concepts += load_json(r[5])
            if not ground and r[6]:
                ground = r[6]

        # Prefer the figure's documented dates from the biography; fall back to
        # the median of their (often arbitrary skeleton) event years.
        bio_date = floruit_from_bio(persons[pslug]["bio"])
        if bio_date:
            floruit, date_label = bio_date
        elif years:
            floruit = int(statistics.median(years))
            date_label = f"fl. c. {floruit} CE"
        else:
            floruit, date_label = None, "date uncertain"

        location = max(set(locations), key=locations.count) if locations else None
        texts = list(dict.fromkeys(texts))
        concepts = list(dict.fromkeys(concepts))
        fig_slug = f"figure-{pslug}"

        cur.execute("""INSERT INTO timeline_events
            (slug, date_label, date_start_year, date_end_year, location_slug,
             description, persons_involved, texts_involved, concepts_involved,
             source_method, review_status, confidence, scholarly_grounding,
             is_figure, primary_person_slug, card_preview)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,1,?,?)""",
            (fig_slug, date_label, floruit, floruit, location,
             "", json.dumps([pslug]), json.dumps(texts), json.dumps(concepts),
             "AI_ASSISTED", "DRAFT", "MEDIUM", ground, pslug, None))

        for r in evs:
            cur.execute("DELETE FROM timeline_events WHERE slug = ?", (r[0],))
            deleted += 1
        consolidated += 1

    # Rebuild person_event_refs from the (now clean) persons_involved JSON.
    cur.execute("DELETE FROM person_event_refs")
    cur.execute("SELECT slug, persons_involved FROM timeline_events")
    for ev, pi in cur.fetchall():
        for p in load_json(pi):
            if p in persons:
                cur.execute(
                    "INSERT INTO person_event_refs (person_slug, event_slug) VALUES (?,?)",
                    (p, ev))

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM timeline_events")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM timeline_events WHERE is_figure = 1")
    figs = cur.fetchone()[0]
    conn.close()

    print(f"\n  [OK] {consolidated} figure events created")
    print(f"  [OK] {deleted} duplicate single-person events removed")
    print(f"  [OK] {figs} figure events / {total} total events remain")


if __name__ == "__main__":
    main()
