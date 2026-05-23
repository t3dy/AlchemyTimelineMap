#!/usr/bin/env python3
"""Load enriched person biographies into database."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"

PERSONS_TO_LOAD = [
    "zosimos-of-panopolis",
    "jabir-ibn-hayyan",
    "al-razi",
    "al-kindi",
    "gerard-of-cremona",
    "roger-bacon",
]

def load_enriched_persons():
    """Load enriched person biographies from staging into database."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    for person_slug in PERSONS_TO_LOAD:
        file_path = STAGING_DIR / f"enriched_person_{person_slug}.json"

        if not file_path.exists():
            print(f"  [SKIP] {person_slug}: file not found")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                enriched = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  [SKIP] {person_slug}: {type(e).__name__}")
            continue

        bio_html = enriched.get("bio_html", "")

        # Update person record
        cursor.execute(
            "UPDATE persons SET bio_html = ? WHERE slug = ?",
            (bio_html, person_slug)
        )

        loaded += 1
        word_count = len(bio_html.split())
        print(f"  [OK] {person_slug:30s} {word_count:4d} words")

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Loaded {loaded} enriched persons")

if __name__ == "__main__":
    load_enriched_persons()
