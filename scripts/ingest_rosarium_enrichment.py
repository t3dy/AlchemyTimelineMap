#!/usr/bin/env python3
"""
Ingest enriched Rosarium Philosophorum content into ALCHEMYTIMELINEMAP database.
Updates text entry and creates related timeline events.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = "db/alchemy_timeline.db"
EXTRACTED_DIR = Path("rosarium_extracted")

def read_enriched_html():
    """Read enriched HTML analysis."""
    html_file = EXTRACTED_DIR / "rosarium_enriched_analysis.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def read_metadata():
    """Read enrichment metadata."""
    metadata_file = EXTRACTED_DIR / "rosarium_enrichment_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def update_text_entry(conn, enriched_html, metadata):
    """Update Rosarium Philosophorum text entry in database."""
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE texts
        SET analysis_html = ?,
            review_status = ?,
            source_method = 'AI_ASSISTED',
            confidence = 'MEDIUM'
        WHERE slug = 'rosarium-philosophorum'
    """, (enriched_html, 'DRAFT'))

    conn.commit()
    print(f"[UPDATE] Rosarium Philosophorum text entry updated")
    print(f"  Analysis length: {len(enriched_html)} chars (~{len(enriched_html)//5} words)")

def create_timeline_events(conn, metadata):
    """Create timeline events related to Rosarium Philosophorum."""
    cursor = conn.cursor()

    events = [
        {
            "slug": "rosarium-composition-1350-1450",
            "date_label": "c. 1350–1450",
            "date_start_year": 1350,
            "date_end_year": 1450,
            "location_slug": "paris",
            "description": "Composition of the Rosarium Philosophorum, an influential Latin alchemical treatise employing the rose-garden metaphor as its organizing principle for describing the stages of the Great Work. The work circulated widely in manuscript form and would become one of the most important alchemical texts of the medieval and Renaissance periods, later appearing in major sixteenth- and seventeenth-century printed anthologies.",
            "persons_involved": ["arnaud-de-villanova"],
            "texts_involved": ["rosarium-philosophorum"],
            "concepts_involved": ["philosopher-s-stone", "transmutation", "conjunction", "prima-materia"],
            "scholarly_grounding": "Joachim Telle documented the textual tradition and manuscript variants of the Rosarium Philosophorum in his comprehensive German edition and commentary (1992).",
            "source_method": "SCHOLARSHIP_BASED",
            "review_status": "DRAFT",
            "confidence": "MEDIUM"
        },
        {
            "slug": "rosarium-printing-frankfurt-1550",
            "date_label": "1550",
            "date_start_year": 1550,
            "date_end_year": 1550,
            "location_slug": "frankfurt",
            "description": "The Rosarium Philosophorum is printed in Frankfurt as part of De Alchemia: Opuscula complura veterum philosophorum, a major sixteenth-century alchemical anthology. This edition includes a series of 20 emblematic woodcuts that become influential in the visual culture of Renaissance alchemy, serving as visual keys to interpreting the text's complex allegorical language.",
            "persons_involved": [],
            "texts_involved": ["rosarium-philosophorum", "de-alchemia-1550"],
            "concepts_involved": ["emblematic-alchemy"],
            "scholarly_grounding": "The 1550 Frankfurt edition is documented in Patrick J. Smith's introduction to the 2008 English translation of the Rosarium Philosophorum.",
            "source_method": "SCHOLARSHIP_BASED",
            "review_status": "DRAFT",
            "confidence": "HIGH"
        },
        {
            "slug": "rosarium-theatrum-chemicum-1659",
            "date_label": "1659",
            "date_start_year": 1659,
            "date_end_year": 1659,
            "location_slug": "strasbourg",
            "description": "The Rosarium Philosophorum is included in the Theatrum Chemicum, a comprehensive printed anthology of major alchemical texts. Its inclusion in this prestigious collection establishes the work as canonical within early modern alchemy and ensures its continued study and influence among natural philosophers and alchemists through the seventeenth and eighteenth centuries.",
            "persons_involved": [],
            "texts_involved": ["rosarium-philosophorum", "theatrum-chemicum"],
            "concepts_involved": ["philosopher-s-stone"],
            "scholarly_grounding": "The Theatrum Chemicum editions (1659-1661) are documented as the major seventeenth-century platform for disseminating the Rosarium Philosophorum across Europe.",
            "source_method": "SCHOLARSHIP_BASED",
            "review_status": "DRAFT",
            "confidence": "HIGH"
        },
        {
            "slug": "rosarium-ferguson-manuscript-18c",
            "date_label": "18th century",
            "date_start_year": 1700,
            "date_end_year": 1800,
            "location_slug": "london",
            "description": "An English translation of the Rosarium Philosophorum is produced, now preserved as MS Ferguson 210 in the University of Glasgow Library. This manuscript represents the continued circulation and reinterpretation of the Rosarium in early modern English alchemy and demonstrates the text's adaptation across linguistic and cultural boundaries.",
            "persons_involved": [],
            "texts_involved": ["rosarium-philosophorum"],
            "concepts_involved": ["philosophy-of-alchemy"],
            "scholarly_grounding": "Patrick J. Smith's 2008 English translation was based on the transcription of MS Ferguson 210, documented in his introductory analysis.",
            "source_method": "SCHOLARSHIP_BASED",
            "review_status": "DRAFT",
            "confidence": "HIGH"
        },
        {
            "slug": "rosarium-telle-edition-1992",
            "date_label": "1992",
            "date_start_year": 1992,
            "date_end_year": 1992,
            "location_slug": "frankfurt",
            "description": "Joachim Telle, Luth Clären, and Joachim Huber publish a comprehensive German scholarly edition of the Rosarium Philosophorum with full textual commentary, apparatus, and analysis (VCH Verlagsgesellschaft). This two-volume edition represents the most authoritative modern treatment of the manuscript tradition and becomes the standard scholarly reference for the work's textual history, composition, and significance within medieval and Renaissance alchemy.",
            "persons_involved": ["joachim-telle"],
            "texts_involved": ["rosarium-philosophorum"],
            "concepts_involved": ["textual-transmission", "emblematic-alchemy"],
            "scholarly_grounding": "Joachim Telle's edition and commentary (Rosarium Philosophorum, Band 1-2, VCH Verlagsgesellschaft, 1992) established new standards for the scholarly study of alchemical texts and manuscript traditions.",
            "source_method": "SCHOLARSHIP_BASED",
            "review_status": "DRAFT",
            "confidence": "HIGH"
        }
    ]

    for event in events:
        # Check if event already exists
        cursor.execute("SELECT id FROM timeline_events WHERE slug = ?", (event['slug'],))
        if cursor.fetchone():
            print(f"[SKIP] Event already exists: {event['slug']}")
            continue

        # Convert lists to JSON for storage
        persons_json = json.dumps(event.get('persons_involved', []))
        texts_json = json.dumps(event.get('texts_involved', []))
        concepts_json = json.dumps(event.get('concepts_involved', []))

        cursor.execute("""
            INSERT INTO timeline_events (
                slug, date_label, date_start_year, date_end_year,
                location_slug, description, persons_involved, texts_involved,
                concepts_involved, scholarly_grounding, source_method,
                review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event['slug'],
            event['date_label'],
            event['date_start_year'],
            event['date_end_year'],
            event['location_slug'],
            event['description'],
            persons_json,
            texts_json,
            concepts_json,
            event['scholarly_grounding'],
            event['source_method'],
            event['review_status'],
            event['confidence']
        ))

        print(f"[CREATE] Event: {event['slug']}")

    conn.commit()

def main():
    """Main ingestion function."""
    print("="*70)
    print("ROSARIUM PHILOSOPHORUM DATABASE INGESTION")
    print("="*70)

    # Read enriched content
    enriched_html = read_enriched_html()
    if not enriched_html:
        print("ERROR: Could not read enriched HTML")
        return

    metadata = read_metadata()
    if not metadata:
        print("ERROR: Could not read metadata")
        return

    # Connect to database
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(f"ERROR: Could not connect to database: {e}")
        return

    try:
        # Update text entry
        print("\n[STEP 1] Updating text entry...")
        update_text_entry(conn, enriched_html, metadata)

        # Create timeline events
        print("\n[STEP 2] Creating timeline events...")
        create_timeline_events(conn, metadata)

        print("\n" + "="*70)
        print("INGESTION COMPLETE")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review DRAFT entries: run build_site.py to verify rendering")
        print("  2. Update review_status to REVIEWED when satisfied")
        print("  3. Commit changes to git")

    except sqlite3.Error as e:
        print(f"ERROR: Database operation failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
