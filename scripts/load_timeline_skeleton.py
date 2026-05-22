#!/usr/bin/env python3
"""
Load timeline event skeleton (500 event stubs) into ALCHEMYTIMELINEMAP database.

This script reads timeline_events_skeleton.json and loads all events with NULL/STUB descriptions.
It also populates reference tables (person_event_refs, text_event_refs, concept_event_refs).
Idempotent: uses INSERT OR IGNORE.

Usage:
    python scripts/load_timeline_skeleton.py

Input:
    data/timeline_events_skeleton.json (events array with date/location/entities)

Output:
    Populated timeline_events table + reference tables

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
SKELETON_PATH = Path(__file__).parent.parent / "data" / "timeline_events_skeleton.json"


def load_timeline_skeleton():
    """Load timeline event skeleton into SQLite database."""

    # Read skeleton
    print(f"Loading timeline event skeleton from {SKELETON_PATH}...")
    with open(SKELETON_PATH, "r", encoding="utf-8") as f:
        skeleton_data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ========== Load Timeline Events ==========
    print(f"\nLoading {len(skeleton_data['events'])} timeline events...")
    for event in skeleton_data["events"]:
        # Insert event with NULL description (to be filled by agents)
        cursor.execute(
            """
            INSERT OR IGNORE INTO timeline_events
            (slug, date_label, date_start_year, date_end_year, location_slug,
             description, persons_involved, texts_involved, concepts_involved,
             source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event["slug"],
                event["date_label"],
                event["date_start_year"],
                event["date_end_year"],
                event["location_slug"],
                None,  # description to be filled by agents
                json.dumps(event.get("persons_involved", [])),
                json.dumps(event.get("texts_involved", [])),
                json.dumps(event.get("concepts_involved", [])),
                event.get("source_method", "MANUAL"),
                "DRAFT",  # initial status
                event.get("confidence", "MEDIUM"),
            ),
        )
    print(f"  [OK] {len(skeleton_data['events'])} events loaded")

    # ========== Populate Reference Tables ==========
    print(f"\nPopulating reference tables...")
    person_refs = 0
    text_refs = 0
    concept_refs = 0

    for event in skeleton_data["events"]:
        event_slug = event["slug"]

        # Add person references
        for person_slug in event.get("persons_involved", []):
            cursor.execute(
                """
                INSERT OR IGNORE INTO person_event_refs
                (person_slug, event_slug)
                VALUES (?, ?)
                """,
                (person_slug, event_slug),
            )
            person_refs += 1

        # Add text references
        for text_slug in event.get("texts_involved", []):
            cursor.execute(
                """
                INSERT OR IGNORE INTO text_event_refs
                (text_slug, event_slug)
                VALUES (?, ?)
                """,
                (text_slug, event_slug),
            )
            text_refs += 1

        # Add concept references
        for concept_slug in event.get("concepts_involved", []):
            cursor.execute(
                """
                INSERT OR IGNORE INTO concept_event_refs
                (concept_slug, event_slug)
                VALUES (?, ?)
                """,
                (concept_slug, event_slug),
            )
            concept_refs += 1

    print(f"  [OK] {person_refs} person_event_refs created")
    print(f"  [OK] {text_refs} text_event_refs created")
    print(f"  [OK] {concept_refs} concept_event_refs created")

    # Commit and close
    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Timeline skeleton loaded successfully")
    print(f"   Total events: {len(skeleton_data['events'])}")
    print(f"   Ready for agent enrichment (Phase 1)")


if __name__ == "__main__":
    load_timeline_skeleton()
