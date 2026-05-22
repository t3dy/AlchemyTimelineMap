#!/usr/bin/env python3
"""
Load enriched timeline events from agent output into database.

This script reads enriched_events JSON from staging/, validates descriptions,
converts [LINK:slug] markup to <a href> tags, and updates the database.
Idempotent: uses UPDATE OR IGNORE.

Usage:
    python scripts/enrich_timeline_events.py --staging_file staging/enriched_events_Medieval_Islam_Iraq_Persia.json

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
import sys
import re
import argparse
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_PATH = Path(__file__).parent.parent / "staging"


def convert_link_markup(text, db_connection):
    """Convert [LINK:slug] markup to <a href> HTML tags."""

    def replace_link(match):
        slug = match.group(1)

        # Look up entity name from database
        cursor = db_connection.cursor()

        # Try to find in persons
        cursor.execute("SELECT name FROM persons WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        if row:
            entity_name = row[0]
            entity_type = "persons"
        else:
            # Try texts
            cursor.execute("SELECT title FROM texts WHERE slug = ?", (slug,))
            row = cursor.fetchone()
            if row:
                entity_name = row[0]
                entity_type = "texts"
            else:
                # Try concepts
                cursor.execute("SELECT label FROM concepts WHERE slug = ?", (slug,))
                row = cursor.fetchone()
                if row:
                    entity_name = row[0]
                    entity_type = "concepts"
                else:
                    # Entity not found; return placeholder
                    return f"[UNKNOWN: {slug}]"

        href = f"../{entity_type}/{slug}.html"
        return f'<a href="{href}">{entity_name}</a>'

    # Replace all [LINK:slug] with <a> tags
    pattern = r"\[LINK:(\w+(?:-\w+)*)\]"
    result = re.sub(pattern, replace_link, text)
    return result


def validate_event_description(slug, description, word_count_min=100, word_count_max=250):
    """Validate event description meets standards."""

    errors = []

    if not description or description == "STUB":
        errors.append(f"  ✗ {slug}: Description is empty or STUB")
        return errors

    word_count = len(description.split())
    if word_count < word_count_min:
        errors.append(f"  ✗ {slug}: Too short ({word_count} words; min {word_count_min})")
    elif word_count > word_count_max:
        errors.append(f"  ✗ {slug}: Too long ({word_count} words; max {word_count_max})")

    # Check for historiographical significance (final sentence should declare it)
    if not re.search(r"(significance|matters|important|reveal|demonstrate)", description.lower()):
        errors.append(f"  ~ {slug}: May lack explicit historiographical significance")

    return errors


def load_enriched_events(staging_file):
    """Load enriched events from staging file into database."""

    staging_file = Path(staging_file)
    if not staging_file.exists():
        print(f"Error: File not found: {staging_file}")
        sys.exit(1)

    print(f"Loading enriched events from {staging_file}...")
    with open(staging_file, "r", encoding="utf-8") as f:
        enriched_data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    batch_id = enriched_data.get("batch_id", "unknown")
    enriched_events = enriched_data.get("enriched_events", [])

    print(f"\nBatch: {batch_id}")
    print(f"Events to load: {len(enriched_events)}")

    # Track validation results
    valid_count = 0
    warning_count = 0
    error_count = 0

    # Load each enriched event
    for event in enriched_events:
        slug = event["slug"]
        description = event.get("description", "").strip()

        # Validate
        errors = validate_event_description(slug, description)
        if errors:
            for error in errors:
                if "✗" in error:
                    error_count += 1
                    print(error)
                elif "~" in error:
                    warning_count += 1
                    print(error)
            if any("✗" in e for e in errors):
                continue  # Skip this event

        # Convert [LINK:slug] markup to <a> tags
        description_html = convert_link_markup(description, conn)

        # Determine review status
        review_status = "REVIEWED" if len(description.split()) >= 100 else "DRAFT"

        # Update database
        cursor.execute(
            """
            UPDATE timeline_events
            SET description = ?, review_status = ?, confidence = ?
            WHERE slug = ?
            """,
            (description_html, review_status, "MEDIUM", slug),
        )
        valid_count += 1

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Load complete")
    print(f"   Valid: {valid_count}")
    print(f"   Warnings: {warning_count}")
    print(f"   Errors: {error_count}")

    if error_count == 0:
        print(f"\n   All events loaded successfully")
        # Move staging file to PROCESSED
        processed_path = staging_file.parent / f"PROCESSED_{staging_file.name}"
        staging_file.rename(processed_path)
        print(f"   Staging file moved to: {processed_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load enriched timeline events from agent output into database"
    )
    parser.add_argument(
        "--staging_file", required=True, help="Path to enriched_events JSON file in staging/"
    )

    args = parser.parse_args()
    load_enriched_events(args.staging_file)
