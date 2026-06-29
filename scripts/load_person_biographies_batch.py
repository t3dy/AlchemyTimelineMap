#!/usr/bin/env python3
"""Load person biography batches from staging into persons table."""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

def load_person_biographies(batch_file: str):
    """Load person biographies from staging JSON into persons table."""

    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    with open(batch_path, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Loading person biographies from batch: {batch_path.name}\n")

    persons_loaded = 0
    persons_updated = 0
    persons_skipped = 0

    # Batch is a list of person objects
    for person in batch:
        try:
            slug = person.get("slug", "")
            if not slug:
                print(f"  [SKIP] Person has no slug")
                persons_skipped += 1
                continue

            # Check if person already exists
            cursor.execute("SELECT id FROM persons WHERE slug = ?", (slug,))
            existing = cursor.fetchone()

            if existing:
                # Update existing person with biography
                cursor.execute("""
                    UPDATE persons
                    SET bio_html = ?, review_status = ?, confidence = ?
                    WHERE slug = ?
                """, (
                    person.get("bio_html", ""),
                    person.get("metadata", {}).get("review_status", "DRAFT"),
                    person.get("metadata", {}).get("confidence", "MEDIUM"),
                    slug
                ))
                persons_updated += 1
                print(f"  [UPDATED] Person: {slug}")
            else:
                # Insert new person
                # Infer role and era from name or metadata
                name = person.get("name", slug.replace("-", " ").title())
                role = person.get("role_primary", "ALCHEMIST")
                era = person.get("era", "MEDIEVAL")

                cursor.execute("""
                    INSERT INTO persons
                    (slug, name, era, role_primary, bio_html, source_method, review_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    slug,
                    name,
                    era,
                    role,
                    person.get("bio_html", ""),
                    person.get("source_method", "SCHOLARSHIP_BASED"),
                    person.get("metadata", {}).get("review_status", "DRAFT"),
                    person.get("metadata", {}).get("confidence", "MEDIUM")
                ))
                persons_loaded += 1
                print(f"  [NEW] Person: {slug}")

        except Exception as e:
            print(f"  [ERROR] Person {person.get('slug', '?')}: {e}")

    # Commit all changes
    conn.commit()
    conn.close()

    print(f"\n=== BATCH LOADED ===")
    print(f"Persons loaded: {persons_loaded}")
    print(f"Persons updated: {persons_updated}")
    print(f"Persons skipped: {persons_skipped}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_person_biographies_batch.py <batch_file.json>")
        sys.exit(1)

    success = load_person_biographies(sys.argv[1])
    sys.exit(0 if success else 1)
