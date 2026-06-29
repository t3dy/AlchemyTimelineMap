#!/usr/bin/env python3
"""Load text analysis batches from staging into texts table."""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

def load_text_analyses(batch_file: str):
    """Load text analyses from staging JSON into texts table."""

    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    with open(batch_path, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Loading text analyses from batch: {batch_path.name}\n")

    texts_loaded = 0
    texts_updated = 0
    texts_skipped = 0

    # Batch is a list of text objects
    for text in batch:
        try:
            slug = text.get("slug", "")
            if not slug:
                print(f"  [SKIP] Text has no slug")
                texts_skipped += 1
                continue

            # Check if text already exists
            cursor.execute("SELECT id FROM texts WHERE slug = ?", (slug,))
            existing = cursor.fetchone()

            if existing:
                # Update existing text with analysis
                cursor.execute("""
                    UPDATE texts
                    SET analysis_html = ?, review_status = ?, confidence = ?
                    WHERE slug = ?
                """, (
                    text.get("analysis_html", ""),
                    text.get("metadata", {}).get("review_status", "DRAFT"),
                    text.get("metadata", {}).get("confidence", "MEDIUM"),
                    slug
                ))
                texts_updated += 1
                print(f"  [UPDATED] Text: {slug}")
            else:
                # Insert new text
                cursor.execute("""
                    INSERT INTO texts
                    (slug, title, text_type, composition_date, analysis_html, source_method, review_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    slug,
                    text.get("title", slug.replace("-", " ").title()),
                    text.get("text_type", "TREATISE"),
                    text.get("composition_date", ""),
                    text.get("analysis_html", ""),
                    text.get("source_method", "SCHOLARSHIP_BASED"),
                    text.get("metadata", {}).get("review_status", "DRAFT"),
                    text.get("metadata", {}).get("confidence", "MEDIUM")
                ))
                texts_loaded += 1
                print(f"  [NEW] Text: {slug}")

        except Exception as e:
            print(f"  [ERROR] Text {text.get('slug', '?')}: {e}")

    # Commit all changes
    conn.commit()
    conn.close()

    print(f"\n=== BATCH LOADED ===")
    print(f"Texts loaded: {texts_loaded}")
    print(f"Texts updated: {texts_updated}")
    print(f"Texts skipped: {texts_skipped}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_text_analyses_batch.py <batch_file.json>")
        sys.exit(1)

    success = load_text_analyses(sys.argv[1])
    sys.exit(0 if success else 1)
