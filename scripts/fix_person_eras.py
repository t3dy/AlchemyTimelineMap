#!/usr/bin/env python3
"""
Fix two data quality issues:
1. Historical figures misclassified as MODERN/SCHOLAR - correct their era/role.
2. Duplicate person stubs (shorter entries for the same historical figure) -
   re-point any event references to the canonical slug, then delete the stub.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"


# Corrections: (slug, correct_era, correct_role)
CORRECTIONS = [
    ("jabir-ibn-hayyan",      "MEDIEVAL",     "ALCHEMIST"),
    ("al-kindi",              "MEDIEVAL",     "PHILOSOPHER"),
    ("avicenna",              "MEDIEVAL",     "PHYSICIAN"),
    ("albertus-magnus",       "MEDIEVAL",     "PHILOSOPHER"),
    ("isaac-newton",          "EARLY_MODERN", "MATHEMATICIAN"),
    ("paracelsus",            "RENAISSANCE",  "PHYSICIAN"),
    ("robert-boyle",          "EARLY_MODERN", "CHEMIST"),
    ("roger-bacon",           "MEDIEVAL",     "PHILOSOPHER"),
    ("thomas-aquinas",        "MEDIEVAL",     "PHILOSOPHER"),
    ("jan-van-helmont",       "EARLY_MODERN", "PHYSICIAN"),
    ("nicholas-flamel",       "MEDIEVAL",     "ALCHEMIST"),
    ("johann-rudolph-glauber","EARLY_MODERN", "CHEMIST"),
    ("hunayn-ibn-ishaq",      "MEDIEVAL",     "TRANSLATOR"),
    ("thaddeus-the-physician","MEDIEVAL",     "PHYSICIAN"),
    # al-razi is a duplicate stub BUT has more content than muhammad-al-razi,
    # so correct it in place rather than delete.
    ("al-razi",               "MEDIEVAL",     "PHYSICIAN"),
]

# Duplicates: (stub_slug, canonical_slug)
# Stub will be deleted; any event references will be re-pointed to canonical.
DUPLICATES = [
    ("gerard-cremona",        "gerard-of-cremona"),
    ("stephen-of-alexandria", "stephanus-of-alexandria"),
    ("zosimos-panopolis",     "zosimos-of-panopolis"),
    ("ramon-llull",           "raymond-lull"),
    ("muhammad-al-razi",      "al-razi"),  # al-razi corrected above
]


def fix_event_refs(cursor, old_slug, new_slug):
    cursor.execute(
        "SELECT id, persons_involved FROM timeline_events WHERE persons_involved LIKE ?",
        (f'%"{old_slug}"%',),
    )
    rows = cursor.fetchall()
    count = 0
    for event_id, raw in rows:
        try:
            persons = json.loads(raw)
            updated = [new_slug if p == old_slug else p for p in persons]
            if updated != persons:
                cursor.execute(
                    "UPDATE timeline_events SET persons_involved=? WHERE id=?",
                    (json.dumps(updated), event_id),
                )
                count += 1
        except (json.JSONDecodeError, TypeError):
            pass
    return count


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=== Fix 1: Correct era/role for misclassified historical figures ===")
    for slug, era, role in CORRECTIONS:
        cursor.execute(
            "UPDATE persons SET era=?, role_primary=? WHERE slug=? AND era='MODERN' AND role_primary='SCHOLAR'",
            (era, role, slug),
        )
        if cursor.rowcount:
            print(f"  [FIX] {slug} -> {era}/{role}")
        else:
            cursor.execute("SELECT era, role_primary FROM persons WHERE slug=?", (slug,))
            row = cursor.fetchone()
            if row:
                print(f"  [SKIP] {slug} already {row[0]}/{row[1]}")
            else:
                print(f"  [MISS] {slug} not found")

    print("\n=== Fix 2: Redirect event refs + delete duplicate stubs ===")
    for stub, canonical in DUPLICATES:
        cursor.execute("SELECT id FROM persons WHERE slug=?", (canonical,))
        if not cursor.fetchone():
            print(f"  [WARN] canonical {canonical} missing - skipping {stub}")
            continue

        n = fix_event_refs(cursor, stub, canonical)
        if n:
            print(f"  [REFS] {stub} -> {canonical}: {n} event(s) updated")

        cursor.execute("DELETE FROM persons WHERE slug=?", (stub,))
        if cursor.rowcount:
            print(f"  [DEL]  {stub} deleted")
        else:
            print(f"  [MISS] {stub} not found (already gone?)")

    conn.commit()
    conn.close()
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
