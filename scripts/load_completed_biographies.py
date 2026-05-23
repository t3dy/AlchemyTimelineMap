#!/usr/bin/env python3
"""Load completed biographies from staging into database."""

import json
import sqlite3
import glob
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"

def load_biographies():
    """Load all completed biography JSON files from staging."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    failed = 0

    # Find all biography JSON files
    biography_files = glob.glob(str(STAGING_DIR / "*biography*.json")) + \
                      glob.glob(str(STAGING_DIR / "*persons*.json")) + \
                      glob.glob(str(STAGING_DIR / "complete_*.json"))

    for file_path in biography_files:
        if "aggregated" in file_path or "archive" in file_path:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  [SKIP] {Path(file_path).name}: {type(e).__name__}")
            failed += 1
            continue

        # Handle different JSON structures
        persons = []
        if isinstance(data, list):
            persons = data
        elif isinstance(data, dict) and "persons" in data:
            persons = data["persons"]
        elif isinstance(data, dict) and "slug" in data:
            persons = [data]

        for person in persons:
            slug = person.get("slug", "")
            if not slug:
                continue

            bio_html = person.get("bio_html", "")
            if not bio_html:
                continue

            # Update person record
            cursor.execute(
                "UPDATE persons SET bio_html = ?, review_status = 'DRAFT', source_method = 'AI_ASSISTED' WHERE slug = ?",
                (bio_html, slug)
            )

            if cursor.rowcount > 0:
                loaded += 1
            else:
                print(f"    [NOTFOUND] {slug}")

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Loaded {loaded} completed biographies into database")
    if failed > 0:
        print(f"[FAILED] {failed} files with errors")

    return loaded

if __name__ == "__main__":
    load_biographies()
