#!/usr/bin/env python3
r"""
Markdown Batch Reader — ALCHEMYTIMELINEMAP

Reads markdown files from e:\pdf\alchemy, extracts entities (persons, texts, locations, concepts),
and generates working notes + metadata index.

Idempotent: Skips already-processed files. Can resume interrupted runs.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import hashlib
import io

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
SOURCE_DIR = Path("e:\\pdf\\alchemy")
STAGING_DIR = Path("C:\\Dev\\ALCHEMYTIMELINEMAP\\staging")
WORKING_NOTES_DIR = STAGING_DIR / "working_notes"
TEMPLATE_FILE = Path("C:\\Dev\\ALCHEMYTIMELINEMAP\\staging\\WORKING_NOTES_TEMPLATE.md")
PROCESSED_LOG = STAGING_DIR / "processed_files.json"

# Entity recognition patterns
PERSON_PATTERN = re.compile(
    r"\b([A-Z][a-z]+ (?:[a-z]+ )?(?:of |ibn )?[A-Z][a-z]+(?:\s+(?:the|of|ibn)\s+[A-Z][a-z]+)?)\b"
)
TEXT_PATTERN = re.compile(
    r"[\"']([A-Z][A-Za-z\s:,—–-]+)[\"']|(?:^|\s)(?:The|A)\s+([A-Z][A-Za-z\s:,—–-]+)(?:\s+(?:was|is|describes|contains|discusses))"
)
LOCATION_PATTERN = re.compile(
    r"\b((?:Ancient |Medieval |Early Modern )?(?:Alexandria|Baghdad|Cairo|Damascus|Antioch|Constantinople|Athens|Rome|Venice|Florence|Prague|Paris|London|Toledo|Córdoba|Seville|Amsterdam|Antwerp|Strasbourg|Montpellier|Salerno|Palermo|Leipzig|Wittenberg|Zurich|Geneva))\b"
)
CONCEPT_PATTERN = re.compile(
    r"\b((?:distillation|sublimation|calcination|fermentation|crystallization|putrefaction|projection|transmutation|quintessence|prima materia|philosopher'?s? stone|chrysopoeia|spagyrics|alchemy|hermetic|magick|iatro?chemistry))\b",
    re.IGNORECASE
)

def load_processed_log() -> Dict[str, Dict]:
    """Load the log of already-processed files."""
    if PROCESSED_LOG.exists():
        with open(PROCESSED_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed_log(log: Dict[str, Dict]) -> None:
    """Save the processed log."""
    with open(PROCESSED_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def get_file_hash(filepath: Path) -> str:
    """Get SHA256 hash of a file to detect changes."""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def extract_entities_from_text(text: str) -> Dict[str, Set[str]]:
    """Extract persons, texts, locations, concepts from markdown text."""
    entities = {
        "persons": set(),
        "texts": set(),
        "locations": set(),
        "concepts": set(),
    }

    # Extract locations
    for match in LOCATION_PATTERN.finditer(text):
        entities["locations"].add(match.group(1))

    # Extract concepts
    for match in CONCEPT_PATTERN.finditer(text):
        entities["concepts"].add(match.group(1).lower())

    # Extract persons (heuristic: capitalized names)
    # Look for patterns like "Name of/ibn Place" or "First Last"
    for match in PERSON_PATTERN.finditer(text):
        potential_person = match.group(1)
        # Filter out common false positives
        if not potential_person.startswith(("The ", "A ", "In ", "By ", "At ")):
            entities["persons"].add(potential_person)

    # Extract texts in quotes or mentioned explicitly
    for match in TEXT_PATTERN.finditer(text):
        text_title = match.group(1) or match.group(2)
        if text_title and len(text_title) > 3:
            entities["texts"].add(text_title.strip())

    return {k: sorted(list(v)) for k, v in entities.items()}

def generate_working_note_stub(
    source_file: Path,
    entities: Dict[str, List[str]],
    preview_text: str,
    processed_date: str
) -> str:
    """Generate a working note based on extracted entities."""

    # Load template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Prepare entity lists for template
    persons_section = "\n".join(
        f"- **{p}**: [Description needed]\n  - Status: NEW\n  - Context: [Extracted from source]\n  - Event potential: [To be determined]"
        for p in entities["persons"][:10]  # Limit to first 10
    )

    texts_section = "\n".join(
        f"- **{t}**: [Author/Date needed]\n  - Status: NEW\n  - Content type: [To be determined]"
        for t in entities["texts"][:10]
    )

    locations_section = "\n".join(
        f"- **{l}**: [Period needed]\n  - Why significant: [To be determined]"
        for l in entities["locations"][:10]
    )

    concepts_section = "\n".join(
        f"- **{c}**: [Definition needed]\n  - Type: ACTOR_TERM / ANALYST_TERM (to determine)\n  - Status: NEW"
        for c in entities["concepts"][:10]
    )

    # Fill template
    stub = template.replace("[SOURCE TITLE]", source_file.stem)
    stub = stub.replace("[Original filename from e:\\pdf\\alchemy]", str(source_file))
    stub = stub.replace("[ISO date]", processed_date)
    stub = stub.replace("[Agent ID or name]", "BATCH_READER")
    stub = stub.replace("[Batch category, e.g., \"Early Islamic Baghdad\"]", "UNASSIGNED")

    # Replace entity sections with extracted entities
    stub = re.sub(
        r"(## Persons Identified\n\n).*?(\n\n### Notes on Persons)",
        f"\\1{persons_section}\\2",
        stub,
        flags=re.DOTALL
    )

    # Add preview note
    preview_note = f"\n\n**Preview (first 500 chars):**\n```\n{preview_text[:500]}...\n```"
    stub = stub.replace("**Processed:**", f"**Preview:**{preview_note}\n\n**Processed:**")

    return stub

def process_markdown_file(filepath: Path, processed_log: Dict[str, Dict]) -> None:
    """Process a single markdown file and generate working note."""

    file_key = str(filepath)
    current_hash = get_file_hash(filepath)

    # Check if already processed with same hash
    if file_key in processed_log and processed_log[file_key].get("hash") == current_hash:
        print(f"  [SKIP] Already processed: {filepath.name}", flush=True)
        return

    try:
        print(f"  [READ] {filepath.name}", flush=True)
    except UnicodeEncodeError:
        print(f"  [READ] {filepath.stem[:40]}... (Unicode filename)", flush=True)

    # Read file
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Extract entities
    entities = extract_entities_from_text(content)

    # Generate working note
    processed_date = datetime.now().isoformat().split('T')[0]
    working_note = generate_working_note_stub(
        filepath,
        entities,
        content,
        processed_date
    )

    # Save working note
    note_filename = f"note_{filepath.stem}.md"
    note_path = WORKING_NOTES_DIR / note_filename
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(working_note)

    # Update log
    processed_log[file_key] = {
        "hash": current_hash,
        "processed": processed_date,
        "note_file": note_filename,
        "entity_count": {
            "persons": len(entities["persons"]),
            "texts": len(entities["texts"]),
            "locations": len(entities["locations"]),
            "concepts": len(entities["concepts"]),
        }
    }

    print(f"    → {len(entities['persons'])} persons, {len(entities['texts'])} texts, {len(entities['locations'])} locations, {len(entities['concepts'])} concepts", flush=True)

def batch_process(pattern: str = "*.md", limit: int = None) -> None:
    """Process all markdown files matching pattern."""

    print(f"Reading markdown batch from: {SOURCE_DIR}")
    print(f"Working notes output: {WORKING_NOTES_DIR}\n")

    # Create directories if needed
    WORKING_NOTES_DIR.mkdir(parents=True, exist_ok=True)

    # Load processed log
    processed_log = load_processed_log()

    # Find files
    files = sorted(SOURCE_DIR.glob(f"**/{pattern}"))
    if limit:
        files = files[:limit]

    print(f"Found {len(files)} markdown files\n")

    # Process each file
    for i, filepath in enumerate(files, 1):
        if i % 100 == 0:
            print(f"\n[Progress] {i}/{len(files)}", flush=True)
        try:
            process_markdown_file(filepath, processed_log)
        except Exception as e:
            try:
                print(f"  [ERROR] {filepath.name}: {e}", flush=True)
            except UnicodeEncodeError:
                print(f"  [ERROR] {filepath.stem[:40]}...: {str(e)[:60]}", flush=True)

    # Save updated log
    save_processed_log(processed_log)

    # Summary
    total_persons = sum(
        log.get("entity_count", {}).get("persons", 0)
        for log in processed_log.values()
    )
    total_texts = sum(
        log.get("entity_count", {}).get("texts", 0)
        for log in processed_log.values()
    )
    total_locations = sum(
        log.get("entity_count", {}).get("locations", 0)
        for log in processed_log.values()
    )
    total_concepts = sum(
        log.get("entity_count", {}).get("concepts", 0)
        for log in processed_log.values()
    )

    print(f"\n✅ Processing complete:")
    print(f"   Working notes created: {len([f for f in WORKING_NOTES_DIR.glob('note_*.md')])}")
    print(f"   Total persons extracted: {total_persons}")
    print(f"   Total texts extracted: {total_texts}")
    print(f"   Total locations extracted: {total_locations}")
    print(f"   Total concepts extracted: {total_concepts}")
    print(f"   Processed log saved: {PROCESSED_LOG}")

if __name__ == "__main__":
    import sys

    # Run with optional limit for testing
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    batch_process(limit=limit)

    print("\n📖 Next steps:")
    print("   1. Review working notes in staging/working_notes/")
    print("   2. Run entity_extraction_index.py to create XLSX of all entities")
    print("   3. Group working notes by era/region")
    print("   4. Launch enrichment agents for each region batch")
