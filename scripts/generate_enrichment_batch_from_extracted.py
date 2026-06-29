#!/usr/bin/env python3
"""Generate enrichment batch from extracted entities in working notes."""

import json
import glob
from pathlib import Path
from datetime import datetime

WORKING_NOTES_DIR = Path("staging/working_notes")
STAGING_DIR = Path("staging")

def generate_batch_from_notes(output_file: str, entity_type: str = "all", limit: int = 10):
    """
    Read working notes and generate enrichment batch.

    Args:
        output_file: Output batch JSON filename
        entity_type: "persons", "texts", "concepts", or "all"
        limit: Number of entities to include
    """

    working_notes = sorted(glob.glob(str(WORKING_NOTES_DIR / "note_*.md")))
    print(f"Found {len(working_notes)} working note files\n")

    persons = {}
    texts = {}
    concepts = {}
    events = []

    # Parse working notes
    for note_file in working_notes[:limit*3]:  # Read more files to get diverse entities
        try:
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract persons section
            if "## Persons Identified" in content:
                persons_section = content.split("## Persons Identified")[1].split("##")[0]
                # Simple line-based extraction
                for line in persons_section.split('\n'):
                    if line.strip().startswith('-') and '(' in line:
                        parts = line.split('(')
                        if len(parts) >= 2:
                            name = parts[0].replace('-', '').strip()
                            dates = parts[1].split(')')[0]
                            if name and len(name) > 2:
                                slug = name.lower().replace(' ', '-')
                                persons[slug] = {
                                    "name": name,
                                    "dates": dates,
                                    "source": Path(note_file).name
                                }

            # Extract texts section
            if "## Texts Identified" in content:
                texts_section = content.split("## Texts Identified")[1].split("##")[0]
                for line in texts_section.split('\n'):
                    if line.strip().startswith('-') and len(line) > 3:
                        title = line.replace('-', '').strip()
                        if title and len(title) > 2:
                            slug = title.lower().replace(' ', '-').replace('"', '')[:40]
                            texts[slug] = {
                                "title": title,
                                "source": Path(note_file).name
                            }

        except Exception as e:
            print(f"  [ERROR reading {note_file}]: {e}")
            continue

    # Build enrichment batch
    batch = {
        "batch_name": f"Extracted Entities Batch — {datetime.now().strftime('%Y-%m-%d')}",
        "created": datetime.now().isoformat() + "Z",
        "persons": [],
        "texts": [],
        "concepts": [],
        "events": []
    }

    # Add persons to batch (limit to avoid huge files)
    for slug, data in list(persons.items())[:limit]:
        batch["persons"].append({
            "slug": slug,
            "name": data["name"],
            "era": "MEDIEVAL",  # Default, should be refined
            "role_primary": "ALCHEMIST",  # Default, should be refined
            "birth_year": 1200,  # Default, should be refined
            "bio_html": f"<p>{data['name']} ({data['dates']}) was an alchemist mentioned in multiple manuscript sources. Further enrichment needed.</p>",
            "source_method": "EXTRACTION_FROM_MARKDOWN",
            "review_status": "DRAFT",
            "confidence": "LOW"
        })

    # Add texts to batch
    for slug, data in list(texts.items())[:limit]:
        batch["texts"].append({
            "slug": slug,
            "title": data["title"],
            "text_type": "TREATISE",
            "composition_date": "c. 1300",  # Default, should be refined
            "analysis_html": f"<p>Title: {data['title']}. Extracted from markdown sources. Full analysis needed.</p>",
            "source_method": "EXTRACTION_FROM_MARKDOWN",
            "review_status": "STUB",
            "confidence": "LOW"
        })

    # Write batch file
    output_path = STAGING_DIR / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Batch generated: {output_path}")
    print(f"  Persons: {len(batch['persons'])}")
    print(f"  Texts: {len(batch['texts'])}")
    print(f"  Concepts: {len(batch['concepts'])}")
    print(f"  Events: {len(batch['events'])}")

    return True

if __name__ == "__main__":
    import sys

    output_file = sys.argv[1] if len(sys.argv) > 1 else "batch_extracted_entities_20.json"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    generate_batch_from_notes(output_file, limit=limit)
