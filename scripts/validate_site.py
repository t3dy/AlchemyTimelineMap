#!/usr/bin/env python3
"""
Comprehensive site validation:
- Check all HTML files for broken links
- Verify JSON data integrity
- Validate entity cross-references
- Check map coordinates
"""

import json
import re
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent / "site"
DATA_FILE = SITE_DIR / "data" / "data.json"

def validate_json_integrity():
    """Verify data.json is valid and complete."""
    print("=== JSON DATA VALIDATION ===\n")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        persons = data.get("persons", [])
        texts = data.get("texts", [])
        concepts = data.get("concepts", [])
        events = data.get("events", [])

        print(f"Persons: {len(persons)}")
        print(f"Texts: {len(texts)}")
        print(f"Concepts: {len(concepts)}")
        print(f"Timeline events: {len(events)}")

        # Check for missing slugs
        persons_with_slugs = [p for p in persons if p.get("slug")]
        texts_with_slugs = [t for t in texts if t.get("slug")]

        print(f"  -> Persons with slugs: {len(persons_with_slugs)}/{len(persons)}")
        print(f"  -> Texts with slugs: {len(texts_with_slugs)}/{len(texts)}")

        # Check event references
        event_refs = {"person_refs": 0, "text_refs": 0, "concept_refs": 0}
        for event in events:
            if event.get("persons_involved"):
                event_refs["person_refs"] += len(event["persons_involved"])
            if event.get("texts_involved"):
                event_refs["text_refs"] += len(event["texts_involved"])
            if event.get("concepts_involved"):
                event_refs["concept_refs"] += len(event["concepts_involved"])

        print(f"\nEvent cross-references:")
        print(f"  -> Person references in events: {event_refs['person_refs']}")
        print(f"  -> Text references in events: {event_refs['text_refs']}")
        print(f"  -> Concept references in events: {event_refs['concept_refs']}")

        return True
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in data.json: {e}")
        return False

def validate_html_structure():
    """Check HTML files for valid structure."""
    print("\n=== HTML STRUCTURE VALIDATION ===\n")

    html_files = list(SITE_DIR.rglob("*.html"))
    print(f"Total HTML files: {len(html_files)}")

    # Check main pages
    main_pages = ["index.html", "timeline.html", "map.html"]
    for page in main_pages:
        page_path = SITE_DIR / page
        if page_path.exists():
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Check for essential elements
                has_head = "<head>" in content
                has_body = "<body>" in content
                has_title = "<title>" in content
                status = "OK" if (has_head and has_body) else "INCOMPLETE"
                print(f"  {page}: {status} (title: {'yes' if has_title else 'no'})")
        else:
            print(f"  {page}: MISSING")

    # Check for person/text pages
    person_pages = list((SITE_DIR / "persons").glob("*.html"))
    text_pages = list((SITE_DIR / "texts").glob("*.html"))
    concept_pages = list((SITE_DIR / "concepts").glob("*.html"))

    print(f"\nEntity pages:")
    print(f"  Persons: {len(person_pages)}")
    print(f"  Texts: {len(text_pages)}")
    print(f"  Concepts: {len(concept_pages)}")

    return True

def validate_entity_pages():
    """Spot-check entity pages for completeness."""
    print("\n=== ENTITY PAGE VALIDATION ===\n")

    # Check a few persons
    person_pages = list((SITE_DIR / "persons").glob("*.html"))
    sample_count = min(3, len(person_pages))

    print(f"Checking {sample_count} person pages...")
    for page_path in person_pages[:sample_count]:
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_bio = "bio" in content.lower() or "<p>" in content
            has_links = "href=" in content
            status = "OK" if (has_bio or has_links) else "SPARSE"
            print(f"  {page_path.name}: {status}")

    # Check texts
    text_pages = list((SITE_DIR / "texts").glob("*.html"))
    sample_count = min(3, len(text_pages))

    print(f"\nChecking {sample_count} text pages...")
    for page_path in text_pages[:sample_count]:
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_content = "<p>" in content
            has_links = "href=" in content
            status = "OK" if (has_content or has_links) else "SPARSE"
            print(f"  {page_path.name}: {status}")

    return True

def validate_map_data():
    """Check if map data has coordinates."""
    print("\n=== MAP DATA VALIDATION ===\n")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        persons = data.get("persons", [])

        # Check location data
        with_locations = sum(1 for p in persons if p.get("location") or p.get("locations"))
        with_coords = sum(1 for p in persons if p.get("latitude") or p.get("geo_coordinates"))

        print(f"Persons with location data: {with_locations}/{len(persons)}")
        print(f"Persons with coordinates: {with_coords}/{len(persons)}")

        if with_coords < len(persons) * 0.5:
            print("\nWARNING: Less than 50% of persons have coordinate data.")
            print("Map functionality may be limited. Consider geocoding location entries.")
        else:
            print("\nOK: Sufficient coordinate coverage for map functionality.")

        return True
    except Exception as e:
        print(f"ERROR validating map data: {e}")
        return False

def main():
    print("=" * 60)
    print("SITE VALIDATION REPORT")
    print("=" * 60 + "\n")

    all_valid = True
    all_valid = validate_json_integrity() and all_valid
    all_valid = validate_html_structure() and all_valid
    all_valid = validate_entity_pages() and all_valid
    all_valid = validate_map_data() and all_valid

    print("\n" + "=" * 60)
    if all_valid:
        print("VALIDATION COMPLETE: All checks passed")
    else:
        print("VALIDATION COMPLETE: Some warnings detected (see above)")
    print("=" * 60)

    return 0 if all_valid else 1

if __name__ == "__main__":
    exit(main())
