#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load enhanced location data (alchemical significance descriptions) into database.

This script reads locations_enhanced.json and updates existing location records
with detailed alchemical significance information and key periods.
Idempotent: uses UPDATE for existing records.

Usage:
    python scripts/load_enhanced_locations.py

Input:
    data/locations_enhanced.json (enhanced location data)

Output:
    Updated locations table with significance data

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
import sys
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
ENHANCED_PATH = Path(__file__).parent.parent / "data" / "locations_enhanced.json"


def load_enhanced_locations():
    """Load enhanced location data into database."""

    # Read enhanced location data
    print(f"Loading enhanced location data from {ENHANCED_PATH}...")
    with open(ENHANCED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    updated_count = 0
    not_found_count = 0

    print(f"\nUpdating {len(data['locations'])} locations with enhanced data...")

    for location in data["locations"]:
        slug = location["slug"]

        # Check if location exists
        cursor.execute("SELECT id FROM locations WHERE slug = ?", (slug,))
        if not cursor.fetchone():
            not_found_count += 1
            print(f"  ~ {slug}: Location not found in database")
            continue

        # Convert key_periods list to comma-separated string
        key_periods_str = ",".join(location.get("key_periods", []))

        # Update location with enhanced data
        cursor.execute(
            """
            UPDATE locations
            SET alchemical_significance = ?, key_periods = ?
            WHERE slug = ?
            """,
            (
                location.get("alchemical_significance", ""),
                key_periods_str,
                slug,
            ),
        )
        updated_count += 1

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Enhanced locations loaded")
    print(f"   Updated: {updated_count}")
    print(f"   Not found: {not_found_count}")


if __name__ == "__main__":
    load_enhanced_locations()
