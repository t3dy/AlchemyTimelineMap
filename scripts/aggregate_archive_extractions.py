#!/usr/bin/env python3
"""
Aggregate and deduplicate all archive entity extraction results.
Combines JSON files from all extraction agents into a master list with deduplication.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

EXTRACTION_DIR = Path(__file__).parent.parent / "staging"
OUTPUT_FILE = EXTRACTION_DIR / "master_entities_aggregated.json"

def normalize_name(name):
    """Normalize person/text names for deduplication."""
    return re.sub(r'[\s\-\._]+', ' ', name).lower().strip()

def find_duplicate_persons(persons_list):
    """Identify duplicate persons using name normalization and alternate names."""
    normalized_map = {}  # normalized_name -> list of original entries

    for person in persons_list:
        name = person.get("name", "")
        normalized = normalize_name(name)
        if normalized not in normalized_map:
            normalized_map[normalized] = []
        normalized_map[normalized].append(person)

        # Also check alternate names
        for alt_name in person.get("alternate_names", []):
            alt_normalized = normalize_name(alt_name)
            if alt_normalized not in normalized_map:
                normalized_map[alt_normalized] = []
            if person not in normalized_map[alt_normalized]:
                normalized_map[alt_normalized].append(person)

    return normalized_map

def merge_person_records(duplicates_list):
    """Merge multiple records of the same person into one comprehensive record."""
    if not duplicates_list:
        return None

    # Use the record with the most complete data as base
    base = max(duplicates_list, key=lambda p: len(str(p)))
    merged = dict(base)

    # Merge alternate names
    all_alt_names = set(merged.get("alternate_names", []))
    for dup in duplicates_list:
        if dup != base:
            all_alt_names.update(dup.get("alternate_names", []))
            merged["name"] = merged.get("name") or dup.get("name")
            merged["era_mentioned"] = merged.get("era_mentioned") or dup.get("era_mentioned")
            merged["role_category"] = merged.get("role_category") or dup.get("role_category")
            merged["location_mentioned"] = merged.get("location_mentioned") or dup.get("location_mentioned")

    merged["alternate_names"] = sorted(list(all_alt_names))
    return merged

def deduplicate_persons(persons_list):
    """Deduplicate person list, merging records for the same individual."""
    dup_map = find_duplicate_persons(persons_list)
    seen = set()
    deduped = []

    for normalized, duplicates in dup_map.items():
        if not duplicates or normalized in seen:
            continue

        merged = merge_person_records(duplicates)
        if merged:
            deduped.append(merged)
            seen.add(normalized)

    return deduped

def find_duplicate_texts(texts_list):
    """Identify duplicate texts using title normalization."""
    normalized_map = defaultdict(list)

    for text in texts_list:
        title = text.get("title", "")
        normalized = normalize_name(title)
        normalized_map[normalized].append(text)

        for alt_title in text.get("alternate_titles", []):
            alt_normalized = normalize_name(alt_title)
            if text not in normalized_map[alt_normalized]:
                normalized_map[alt_normalized].append(text)

    return normalized_map

def merge_text_records(duplicates_list):
    """Merge multiple records of the same text into one comprehensive record."""
    if not duplicates_list:
        return None

    base = max(duplicates_list, key=lambda t: len(str(t)))
    merged = dict(base)

    # Merge alternate titles
    all_alt_titles = set(merged.get("alternate_titles", []))
    for dup in duplicates_list:
        if dup != base:
            all_alt_titles.update(dup.get("alternate_titles", []))
            merged["title"] = merged.get("title") or dup.get("title")
            merged["author_or_tradition"] = merged.get("author_or_tradition") or dup.get("author_or_tradition")
            merged["original_language"] = merged.get("original_language") or dup.get("original_language")
            merged["date_or_period"] = merged.get("date_or_period") or dup.get("date_or_period")

    merged["alternate_titles"] = sorted(list(all_alt_titles))
    return merged

def deduplicate_texts(texts_list):
    """Deduplicate text list, merging records for the same work."""
    dup_map = find_duplicate_texts(texts_list)
    seen = set()
    deduped = []

    for normalized, duplicates in dup_map.items():
        if not duplicates or normalized in seen:
            continue

        merged = merge_text_records(duplicates)
        if merged:
            deduped.append(merged)
            seen.add(normalized)

    return deduped

def load_extraction_files():
    """Load all extraction JSON files from staging directory."""
    all_persons = []
    all_scholars = []
    all_texts = []

    extraction_files = list(EXTRACTION_DIR.glob("*.json"))

    for file_path in extraction_files:
        if "master" in file_path.name or "aggregated" in file_path.name:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle different structure formats
            if "extracted_entities" in data:
                extracted = data["extracted_entities"]
                all_persons.extend(extracted.get("alchemists", []))
                all_scholars.extend(extracted.get("scholars", []))
                all_texts.extend(extracted.get("texts", []))

            print(f"  Loaded {file_path.name}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [SKIP] {file_path.name}: {type(e).__name__}")
            continue

    return all_persons, all_scholars, all_texts

def main():
    print("Aggregating and deduplicating archive extractions...\n")

    print("Loading extraction files:")
    all_persons, all_scholars, all_texts = load_extraction_files()
    print(f"\nLoaded: {len(all_persons)} persons, {len(all_scholars)} scholars, {len(all_texts)} texts (before dedup)\n")

    print("Deduplicating persons...")
    deduped_persons = deduplicate_persons(all_persons)
    print(f"  After dedup: {len(deduped_persons)} unique persons\n")

    print("Deduplicating texts...")
    deduped_texts = deduplicate_texts(all_texts)
    print(f"  After dedup: {len(deduped_texts)} unique texts\n")

    # Scholars typically don't duplicate as much; just keep unique
    deduped_scholars = []
    seen_scholars = set()
    for scholar in all_scholars:
        name = scholar.get("name", "")
        norm_name = normalize_name(name)
        if norm_name not in seen_scholars:
            deduped_scholars.append(scholar)
            seen_scholars.add(norm_name)

    print(f"Deduplicated scholars: {len(deduped_scholars)} unique scholars\n")

    # Build master JSON
    master = {
        "metadata": {
            "source": "Archive extraction and aggregation pipeline",
            "total_persons": len(deduped_persons),
            "total_scholars": len(deduped_scholars),
            "total_texts": len(deduped_texts),
            "aggregation_date": "2026-05-22",
            "deduplication_applied": True
        },
        "entities": {
            "persons": deduped_persons,
            "scholars": deduped_scholars,
            "texts": deduped_texts
        }
    }

    # Write master file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Master aggregated file written: {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  Total unique persons: {len(deduped_persons)}")
    print(f"  Total unique scholars: {len(deduped_scholars)}")
    print(f"  Total unique texts: {len(deduped_texts)}")
    print(f"\nReduction from duplicates:")
    print(f"  Persons: {len(all_persons)} -> {len(deduped_persons)} ({len(all_persons) - len(deduped_persons)} duplicates)")
    print(f"  Texts: {len(all_texts)} -> {len(deduped_texts)} ({len(all_texts) - len(deduped_texts)} duplicates)")

if __name__ == "__main__":
    main()
