#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize ALCHEMYTIMELINEMAP SQLite database with schema and CHECK constraints.

This script creates all 8 tables with proper foreign keys, indexes, and enum
value CHECK constraints. It is fully idempotent: runs `CREATE TABLE IF NOT EXISTS`
and can be re-run safely.

Usage:
    python scripts/init_db.py

Output:
    Creates db/alchemy_timeline.db with empty schema.

Author: Claude
Date: 2026-05-22
"""

import sqlite3
import sys
from pathlib import Path

# Set output encoding to UTF-8 on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"


def create_schema():
    """Create database schema with all tables and constraints."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Creating database schema at {DB_PATH}...")

    # ========== Core Tables ==========

    # TIMELINE_EVENTS: Primary content unit
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            date_label TEXT NOT NULL,
            date_start_year INTEGER,
            date_end_year INTEGER,
            location_slug TEXT NOT NULL,
            description TEXT,

            -- JSON arrays of entity slugs (denormalized for query efficiency)
            persons_involved TEXT,  -- JSON: ["person1", "person2"]
            texts_involved TEXT,    -- JSON: ["text1"]
            concepts_involved TEXT, -- JSON: ["concept1"]

            -- Provenance
            source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
            review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
            confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (location_slug) REFERENCES locations(slug)
        )
    """)
    print("  [OK] timeline_events")

    # PERSONS: Alchemists, chemists, scholars
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role_primary TEXT NOT NULL CHECK(role_primary IN (
                'ALCHEMIST', 'CHEMIST', 'SCHOLAR', 'PHILOSOPHER', 'PHYSICIAN',
                'TRANSLATOR', 'MATHEMATICIAN', 'POET', 'PATRON', 'CLERICAL'
            )),
            era TEXT NOT NULL CHECK(era IN (
                'ANTIQUITY', 'LATE_ANTIQUE', 'MEDIEVAL', 'RENAISSANCE', 'EARLY_MODERN', 'MODERN'
            )),
            bio_html TEXT NOT NULL,

            -- Provenance
            source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
            review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
            confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(name, era)
        )
    """)
    print("  [OK] persons")

    # TEXTS: Treatises, scholarship, compilations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            text_type TEXT NOT NULL CHECK(text_type IN (
                'PRIMARY_SOURCE', 'COMMENTARY', 'COMPILATION', 'TREATISE', 'SCHOLARSHIP', 'ENCYCLOPEDIA'
            )),
            original_language TEXT,
            composition_date TEXT,
            composition_year_start INTEGER,
            composition_year_end INTEGER,
            analysis_html TEXT NOT NULL,

            -- Provenance
            source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
            review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
            confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(title, text_type)
        )
    """)
    print("  [OK] texts")

    # CONCEPTS: Chemical operations, theories, analytical categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            label TEXT NOT NULL,
            category_type TEXT NOT NULL CHECK(category_type IN ('ACTOR_TERM', 'ANALYST_TERM')),
            definition_short TEXT,  -- 60–120 words (index card)
            definition_long TEXT,   -- 1,500–2,500 words (encyclopedia)
            operation_type TEXT CHECK(operation_type IN (
                'DISTILLATION', 'SUBLIMATION', 'CALCINATION', 'FERMENTATION', 'CRYSTALLIZATION',
                'DISSOLUTION', 'COAGULATION', 'PUTREFACTION', 'CIRCULATION'
            )),

            -- Provenance
            source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
            review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
            confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(label, category_type)
        )
    """)
    print("  [OK] concepts")

    # LOCATIONS: Cities and regions with coordinates
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            place_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            region TEXT NOT NULL,
            modern_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(place_name, latitude, longitude)
        )
    """)
    print("  [OK] locations")

    # ========== Reference Tables ==========

    # PERSON_EVENT_REFS: Many-to-many (persons to events)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS person_event_refs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_slug TEXT NOT NULL,
            event_slug TEXT NOT NULL,
            FOREIGN KEY (person_slug) REFERENCES persons(slug),
            FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
            UNIQUE(person_slug, event_slug)
        )
    """)
    print("  [OK] person_event_refs")

    # TEXT_EVENT_REFS: Many-to-many (texts to events)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS text_event_refs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_slug TEXT NOT NULL,
            event_slug TEXT NOT NULL,
            FOREIGN KEY (text_slug) REFERENCES texts(slug),
            FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
            UNIQUE(text_slug, event_slug)
        )
    """)
    print("  [OK] text_event_refs")

    # CONCEPT_EVENT_REFS: Many-to-many (concepts to events)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_event_refs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_slug TEXT NOT NULL,
            event_slug TEXT NOT NULL,
            FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
            FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
            UNIQUE(concept_slug, event_slug)
        )
    """)
    print("  [OK] concept_event_refs")

    # CONCEPT_PERSON_REFS: Many-to-many (concepts to persons)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_person_refs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_slug TEXT NOT NULL,
            person_slug TEXT NOT NULL,
            FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
            FOREIGN KEY (person_slug) REFERENCES persons(slug),
            UNIQUE(concept_slug, person_slug)
        )
    """)
    print("  [OK] concept_person_refs")

    # CONCEPT_TEXT_REFS: Many-to-many (concepts to texts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_text_refs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_slug TEXT NOT NULL,
            text_slug TEXT NOT NULL,
            FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
            FOREIGN KEY (text_slug) REFERENCES texts(slug),
            UNIQUE(concept_slug, text_slug)
        )
    """)
    print("  [OK] concept_text_refs")

    # ========== Create Indexes ==========

    print("\nCreating indexes...")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_date ON timeline_events(date_start_year, date_end_year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_location ON timeline_events(location_slug)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_persons_era ON persons(era)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_persons_role ON persons(role_primary)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_texts_type ON texts(text_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_texts_language ON texts(original_language)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_concepts_category ON concepts(category_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_concepts_operation ON concepts(operation_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_locations_region ON locations(region)")

    print("  [OK] All indexes created")

    # Commit and close
    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Database schema created successfully at {DB_PATH}")
    print(f"   Run `python scripts/load_seed_data.py` next to load initial entities.")


if __name__ == "__main__":
    # Create parent directory if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    create_schema()
