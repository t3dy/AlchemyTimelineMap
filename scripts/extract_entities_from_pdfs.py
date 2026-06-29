#!/usr/bin/env python3
"""Extract entities from converted PDF markdown files, with special focus on Rampling scholarship."""

import json
import re
from pathlib import Path
from datetime import datetime

MARKDOWN_DIR = Path("staging/pdfs_to_markdown")
WORKING_NOTES_DIR = Path("staging/pdf_working_notes")
EXTRACTION_INDEX = Path("staging/pdf_entity_extraction.json")

def extract_persons(text: str) -> list:
    """Extract person names from academic text, especially alchemists and scholars."""
    persons = []

    # Academic name patterns
    patterns = [
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+(?:van|von|ibn|de|al-|al)[A-Za-z\-]+)?)\s*(?:\(c\.\s+\d{3,4}[–-]\d{3,4}|\(\d{3,4}[–-]\d{3,4}|\[[A-Za-z\s]+\])",
        r"(?:by|author:|written by|attributed to|developed by|studied by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            name = match.group(1).strip()
            if len(name) > 3 and name not in persons:
                persons.append(name)

    return persons[:20]  # Limit to top mentions

def extract_texts(text: str) -> list:
    """Extract titles of texts mentioned in academic papers."""
    texts = []

    # Patterns for quoted titles and italicized titles
    patterns = [
        r'"([A-Z][A-Za-z\s:,—–\'-]+[A-Za-z])"',  # Quoted titles
        r'\*([A-Z][A-Za-z\s:,—–\'-]+[A-Za-z])\*',  # Markdown italics
        r'<i>([A-Z][A-Za-z\s:,—–\'-]+[A-Za-z])</i>',  # HTML italics
        r"'([A-Z][A-Za-z\s:,—–\'-]+[A-Za-z])'",  # Single quoted
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            title = match.group(1).strip()
            if len(title) > 5 and title not in texts and not title.endswith('.'):
                texts.append(title)

    return texts[:30]

def extract_concepts(text: str) -> list:
    """Extract alchemical and historical concepts from text."""
    concepts = []

    # Alchemical terms and concepts
    alchemical_terms = [
        'transmutation', 'distillation', 'sublimation', 'calcination', 'fermentation',
        'putrefaction', 'dissolution', 'coagulation', 'circulation', 'quintessence',
        'elixir', 'philosopher\'s stone', 'prima materia', 'white stone', 'red stone',
        'opus magnum', 'great work', 'great operation', 'hermetic', 'hermeticism',
        'neoplatonic', 'mysticism', 'cosmology', 'microcosm', 'macrocosm',
        'alchemy', 'alchemist', 'chymistry', 'chemistry', 'natural magic',
        'astrology', 'zodiac', 'correspondences', 'symbolic', 'allegory',
    ]

    for term in alchemical_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            concepts.append(term.capitalize())

    return list(set(concepts))

def create_working_note(markdown_path: Path, persons: list, texts: list, concepts: list) -> str:
    """Create a working note from extracted entities."""

    note = f"""# Working Note: {markdown_path.stem}

**Source File:** {markdown_path.name}
**Extracted:** {datetime.now().isoformat()}

## Metadata
- **Source Type:** Academic paper / Book chapter
- **Format:** PDF (converted to markdown)

## Persons Identified
"""

    for person in persons:
        note += f"- {person}\n"

    note += "\n## Texts Identified\n"
    for text in texts:
        note += f"- {text}\n"

    note += "\n## Concepts Mentioned\n"
    for concept in concepts:
        note += f"- {concept}\n"

    note += "\n## Key Themes\n"
    note += "- [To be filled in during enrichment]\n"

    note += "\n## Scholarly Contributions\n"
    note += "- [To be identified from abstract/introduction]\n"

    note += "\n## Historiographical Significance\n"
    note += "- [To be determined]\n"

    note += "\n## Connections to Existing Database\n"
    note += "- [Cross-references to persons, texts, concepts]\n"

    note += "\n---\n*Working note for manual review and enrichment*\n"

    return note

def main():
    """Extract entities from converted PDF markdown files."""

    WORKING_NOTES_DIR.mkdir(parents=True, exist_ok=True)

    # Find all markdown files
    md_files = list(MARKDOWN_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files to extract from\n")

    extraction_results = {}

    for idx, md_path in enumerate(sorted(md_files), 1):
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            persons = extract_persons(content)
            texts = extract_texts(content)
            concepts = extract_concepts(content)

            working_note = create_working_note(md_path, persons, texts, concepts)
            note_path = WORKING_NOTES_DIR / f"note_{md_path.stem}.md"

            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(working_note)

            extraction_results[md_path.name] = {
                "status": "success",
                "persons_found": len(persons),
                "texts_found": len(texts),
                "concepts_found": len(concepts),
                "working_note": str(note_path)
            }

            print(f"[{idx}/{len(md_files)}] {md_path.stem[:40]}: {len(persons)} persons, {len(texts)} texts, {len(concepts)} concepts")

        except Exception as e:
            extraction_results[md_path.name] = {
                "status": "error",
                "error": str(e)
            }
            print(f"[{idx}/{len(md_files)}] ERROR: {str(e)[:50]}")

    # Save extraction index
    index_data = {
        "extraction_date": datetime.now().isoformat(),
        "total_files": len(md_files),
        "extraction_results": extraction_results
    }

    with open(EXTRACTION_INDEX, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Working notes created in: {WORKING_NOTES_DIR}")
    print(f"Extraction index: {EXTRACTION_INDEX}")

if __name__ == "__main__":
    main()
