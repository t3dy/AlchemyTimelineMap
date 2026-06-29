#!/usr/bin/env python3
"""Load enriched event batches from staging into timeline_events table."""

import json
import sqlite3
import sys
import re
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

def generate_slug(text):
    """Generate a slug from text."""
    slug = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')[:50]
    # Remove trailing hyphens
    while slug.endswith('-'):
        slug = slug[:-1]
    return slug

def load_enriched_events(batch_file: str):
    """Load enriched events from staging JSON into timeline_events table."""

    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    with open(batch_path, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Determine batch ID from filename or batch data
    batch_id = batch.get("batch_id", batch_path.stem)
    print(f"Loading enriched events from batch: {batch_id}\n")

    events_loaded = 0
    events_skipped = 0

    # Events can be under "enriched_events" or "events" key
    event_list = batch.get("enriched_events", batch.get("events", []))

    for event in event_list:
        try:
            # Generate slug if not provided
            if "slug" not in event:
                event["slug"] = generate_slug(event.get("title", ""))

            slug = event["slug"]

            # Check if event already exists
            cursor.execute("SELECT id FROM timeline_events WHERE slug = ?", (slug,))
            if cursor.fetchone():
                events_skipped += 1
                continue

            # Parse event data
            date_label = event.get("date_label", "")
            date_start_year = event.get("date_start_year", 1000)
            description = event.get("description", "")
            location_slug = event.get("location_slug", "unknown")
            scholarly_grounding = event.get("scholarly_grounding", "")

            # Serialize entity references as JSON
            persons_json = json.dumps(event.get("persons_involved", []))
            texts_json = json.dumps(event.get("texts_involved", []))
            concepts_json = json.dumps(event.get("concepts_involved", []))

            # Insert event
            cursor.execute("""
                INSERT INTO timeline_events
                (slug, date_label, date_start_year, location_slug, description,
                 scholarly_grounding, persons_involved, texts_involved, concepts_involved,
                 source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                slug,
                date_label,
                date_start_year,
                location_slug,
                description,
                scholarly_grounding,
                persons_json,
                texts_json,
                concepts_json,
                event.get("source_method", "SCHOLARSHIP_BASED"),
                event.get("review_status", "DRAFT"),
                event.get("confidence", "MEDIUM")
            ))

            events_loaded += 1
            print(f"  [OK] Event: {slug}")

        except Exception as e:
            print(f"  [ERROR] Event {event.get('slug', '?')}: {e}")

    # Commit all changes
    conn.commit()
    conn.close()

    print(f"\n=== BATCH LOADED ===")
    print(f"Events loaded: {events_loaded}")
    print(f"Events skipped (already exist): {events_skipped}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_enriched_events_batch.py <batch_file.json>")
        sys.exit(1)

    success = load_enriched_events(sys.argv[1])
    sys.exit(0 if success else 1)
