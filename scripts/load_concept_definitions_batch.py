#!/usr/bin/env python3
"""Load concept definition batches from staging into concepts table."""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

def load_concept_definitions(batch_file: str):
    """Load concept definitions from staging JSON into concepts table."""

    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    with open(batch_path, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Loading concept definitions from batch: {batch_path.name}\n")

    concepts_loaded = 0
    concepts_updated = 0
    concepts_skipped = 0

    # Batch can be a list or a dict with a "concepts" key
    if isinstance(batch, dict) and "concepts" in batch:
        concept_list = batch["concepts"]
    else:
        concept_list = batch if isinstance(batch, list) else [batch]

    for concept in concept_list:
        try:
            slug = concept.get("slug", "")
            if not slug:
                print(f"  [SKIP] Concept has no slug")
                concepts_skipped += 1
                continue

            # Check if concept already exists
            cursor.execute("SELECT id FROM concepts WHERE slug = ?", (slug,))
            existing = cursor.fetchone()

            label = concept.get("label", concept.get("term", slug.replace("-", " ").title()))
            category = concept.get("category_type", concept.get("type", "ANALYST_TERM"))
            definition = concept.get("definition_long", concept.get("definition", ""))

            if existing:
                # Update existing concept with definition
                cursor.execute("""
                    UPDATE concepts
                    SET definition_long = ?, category_type = ?, review_status = ?, confidence = ?
                    WHERE slug = ?
                """, (
                    definition,
                    category,
                    concept.get("review_status", "DRAFT"),
                    concept.get("confidence", "MEDIUM"),
                    slug
                ))
                concepts_updated += 1
                print(f"  [UPDATED] Concept: {slug}")
            else:
                # Insert new concept
                cursor.execute("""
                    INSERT INTO concepts
                    (slug, label, category_type, definition_long, source_method, review_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    slug,
                    label,
                    category,
                    definition,
                    concept.get("source_method", "SCHOLARSHIP_BASED"),
                    concept.get("review_status", "DRAFT"),
                    concept.get("confidence", "MEDIUM")
                ))
                concepts_loaded += 1
                print(f"  [NEW] Concept: {slug}")

        except Exception as e:
            print(f"  [ERROR] Concept {concept.get('slug', '?')}: {e}")

    # Commit all changes
    conn.commit()
    conn.close()

    print(f"\n=== BATCH LOADED ===")
    print(f"Concepts loaded: {concepts_loaded}")
    print(f"Concepts updated: {concepts_updated}")
    print(f"Concepts skipped: {concepts_skipped}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_concept_definitions_batch.py <batch_file.json>")
        sys.exit(1)

    success = load_concept_definitions(sys.argv[1])
    sys.exit(0 if success else 1)
