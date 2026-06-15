#!/usr/bin/env python3
"""
Merge duplicate person records into their canonical entry.

Some figures were entered twice (e.g. `muhammad-al-razi` is a stub duplicate of
`al-razi` / Rhazes). Duplicate person records produce duplicate figure cards on
the timeline, which is exactly the repetition we are eliminating. This script
remaps every reference from a duplicate slug to its canonical slug across
events and refs, then deletes the duplicate person row.

Idempotent. Usage:
    python scripts/merge_duplicate_persons.py
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

# duplicate_slug -> canonical_slug
MERGES = {
    "muhammad-al-razi": "al-razi",
}


def remap_json(val, mapping):
    try:
        arr = json.loads(val or "[]")
    except (json.JSONDecodeError, TypeError):
        return val, False
    if not isinstance(arr, list):
        return val, False
    new = list(dict.fromkeys(mapping.get(x, x) for x in arr))
    return (json.dumps(new), True) if new != arr else (val, False)


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    changed = 0

    cur.execute("SELECT slug, persons_involved FROM timeline_events")
    for ev, pi in cur.fetchall():
        new, did = remap_json(pi, MERGES)
        if did:
            cur.execute("UPDATE timeline_events SET persons_involved = ? WHERE slug = ?", (new, ev))
            changed += 1

    for dup, canon in MERGES.items():
        cur.execute("UPDATE person_event_refs SET person_slug = ? WHERE person_slug = ?", (canon, dup))
        cur.execute("DELETE FROM persons WHERE slug = ?", (dup,))
        print(f"  [OK] merged {dup} -> {canon}")

    conn.commit()
    conn.close()
    print(f"  [OK] {changed} events remapped")


if __name__ == "__main__":
    main()
