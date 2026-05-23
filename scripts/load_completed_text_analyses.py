#!/usr/bin/env python3
"""Load completed text analyses from staging into database."""

import json
import sqlite3
import glob
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"

def load_text_analyses():
    """Load all completed text analysis JSON files from staging."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    failed = 0

    # Find all text analysis JSON files
    analysis_files = sorted(glob.glob(str(STAGING_DIR / "text_analyses_complete_batch_*.json")))

    for file_path in analysis_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  [SKIP] {Path(file_path).name}: {type(e).__name__}")
            failed += 1
            continue

        # Handle different JSON structures
        texts = []
        if isinstance(data, list):
            texts = data
        elif isinstance(data, dict) and "texts" in data:
            texts = data["texts"]
        elif isinstance(data, dict) and "slug" in data:
            texts = [data]

        for text in texts:
            slug = text.get("slug", "")
            if not slug:
                continue

            analysis_html = text.get("analysis_html", "")
            if not analysis_html:
                continue

            # Update text record
            cursor.execute(
                "UPDATE texts SET analysis_html = ?, review_status = 'DRAFT', source_method = 'AI_ASSISTED' WHERE slug = ?",
                (analysis_html, slug)
            )

            if cursor.rowcount > 0:
                loaded += 1
            else:
                print(f"    [NOTFOUND] {slug}")

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Loaded {loaded} completed text analyses into database")
    if failed > 0:
        print(f"[FAILED] {failed} files with errors")

    return loaded

if __name__ == "__main__":
    load_text_analyses()
