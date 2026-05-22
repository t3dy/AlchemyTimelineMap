#!/usr/bin/env python3
"""
Load seed data (persons, texts, concepts, locations) into ALCHEMYTIMELINEMAP database.

This script reads seed_data.json and loads all entities into SQLite. It is fully idempotent
using INSERT OR IGNORE to prevent duplication.

Usage:
    python scripts/load_seed_data.py

Input:
    data/seed_data.json (persons, texts, concepts, locations arrays)

Output:
    Populated SQLite tables: persons, texts, concepts, locations

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
SEED_DATA_PATH = Path(__file__).parent.parent / "data" / "seed_data.json"


def load_seed_data():
    """Load seed data from JSON into SQLite database."""

    # Read seed data
    print(f"Loading seed data from {SEED_DATA_PATH}...")
    with open(SEED_DATA_PATH, "r", encoding="utf-8") as f:
        seed_data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ========== Load Persons ==========
    print(f"\nLoading {len(seed_data['persons'])} persons...")
    for person in seed_data["persons"]:
        cursor.execute(
            """
            INSERT OR IGNORE INTO persons
            (slug, name, role_primary, era, bio_html, source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                person["slug"],
                person["name"],
                person["role_primary"],
                person["era"],
                person.get("bio_html", person.get("bio_summary", "")),
                person["source_method"],
                person["review_status"],
                person["confidence"],
            ),
        )
    print(f"  [OK] {len(seed_data['persons'])} persons loaded")

    # ========== Load Texts ==========
    print(f"\nLoading {len(seed_data['texts'])} texts...")
    for text in seed_data["texts"]:
        cursor.execute(
            """
            INSERT OR IGNORE INTO texts
            (slug, title, text_type, original_language, composition_date,
             composition_year_start, composition_year_end, analysis_html,
             source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                text["slug"],
                text["title"],
                text["text_type"],
                text.get("original_language", ""),
                text["composition_date"],
                text["composition_year_start"],
                text["composition_year_end"],
                text.get("analysis_html", text.get("analysis_summary", "")),
                text["source_method"],
                text["review_status"],
                text["confidence"],
            ),
        )
    print(f"  [OK] {len(seed_data['texts'])} texts loaded")

    # ========== Load Concepts ==========
    print(f"\nLoading {len(seed_data['concepts'])} concepts...")
    for concept in seed_data["concepts"]:
        cursor.execute(
            """
            INSERT OR IGNORE INTO concepts
            (slug, label, category_type, definition_short, definition_long,
             operation_type, source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                concept["slug"],
                concept["label"],
                concept["category_type"],
                concept.get("definition_short", ""),
                concept.get("definition_long", ""),
                concept.get("operation_type", None),
                concept.get("source_method", "MANUAL"),
                concept.get("review_status", "DRAFT"),
                concept.get("confidence", "MEDIUM"),
            ),
        )
    print(f"  [OK] {len(seed_data['concepts'])} concepts loaded")

    # ========== Load Locations ==========
    print(f"\nLoading {len(seed_data['locations'])} locations...")
    for location in seed_data["locations"]:
        cursor.execute(
            """
            INSERT OR IGNORE INTO locations
            (slug, place_name, latitude, longitude, region, modern_name)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                location["slug"],
                location["place_name"],
                location["latitude"],
                location["longitude"],
                location["region"],
                location.get("modern_name", ""),
            ),
        )
    print(f"  [OK] {len(seed_data['locations'])} locations loaded")

    # Commit and close
    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Seed data loaded successfully")
    print(f"   Total persons: {len(seed_data['persons'])}")
    print(f"   Total texts: {len(seed_data['texts'])}")
    print(f"   Total concepts: {len(seed_data['concepts'])}")
    print(f"   Total locations: {len(seed_data['locations'])}")


if __name__ == "__main__":
    load_seed_data()
