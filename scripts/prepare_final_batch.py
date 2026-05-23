#!/usr/bin/env python3
"""
Prepare final batch of 40 unenriched events for enrichment.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"
STAGING_DIR.mkdir(exist_ok=True)


def prepare_final_batch():
    """Prepare all remaining unenriched events."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all events without descriptions
    cursor.execute(
        """
        SELECT
            slug, date_label, date_start_year, date_end_year,
            location_slug, persons_involved, texts_involved, concepts_involved
        FROM timeline_events
        WHERE description IS NULL
        ORDER BY date_start_year
        """
    )

    events = []
    all_person_slugs = set()
    all_text_slugs = set()
    all_concept_slugs = set()

    for row in cursor.fetchall():
        event = {
            "slug": row["slug"],
            "date_label": row["date_label"],
            "date_start_year": row["date_start_year"],
            "date_end_year": row["date_end_year"],
            "location_slug": row["location_slug"],
            "persons_involved": json.loads(row["persons_involved"] or "[]"),
            "texts_involved": json.loads(row["texts_involved"] or "[]"),
            "concepts_involved": json.loads(row["concepts_involved"] or "[]"),
        }
        events.append(event)

        all_person_slugs.update(event["persons_involved"])
        all_text_slugs.update(event["texts_involved"])
        all_concept_slugs.update(event["concepts_involved"])

    # Fetch all unique entities
    persons = {}
    if all_person_slugs:
        placeholders = ",".join("?" * len(all_person_slugs))
        cursor.execute(
            f"""
            SELECT slug, name, role_primary, era
            FROM persons
            WHERE slug IN ({placeholders})
            """,
            list(all_person_slugs),
        )
        for row in cursor.fetchall():
            persons[row["slug"]] = {
                "slug": row["slug"],
                "name": row["name"],
                "role_primary": row["role_primary"],
                "era": row["era"],
            }

    texts = {}
    if all_text_slugs:
        placeholders = ",".join("?" * len(all_text_slugs))
        cursor.execute(
            f"""
            SELECT slug, title, text_type, composition_date
            FROM texts
            WHERE slug IN ({placeholders})
            """,
            list(all_text_slugs),
        )
        for row in cursor.fetchall():
            texts[row["slug"]] = {
                "slug": row["slug"],
                "title": row["title"],
                "text_type": row["text_type"],
                "composition_date": row["composition_date"],
            }

    concepts = {}
    if all_concept_slugs:
        placeholders = ",".join("?" * len(all_concept_slugs))
        cursor.execute(
            f"""
            SELECT slug, label, category_type
            FROM concepts
            WHERE slug IN ({placeholders})
            """,
            list(all_concept_slugs),
        )
        for row in cursor.fetchall():
            concepts[row["slug"]] = {
                "slug": row["slug"],
                "label": row["label"],
                "category_type": row["category_type"],
            }

    # Fetch all locations
    cursor.execute("SELECT slug, place_name, latitude, longitude FROM locations")
    locations = {}
    for row in cursor.fetchall():
        locations[row["slug"]] = {
            "slug": row["slug"],
            "place_name": row["place_name"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
        }

    conn.close()

    # Build context JSON
    context = {
        "batch_id": "Final_Remaining_Events",
        "event_count": len(events),
        "instructions": (
            "Enrich all remaining unenriched events with 100–250 word descriptions. "
            "Follow STYLEGUIDE.md. Wrap entities in [LINK:slug]. End with historiographical significance."
        ),
        "events": events,
        "entities": {
            "persons": list(persons.values()),
            "texts": list(texts.values()),
            "concepts": list(concepts.values()),
            "locations": list(locations.values()),
        },
        "metadata": {
            "batch_name": "Final_Remaining_Events",
            "total_events": len(events),
            "unique_persons": len(persons),
            "unique_texts": len(texts),
            "unique_concepts": len(concepts),
        },
    }

    # Write to staging
    output_path = STAGING_DIR / "batch_Final_Remaining_Events.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Final batch prepared")
    print(f"  Events: {len(events)}")
    print(f"  Persons: {len(persons)}")
    print(f"  Texts: {len(texts)}")
    print(f"  Concepts: {len(concepts)}")
    print(f"  Output: {output_path}")

    return len(events)


if __name__ == "__main__":
    prepare_final_batch()
