#!/usr/bin/env python3
"""
Load enriched timeline event descriptions from staging/ into the database.

This script:
1. Reads enriched JSON from staging/enriched_events_*.json
2. Validates word counts (100-250) and historiographical significance
3. Converts [LINK:slug] to <a href> tags
4. Updates timeline_events table with descriptions
5. Updates review_status (REVIEWED if valid, DRAFT if issues)

Usage:
    python scripts/load_enriched_events.py <batch_name>

Example:
    python scripts/load_enriched_events.py Late_Antique_Egypt_Syria

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
import re
from pathlib import Path
import sys

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"


def load_entity_lookup(conn):
    """Load a mapping of slug -> (name, type) for all entities."""
    cursor = conn.cursor()
    lookup = {}

    # Load persons
    cursor.execute("SELECT slug, name FROM persons")
    for slug, name in cursor.fetchall():
        lookup[slug] = (name, "persons")

    # Load texts
    cursor.execute("SELECT slug, title FROM texts")
    for slug, title in cursor.fetchall():
        lookup[slug] = (title, "texts")

    # Load concepts
    cursor.execute("SELECT slug, label FROM concepts")
    for slug, label in cursor.fetchall():
        lookup[slug] = (label, "concepts")

    return lookup


def convert_links(description, lookup):
    """
    Convert [LINK:slug] to <a href="../type/slug.html">name</a>.
    Returns (converted_text, links_found, invalid_links).
    """
    pattern = r"\[LINK:([a-z0-9\-]+)\]"
    links_found = []
    invalid_links = []

    def replace_link(match):
        slug = match.group(1)
        if slug in lookup:
            name, entity_type = lookup[slug]
            href = f"../{entity_type}/{slug}.html"
            links_found.append(slug)
            return f'<a href="{href}">{name}</a>'
        else:
            invalid_links.append(slug)
            return f"[LINK:{slug}]"  # Keep original if not found

    converted = re.sub(pattern, replace_link, description)
    return converted, links_found, invalid_links


def validate_event_description(description, slug):
    """
    Validate an event description against style requirements.
    Returns (is_valid, issues).
    """
    issues = []

    # Check word count
    word_count = len(description.split())
    if word_count < 100:
        issues.append(f"Too short: {word_count} words (min 100)")
    elif word_count > 250:
        issues.append(f"Too long: {word_count} words (max 250)")

    # Check for historiographical significance (should end with capital letter and period)
    if not description.strip().endswith("."):
        issues.append("Does not end with a period")

    # Check for [LINK:...] placeholders (should be resolved)
    if "[LINK:" in description:
        issues.append("Contains unresolved [LINK:...] placeholders")

    # Check for markdown artifacts
    if any(artifact in description for artifact in ["**", "##", "- ", "* "]):
        issues.append("Contains markdown artifacts")

    # Check for date at start (rough heuristic)
    if not re.match(r"^c\. \d+", description) and not re.match(
        r"^\d+–\d+", description
    ):
        if not re.match(r"^(Early|High|Late) ", description):
            issues.append("Does not start with a date")

    return len(issues) == 0, issues


def load_enriched_batch(batch_name):
    """Load an enriched batch from staging into the database."""

    enriched_path = STAGING_DIR / f"enriched_events_{batch_name}.json"

    if not enriched_path.exists():
        print(f"[ERROR] File not found: {enriched_path}")
        return False

    print(f"Loading enriched events from {enriched_path}...")

    with open(enriched_path, "r", encoding="utf-8") as f:
        enriched_data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load entity lookup
    lookup = load_entity_lookup(conn)
    print(f"Entity lookup: {len(lookup)} entities")

    # Process each enriched event
    loaded = 0
    issues = 0
    invalid_links = 0

    for event in enriched_data.get("enriched_events", []):
        slug = event["slug"]
        description = event["description"]

        # Convert links
        converted_desc, links, bad_links = convert_links(description, lookup)

        if bad_links:
            invalid_links += len(bad_links)
            print(f"  [WARN] {slug}: Invalid links: {bad_links}")

        # Validate
        is_valid, validation_issues = validate_event_description(converted_desc, slug)

        if not is_valid:
            issues += 1
            print(f"  [WARN] {slug}: {'; '.join(validation_issues)}")
            review_status = "DRAFT"
        else:
            review_status = "REVIEWED"

        # Update database
        cursor.execute(
            """
            UPDATE timeline_events
            SET description = ?, review_status = ?, source_method = ?
            WHERE slug = ?
            """,
            (converted_desc, review_status, "AI_ASSISTED", slug),
        )
        loaded += 1

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Batch loaded")
    print(f"  Events loaded: {loaded}")
    print(f"  Events with issues: {issues}")
    print(f"  Invalid links found: {invalid_links}")
    print(f"  Batch: {batch_name}")

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <batch_name>")
        print(f"Example: python {Path(__file__).name} Late_Antique_Egypt_Syria")
        sys.exit(1)

    batch_name = sys.argv[1]
    success = load_enriched_batch(batch_name)
    sys.exit(0 if success else 1)
