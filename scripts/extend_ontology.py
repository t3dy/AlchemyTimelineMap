#!/usr/bin/env python3
"""
extend_ontology.py — add the missing data-ontology structures (idempotent).

Closes the relational + itinerary holes identified in the AUDIT:
  - person_itinerary       : where a figure was, when, on what evidence
  - person_relationships   : typed, directed, weighted, evidence-bearing ties
(concept_person_refs / concept_text_refs already exist as tables but are empty; they
are populated by the enrichment loader, not here.)

Every row carries provenance: source, confidence, review_status, source_method.
Safe to run repeatedly.
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db" / "alchemy_timeline.db"

DDL = [
    """
    CREATE TABLE IF NOT EXISTS person_itinerary (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        person_slug   TEXT NOT NULL,
        seq           INTEGER NOT NULL,            -- order within the life
        place_name    TEXT NOT NULL,
        location_slug TEXT,                         -- link to locations table if known
        latitude      REAL,
        longitude     REAL,
        year_start    INTEGER,
        year_end      INTEGER,
        dwell         REAL,                         -- years in place (nullable)
        what          TEXT,                         -- what happened there
        evidence      TEXT DEFAULT 'attested',      -- attested|approximate|inferred
        leg_evidence  TEXT,                         -- evidence for travel INTO this stop
        source        TEXT NOT NULL,
        confidence    TEXT DEFAULT 'MEDIUM',        -- HIGH|MEDIUM|LOW
        review_status TEXT DEFAULT 'DRAFT',
        source_method TEXT,
        created_at    TEXT DEFAULT (datetime('now')),
        UNIQUE(person_slug, seq)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS person_relationships (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        source_slug   TEXT NOT NULL,
        target_slug   TEXT NOT NULL,
        target_label  TEXT,                         -- display name if target not a DB person
        rel_type      TEXT NOT NULL,                -- patron-of|taught|studied-under|cited|
                                                    -- collected|collaborated|corresponded|
                                                    -- influenced|polemicized-against|dedicated-to
        direction     INTEGER DEFAULT 0,            -- 1 = asymmetric source->target
        weight        REAL DEFAULT 1,
        evidence      TEXT DEFAULT 'attested',      -- attested|inferred
        survives      INTEGER DEFAULT 1,            -- documentary evidence survives?
        note          TEXT,                         -- citation / actor's own language
        source        TEXT NOT NULL,
        date_start    INTEGER,
        date_end      INTEGER,
        confidence    TEXT DEFAULT 'MEDIUM',
        review_status TEXT DEFAULT 'DRAFT',
        source_method TEXT,
        created_at    TEXT DEFAULT (datetime('now')),
        UNIQUE(source_slug, target_slug, rel_type)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_itin_person ON person_itinerary(person_slug)",
    "CREATE INDEX IF NOT EXISTS idx_rel_source ON person_relationships(source_slug)",
    "CREATE INDEX IF NOT EXISTS idx_rel_target ON person_relationships(target_slug)",
]


def main():
    conn = sqlite3.connect(DB)
    for stmt in DDL:
        conn.execute(stmt)
    conn.commit()
    tables = [r[0] for r in conn.execute("select name from sqlite_master where type='table'")]
    print("Ontology extended. Present tables now include:")
    for t in ("person_itinerary", "person_relationships", "concept_person_refs", "concept_text_refs"):
        cnt = conn.execute(f"select count(*) from {t}").fetchone()[0] if t in tables else "MISSING"
        print(f"  {t}: {cnt} rows")
    conn.close()


if __name__ == "__main__":
    main()
