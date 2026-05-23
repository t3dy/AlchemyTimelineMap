# EXECUTABLE CONTRACT STRATEGY — ALCHEMYTIMELINEMAP

**Purpose:** Convert prose rules into executable validation (JSON schema, SQL constraints, Python validators). Eliminate interpretive rule-following; enforce rules mechanically.

---

## PRINCIPLE: PROSE IS DESCRIPTION, CODE IS AUTHORITY

**Current problem:**
- Word count rules in STYLEGUIDE.md (prose) → agent must read and remember
- Enum values in PROMPTS.md (prose) → agent must check table before using
- Bibliography format in STYLEGUIDE.md (prose) → agent must infer regex pattern
- Required sections in STYLEGUIDE.md (prose) → agent must parse and verify manually

**Post-refactor solution:**
- Word count rules in docs/SCHEMA.json (executable) → validation script enforces
- Enum values in docs/SCHEMA.json (executable) → SQL CHECK constraint enforces
- Bibliography format in validation script (regex) → validation script enforces
- Required sections in docs/SCHEMA.json (structured) → validation script checks presence

**Rule:** If it can be checked mechanically, it must be. Prose rules are interpretable and decay over time; code rules are not.

---

## LAYER 4 EXECUTABLE SCHEMA: SCHEMA.JSON

**Purpose:** Single authoritative source for all content type specs, enum definitions, field definitions.

**Format:** Hierarchical JSON (readable by humans and machines)

**Authority rule:** If docs/SCHEMA.json contradicts STANDARD_*.md, the schema wins. STANDARD_*.md is derived from docs/SCHEMA.json, not vice versa.

**Content structure (see REFACTOR_RECOMMENDATIONS.md Phase 3.1 for full spec):**

```json
{
  "content_types": {
    "timeline_event": {
      "word_count": { "min": 100, "max": 250 },
      "required_fields": ["slug", "date_label", ..., "description"],
      "validation_rules": [
        "description word count must be 100–250",
        "location_slug must exist in locations",
        "persons_involved slugs must exist in persons",
        ...
      ]
    },
    "person_biography": {
      "word_count": { "min": 1200, "max": 2200 },
      "required_sections": [
        { "name": "opening_paragraph", "min": 200, "max": 350 },
        ...
      ],
      "validation_rules": [...]
    },
    ...
  },
  "enums": {
    "era": ["ANTIQUITY", "LATE_ANTIQUE", "MEDIEVAL", ...],
    "role_primary": ["ALCHEMIST", "CHEMIST", ...],
    ...
  }
}
```

**Usage:**
- docs/VOCABULARY.md references this file (not the reverse)
- STANDARD_*.md reference this file (derive their rules from it)
- Validation scripts load and enforce this schema (source of truth)

---

## LAYER 4 EXECUTABLE CONTRACTS: CONTRACTS.JSON

**Purpose:** Staging manifest format, validation gates, error codes.

**Content structure (see REFACTOR_RECOMMENDATIONS.md Phase 3.2):**

```json
{
  "staging_manifest_contract": {
    "format": "JSON array of entries",
    "required_fields": ["content_type", "entity_slug", "word_count", ...],
    "validation_gates": [
      "word_count_matches_actual",
      "entity_links_exist_in_db",
      "enum_values_valid",
      "required_sections_present"
    ],
    "checksum_field": "SHA256 hash of description",
    "checksum_purpose": "Detect accidental mutations"
  },
  "error_codes": {
    "word_count_too_low": { "code": "WC_LOW", "message": "..." },
    ...
  }
}
```

**Usage:**
- Agents write to staging/ as JSON
- Staging manifest includes entry-level checksums
- Validation script reads manifest, checks all gates, reports errors by code
- On pass, manifest is ingested into database

---

## LAYER 5 EXECUTABLE VALIDATION: PYTHON SCRIPTS

### 5.1 scripts/validate_content.py

**Purpose:** Enforce word count, required sections, enum values mechanically.

**Inputs:**
- docs/SCHEMA.json (specifications)
- Staging JSON file (content to validate)

**Outputs:**
- Pass/fail status
- List of errors (by error code from docs/CONTRACTS.json)
- Suggestions for fixes

**Implementation sketch:**

```python
import json
import re
from pathlib import Path

def load_schema(schema_path="docs/SCHEMA.json"):
    """Load SCHEMA.json as authoritative specification."""
    with open(schema_path) as f:
        return json.load(f)

def load_contracts(contracts_path="docs/CONTRACTS.json"):
    """Load CONTRACTS.json for error codes."""
    with open(contracts_path) as f:
        return json.load(f)

def validate_word_count(text, content_type, schema):
    """Check word count against schema.content_types[content_type].word_count."""
    spec = schema["content_types"][content_type]
    word_count = len(text.split())
    min_words = spec["word_count"]["min"]
    max_words = spec["word_count"]["max"]
    
    errors = []
    if word_count < min_words:
        errors.append({"code": "WC_LOW", "actual": word_count, "min": min_words})
    elif word_count > max_words:
        errors.append({"code": "WC_HIGH", "actual": word_count, "max": max_words})
    
    return errors

def validate_enum_values(entry, content_type, schema):
    """Check that enum fields use valid values from schema.enums."""
    errors = []
    
    # Get enum fields for this content type (e.g., "era" for person_biography)
    content_spec = schema["content_types"][content_type]
    
    for field_name, field_value in entry.items():
        if field_name in schema["enums"]:
            valid_values = schema["enums"][field_name]
            if field_value not in valid_values:
                errors.append({
                    "code": "ENUM_INVALID",
                    "field": field_name,
                    "actual": field_value,
                    "valid": valid_values
                })
    
    return errors

def validate_required_sections(content, content_type, schema):
    """Check that all required sections are present."""
    errors = []
    
    content_spec = schema["content_types"][content_type]
    if "required_sections" not in content_spec:
        return []  # No section requirements for this type
    
    required = [s["name"] for s in content_spec["required_sections"]]
    
    # Parse content for section headers (e.g., "### Section Name")
    section_pattern = re.compile(r'^#{2,4}\s+(.+)$', re.MULTILINE)
    found_sections = {s.lower() for s in section_pattern.findall(content)}
    
    for req_section in required:
        if req_section.lower() not in found_sections:
            errors.append({
                "code": "MISSING_SEC",
                "section": req_section
            })
    
    return errors

def validate_entity_slugs(entry, content_type, db_connection):
    """Check that all entity slugs (persons, texts, concepts, locations) exist in DB."""
    errors = []
    
    # Check person slugs
    for person_slug in entry.get("persons_involved", []):
        if not db_connection.execute(
            "SELECT 1 FROM persons WHERE slug = ?", (person_slug,)
        ).fetchone():
            errors.append({
                "code": "SLUG_INVALID",
                "field": "persons_involved",
                "slug": person_slug
            })
    
    # Similar checks for texts, concepts, locations...
    
    return errors

def validate_bibliography_format(bibliography_text, schema):
    """Check that bibliography follows DGWE format."""
    errors = []
    
    # DGWE format: Author. Title. Year. etc.
    # Simple check: entries should start with capital letter, contain year in parens
    lines = [l.strip() for l in bibliography_text.split('\n') if l.strip()]
    
    for i, line in enumerate(lines):
        if not re.match(r'^[A-Z]', line):
            errors.append({
                "code": "BIB_INVALID",
                "line": i,
                "issue": "Does not start with capital letter"
            })
        if not re.search(r'\(\d{4}\)', line):
            errors.append({
                "code": "BIB_INVALID",
                "line": i,
                "issue": "Missing year in (YYYY) format"
            })
    
    return errors

def validate_staging_entry(entry, schema, contracts, db_connection):
    """Validate a single entry from staging manifest."""
    errors = []
    
    content_type = entry.get("content_type")
    description = entry.get("description", "")
    
    # 1. Word count
    errors.extend(validate_word_count(description, content_type, schema))
    
    # 2. Enum values
    errors.extend(validate_enum_values(entry, content_type, schema))
    
    # 3. Required sections
    errors.extend(validate_required_sections(description, content_type, schema))
    
    # 4. Entity slugs
    errors.extend(validate_entity_slugs(entry, content_type, db_connection))
    
    # 5. Bibliography (if present)
    if "bibliography" in entry:
        errors.extend(validate_bibliography_format(entry["bibliography"], schema))
    
    return errors

def main():
    schema = load_schema()
    contracts = load_contracts()
    
    # Load staging file
    staging_path = Path("staging/timeline_events_batch1.json")
    with open(staging_path) as f:
        entries = json.load(f)
    
    # Validate each entry
    errors_by_entry = {}
    for i, entry in enumerate(entries):
        entry_errors = validate_staging_entry(entry, schema, contracts, db)
        if entry_errors:
            errors_by_entry[i] = entry_errors
    
    # Report
    if errors_by_entry:
        print("VALIDATION FAILED")
        for entry_idx, errors in errors_by_entry.items():
            print(f"\nEntry {entry_idx} ({entries[entry_idx]['entity_slug']}):")
            for error in errors:
                print(f"  - {error['code']}: {error.get('message', str(error))}")
        return False
    else:
        print("VALIDATION PASSED: All entries ready for database ingestion")
        return True

if __name__ == "__main__":
    main()
```

**Execution:** Run before ingesting staging files into database.

**Error handling:** Print error code + suggestions for fix (from docs/CONTRACTS.json)

---

### 5.2 scripts/validate_staging_manifest.py

**Purpose:** Validate manifest structure and checksums before database ingestion.

**Checks:**
1. Manifest has required fields (content_type, entity_slug, word_count, entity_links, checksum)
2. All referenced entity slugs exist in database
3. Checksums match (detect mutations since manifest creation)
4. No duplicate slugs in manifest
5. All entries pass SCHEMA.json validation

**Implementation sketch:**

```python
def validate_manifest(manifest_path, db_connection):
    """Validate staging manifest before ingestion."""
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    errors = []
    
    for i, entry in enumerate(manifest):
        # 1. Check required fields
        required = ["content_type", "entity_slug", "word_count", "checksum"]
        for field in required:
            if field not in entry:
                errors.append({
                    "entry": i,
                    "code": "MANIFEST_INVALID",
                    "issue": f"Missing required field: {field}"
                })
        
        # 2. Check checksum
        expected_checksum = entry.get("checksum")
        actual_checksum = compute_checksum(entry.get("description", ""))
        if expected_checksum != actual_checksum:
            errors.append({
                "entry": i,
                "code": "CHECKSUM_FAIL",
                "slug": entry["entity_slug"]
            })
        
        # 3. Check word count accuracy
        actual_word_count = len(entry.get("description", "").split())
        claimed_word_count = entry.get("word_count", 0)
        if actual_word_count != claimed_word_count:
            errors.append({
                "entry": i,
                "code": "WC_MISMATCH",
                "claimed": claimed_word_count,
                "actual": actual_word_count
            })
    
    # 4. Check for duplicate slugs
    slugs = [e["entity_slug"] for e in manifest]
    if len(slugs) != len(set(slugs)):
        errors.append({
            "code": "DUPLICATE_SLUG",
            "slugs": [s for s in slugs if slugs.count(s) > 1]
        })
    
    return errors
```

---

### 5.3 Update scripts/init_db.py: Add CHECK Constraints

**Purpose:** Database-level validation (source of truth for enum values).

**Implementation:**

```python
def create_persons_table(conn):
    """Create persons table with enum CHECK constraints."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            slug TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role_primary TEXT NOT NULL CHECK(
                role_primary IN (
                    'ALCHEMIST', 'CHEMIST', 'SCHOLAR', 'PHILOSOPHER', 
                    'PHYSICIAN', 'TRANSLATOR', 'MATHEMATICIAN', 'POET', 
                    'PATRON', 'CLERICAL'
                )
            ),
            era TEXT NOT NULL CHECK(
                era IN (
                    'ANTIQUITY', 'LATE_ANTIQUE', 'MEDIEVAL', 
                    'RENAISSANCE', 'EARLY_MODERN', 'MODERN'
                )
            ),
            bio_html TEXT,
            source_method TEXT CHECK(
                source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')
            ),
            review_status TEXT CHECK(
                review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')
            ),
            confidence TEXT CHECK(
                confidence IN ('HIGH', 'MEDIUM', 'LOW')
            ),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def create_timeline_events_table(conn):
    """Create timeline_events table with CHECK constraints."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS timeline_events (
            slug TEXT PRIMARY KEY,
            date_label TEXT NOT NULL,
            date_start_year INTEGER,
            date_end_year INTEGER,
            location_slug TEXT NOT NULL REFERENCES locations(slug),
            description TEXT NOT NULL CHECK(
                LENGTH(description) BETWEEN 500 AND 5000  -- 100–250 words in chars
            ),
            persons_involved TEXT,  -- JSON array of slugs
            texts_involved TEXT,    -- JSON array of slugs
            concepts_involved TEXT, -- JSON array of slugs
            source_method TEXT CHECK(
                source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')
            ),
            review_status TEXT CHECK(
                review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')
            ),
            confidence TEXT CHECK(
                confidence IN ('HIGH', 'MEDIUM', 'LOW')
            ),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
```

**Authority rule:** Database CHECK constraints are the final enforcement. No invalid enum value can be inserted.

---

## CONVERSION TABLE: PROSE RULES → EXECUTABLE RULES

| Rule Type | Current (Prose) | Post-Refactor (Executable) | Authority |
|-----------|-----------------|---------------------------|-----------|
| **Word count: Timeline events** | STYLEGUIDE.md § 4: "100–250 words" | docs/SCHEMA.json: `timeline_event.word_count: {min: 100, max: 250}` | Schema |
| **Word count: Person bio** | STYLEGUIDE.md § 2: "1,200–2,200 words" | docs/SCHEMA.json: `person_biography.word_count: {min: 1200, max: 2200}` | Schema |
| **Enum: era** | docs/VOCABULARY.md (reference) | docs/SCHEMA.json + scripts/init_db.py CHECK constraint | Schema + SQL |
| **Enum: role_primary** | docs/VOCABULARY.md (reference) | docs/SCHEMA.json + scripts/init_db.py CHECK constraint | Schema + SQL |
| **Required sections: Person bio** | STYLEGUIDE.md § 2: "opening, narrative, disputes, legacy" | docs/SCHEMA.json: `person_biography.required_sections: [...]` | Schema |
| **Bibliography format** | STYLEGUIDE.md § 6: "DGWE model" | scripts/validate_content.py: regex enforcement | Validator script |
| **Entity link validation** | STYLEGUIDE.md: "all links must exist" | scripts/validate_content.py + scripts/validate_staging_manifest.py | Validator + manifest |
| **Checksum validation** | Not currently enforced | docs/CONTRACTS.json + scripts/validate_staging_manifest.py | Manifest contract |
| **Provenance metadata** | STYLEGUIDE.md: "source_method, confidence, review_status required" | docs/SCHEMA.json + scripts/init_db.py | Schema + SQL |

---

## VALIDATION PIPELINE: EXECUTION ORDER

### Step 1: Staging File Creation (Agent)

Agent writes to `staging/[type]_[batch].json`:

```json
[
  {
    "content_type": "timeline_event",
    "entity_slug": "roger-bacon-1260",
    "description": "Roger Bacon's work on optical properties...",
    "persons_involved": ["roger-bacon"],
    "texts_involved": ["opus-majus"],
    "concepts_involved": ["distillation"],
    "source_method": "SCHOLARSHIP_BASED",
    "confidence": "HIGH",
    "review_status": "DRAFT",
    "word_count": 180,
    "checksum": "SHA256(description)"
  },
  ...
]
```

**Agent responsibility:**
- Write valid JSON
- Compute word count accurately
- Compute SHA256 checksum
- Use valid enum values (from docs/SCHEMA.json)

---

### Step 2: Validate Content (Validation Script)

```bash
python scripts/validate_content.py staging/timeline_events_batch1.json
```

**Script checks:**
- Word count in range (100–250 for timeline events)
- Enum values valid (era, confidence, etc. exist in docs/SCHEMA.json)
- Required sections present (for types that have them)
- Entity slugs exist in database
- Bibliography format (if applicable)

**Output:**
- PASS: All entries valid
- FAIL: List of errors by code (WC_LOW, ENUM_INVALID, SLUG_INVALID, etc.)

---

### Step 3: Validate Manifest (Manifest Script)

```bash
python scripts/validate_staging_manifest.py staging/timeline_events_batch1.json
```

**Script checks:**
- Manifest has required fields
- Checksums match (no mutations)
- Word counts claimed accurately
- No duplicate slugs
- All entries are unique

**Output:**
- PASS: Manifest ready for ingestion
- FAIL: List of issues (CHECKSUM_FAIL, DUPLICATE_SLUG, etc.)

---

### Step 4: Ingest into Database (Main Script)

```bash
python scripts/enrich_timeline_events.py --ingest staging/timeline_events_batch1.json
```

**Script does:**
- Read validated manifest
- For each entry: INSERT INTO timeline_events (...)
- Database CHECK constraints enforce: enum values, word count range (via character limit), required fields
- If any INSERT fails (enum invalid, FK violation, etc.), transaction rolls back

**Output:**
- SUCCESS: N entries added to database
- FAILURE: Database error (constraint violation, FK error, etc.)

---

### Step 5: Generate Static Site

```bash
python scripts/build_site.py
```

**Script does:**
- Query all entries from database (now validated)
- Generate HTML pages
- Generate data.json for JavaScript

**Guarantee:** All content in database is valid (enforced by layers 4 and 5)

---

## CHECKSUM STRATEGY

**Purpose:** Detect accidental mutations between staging manifest creation and database ingestion.

**How it works:**

1. **Agent creates entry** → computes SHA256(description field)
2. **Agent includes checksum in manifest** → `"checksum": "abc123..."`
3. **Validation script re-computes checksum** → confirms no mutation
4. **If checksums don't match** → error code CHECKSUM_FAIL

**Example:**

```python
import hashlib

description = "Roger Bacon's experiments with light refraction..."
checksum = hashlib.sha256(description.encode()).hexdigest()

manifest_entry = {
    "entity_slug": "roger-bacon-1260",
    "description": description,
    "checksum": checksum  # "a1b2c3d4e5f6..."
}

# Later, during validation:
recomputed = hashlib.sha256(manifest_entry["description"].encode()).hexdigest()
if recomputed != manifest_entry["checksum"]:
    # CHECKSUM_FAIL: description was modified after manifest creation
```

**Why this matters:** If a human hand-edits a staging file, the checksum will mismatch, and validation will catch it before database ingestion.

---

## TESTING EXECUTABLE CONTRACTS

### Test Case 1: Word Count Too Low

**Input:** Timeline event with 50 words (should be 100–250)

**Expected output:** Error code WC_LOW
- Script output: `WC_LOW: actual=50, min=100`
- Agent sees this and expands content
- Resubmit with 120 words → passes

---

### Test Case 2: Invalid Enum Value

**Input:** Person with role_primary="NECROMANCER" (not in schema)

**Expected output:** Error code ENUM_INVALID
- Script output: `ENUM_INVALID: field=role_primary, actual=NECROMANCER, valid=[ALCHEMIST, CHEMIST, ...]`
- Agent sees this and chooses valid value (ALCHEMIST)
- Resubmit with valid enum → passes

---

### Test Case 3: Missing Entity Slug

**Input:** Timeline event references person slug "john-doe" (doesn't exist in DB)

**Expected output:** Error code SLUG_INVALID
- Script output: `SLUG_INVALID: field=persons_involved, slug=john-doe`
- Agent creates person entry first
- Resubmit timeline event → passes

---

### Test Case 4: Checksum Mismatch

**Input:** Manifest created with description A, but file now contains description B

**Expected output:** Error code CHECKSUM_FAIL
- Script output: `CHECKSUM_FAIL: slug=roger-bacon-1260`
- Human has hand-edited the staging file
- Agent re-generates manifest with correct checksum

---

## AUTHORITY HIERARCHY FOR EXECUTABLES

1. **Database CHECK constraints** (highest authority) — enforced at insertion time
2. **docs/SCHEMA.json** (specification) — source of truth for all rules
3. **Validation scripts** (enforcement) — implement schema checks
4. **docs/CONTRACTS.json** (error codes) — standardized error reporting
5. **Prose documentation** (reference only) — derived from schema, never contradicts

**Rule:** If you need to change a validation rule, update docs/SCHEMA.json first, then update the validation script, then update prose docs.

---

## MIGRATION: FROM PROSE TO EXECUTABLE

**Phase 1 (Now):** Create SCHEMA.json and validation scripts; keep prose docs in sync

**Phase 2:** Run validation on all existing staging files; fix any that fail

**Phase 3:** Make validation mandatory in pipeline (fail build if validation fails)

**Phase 4:** Archive prose-only rule documents (keep as reference only)

**Result:** Within 2–3 sprints, the system is fully executable (rules enforced by code, not prose).

---

*Next document: PROGRESSIVE_REVELATION_CRITIQUE.md*
