#!/usr/bin/env python3
"""
Prepare ALL remaining batches (11 of 12) for agent enrichment.

This script prepares batch context files for all 11 remaining batches:
1. Medieval_Islam_Baghdad_Persia
2. Medieval_Islam_Iberia_AlAndalus
3. Medieval_Latin_Europe_Monasteries
4. Medieval_Latin_Europe_Universities
5. Medieval_Byzantium
6. Renaissance_Italy_Florence_Venice
7. Renaissance_Low_Countries
8. Early_Modern_Central_Europe
9. Early_Modern_England
10. Early_Modern_France
11. Early_Modern_Spain_Portugal

Each batch context is saved to staging/batch_{batch_name}.json

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"
STAGING_DIR.mkdir(exist_ok=True)

# Batch definitions: map batch name to slug prefix
BATCHES = [
    ("Medieval_Islam_Baghdad_Persia", "medieval_islam_baghdad_persia"),
    ("Medieval_Islam_Iberia_AlAndalus", "medieval_islam_iberia"),
    ("Medieval_Latin_Europe_Monasteries", "medieval_latin_monasteries"),
    ("Medieval_Latin_Europe_Universities", "medieval_universities"),
    ("Medieval_Byzantium", "medieval_byzantium"),
    ("Renaissance_Italy_Florence_Venice", "renaissance_italy"),
    ("Renaissance_Low_Countries", "renaissance_low_countries"),
    ("Early_Modern_Central_Europe", "early_modern_central_europe"),
    ("Early_Modern_England", "early_modern_england"),
    ("Early_Modern_France", "early_modern_france"),
    ("Early_Modern_Spain_Portugal", "early_modern_spain_portugal"),
]


def prepare_batch(batch_name, slug_prefix):
    """Prepare a single batch for agent enrichment."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query all events with this slug prefix that don't have descriptions yet
    cursor.execute(
        """
        SELECT
            slug, date_label, date_start_year, date_end_year,
            location_slug, persons_involved, texts_involved, concepts_involved
        FROM timeline_events
        WHERE slug LIKE ? AND description IS NULL
        ORDER BY date_start_year
        """,
        (f"event_{slug_prefix}_%",),
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
        "batch_id": batch_name,
        "event_count": len(events),
        "instructions": (
            "For each event stub, write a 100–250 word description following STYLEGUIDE.md. "
            "Wrap entity mentions in [LINK:slug] markup. End with historiographical significance."
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
        },
    }

    # Write to staging
    output_path = STAGING_DIR / f"batch_{batch_name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    return len(events), output_path


def main():
    print("Preparing all 11 remaining batches for agent enrichment...")
    print()

    total_events = 0
    for batch_name, slug_prefix in BATCHES:
        event_count, output_path = prepare_batch(batch_name, slug_prefix)
        total_events += event_count
        print(f"  {batch_name:40s} : {event_count:3d} events -> {output_path.name}")

    print()
    print(f"[SUCCESS] All batches prepared")
    print(f"  Total remaining events: {total_events}")
    print(f"  Batches ready for agent enrichment: {len(BATCHES)}")
    print()
    print("Next steps:")
    print("  1. Run agents for each batch (can parallelize)")
    print("  2. Load enriched events with scripts/load_enriched_events.py")
    print("  3. Rebuild site with scripts/build_site.py")


if __name__ == "__main__":
    main()
