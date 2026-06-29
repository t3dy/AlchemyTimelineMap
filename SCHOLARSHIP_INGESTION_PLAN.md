# Scholarship PDF Ingestion Plan (2026-06-14)

**Objective:** Integrate 85 alchemy scholarship PDFs into ALCHEMYTIMELINEMAP, with special emphasis on Jennifer Rampling's work, to substantially populate the database and update ontology/style guides.

---

## Current Status

| Stage | Count | Status |
|-------|-------|--------|
| PDFs collected | 85 | ✓ Complete |
| PDFs converted to markdown | 44 | ⧗ In progress (background task) |
| Entities extracted (from 44) | 212 persons, 350+ texts, 228+ concepts | ✓ Complete |
| Working notes created | 44 | ✓ Complete |
| Jennifer Rampling papers analyzed | 24 | ⧗ Awaiting conversion |

---

## Phase 1: Completion of PDF Conversion (In Progress)

**Target:** Convert all 85 PDFs to markdown
- Alchemy folder: ~60 PDFs (44 completed, 16 remaining)
- Jennifer Rampling folder: 25 PDFs (awaiting)

**Output:** 85 markdown files in `staging/pdfs_to_markdown/`

**Completion Condition:** All PDFs converted OR timeout/error handling triggers manual review

---

## Phase 2: Entity Extraction from All PDFs

**Timeline:** Upon completion of Phase 1

**Script:** `scripts/extract_entities_from_pdfs.py`

**Expected Extraction:**
- **Persons:** 400+ unique scholars and alchemists mentioned
- **Texts:** 500+ alchemical and scholarly works referenced
- **Concepts:** 400+ alchemical, philosophical, and historical concepts

**Output:**
- 85 working notes in `staging/pdf_working_notes/`
- Entity extraction index: `staging/pdf_entity_extraction.json`

---

## Phase 3: Rampling Scholarship Deep-Read

**Timeline:** Concurrent with Phase 2

**Process:**
1. Read all 24 Rampling papers (markdown versions)
2. Extract specialized entities:
   - George Ripley tradition figures
   - English alchemical practitioners
   - Manuscript collections and lineages
   - Vernacular alchemical concepts
3. Identify historiographical contributions (see `RAMPLING_SCHOLARSHIP_ANALYSIS.md`)

**Output:**
- Updated `RAMPLING_SCHOLARSHIP_ANALYSIS.md` with detailed findings
- Proposed ontology changes (entity types, relationships, schema additions)
- Proposed style guide updates (person/text/concept standards)

---

## Phase 4: Ontology & Style Guide Updates

**Timeline:** As Phase 3 findings emerge

**Target Documents to Update:**
- `SCHEMA.json` — Add new entity types, relationship fields
- `STANDARD_PERSON_BIOGRAPHIES.md` — Incorporate Rampling's framework
- `STANDARD_TEXT_DESCRIPTIONS.md` — Add textual genealogy sections
- `STANDARD_CONCEPT_DEFINITIONS.md` — Account for linguistic/regional variation
- `CONCEPTUAL_FRAMEWORK.md` — Integrate Rampling's historiographical insights

**Key Changes Expected:**
1. New field: `textual_genealogy` for texts
2. New field: `learned_works_studied` for persons
3. New field: `transmission_history` for concepts
4. New entity type: `manuscript_collection`
5. New relationship types: `derives_from`, `translated_into`, `adapted_as`
6. Enhanced enums for `text_genre` (practical, theoretical, emblematic, pedagogical, etc.)

---

## Phase 5: Enrichment Batch Creation

**Timeline:** Weeks 2-3

**Strategy:** Create batches organized by scholarly themes

### Batch A: George Ripley Tradition (Priority 1)
- **Persons:** George Ripley, Ripley students, Ripley copyists (10-15)
- **Texts:** Ripley corpus variants, commentaries (8-12)
- **Concepts:** Ripley-specific concepts (5-8)
- **Events:** Dates of composition, transmission, printed editions (10-15)
- **Source:** Rampling's George Ripley papers

### Batch B: English Alchemical Tradition (Priority 1)
- **Persons:** English alchemists beyond Ripley (15-20)
- **Texts:** English alchemical works, vernacular pieces (12-18)
- **Concepts:** English-specific terminology and practices (8-12)
- **Events:** Regional developments, institutional contexts (15-20)
- **Source:** Rampling's "Englishing" and "Experimental Fire" papers

### Batch C: Medieval Alchemical Cosmos (Priority 2)
- **Persons:** Medieval cosmological thinkers (8-12)
- **Texts:** Cosmological and emblematic works (10-15)
- **Concepts:** Cosmic correspondence, microcosm/macrocosm variations (8-12)
- **Events:** Manuscript production, visual representation emergence (8-12)
- **Source:** Rampling's "Depicting the Medieval Alchemical Cosmos" + related papers

### Batch D: Chemical Knowledge in Transit (Priority 2)
- **Persons:** Translators, adapters, regional practitioners (12-18)
- **Texts:** Translated and adapted works, regional variants (15-20)
- **Concepts:** Concepts as they evolved across languages/regions (12-18)
- **Events:** Translation events, linguistic/cultural adaptation (12-18)
- **Source:** Multi-author papers on transmission, Rampling's transmission work

### Batch E: Alchemical Pedagogy (Priority 3)
- **Persons:** Teachers, students, patrons (10-15)
- **Texts:** Pedagogical guides, instructional works (8-12)
- **Concepts:** Mastery, learning stages, craft hierarchies (6-10)
- **Events:** Institutional teaching, apprenticeship records (8-12)
- **Source:** Rampling's education and pedagogy papers

---

## Phase 6: Database Population

**Timeline:** Weeks 3-6

**Process:**
1. Create enrichment batches (JSON format)
2. Validate against updated SCHEMA.json
3. Load batches using existing loading scripts
4. Rebuild site
5. Verify all entity links and relationships

**Expected Additions:**
- **Persons:** 60-80 new entries (George Ripley + English tradition + support figures)
- **Texts:** 50-70 new entries (Ripley corpus, English alchemical works, variants)
- **Concepts:** 30-50 new entries (Rampling-defined concepts)
- **Events:** 80-120 new entries (transmission events, publication dates, institutional contexts)

**Database Target After Population:**
- Persons: 150-170 (from current 93)
- Texts: 93-113 (from current 43)
- Concepts: 68-88 (from current 38)
- Events: 680-720 (from current 602)

---

## Phase 7: Remaining Scholarship Integration

**Timeline:** Weeks 6-8

**Process:**
1. Extract remaining persons, texts, concepts from non-Rampling papers
2. Create batches for:
   - Islamic and medieval foundations
   - Renaissance Italian alchemy
   - Early modern continental alchemy
   - Historiographical figures (Taylor, Holmyard, Newman, Principe, etc.)

**Expected Additional Population:**
- Persons: 40-60
- Texts: 40-60
- Concepts: 20-30
- Events: 60-100

**Database Target After Full Ingestion:**
- Persons: 190-230
- Texts: 133-173
- Concepts: 88-118
- Events: 740-820

---

## Integration with Existing 4,446 Markdown Files

**Current State:** 200 of 4,446 files processed (4.5%)
**New Scholarship Addition:** 85 PDFs (structured, peer-reviewed publications)

**Strategy:**
1. Prioritize Rampling and related scholarship (25-30 papers) for detailed enrichment
2. Use remaining 50-60 papers for entity reference and validation
3. Integrate findings back into 4,446-file processing pipeline
4. Use Rampling's framework to guide enrichment of 4,246 remaining files

**Synergy:**
- Rampling's historiographical framework will improve enrichment quality across full collection
- Identified persons/texts/concepts provide anchors for processing general PDF collection
- Regional and traditional distinctions from Rampling will help organize large collection

---

## Success Criteria

✓ All 85 PDFs converted to markdown
✓ Entities extracted and working notes created
✓ Ontology updated with new entity types and relationships
✓ Style guides revised to reflect Rampling's framework
✓ 100-150 new database entries created from scholarship
✓ Database reaches ~200-250 total persons (vs. 93 current)
✓ Database reaches ~130-180 total texts (vs. 43 current)
✓ Database reaches ~90-120 total concepts (vs. 38 current)
✓ Site rebuilt and validated with new content
✓ 4,446 markdown files processing informed by scholarship

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| PDF conversion incomplete | Fallback to manual extraction for key papers, especially Rampling |
| Entity extraction imprecision | Manual review and curation of working notes before enrichment |
| Ontology changes break existing data | Test schema updates on copy; migrate carefully |
| Enrichment quality degradation | Use Rampling's methodological framework for consistency |
| Scope creep beyond 85 PDFs | Explicitly limit to this collection; 4,446 files are separate project |

---

## Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| Week 1 (now) | 1-2 | PDF conversion complete, entities extracted |
| Week 2 | 3-4 | Rampling analysis complete, ontology drafted |
| Week 3 | 4-5 | Ontology finalized, style guides updated |
| Week 4 | 5-6 | First enrichment batches created and loaded |
| Week 5-6 | 6 | Remaining batches created, tested, loaded |
| Week 7-8 | 7 | Non-Rampling scholarship integrated |

---

*This plan integrates 85 scholarship PDFs into ALCHEMYTIMELINEMAP, with primary focus on Jennifer Rampling's historiographical framework, aiming to add 100-150+ new high-quality entries to the database and update ontology/style guides to reflect contemporary scholarly practice in the history of alchemy.*
