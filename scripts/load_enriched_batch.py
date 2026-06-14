#!/usr/bin/env python3
"""Load enriched batch JSON into database (persons, texts, concepts, events)."""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

def load_batch(batch_file: str):
    """Load all entities from a batch JSON file."""

    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    with open(batch_path, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    batch_name = batch.get("batch_name", "Unknown")
    print(f"Loading batch: {batch_name}\n")

    # Load persons
    persons_loaded = 0
    role_map = {
        'Alchemist': 'ALCHEMIST',
        'Chemist': 'CHEMIST',
        'Scholar': 'SCHOLAR',
        'Philosopher': 'PHILOSOPHER',
        'Physician': 'PHYSICIAN',
        'Translator': 'TRANSLATOR',
        'Mathematician': 'MATHEMATICIAN',
        'Poet': 'POET',
        'Patron': 'PATRON',
        'Clerical': 'CLERICAL'
    }
    era_map = {
        'Antiquity': 'ANTIQUITY',
        'Late Antique': 'LATE_ANTIQUE',
        'Medieval': 'MEDIEVAL',
        'Renaissance': 'RENAISSANCE',
        'Early Modern': 'EARLY_MODERN',
        'Modern': 'MODERN'
    }

    for person in batch.get("persons", []):
        try:
            role = role_map.get(person.get('role', 'Scholar'), 'SCHOLAR')
            era = era_map.get(person.get('era', 'Modern'), 'MODERN')

            cursor.execute("""
                INSERT OR REPLACE INTO persons
                (slug, name, era, role_primary, bio_html, source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                person['slug'],
                person['name'],
                era,
                role,
                person['bio_html'],
                person.get('source_method', 'SCHOLARSHIP_BASED'),
                person.get('review_status', 'DRAFT'),
                person.get('confidence', 'MEDIUM')
            ))
            persons_loaded += 1
            print(f"  [OK] Person: {person['name']}")
        except Exception as e:
            print(f"  [ERROR] Person {person.get('slug', '?')}: {e}")

    # Load texts
    texts_loaded = 0
    text_type_map = {
        'PRIMARY_SOURCE': 'PRIMARY_SOURCE',
        'COMMENTARY': 'COMMENTARY',
        'COMPILATION': 'COMPILATION',
        'TREATISE': 'TREATISE',
        'SCHOLARSHIP': 'SCHOLARSHIP',
        'ENCYCLOPEDIA': 'ENCYCLOPEDIA',
        'Emblem book': 'TREATISE',  # Map Maier's emblem book to TREATISE
        'emblem-book': 'TREATISE'
    }

    for text in batch.get("texts", []):
        try:
            text_type = text_type_map.get(text.get('format', 'TREATISE'), 'TREATISE')

            cursor.execute("""
                INSERT OR REPLACE INTO texts
                (slug, title, text_type, composition_date, analysis_html, source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                text['slug'],
                text['title'],
                text_type,
                text.get('composition_date', text.get('date_label', '')),
                text.get('analysis_html', text.get('analysis', '')),
                text.get('source_method', 'SCHOLARSHIP_BASED'),
                text.get('review_status', 'DRAFT'),
                text.get('confidence', 'MEDIUM')
            ))
            texts_loaded += 1
            print(f"  [OK] Text: {text['title']}")
        except Exception as e:
            print(f"  [ERROR] Text {text.get('slug', '?')}: {e}")

    # Load concepts
    concepts_loaded = 0
    for concept in batch.get("concepts", []):
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO concepts
                (slug, label, category_type, definition_long, source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                concept['slug'],
                concept.get('label', concept.get('term', '')),
                concept.get('type', 'ANALYST_TERM'),
                concept['definition_long'],
                concept.get('source_method', 'SCHOLARSHIP_BASED'),
                concept.get('review_status', 'DRAFT'),
                concept.get('confidence', 'MEDIUM')
            ))
            concepts_loaded += 1
            term_label = concept.get('label', concept.get('term', '?'))
            print(f"  [OK] Concept: {term_label}")
        except Exception as e:
            print(f"  [ERROR] Concept {concept.get('slug', '?')}: {e}")

    # Load events
    events_loaded = 0
    for event in batch.get("events", []):
        try:
            # Generate slug from title
            import re
            event_slug = re.sub(r'[^\w\s-]', '', event['title'].lower()).replace(' ', '-')[:50]

            # Parse date_sort to start_year
            date_start_year = event.get('date_sort', 1000)
            date_end_year = None

            # Serialize entity references as JSON
            persons_json = json.dumps(event.get('persons_involved', []))
            texts_json = json.dumps(event.get('texts_involved', []))
            concepts_json = json.dumps(event.get('concepts_involved', []))

            # Insert event
            cursor.execute("""
                INSERT INTO timeline_events
                (slug, date_label, date_start_year, location_slug, description,
                 scholarly_grounding, persons_involved, texts_involved, concepts_involved,
                 source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_slug,
                event['date_label'],
                date_start_year,
                event.get('location_slug', 'unknown'),
                event['description'],
                event.get('scholarly_grounding', ''),
                persons_json,
                texts_json,
                concepts_json,
                event.get('source_method', 'SCHOLARSHIP_BASED'),
                event.get('review_status', 'DRAFT'),
                event.get('confidence', 'MEDIUM')
            ))

            events_loaded += 1
            print(f"  [OK] Event: {event['title']}")
        except Exception as e:
            print(f"  [ERROR] Event {event.get('title', '?')}: {e}")

    # Commit all changes
    conn.commit()
    conn.close()

    print(f"\n=== BATCH LOADED ===")
    print(f"Persons: {persons_loaded}")
    print(f"Texts: {texts_loaded}")
    print(f"Concepts: {concepts_loaded}")
    print(f"Events: {events_loaded}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_enriched_batch.py <batch_file.json>")
        sys.exit(1)

    success = load_batch(sys.argv[1])
    sys.exit(0 if success else 1)
