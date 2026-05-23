#!/usr/bin/env python3
"""Load completed concept definitions from staging into database."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_FILE = Path(__file__).parent.parent / "staging" / "concept_definitions_complete.json"

def load_concept_definitions():
    """Load all completed concept definition JSON from staging."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    loaded = 0
    failed = 0

    try:
        with open(STAGING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"  [ERROR] Failed to load {STAGING_FILE.name}: {type(e).__name__}")
        return 0

    # Handle both list and dict structures
    concepts = []
    if isinstance(data, list):
        concepts = data
    elif isinstance(data, dict) and "concepts" in data:
        concepts = data["concepts"]

    for concept in concepts:
        slug = concept.get("slug", "")
        if not slug:
            continue

        definition_long = concept.get("definition_long", "")
        definition_short = concept.get("definition_short", "")

        if not definition_long or not definition_short:
            print(f"    [SKIP] {slug}: missing definition")
            failed += 1
            continue

        # Update concept record
        cursor.execute(
            """UPDATE concepts
               SET definition_long = ?, definition_short = ?, review_status = 'DRAFT', source_method = 'AI_ASSISTED'
               WHERE slug = ?""",
            (definition_long, definition_short, slug)
        )

        if cursor.rowcount > 0:
            loaded += 1
        else:
            print(f"    [NOTFOUND] {slug}")

    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Loaded {loaded} completed concept definitions into database")
    if failed > 0:
        print(f"[FAILED] {failed} concepts with errors")

    return loaded

if __name__ == "__main__":
    load_concept_definitions()
