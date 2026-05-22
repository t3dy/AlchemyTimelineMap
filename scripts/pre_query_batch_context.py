#!/usr/bin/env python3
"""
Pre-query entity context for a batch of timeline events.

This script queries the database for all entities involved in a batch of events
and outputs a compact JSON file with full entity details. Agents use this as context
when enriching event descriptions.

Usage:
    python scripts/pre_query_batch_context.py --batch_id "Medieval_Islam_Iraq_Persia"

Output:
    staging/batch_Medieval_Islam_Iraq_Persia.json (with all entities involved)

See: docs/CONTEXT_ENGINEERING.md for batch strategy

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
import sys
import argparse
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_PATH = Path(__file__).parent.parent / "staging"


def pre_query_batch_context(batch_id, events_query=None):
    """
    Query database and generate batch context JSON for agents.

    Args:
        batch_id: Unique batch identifier (e.g., "Medieval_Islam_Iraq_Persia")
        events_query: Optional SQL WHERE clause to filter events (default: all with NULL descriptions)
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query events for this batch
    # You can refine this query to select specific events by era/region/date range
    if events_query:
        query = f"SELECT * FROM timeline_events WHERE {events_query} ORDER BY date_start_year"
    else:
        # Default: events with NULL descriptions
        query = "SELECT * FROM timeline_events WHERE description IS NULL LIMIT 20 ORDER BY date_start_year"

    cursor.execute(query)
    events = [dict(row) for row in cursor.fetchall()]

    if not events:
        print(f"No events found for batch: {batch_id}")
        conn.close()
        return

    print(f"Querying context for batch: {batch_id}")
    print(f"  Events: {len(events)}")

    # Collect all unique entity slugs involved in this batch
    person_slugs = set()
    text_slugs = set()
    concept_slugs = set()
    location_slugs = set()

    for event in events:
        person_slugs.update(json.loads(event["persons_involved"] or "[]"))
        text_slugs.update(json.loads(event["texts_involved"] or "[]"))
        concept_slugs.update(json.loads(event["concepts_involved"] or "[]"))
        location_slugs.add(event["location_slug"])

    # Query full details for all entities
    print(f"  Persons: {len(person_slugs)}")
    print(f"  Texts: {len(text_slugs)}")
    print(f"  Concepts: {len(concept_slugs)}")
    print(f"  Locations: {len(location_slugs)}")

    # Fetch person details
    persons = []
    if person_slugs:
        placeholders = ",".join("?" * len(person_slugs))
        cursor.execute(
            f"SELECT slug, name, role_primary, era FROM persons WHERE slug IN ({placeholders})",
            list(person_slugs),
        )
        persons = [dict(row) for row in cursor.fetchall()]

    # Fetch text details
    texts = []
    if text_slugs:
        placeholders = ",".join("?" * len(text_slugs))
        cursor.execute(
            f"SELECT slug, title, text_type FROM texts WHERE slug IN ({placeholders})",
            list(text_slugs),
        )
        texts = [dict(row) for row in cursor.fetchall()]

    # Fetch concept details
    concepts = []
    if concept_slugs:
        placeholders = ",".join("?" * len(concept_slugs))
        cursor.execute(
            f"SELECT slug, label, category_type FROM concepts WHERE slug IN ({placeholders})",
            list(concept_slugs),
        )
        concepts = [dict(row) for row in cursor.fetchall()]

    # Fetch location details
    locations = []
    if location_slugs:
        placeholders = ",".join("?" * len(location_slugs))
        cursor.execute(
            f"SELECT slug, place_name, latitude, longitude, region FROM locations WHERE slug IN ({placeholders})",
            list(location_slugs),
        )
        locations = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # Build batch context JSON
    batch_context = {
        "batch_id": batch_id,
        "instructions": """For each event stub, write a 100–250 word description.
Use the entity context provided to understand who/what/where each event involves.
When mentioning a person, text, or concept that exists in the entity list,
wrap it in [LINK:slug] markup. The main session will convert to <a href> tags.
Declare historiographical significance in the final sentence.""",
        "events": events,
        "entities": {
            "persons": persons,
            "texts": texts,
            "concepts": concepts,
            "locations": locations,
        },
    }

    # Write to staging
    STAGING_PATH.mkdir(parents=True, exist_ok=True)
    output_path = STAGING_PATH / f"batch_{batch_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(batch_context, f, indent=2, default=str, ensure_ascii=False)

    print(f"\n[SUCCESS] Batch context saved to {output_path}")
    print(f"   Ready for agent enrichment")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pre-query entity context for a batch of timeline events"
    )
    parser.add_argument(
        "--batch_id", required=True, help="Batch identifier (e.g. Medieval_Islam_Iraq_Persia)"
    )
    parser.add_argument(
        "--query",
        help="Optional SQL WHERE clause to filter events (default: first 20 with NULL descriptions)",
    )

    args = parser.parse_args()
    pre_query_batch_context(args.batch_id, args.query)
