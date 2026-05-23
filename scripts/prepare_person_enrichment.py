#!/usr/bin/env python3
"""
Prepare person enrichment context for Phase 2.
Query each person's related texts, events, and concepts, then write JSON for agent enrichment.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
STAGING_DIR = Path(__file__).parent.parent / "staging"
STAGING_DIR.mkdir(exist_ok=True)

# Priority persons for enrichment (most historically important)
PRIORITY_PERSONS = [
    "zosimos-of-panopolis",
    "jabir-ibn-hayyan",
    "al-razi",
    "al-kindi",
    "gerard-of-cremona",
    "roger-bacon",
]

def prepare_person_context(person_slug):
    """Prepare enrichment context for a single person."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get person data
    cursor.execute(
        "SELECT slug, name, role_primary, era, bio_html FROM persons WHERE slug = ?",
        (person_slug,)
    )
    person_row = cursor.fetchone()
    if not person_row:
        print(f"Person not found: {person_slug}")
        return None

    person = dict(person_row)

    # Get texts authored/translated by this person
    cursor.execute(
        """
        SELECT DISTINCT t.slug, t.title, t.text_type
        FROM texts t
        WHERE t.slug IN (
            SELECT text_slug FROM text_event_refs tr
            JOIN timeline_events te ON te.slug = tr.event_slug
            WHERE te.persons_involved LIKE ?
        )
        LIMIT 10
        """,
        (f'%{person_slug}%',)
    )
    texts_authored = [dict(row) for row in cursor.fetchall()]

    # Get events involving this person
    cursor.execute(
        """
        SELECT slug, date_label, date_start_year, location_slug, description
        FROM timeline_events
        WHERE persons_involved LIKE ?
        ORDER BY date_start_year
        LIMIT 20
        """,
        (f'%"{person_slug}"%',)
    )
    events_involving = [dict(row) for row in cursor.fetchall()]

    # Get related persons (from person_event_refs)
    cursor.execute(
        """
        SELECT DISTINCT p.slug, p.name
        FROM persons p
        WHERE p.slug != ? AND p.slug IN (
            SELECT DISTINCT person_slug FROM person_event_refs
            WHERE event_slug IN (
                SELECT slug FROM timeline_events WHERE persons_involved LIKE ?
            )
        )
        LIMIT 10
        """,
        (person_slug, f'%"{person_slug}"%')
    )
    related_persons = [dict(row) for row in cursor.fetchall()]

    # Get related concepts (from concept_event_refs)
    cursor.execute(
        """
        SELECT DISTINCT c.slug, c.label
        FROM concepts c
        WHERE c.slug IN (
            SELECT DISTINCT concept_slug FROM concept_event_refs
            WHERE event_slug IN (
                SELECT slug FROM timeline_events WHERE persons_involved LIKE ?
            )
        )
        LIMIT 10
        """,
        (f'%"{person_slug}"%',)
    )
    related_concepts = [dict(row) for row in cursor.fetchall()]

    conn.close()

    context = {
        "person": person,
        "context": {
            "texts_authored": texts_authored,
            "events_involving": events_involving,
            "related_persons": related_persons,
            "related_concepts": related_concepts,
        },
        "instructions": (
            "Expand this person's bio_html from current length to 1,200–2,200 words. "
            "Follow STYLEGUIDE.md and AGENT_PROMPT_BIOGRAPHY_ENRICHER.md. "
            "Include opening + 2–4 <h2> sections + Literature section. "
            "Use context provided (related texts, events, persons, concepts). "
            "Wrap entity links in [LINK:slug]. Use DGWE format for bibliography."
        ),
    }

    return context

def main():
    print("Preparing person enrichment contexts...")

    for person_slug in PRIORITY_PERSONS:
        context = prepare_person_context(person_slug)
        if not context:
            continue

        output_path = STAGING_DIR / f"person_context_{person_slug}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2, ensure_ascii=False)

        print(f"  {context['person']['name']:30s} -> {output_path.name}")

    print(f"\n[SUCCESS] {len(PRIORITY_PERSONS)} person contexts prepared")
    print("Next: Spawn Biography Enricher agents for each person")

if __name__ == "__main__":
    main()
