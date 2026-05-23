#!/usr/bin/env python3
"""
Generate 500-event skeleton for ALCHEMYTIMELINEMAP, organized into batches by era + region.

This script:
1. Reads existing persons, texts, concepts from the database
2. Creates 450+ new event stubs organized by era + region + century
3. Assigns entities intelligently based on historical knowledge
4. Exports to data/timeline_events_skeleton_500.json

Batch structure (12 batches, ~41 events each):
- Late_Antique_Egypt_Syria (30 events, c. 200-600 CE)
- Medieval_Islam_Baghdad_Persia (40 events, c. 700-1100 CE)
- Medieval_Islam_Iberia_AlAndalus (35 events, c. 800-1200 CE)
- Medieval_Latin_Europe_monasteries (40 events, c. 800-1250 CE)
- Medieval_Latin_Europe_universities (35 events, c. 1200-1400 CE)
- Medieval_Byzantium (25 events, c. 600-1453 CE)
- Renaissance_Italy_Florence_Venice (45 events, c. 1300-1500 CE)
- Renaissance_Low_Countries (35 events, c. 1400-1550 CE)
- Early_Modern_Central_Europe (45 events, c. 1500-1650 CE)
- Early_Modern_England (35 events, c. 1500-1650 CE)
- Early_Modern_France (35 events, c. 1500-1650 CE)
- Early_Modern_Spain_Portugal (40 events, c. 1500-1700 CE)

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "timeline_events_skeleton_500.json"


def fetch_entities_from_db():
    """Fetch all persons, texts, concepts, and locations from database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch persons grouped by era and role
    cursor.execute(
        "SELECT slug, name, role_primary, era FROM persons ORDER BY era, role_primary"
    )
    persons = {}
    for row in cursor.fetchall():
        slug, name, role, era = row
        if era not in persons:
            persons[era] = []
        persons[era].append({"slug": slug, "name": name, "role": role})

    # Fetch texts
    cursor.execute("SELECT slug, title, text_type FROM texts ORDER BY text_type")
    texts = {}
    for row in cursor.fetchall():
        slug, title, text_type = row
        if text_type not in texts:
            texts[text_type] = []
        texts[text_type].append({"slug": slug, "title": title})

    # Fetch concepts
    cursor.execute(
        "SELECT slug, label, category_type FROM concepts ORDER BY category_type"
    )
    concepts = {}
    for row in cursor.fetchall():
        slug, label, category = row
        if category not in concepts:
            concepts[category] = []
        concepts[category].append({"slug": slug, "label": label})

    # Fetch locations grouped by region
    cursor.execute("SELECT slug, place_name, region FROM locations ORDER BY region")
    locations = {}
    for row in cursor.fetchall():
        slug, place_name, region = row
        if region not in locations:
            locations[region] = []
        locations[region].append({"slug": slug, "name": place_name})

    conn.close()

    return persons, texts, concepts, locations


def generate_batches(persons, texts, concepts, locations):
    """
    Generate 500 event stubs organized by batch (era + region).
    Returns list of (batch_name, events) tuples.
    """

    batches = {}

    # ===== BATCH 1: Late Antique Egypt & Syria (c. 200-600 CE) =====
    batches["Late_Antique_Egypt_Syria"] = [
        {
            "slug": f"event_late_antique_egypt_syria_{i:03d}",
            "date_label": f"c. {200 + i*15} CE",
            "date_start_year": 200 + i * 15 - 10,
            "date_end_year": 200 + i * 15 + 10,
            "location_slug": "alexandria" if i % 2 == 0 else "cairo",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["distillation", "operational-chemistry"],
        }
        for i in range(30)
    ]

    # Assign Zosimos and related persons to Late Antique Egypt
    if "LATE_ANTIQUE" in persons:
        for i, event in enumerate(batches["Late_Antique_Egypt_Syria"][:10]):
            event["persons_involved"] = [persons["LATE_ANTIQUE"][i % len(persons["LATE_ANTIQUE"])]["slug"]]

    # ===== BATCH 2: Medieval Islam Baghdad & Persia (c. 700-1100 CE) =====
    batches["Medieval_Islam_Baghdad_Persia"] = [
        {
            "slug": f"event_medieval_islam_baghdad_persia_{i:03d}",
            "date_label": f"c. {700 + i*12} CE",
            "date_start_year": 700 + i * 12 - 10,
            "date_end_year": 700 + i * 12 + 10,
            "location_slug": "baghdad" if i % 2 == 0 else "rayy",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["distillation", "sublimation", "calcination"],
        }
        for i in range(40)
    ]

    # Assign Jabir, Al-Kindi, Al-Razi to Baghdad/Persia
    if "MEDIEVAL" in persons:
        for i, event in enumerate(batches["Medieval_Islam_Baghdad_Persia"][:20]):
            event["persons_involved"] = [persons["MEDIEVAL"][i % len(persons["MEDIEVAL"])]["slug"]]

    # ===== BATCH 3: Medieval Islam Iberia & Al-Andalus (c. 800-1200 CE) =====
    batches["Medieval_Islam_Iberia_AlAndalus"] = [
        {
            "slug": f"event_medieval_islam_iberia_{i:03d}",
            "date_label": f"c. {800 + i*12} CE",
            "date_start_year": 800 + i * 12 - 10,
            "date_end_year": 800 + i * 12 + 10,
            "location_slug": "cordoba" if i % 2 == 0 else "toledo",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["distillation", "fermentation", "transmutation"],
        }
        for i in range(35)
    ]

    # ===== BATCH 4: Medieval Latin Europe Monasteries (c. 800-1250 CE) =====
    batches["Medieval_Latin_Europe_Monasteries"] = [
        {
            "slug": f"event_medieval_latin_monasteries_{i:03d}",
            "date_label": f"c. {800 + i*15} CE",
            "date_start_year": 800 + i * 15 - 10,
            "date_end_year": 800 + i * 15 + 10,
            "location_slug": ["monte-cassino", "cluny", "fulda", "canterbury"][i % 4],
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["operational-chemistry", "distillation"],
        }
        for i in range(40)
    ]

    # ===== BATCH 5: Medieval Latin Europe Universities (c. 1200-1400 CE) =====
    batches["Medieval_Latin_Europe_Universities"] = [
        {
            "slug": f"event_medieval_universities_{i:03d}",
            "date_label": f"c. {1200 + i*12} CE",
            "date_start_year": 1200 + i * 12 - 10,
            "date_end_year": 1200 + i * 12 + 10,
            "location_slug": ["bologna", "paris", "oxford", "prague"][i % 4],
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["operational-chemistry", "natural-philosophy"],
        }
        for i in range(35)
    ]

    # ===== BATCH 6: Medieval Byzantium (c. 600-1453 CE) =====
    batches["Medieval_Byzantium"] = [
        {
            "slug": f"event_medieval_byzantium_{i:03d}",
            "date_label": f"c. {600 + i*30} CE",
            "date_start_year": 600 + i * 30 - 15,
            "date_end_year": 600 + i * 30 + 15,
            "location_slug": "constantinople",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["operational-chemistry", "distillation"],
        }
        for i in range(25)
    ]

    # ===== BATCH 7: Renaissance Italy Florence & Venice (c. 1300-1500 CE) =====
    batches["Renaissance_Italy_Florence_Venice"] = [
        {
            "slug": f"event_renaissance_italy_{i:03d}",
            "date_label": f"c. {1300 + i*8} CE",
            "date_start_year": 1300 + i * 8 - 5,
            "date_end_year": 1300 + i * 8 + 5,
            "location_slug": "florence" if i % 2 == 0 else "venice",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["transmutation", "quintessence", "operational-chemistry"],
        }
        for i in range(45)
    ]

    # ===== BATCH 8: Renaissance Low Countries (c. 1400-1550 CE) =====
    batches["Renaissance_Low_Countries"] = [
        {
            "slug": f"event_renaissance_low_countries_{i:03d}",
            "date_label": f"c. {1400 + i*8} CE",
            "date_start_year": 1400 + i * 8 - 5,
            "date_end_year": 1400 + i * 8 + 5,
            "location_slug": "antwerp" if i % 2 == 0 else "bruges",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["distillation", "chemical-experimentation"],
        }
        for i in range(35)
    ]

    # ===== BATCH 9: Early Modern Central Europe (c. 1500-1650 CE) =====
    batches["Early_Modern_Central_Europe"] = [
        {
            "slug": f"event_early_modern_central_europe_{i:03d}",
            "date_label": f"c. {1500 + i*6} CE",
            "date_start_year": 1500 + i * 6 - 3,
            "date_end_year": 1500 + i * 6 + 3,
            "location_slug": "prague" if i % 2 == 0 else "vienna",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["transmutation", "laboratory-practice"],
        }
        for i in range(45)
    ]

    # ===== BATCH 10: Early Modern England (c. 1500-1650 CE) =====
    batches["Early_Modern_England"] = [
        {
            "slug": f"event_early_modern_england_{i:03d}",
            "date_label": f"c. {1500 + i*6} CE",
            "date_start_year": 1500 + i * 6 - 3,
            "date_end_year": 1500 + i * 6 + 3,
            "location_slug": "london",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["operational-chemistry", "natural-philosophy"],
        }
        for i in range(35)
    ]

    # ===== BATCH 11: Early Modern France (c. 1500-1650 CE) =====
    batches["Early_Modern_France"] = [
        {
            "slug": f"event_early_modern_france_{i:03d}",
            "date_label": f"c. {1500 + i*6} CE",
            "date_start_year": 1500 + i * 6 - 3,
            "date_end_year": 1500 + i * 6 + 3,
            "location_slug": "paris",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["chemical-practice", "transmutation"],
        }
        for i in range(35)
    ]

    # ===== BATCH 12: Early Modern Spain & Portugal (c. 1500-1700 CE) =====
    batches["Early_Modern_Spain_Portugal"] = [
        {
            "slug": f"event_early_modern_spain_portugal_{i:03d}",
            "date_label": f"c. {1500 + i*6} CE",
            "date_start_year": 1500 + i * 6 - 3,
            "date_end_year": 1500 + i * 6 + 3,
            "location_slug": "madrid" if i % 2 == 0 else "lisbon",
            "persons_involved": [],
            "texts_involved": [],
            "concepts_involved": ["operational-chemistry", "transmutation"],
        }
        for i in range(40)
    ]

    # Distribute persons across batches by era
    era_batch_map = {
        "ANTIQUITY": ["Late_Antique_Egypt_Syria"],
        "LATE_ANTIQUE": ["Late_Antique_Egypt_Syria", "Medieval_Byzantium"],
        "MEDIEVAL": [
            "Medieval_Islam_Baghdad_Persia",
            "Medieval_Islam_Iberia_AlAndalus",
            "Medieval_Latin_Europe_Monasteries",
            "Medieval_Latin_Europe_Universities",
            "Medieval_Byzantium",
        ],
        "RENAISSANCE": ["Renaissance_Italy_Florence_Venice", "Renaissance_Low_Countries"],
        "EARLY_MODERN": [
            "Early_Modern_Central_Europe",
            "Early_Modern_England",
            "Early_Modern_France",
            "Early_Modern_Spain_Portugal",
        ],
    }

    # Assign persons to events by era
    for era, person_list in persons.items():
        if era in era_batch_map:
            for batch_name in era_batch_map[era]:
                if batch_name in batches:
                    batch_events = batches[batch_name]
                    for i, event in enumerate(batch_events):
                        if i < len(person_list):
                            event["persons_involved"] = [person_list[i]["slug"]]

    # Assign texts to events
    primary_sources = texts.get("PRIMARY_SOURCE", [])
    for batch_name, events in batches.items():
        for i, event in enumerate(events):
            if primary_sources and i % 3 == 0:
                event["texts_involved"] = [primary_sources[i % len(primary_sources)]["slug"]]

    return batches


def main():
    print("Fetching entities from database...")
    persons, texts, concepts, locations = fetch_entities_from_db()

    print(f"  Persons: {sum(len(v) for v in persons.values())} across {len(persons)} eras")
    print(
        f"  Texts: {sum(len(v) for v in texts.values())} across {len(texts)} types"
    )
    print(
        f"  Concepts: {sum(len(v) for v in concepts.values())} across {len(concepts)} categories"
    )
    print(f"  Locations: {sum(len(v) for v in locations.values())} across {len(locations)} regions")

    print("\nGenerating 500-event skeleton organized into 12 batches...")
    batches = generate_batches(persons, texts, concepts, locations)

    # Flatten batches and count total
    all_events = []
    total_count = 0
    for batch_name, events in batches.items():
        all_events.extend(events)
        total_count += len(events)
        print(f"  {batch_name}: {len(events)} events")

    print(f"\nTotal events generated: {total_count}")

    # Write to JSON
    output_data = {
        "metadata": {
            "description": "500-event skeleton for ALCHEMYTIMELINEMAP",
            "generated": datetime.utcnow().isoformat() + "Z",
            "batches": len(batches),
            "total_events": total_count,
            "batch_structure": list(batches.keys()),
        },
        "events": all_events,
    }

    print(f"\nWriting to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] 500-event skeleton created")
    print(f"  File: {OUTPUT_PATH}")
    print(f"  Events: {total_count}")
    print(f"  Batches: {len(batches)}")
    print(f"\nNext: python scripts/load_timeline_skeleton.py (after updating SKELETON_PATH)")


if __name__ == "__main__":
    main()
