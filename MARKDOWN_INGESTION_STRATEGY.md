# Markdown Ingestion Strategy — ALCHEMYTIMELINEMAP

**Purpose:** Systematically process 4,446 markdown files from `e:\pdf\alchemy` to populate timeline events, person biographies, text descriptions, concept definitions, and map locations.

**Updated:** 2026-06-14  
**Source inventory:** 4,446 `.md` files (converted from PDFs)  
**Current phase:** Phase 2 Complete → Phase 3A (Enrichment from Scholarly Sources)

---

## PART 1: INGESTION ARCHITECTURE

### § 1.1: Three-Layer Processing Pipeline

```
[Raw markdown in e:\pdf\alchemy]
           ↓
[Layer 1: READ & EXTRACTION] → Ingest markdown, extract entities, create working notes
           ↓
[Layer 2: ARTIFACT CREATION] → Generate entity metadata, enrich context, update indices
           ↓
[Layer 3: DATABASE FEEDING] → Validate, standardize, feed into staging/ for main session
```

---

## PART 2: LAYER 1 — READING & EXTRACTION WORKFLOW

### § 2.1: Entity Types to Extract

From each markdown file, identify and extract:

| Entity Type | Examples | Source Signal |
|-------------|----------|----------------|
| **Person/Alchemist** | "Zosimos," "Jabir," "Roger Bacon," "Paracelsus" | Named historical figures, biographies, letters |
| **Text/Publication** | "Emerald Tablet," "Summa Perfectionis," "Zosimos' writings" | Titles, manuscripts, printed editions, commentaries |
| **Location** | "Baghdad," "Alexandria," "Florence," "Prague" | Geographic references, cities, regions |
| **Concept/Theory** | "distillation," "calcination," "transmutation," "quintessence" | Chemical operations, philosophical ideas, symbols |
| **Event/Discovery** | Date + action (e.g., "1200s: Gerard translates Arabic texts into Latin") | Dated occurrences, publications, institutional founding |
| **Chemical Process** | "fermentation," "sublimation," "crystallization" | Material operations, apparatus use |
| **Symbol/Allegory** | "Green Dragon," "King and Queen," "Mercury and Sulfur" | Emblematic language, alchemical symbolism |
| **Scholarly Debate** | "Whether Zosimos practiced transmutation," "Medieval vs. Arabic periodization" | Historiographical disputes, scholarly disagreements |

### § 2.2: Extraction Format — Working Notes

For each markdown file processed, create a working note in `staging/working_notes/`:

**Filename:** `note_[source_slug].md`  
**Location:** `C:\Dev\ALCHEMYTIMELINEMAP\staging\working_notes\`

**Template:**

```markdown
# Working Note: [Source Title]
**Source:** [Original filename from e:\pdf\alchemy]
**Processed:** [ISO date]
**Processor:** [Your name or Agent ID]

## Summary
[2–3 sentence overview of what this source covers]

## Persons Identified
- [Name]: [Role], [Brief context], **Status:** NEW / EXISTS
  - Links to: [related concepts/texts]
  - Event potential: [What events could be created?]
- [Name]: [Role], [Brief context], **Status:** NEW / EXISTS

## Texts Identified
- [Title]: [Author], [Date/Period], **Status:** NEW / EXISTS
  - Content type: [manuscript / printed / secondary]
  - Mentions: [What persons/concepts does it connect to?]

## Locations/Geographic Clusters
- [Location]: [Period], [Why significant?]
  - Alchemists known there: [Names]
  - Key events: [1–2 items]

## Concepts/Operations
- [Term]: ACTOR_TERM / ANALYST_TERM, [Definition in one sentence]
  - Mentioned by: [Which persons/texts?]
  - Historical significance: [1–2 sentences]

## Symbols & Allegories
- [Symbol]: [What does it represent?], [In what texts?]

## Potential Timeline Events
[Number: X] (to be developed)
- [Date/Period]: [Location] — [Brief event description, 1 sentence]
  - Scholarly grounding: [Which modern scholar writes about this?]
  - Links to: [persons/texts/concepts]
- [Repeat]

## Scholarly Debates / Historiographical Notes
- [Debate topic]: [Brief summary], [Scholars involved], [Relevance to ALCHEMYTIMELINEMAP]

## Cross-References to Existing Database
- Persons: [Which ones mentioned are already in DB?]
- Texts: [Which ones already exist?]
- Locations: [Already mapped?]

## Quality Flags
- [ ] Source is primary vs. secondary (note which)
- [ ] Dates are precise or approximate?
- [ ] Any claims about transmutation? (Note as BELIEF vs. FACT)
- [ ] Provenance: Who is the modern author of this markdown?

## Next Steps
- [ ] Create [X] new persons in database
- [ ] Create [X] new texts
- [ ] Generate [X] timeline events
- [ ] Update concept definitions with material from this source
```

---

## PART 3: LAYER 2 — ARTIFACT CREATION

### § 3.1: Artifact Types

As you process each markdown file, generate the following artifacts:

#### **Artifact A: Entity Metadata Index (XLSX)**

**File:** `staging/entity_extraction_index.xlsx`

A spreadsheet tracking every entity discovered:

| Entity Slug | Entity Name | Type | Status | Source File | Date Identified | Confidence | Notes |
|-------------|-------------|------|--------|------------|-----------------|------------|-------|
| zosimos-panopolis | Zosimos of Panopolis | Person | EXISTS | 0001-early-greek.md | 2026-06-14 | HIGH | Multiple sources confirm |
| new-alchemist-x | [Unnamed] | Person | NEW | 0234-medieval-persia.md | 2026-06-14 | MEDIUM | Needs biographical work |

**How to use:**
- One row per entity
- Status: EXISTS (already in DB), NEW (needs creation), VARIANT (alternate spelling of existing)
- Confidence: HIGH / MEDIUM / LOW based on source clarity
- Filter by Type to batch-process similar entities

#### **Artifact B: Event-Candidate List (Markdown)**

**File:** `staging/event_candidates_[region_era].md`

```markdown
# Timeline Event Candidates: [Region/Era, e.g., "Baghdad 9th Century"]

**Compiled from:** [List of source files]
**Count:** [X] event candidates
**Quality:** Draft/Ready for enrichment

| Date | Location | Event Title | Key Actors | Source Doc | Scholarly Grounding (to find) |
|------|----------|-------------|-----------|-----------|------|
| ~825 | Baghdad | Jabir ibn Hayyan's distillation experiments | [LINK:jabir-ibn-hayyan] | 0234-persia.md | [Newman/Kraus on Jabir] |
| 1200 | Toledo | Gerard of Cremona translates alchemical texts | [LINK:gerard-cremona] | 0567-spain.md | [Lindberg on Gerard] |
```

Use this to batch-schedule timeline event enrichment jobs.

#### **Artifact C: Concept Extraction Sheet (Markdown)**

**File:** `staging/concepts_identified.md`

Capture new concepts, new definitions, etymology:

```markdown
# Concepts Identified from PDF Sources

## NEW CONCEPTS (Not in current database)
- **[Concept]**: [Actor definition from sources] / [Analyst interpretation]
  - Sources: [Files where mentioned]
  - Scholarly treatment: [Who writes about it? What's the historiography?]
  - Related to: [Existing concepts in DB]

## REFINEMENTS TO EXISTING CONCEPTS
- **Distillation**: Add material from Source X showing apparatus detail (glass retorts, furnaces)
- **Transmutation**: Expand ACTOR_TERM vs. ANALYST_TERM distinction with new evidence

## SYMBOL/ALLEGORY CATALOG
- **Ouroboros**: Representation in [File X], meaning in context of [Concept Y]
- **Green Dragon**: [Definition], appears in [Texts X, Y, Z]

## PROCESS WORKFLOW NOTES
- **Fermentation** ACTOR_TERM: Add equipment (sealed vessels, temperature control)
- **Sublimation** ACTOR_TERM: New evidence on temperature thresholds in [Source Y]
```

---

## PART 4: LAYER 3 — DATABASE FEEDING

### § 4.1: Ingestion Checklist (Before Writing to Staging/)

Before any markdown file generates database artifacts, verify:

- [ ] **Provenance on every claim:** Every person, text, date, location, and concept is traceable to a source or scholar
- [ ] **Actor/Analyst distinction:** If a term is used, is it the actor's language or modern analytical category?
- [ ] **No endorsement of transmutation:** Transmutation is reported as historical belief, not fact
- [ ] **Geographic specificity:** Every event has a city (or region if city unknown)
- [ ] **Scholarly grounding:** At least one modern scholar cited for each event
- [ ] **Link validation:** Every `[LINK:slug]` references an entity that exists in the database (check SCHEMA.json enum)

### § 4.2: Staging Workflow

**Three documents produced for each batch of markdown files:**

1. **`staging/[batch_name]_persons.json`** — New persons (with bio_html field)
2. **`staging/[batch_name]_texts.json`** — New texts (with analysis field)
3. **`staging/[batch_name]_events.json`** — New timeline events (with scholarly_grounding field)
4. **`staging/[batch_name]_concepts.json`** — New/enriched concepts (with definition_long field)

**Format (example):**

```json
{
  "persons": [
    {
      "slug": "new-person-slug",
      "name": "Full Name",
      "era": "Medieval",
      "role": "Alchemist",
      "bio_html": "[Enriched biography, 1,200+ words...]",
      "source_method": "PDF_INGESTION:e:\\pdf\\alchemy\\[filename]",
      "review_status": "DRAFT",
      "confidence": "HIGH",
      "date_created": "2026-06-14"
    }
  ],
  "events": [
    {
      "date_label": "c. 825",
      "date_sort": 825,
      "era_slug": "early-medieval",
      "location_slug": "baghdad",
      "title": "Event Title",
      "description": "[100–250 words, with [LINK:slug] markup...]",
      "scholarly_grounding": "Scholar LastName demonstrated X in *Title* (Year) ch.X pp.XX-YY",
      "source_method": "PDF_INGESTION:e:\\pdf\\alchemy\\[filename]",
      "review_status": "DRAFT",
      "confidence": "HIGH"
    }
  ]
}
```

---

## PART 5: EXECUTION WORKFLOW

### § 5.1: Reading Phase (Agents)

**Agent role: PDF Source Analyzer**

- **Input:** Directory of markdown files (batched by era/region)
- **Output:** Working notes + Entity Metadata Index + Event Candidates list + Concept sheet
- **Tools:** Read markdown files, extract entities, fill templates
- **Quality gate:** Every entity has a working note entry with sources

**Suggested batches:**
- Late Antique (Egypt, Syria, 1st–4th centuries)
- Early Islamic (Baghdad, Persia, Cairo, 8th–10th centuries)
- Medieval Latin Europe (Monasteries, Universities, 10th–13th centuries)
- Medieval Islam Continued (Spain, Al-Andalus, 9th–15th centuries)
- Renaissance (Italy, Florence, Venice, 15th–16th centuries)
- Early Modern (Central Europe, England, France, 16th–18th centuries)

### § 5.2: Enrichment Phase (Main Session)

**Main session role: Enricher + Validator**

- **Input:** Working notes + Event Candidates + Concept sheets
- **Output:** Staging JSON files with full descriptions, scholarly grounding, complete entity enrichment
- **Tools:** Agent + Manual enrichment for quality control

**Process:**
1. Read working notes
2. For each event candidate: write 100–250 word description with scholarly grounding
3. For each new person: write 1,200+ word biography
4. For each new text: write 1,000+ word analysis
5. For each new concept: write 1,500+ word definition with Actor/Analyst distinction

### § 5.3: Validation Phase

Before inserting into database:

```sql
-- Validate all [LINK:slug] references exist
SELECT COUNT(*) FROM staging_events e 
WHERE e.description LIKE '%[LINK:%' 
AND NOT EXISTS (SELECT 1 FROM entities WHERE entities.slug = extracted_slug);

-- Validate word counts
SELECT COUNT(*) FROM staging_events WHERE LENGTH(description) < 400 OR LENGTH(description) > 5000;

-- Validate scholarly grounding is present
SELECT COUNT(*) FROM staging_events WHERE scholarly_grounding IS NULL;
```

---

## PART 6: ONTOLOGY & STYLEGUIDE UPDATES

### § 6.1: When to Update SCHEMA.json

If markdown files reveal:
- **New entity type** (e.g., "Institution" or "Chemical Apparatus") → Update SCHEMA.json
- **New enum value** (e.g., new era slug, new role type) → Add to `enums/` section
- **New relationship type** → Update foreign key definitions

### § 6.2: When to Update STANDARD_*.md

If enrichment work reveals:
- **New required field** for persons/texts/concepts/events
- **Shift in historiographical understanding** → Update CONCEPTUAL_FRAMEWORK.md
- **New scholarly authority** → Add to key scholars list

---

## PART 7: QUALITY & COMPLETENESS CHECKLIST

### § 7.1: Per-Entity Quality Gate

Every new person, text, concept, or event must pass:

- [ ] **Provenance:** Source file listed; modern scholar cited (if primary source)
- [ ] **Word count:** In range per STANDARD_*.md
- [ ] **Links:** All `[LINK:slug]` validated against SCHEMA.json
- [ ] **No markdown artifacts:** No stray `#`, `*`, `**`, `[]` in final prose
- [ ] **Historiographical clarity:** Actor/Analyst distinction explicit (concepts/persons)
- [ ] **Bibliography:** DGWE format (if person/text/concept)
- [ ] **Review status:** DRAFT, READY_FOR_REVIEW, or REVIEWED
- [ ] **Confidence:** HIGH, MEDIUM, or LOW

### § 7.2: Completeness Targets

| Content Type | Target | Current | Gap |
|---|---|---|---|
| Persons | 150 | 81 | +69 |
| Texts | 80 | 42 | +38 |
| Concepts | 50 | 30 | +20 |
| Timeline Events | 600 | 582 | +18 |
| Locations | 60 | ~60 | ✅ |

---

## PART 8: WORKING NOTES ARCHIVE

All working notes are stored in `staging/working_notes/` and indexed in `staging/WORKING_NOTES_INDEX.md`:

```markdown
# Working Notes Index

[Table of all processed sources]

| Source File | Working Note | Persons | Texts | Events | Status |
|---|---|---|---|---|---|
| 0001-early-greek.md | note_early-greek.md | 5 | 3 | 8 | ✅ PROCESSED |
| 0234-medieval-persia.md | note_medieval-persia.md | 12 | 7 | 15 | ✅ PROCESSED |
```

---

## PART 9: NEXT IMMEDIATE ACTIONS

1. **Create Python batch reader** (`scripts/read_markdown_batch.py`)
   - Input: Directory of markdown files + era/region filter
   - Output: Working notes + Entity Index + Event Candidates
   - Idempotent: skip already-processed files

2. **Deploy working-notes template** to `staging/working_notes/`

3. **Launch pilot batch** (e.g., Early Islamic Baghdad, 20 markdown files)
   - Create working notes for all 20
   - Identify ~5 new persons, ~3 new texts, ~10 event candidates
   - Enrich and validate 5 events as proof-of-concept

4. **Update PHASESTATUS.md** with Phase 3A (PDF Enrichment) progress

5. **Create entity extraction index** (XLSX spreadsheet)
   - Automate with Python script
   - One row per unique person/text/location/concept identified

---

## REFERENCES

- **CLAUDE.md** — Project routing and task structure
- **PHASESTATUS.md** — Current phase and success criteria
- **STANDARD_TIMELINE_EVENTS.md** — Event specification (100–250 words, required fields)
- **STANDARD_PERSON_BIOGRAPHIES.md** — Person specification (1,200+ words)
- **STANDARD_TEXT_DESCRIPTIONS.md** — Text specification
- **CONCEPTUAL_FRAMEWORK.md** — Historiographical principles
- **SCHEMA.json** — Machine-readable entity definitions and enums
