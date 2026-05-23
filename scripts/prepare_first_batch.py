#!/usr/bin/env python3
"""
Prepare FIRST BATCH (Late_Antique_Egypt_Syria) for agent enrichment.

This script queries the database for all events in the first batch,
fetches the full entity context (persons, texts, concepts), and writes
a JSON file that the Timeline Event Enricher agent can consume.

Output: staging/batch_Late_Antique_Egypt_Syria.json

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"
STAGING_DIR.mkdir(exist_ok=True)


def prepare_batch(batch_name, date_range):
    """
    Prepare a batch of events for agent enrichment.

    Args:
        batch_name: e.g., "Late_Antique_Egypt_Syria"
        date_range: (start_year, end_year)

    Returns:
        Writes JSON to staging/batch_{batch_name}.json
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    start_year, end_year = date_range

    # Query all events in this date range
    cursor.execute(
        """
        SELECT
            slug, date_label, date_start_year, date_end_year,
            location_slug, persons_involved, texts_involved, concepts_involved
        FROM timeline_events
        WHERE date_start_year >= ? AND date_start_year <= ?
        ORDER BY date_start_year
        """,
        (start_year, end_year),
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

        # Collect all entity slugs
        all_person_slugs.update(event["persons_involved"])
        all_text_slugs.update(event["texts_involved"])
        all_concept_slugs.update(event["concepts_involved"])

    # Fetch all unique entities involved
    persons = {}
    if all_person_slugs:
        placeholders = ",".join("?" * len(all_person_slugs))
        cursor.execute(
            f"""
            SELECT slug, name, role_primary, era, bio_html
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
                "bio_html_excerpt": (
                    row["bio_html"][:200] + "..." if row["bio_html"] else ""
                ),
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

    # Fetch all locations for reference
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
        "batch_id": batch_name,
        "date_range": date_range,
        "event_count": len(events),
        "instructions": (
            "For each event stub below, write a 100–250 word description that:\n"
            "1. Incorporates the date, location, and involved persons/texts/concepts\n"
            "2. Explains the historiographical significance (why it matters to the history of alchemy/chemistry)\n"
            "3. When mentioning a person, text, or concept from the entity list, wrap it in [LINK:slug] markup\n"
            "4. Uses the tone and vocabulary from STYLEGUIDE.md and PROMPTS.md\n"
            "5. Avoids speculation; grounds claims in what is known from the tradition\n"
            "\n"
            "Output format: JSON with 'enriched_events' array containing {slug, description} pairs."
        ),
        "events": events,
        "entities": {
            "persons": list(persons.values()),
            "texts": list(texts.values()),
            "concepts": list(concepts.values()),
            "locations": list(locations.values()),
        },
        "metadata": {
            "batch_name": batch_name,
            "total_events": len(events),
            "unique_persons": len(persons),
            "unique_texts": len(texts),
            "unique_concepts": len(concepts),
            "unique_locations": len(set(e["location_slug"] for e in events)),
        },
    }

    # Write to staging
    output_path = STAGING_DIR / f"batch_{batch_name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Batch context prepared")
    print(f"  Batch: {batch_name}")
    print(f"  Events: {len(events)}")
    print(f"  Unique persons: {len(persons)}")
    print(f"  Unique texts: {len(texts)}")
    print(f"  Unique concepts: {len(concepts)}")
    print(f"  Output: {output_path}")

    return output_path


if __name__ == "__main__":
    # Prepare first batch: Late_Antique_Egypt_Syria (200-600 CE)
    prepare_batch("Late_Antique_Egypt_Syria", (200, 600))
