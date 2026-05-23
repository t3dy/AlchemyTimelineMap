#!/usr/bin/env python3
"""
Load archive-extracted entities (persons, texts) into the database.
Creates timeline entries for each entity.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"
MASTER_FILE = STAGING_DIR / "master_archive_entities.json"

def load_master_data():
    """Load master archive extraction file."""
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def slug_from_name(name):
    """Generate slug from person/text name."""
    return name.lower().replace(" ", "-").replace(".", "").replace("'", "")

def load_persons(master_data):
    """Load persons from archive extraction into database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    skipped = 0

    for person in master_data["entities"]["persons"]:
        name = person.get("name", "")
        slug = slug_from_name(name)
        era = person.get("era_mentioned", "").split("–")[0].strip()  # Extract era

        # Map era mentions to database enum values
        era_map = {
            "c. 250": "LATE_ANTIQUE",
            "c. 722": "MEDIEVAL",
            "9th": "MEDIEVAL",
            "c. 865": "MEDIEVAL",
            "c. 1098": "MEDIEVAL",
            "c. 1114": "MEDIEVAL",
            "c. 1214": "MEDIEVAL",
            "c. 1235": "MEDIEVAL",
            "1493": "RENAISSANCE",
            "1560": "EARLY_MODERN",
            "1568": "EARLY_MODERN",
            "1627": "EARLY_MODERN",
            "1628": "EARLY_MODERN",
            "1643": "EARLY_MODERN",
            "1749": "EARLY_MODERN",
        }

        db_era = "MEDIEVAL"  # Default
        for key, val in era_map.items():
            if key in person.get("era_mentioned", ""):
                db_era = val
                break

        role = person.get("role_category", "ALCHEMIST")

        # Check if person already exists
        cursor.execute("SELECT slug FROM persons WHERE slug = ?", (slug,))
        if cursor.fetchone():
            skipped += 1
            continue

        # Insert person
        cursor.execute(
            """
            INSERT INTO persons
            (slug, name, role_primary, era, bio_html, source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                slug,
                name,
                role,
                db_era,
                f"<p>{person.get('significance', '')} Born: {person.get('era_mentioned', 'unknown')}. Location: {person.get('location_mentioned', 'unknown')}.</p>",
                "AI_ASSISTED",
                "DRAFT",
                "HIGH"
            )
        )
        loaded += 1

    conn.commit()
    conn.close()
    return loaded, skipped

def load_texts(master_data):
    """Load texts from archive extraction into database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    skipped = 0

    for text in master_data["entities"]["texts"]:
        title = text.get("title", "")
        slug = slug_from_name(title)

        # Check if text already exists
        cursor.execute("SELECT slug FROM texts WHERE slug = ?", (slug,))
        if cursor.fetchone():
            skipped += 1
            continue

        text_type = text.get("text_type", "PRIMARY_SOURCE")
        lang = text.get("original_language", "Latin")

        # Insert text
        cursor.execute(
            """
            INSERT INTO texts
            (slug, title, text_type, original_language, composition_date, analysis_html, source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                slug,
                title,
                text_type,
                lang,
                text.get("date_or_period", "unknown"),
                f"<p>{text.get('significance', '')} Author: {text.get('author_or_tradition', 'unknown')}.</p>",
                "AI_ASSISTED",
                "DRAFT",
                "HIGH"
            )
        )
        loaded += 1

    conn.commit()
    conn.close()
    return loaded, skipped

def create_timeline_entries(master_data):
    """Create timeline events for each loaded entity."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    created = 0

    # Create events for persons
    for person in master_data["entities"]["persons"]:
        name = person.get("name", "")
        slug = slug_from_name(name)

        # Extract year range from era
        era_str = person.get("era_mentioned", "c. 1300")
        event_slug = f"event_{slug}_biography"

        # Check if event already exists
        cursor.execute("SELECT slug FROM timeline_events WHERE slug = ?", (event_slug,))
        if cursor.fetchone():
            continue

        # Insert event
        cursor.execute(
            """
            INSERT INTO timeline_events
            (slug, date_label, date_start_year, date_end_year, location_slug,
             description, persons_involved, texts_involved, concepts_involved,
             source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_slug,
                era_str,
                1200,  # Default start year
                1600,  # Default end year
                "alexandria",  # Default location
                f"Life and work of {name}. {person.get('significance', '')}",
                json.dumps([slug]),
                json.dumps([]),
                json.dumps([]),
                "AI_ASSISTED",
                "DRAFT",
                "MEDIUM"
            )
        )
        created += 1

    # Create events for texts
    for text in master_data["entities"]["texts"]:
        title = text.get("title", "")
        slug = slug_from_name(title)
        event_slug = f"event_{slug}_composition"

        # Check if event already exists
        cursor.execute("SELECT slug FROM timeline_events WHERE slug = ?", (event_slug,))
        if cursor.fetchone():
            continue

        # Insert event
        cursor.execute(
            """
            INSERT INTO timeline_events
            (slug, date_label, date_start_year, date_end_year, location_slug,
             description, persons_involved, texts_involved, concepts_involved,
             source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_slug,
                text.get("date_or_period", "unknown"),
                1200,
                1600,
                "alexandria",
                f"Composition and transmission of {title}. {text.get('significance', '')}",
                json.dumps([]),
                json.dumps([slug]),
                json.dumps([]),
                "AI_ASSISTED",
                "DRAFT",
                "MEDIUM"
            )
        )
        created += 1

    conn.commit()
    conn.close()
    return created

def main():
    print("Loading archive-extracted entities into database...\n")

    # Load master data
    master_data = load_master_data()
    print(f"Loaded master archive file with {len(master_data['entities']['persons'])} persons, "
          f"{len(master_data['entities']['scholars'])} scholars, {len(master_data['entities']['texts'])} texts\n")

    # Load persons
    print("Loading persons...")
    p_loaded, p_skipped = load_persons(master_data)
    print(f"  Loaded: {p_loaded}, Skipped (duplicates): {p_skipped}\n")

    # Load texts
    print("Loading texts...")
    t_loaded, t_skipped = load_texts(master_data)
    print(f"  Loaded: {t_loaded}, Skipped (duplicates): {t_skipped}\n")

    # Create timeline entries
    print("Creating timeline entries...")
    events_created = create_timeline_entries(master_data)
    print(f"  Created: {events_created} timeline events\n")

    print(f"[SUCCESS] Archive entities loaded and timeline entries created")
    print(f"  Total persons added: {p_loaded}")
    print(f"  Total texts added: {t_loaded}")
    print(f"  Total timeline events created: {events_created}")

if __name__ == "__main__":
    main()
