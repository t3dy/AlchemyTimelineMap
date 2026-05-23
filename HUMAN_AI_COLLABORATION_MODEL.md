# HUMAN_AI_COLLABORATION_MODEL — ALCHEMYTIMELINEMAP

**Purpose:** Design patterns for human + AI collaboration that prevent drift, maintain authority, and create clear validation checkpoints. Covers: staging patterns, validation tiers, provenance tracking, review workflow, task isolation, anti-drift mechanisms.

---

## PRINCIPLE: HUMANS DECIDE, AI EXECUTES, SYSTEMS VERIFY

The system is structured so that:

1. **Humans set vision and standards** (CONCEPTUAL_FRAMEWORK.md, STANDARD_*.md, SCHEMA.json)
2. **AI creates content** (writes biographies, enriches events, etc.)
3. **Systems verify automatically** (word count, entity links, enum validation)
4. **Humans review and approve** (spot-check examples, approve batches)
5. **AI revises as needed** (incorporates feedback, re-submits)
6. **Mechanical ingestion** (validated content enters database)

**No step is skipped.** No content enters the database without passing both mechanical and human validation.

---

## STAGING WORKFLOW: THE CANONICAL PATTERN

### Overview

```
Human Decision
    ↓
AI Creation (staging/)
    ↓
Mechanical Validation (scripts/validate_*.py)
    ↓
Human Review (approve/reject)
    ↓
Revision Loop (if needed) ↩
    ↓
Database Ingestion (scripts/enrich_*.py)
    ↓
Site Generation (scripts/build_site.py)
```

---

### Step 1: Human Sets Task + Constraints

**Human:** "I need to add 30 new timeline events for Ibn Sina's lifetime (980–1037)"

**Constraints human specifies:**
- Date range: 980–1037
- Location focus: Persia/Central Asia
- Key events: major works, travels, patronage, influence
- Source preference: Newman's research, Pereira's corpus
- Confidence level: aim for HIGH where documented, MEDIUM for inferred

**Output:** Task specification (written in conversation with Claude)

---

### Step 2: AI Creates Content in Staging

**AI** (Claude Code agent):
1. Reads AGENT_LOADING_STRATEGY.md → routes to timeline event task
2. Reads STANDARD_TIMELINE_EVENTS.md → word count 100–250
3. Pre-queries database → loads all persons, texts, concepts, locations (context engineering)
4. Creates 30 events in `staging/timeline_events_ibn_sina_batch1.json`

**Staging manifest structure:**
```json
[
  {
    "content_type": "timeline_event",
    "entity_slug": "ibn-sina-980-travels-to-rey",
    "date_label": "980–982",
    "date_start_year": 980,
    "date_end_year": 982,
    "location_slug": "rey-persia",
    "description": "[180 words describing his travels to Rey and alchemical studies there]",
    "persons_involved": ["ibn-sina", "abu-sahl-masihi"],
    "texts_involved": ["book-of-the-cure"],
    "concepts_involved": ["distillation", "medicine"],
    "source_method": "SCHOLARSHIP_BASED",
    "confidence": "HIGH",
    "review_status": "DRAFT",
    "word_count": 180,
    "checksum": "SHA256([description])"
  },
  {...},
  {...}
]
```

**AI checklist before submitting:**
- [ ] All 30 events created
- [ ] Word count per event 100–250 words
- [ ] Date range covers 980–1037
- [ ] All entity slugs exist in database (or noted as missing)
- [ ] Checksums computed for all entries
- [ ] Manifest is valid JSON

**Output:** Staging manifest ready for validation

---

### Step 3: Mechanical Validation

**Human runs:**
```bash
python scripts/validate_content.py staging/timeline_events_ibn_sina_batch1.json
python scripts/validate_staging_manifest.py staging/timeline_events_ibn_sina_batch1.json
```

**Validation checks:**

| Check | Purpose | Pass/Fail |
|-------|---------|-----------|
| **Word count in range (100–250)** | Ensure quality brevity | ✓/✗ |
| **All required fields present** | Prevent incomplete entries | ✓/✗ |
| **Entity slugs exist in DB** | Prevent broken links | ✓/✗ |
| **Enum values valid** | Prevent bad data | ✓/✗ |
| **Checksum matches** | Detect mutations | ✓/✗ |
| **No duplicate slugs** | Ensure uniqueness | ✓/✗ |
| **Date range in manifest** | Verify scope coverage | ✓/✗ |

**If all pass:** Green light → Human review
**If any fail:** Error report → AI revision

**Example error output:**
```
VALIDATION FAILED

Entry 5 (ibn-sina-1003-writes-canon-of-medicine):
  - WC_HIGH: actual=290, max=250
  - Entity slug not found: galen (mentioned but not in persons table)

Entry 12 (ibn-sina-1015-travels-to-isfahan):
  - CHECKSUM_FAIL: description was modified after manifest creation

Recommendation: 
  - Condense entry 5 (currently 290 words, need ≤250)
  - Create Galen person entry first (or link to existing Galen if present)
  - Re-compute checksum for entry 12
```

---

### Step 4: Human Review (Spot-Check)

**Human reads 5–10 randomly selected entries** (not all 30):

**Checklist:**
- [ ] Prose matches historiographical standards (CONCEPTUAL_FRAMEWORK.md principles)
- [ ] Material grounding evident (sources cited or inferred from scholarship)
- [ ] Entity links make sense (not overfitting)
- [ ] Dates are plausible (no obvious anachronisms)
- [ ] Tone is scholarly, not hagiographic
- [ ] Confidence levels are justified (HIGH for documented, MEDIUM for inferred)

**Human decision:** APPROVE, APPROVE WITH REVISIONS, or REJECT

---

### Step 5: AI Revision (If Needed)

**If human feedback:** AI reads comments and revises

**Example feedback:**
```
Entry 3 (ibn-sina-985-studies-medicine-with-masihi):
- Issue: "He learned the secrets of alchemy" is too vague. 
  What specific techniques? Which works did he study?
- Fix: Replace with specific operations (distillation, calcination) and cite which text.

Entry 7 (ibn-sina-1000-travels-to-court-of-emir):
- Issue: Confidence is HIGH but date is only approximate.
- Fix: Change confidence to MEDIUM, adjust date_label to "c. 1000" to reflect uncertainty.

Entry 12 (ibn-sina-1015-writes-first-version-of-canon):
- Good! Clear material grounding, well-documented.
- One suggestion: Add a cross-link to "galen" (concept) since Canon is largely a synthesis of Galenic medicine.
```

**AI revises:**
1. Updates staging file with corrections
2. Re-computes checksums
3. Re-runs validation
4. Submits revised manifest

**Loop until:** Human approves all entries

---

### Step 6: Database Ingestion

**Human confirms:** "Looks good, ingest this batch"

**Human runs:**
```bash
python scripts/enrich_timeline_events.py --ingest staging/timeline_events_ibn_sina_batch1.json
```

**Script does:**
1. Reads validated manifest
2. For each entry: INSERT INTO timeline_events (...)
3. Database CHECK constraints enforce: enums, word count, required fields
4. If any INSERT fails: rolls back entire batch (atomic)

**On success:**
```
SUCCESS: 30 events ingested
  - All 30 entries added to timeline_events table
  - Provenance metadata: source_method=SCHOLARSHIP_BASED, confidence tracked
  - Entity links verified at DB level
```

**Output:** Batch is now in database

---

### Step 7: Site Generation

**Human runs:**
```bash
python scripts/build_site.py
```

**Script generates:**
- Static HTML pages for each timeline event
- data.json for JavaScript (map pins, timeline viewer)
- Cross-reference pages (persons → events, texts → events, concepts → events)
- Validation: No broken links (all referenced entities exist)

**Human verifies:** Site looks correct, no 404s

---

## VALIDATION TIERS

### Tier 1: Mechanical Validation (Automatic)

**Purpose:** Catch data quality issues mechanically, not through human reading.

**Who:** Scripts (scripts/validate_*.py)

**Checks:**
- Word count range (100–250 for timeline events, etc.)
- Required fields present
- Enum values valid (era, confidence, etc.)
- Entity slug existence
- Checksum matches
- Bibliography format (regex)

**Pass/fail:** Binary (no ambiguity)

**Speed:** <1 second per batch

**Cost:** Free (automatic)

**Output:** Error codes (from docs/CONTRACTS.json) + fix suggestions

---

### Tier 2: Human Review (Selective)

**Purpose:** Ensure historiographical grounding and tone match project standards.

**Who:** Human editor (Ted Hand)

**Checks:**
- Historiographical grounding (references to authorities, material culture)
- Material practices described (for ACTOR_TERMs)
- Scholarly debates noted (for ANALYST_TERMs)
- Tone is scholarly (not hagiographic, not esoteric)
- Confidence levels justified
- Entity links are not overfitted

**Pass/fail:** Subjective (requires judgment)

**Speed:** ~5 minutes per 5–10 entries (spot-check, not all)

**Cost:** Human time (limited resource)

**Output:** APPROVE / APPROVE WITH REVISIONS / REJECT + feedback

---

### Tier 3: Database Constraints (Enforcement)

**Purpose:** Final safety check at database level.

**Who:** SQL CHECK constraints in scripts/init_db.py

**Checks:**
- Enum values must be one of: ANTIQUITY, LATE_ANTIQUE, ...
- Word count for bio_html must be 1200–2200 (checked via character count)
- Foreign keys exist (location_slug → locations table)

**Pass/fail:** Binary (no INSERT if constraint violated)

**Speed:** <1ms per INSERT

**Cost:** Free (database overhead)

**Output:** Transaction rollback + error message

---

## PROVENANCE TRACKING

**Every entry has provenance metadata:**

```json
{
  "entity_slug": "ibn-sina-980-travels-to-rey",
  "description": "...",
  "source_method": "SCHOLARSHIP_BASED",
  "confidence": "HIGH",
  "review_status": "DRAFT",
  "created_by_agent": "timeline-enricher-v1.0",
  "created_at": "2026-05-22T14:32:00Z",
  "reviewed_by": "ted-hand",
  "reviewed_at": "2026-05-22T15:10:00Z"
}
```

### Source Method Enum

**MANUAL:** Human wrote this entry from scratch
- Example: Ted Hand writes new person biography
- Validation: Spot-check required

**AI_ASSISTED:** AI wrote this entry, human reviewed and approved
- Example: Claude Code agent enriches timeline events, human approves batch
- Validation: Mechanical + human spot-check

**SCHOLARSHIP_BASED:** AI created this from scholarship, with source citations
- Example: Claude Code agent extracts timeline events from published papers
- Validation: Mechanical + human spot-check + bibliography check

---

### Confidence Enum

**HIGH:** Documented in multiple primary sources or widely accepted scholarship
- Example: Ibn Sina's birth year (980) documented in multiple sources
- Standard: Used for facts verified in 2+ independent sources

**MEDIUM:** Documented in one source or inferred from context
- Example: Ibn Sina's travel dates (inferred from writings' locations)
- Standard: Used for facts from single source or reasonable inferences

**LOW:** Speculative or reconstructed from fragmentary evidence
- Example: Ibn Sina's daily routine (not directly documented)
- Standard: Used sparingly; human must approve

---

### Review Status Enum

**DRAFT:** Entry created, not yet reviewed by human
- Pipeline: Passed mechanical validation, awaiting human approval

**REVIEWED:** Human has read and approved this entry
- Pipeline: Passed mechanical + human review, ready for ingestion

**VERIFIED:** Human has verified this entry against primary sources or scholarship
- Pipeline: Triple-checked; high confidence in accuracy

---

## TASK ISOLATION: PREVENTING CROSS-CONTAMINATION

**Problem:** If human is working on timeline events while AI is working on person biographies, changes might collide.

**Solution:** Staging directory structure with clear task isolation

```
staging/
├── timeline_events/
│   ├── ibn_sina_batch1.json (30 events)
│   ├── ibn_sina_batch2.json (25 events)
│   └── roger_bacon_batch1.json (40 events)
├── persons/
│   ├── alchemists_phase2_batch1.json (5 biographies)
│   └── modern_scholars_batch1.json (3 biographies)
├── texts/
│   ├── primary_sources_batch1.json (8 texts)
│   └── scholarship_batch1.json (5 texts)
└── concepts/
    ├── actor_terms_phase2_batch1.json (12 concepts)
    └── analyst_terms_batch1.json (8 concepts)
```

### Rules

**Rule 1:** Each batch is independent
- Batch A can be rejected without affecting Batch B
- Batches can be ingested in any order
- No cross-batch dependencies

**Rule 2:** One entity slug per batch
- Don't ingest the same entity twice in one phase
- Use version numbers if re-enriching: `ibn-sina-1000-travels_v2` for revision

**Rule 3:** Manifest is atomic
- Ingest entire manifest or none
- Partial ingestion is not allowed (prevents inconsistency)

---

## ANTI-DRIFT MECHANISMS

**Problem:** Over time, prose standards (STYLEGUIDE.md) can drift from what's actually validated (SCHEMA.json).

**Solution:** Multiple checkpoints that prevent drift

### Checkpoint 1: Authority Hierarchy

**Rule:** If SCHEMA.json says word count is 100–250, but STYLEGUIDE.md says 100–300, SCHEMA.json wins.

**Enforcement:** Validation script loads word count from SCHEMA.json, not STYLEGUIDE.md.

**Human responsibility:** Keep STYLEGUIDE.md in sync with SCHEMA.json (check monthly)

---

### Checkpoint 2: Automated Validation Testing

**Monthly test:** Run validation on all existing database entries

```bash
python scripts/validate_existing_db.py --all
```

**Checks whether all existing entries still pass current validation rules**

**If any fail:** Flag for human review
- Maybe entry predates current standards (acceptable)
- Maybe validation rule changed and entry wasn't updated (bug)

---

### Checkpoint 3: Explicit Version Numbers

**SCHEMA.json has version number:**
```json
{
  "version": "1.0",
  "generated_date": "2026-05-22",
  ...
}
```

**Staging manifest includes schema version it was validated against:**
```json
{
  "schema_version": "1.0",
  "entries": [...]
}
```

**Ingestion script checks version:**
- If schema version < 1.0: Error (outdated validation)
- If schema version > current: Error (entry validated by future rules)
- If schema version == current: OK

---

### Checkpoint 4: Changelogs

**CHANGELOG.md documents all schema changes:**
```
## [2026-06-15] Schema Update v1.1
- Changed timeline event word count: 100–250 → 80–300 (more flexibility for complex events)
- Added new enum value: confidence: SPECULATIVE (for fragmentary sources)
- Existing entries: No change required (all entries pass new validation)

## [2026-07-01] Schema Update v1.2
- Changed person biography required sections: added "historiographical_disputes" section
- Existing entries: Must be updated to include new section (30 entries affected)
```

**Human responsibility:** Update CHANGELOG.md whenever SCHEMA.json changes

---

### Checkpoint 5: Reconciliation Reports

**Monthly report: "Are prose docs in sync with executable rules?"**

```python
def audit_sync(schema_path, styleguide_path):
    """Check whether STYLEGUIDE.md matches SCHEMA.json"""
    schema = load_json(schema_path)
    styleguide = load_text(styleguide_path)
    
    mismatches = []
    
    # Check word counts
    for content_type, spec in schema["content_types"].items():
        word_count = spec["word_count"]
        min_words = word_count["min"]
        max_words = word_count["max"]
        
        # Look for mention of word count in styleguide
        pattern = rf'{content_type}.*?(\d+).*?(\d+)\s+words'
        matches = re.findall(pattern, styleguide)
        
        if matches and (int(matches[0][0]) != min_words or int(matches[0][1]) != max_words):
            mismatches.append({
                "type": content_type,
                "schema": f"{min_words}–{max_words}",
                "styleguide": f"{matches[0][0]}–{matches[0][1]}"
            })
    
    return mismatches
```

**Output:**
```
SYNC CHECK REPORT

MISMATCHES FOUND:
- timeline_event: schema says 100–250, STYLEGUIDE.md says 100–280
- person_biography: MISSING from STYLEGUIDE.md but present in schema

ACTION REQUIRED:
- Update STYLEGUIDE.md § 4 to match schema (100–250, not 100–280)
- Add person_biography section to STYLEGUIDE.md
```

---

## REVIEW WORKFLOW FOR HUMANS

### Weekly Review Session

**Time:** 1 hour per week (Wednesday 2pm)

**Process:**
1. **Check validation reports** (5 min)
   - Were there any mechanical validation failures this week?
   - Any entity slugs that didn't exist in DB?
   - Any checksum mismatches?

2. **Spot-check approved batches** (40 min)
   - Read 5–10 entries from each batch approved since last week
   - Check historiographical grounding
   - Check tone and quality
   - Approve/reject/request revisions

3. **Ingest approved batches** (10 min)
   - Run `scripts/enrich_*.py --ingest` for approved batches
   - Generate site with `scripts/build_site.py`
   - Verify site looks correct (no broken links, formatting OK)

4. **File sync audit** (5 min)
   - Run `audit_sync()` to check SCHEMA.json vs STYLEGUIDE.md
   - If mismatches found, add to next week's task

---

### Quarterly Schema Review

**Time:** 2 hours per quarter (end of each quarter)

**Process:**
1. **Review validation failures from last quarter**
   - Any patterns? (e.g., "person biographies always exceed word count")
   - Should validation rules change?

2. **Review human feedback from spot-checks**
   - Any themes in feedback? (e.g., "agents keep overfitting entity links")
   - Should standards be clarified?

3. **Propose schema updates**
   - Adjust word counts?
   - Add/remove enum values?
   - Change required sections?

4. **Update documentation**
   - Update SCHEMA.json (version number incremented)
   - Update STYLEGUIDE.md and STANDARD_*.md
   - Update CHANGELOG.md with reason for change

5. **Re-validate existing entries** (if rules changed)
   - If new rules are stricter, which entries need updating?
   - If new rules are looser, no change needed

---

## CONFLICT RESOLUTION: HUMAN FINAL AUTHORITY

**Scenario:** Schema says word count 100–250, but human editor thinks an event needs 300 words to do it justice.

**Resolution process:**
1. **Human requests exception:** "Entry X needs 300 words for proper context"
2. **Schema constraint is temporarily relaxed:** For this entry, confidence = MEDIUM (signal that it's non-standard)
3. **Question is raised:** Should the schema change for all entries?
   - If yes: Update SCHEMA.json word count → 100–300
   - If no: Keep exception as one-off, note in database

**Important:** Humans decide; systems enforce. No content enters without validation, but validation rules can change via human decision.

---

## SUSTAINABLE COLLABORATION MODEL

**Goal:** Humans set standards once, AI executes repeatedly, systems verify automatically.

| Phase | Human Role | AI Role | System Role |
|-------|-----------|---------|-------------|
| **Specification** | Set task, constraints, standards | — | — |
| **Creation** | — | Write content, format correctly | — |
| **Validation** | Spot-check samples | — | Mechanical validation |
| **Revision** | Approve/reject | Revise per feedback | — |
| **Ingestion** | Approve batch | — | Mechanical ingestion |
| **Generation** | Verify output | — | Automatic site build |
| **Maintenance** | Monthly audits, quarterly reviews | — | Continuous validation |

**Time commitment:**
- Human: ~1 hour per week + 2 hours per quarter
- AI: Full-time execution (on demand)
- System: Continuous (no cost beyond initial setup)

**Scalability:**
- Current: 500 timeline events + 100 persons + 50 texts + 30 concepts
- With this model: Can scale to 2000 events without significant overhead increase
- Bottleneck: Human review time (keeps human in final approval loop)

---

*End of architectural deliverables.*
