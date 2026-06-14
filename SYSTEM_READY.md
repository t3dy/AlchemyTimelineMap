# ✅ Markdown Ingestion System — READY FOR PHASE 3A

**Date:** 2026-06-14  
**Status:** System Complete & Ready to Execute  
**Phase:** Phase 3A (Scholarly Source Enrichment via PDF Conversion)

---

## WHAT'S BEEN CREATED

A complete **3-layer systematic ingestion pipeline** for processing 4,446 markdown files (converted from PDFs in `e:\pdf\alchemy`) into scholarly timeline events, person biographies, text analyses, and concept definitions.

### 📋 Documentation (4 Core Files)

1. **MARKDOWN_INGESTION_STRATEGY.md** (Architectural overview)
   - How the 3-layer pipeline works
   - Entity types to extract (persons, texts, locations, concepts, events, symbols, allegories)
   - Working notes format and artifact types
   - Quality gates and validation checklist
   - *Read once to understand the system*

2. **staging/WORKING_NOTES_TEMPLATE.md** (Per-source template)
   - Structured template for capturing entities from each markdown file
   - Sections: Persons, Texts, Locations, Concepts, Symbols, Timeline Events, Scholarly Debates, Cross-references
   - Quality flags and metadata fields
   - *Used by batch reader script to auto-generate stubs*

3. **ENRICHMENT_WORKFLOW.md** (Hands-on execution guide)
   - 6 phases: Preparation → Person → Text → Concept → Event → Validation
   - Detailed specifications for each content type (word counts, required sections, examples)
   - Validation checklists
   - Staging JSON format
   - *Reference daily during enrichment work*

4. **INGESTION_EXECUTION_PLAN.md** (Batch-by-batch roadmap)
   - 13 recommended batches (organized by era/region)
   - Per-batch execution timeline (3–5 days each)
   - Progress tracking templates
   - Troubleshooting Q&A
   - *Follow to organize work week-by-week*

### 🐍 Python Scripts (2 Helper Tools)

1. **scripts/read_markdown_batch.py**
   - Reads markdown files from `e:\pdf\alchemy`
   - Extracts entities (persons, texts, locations, concepts) using regex patterns
   - Generates working note stubs (auto-filled from template)
   - Idempotent: skips already-processed files, resumes interrupted runs
   - **Usage:** `python scripts/read_markdown_batch.py [limit]`
   - **Output:** `staging/working_notes/note_*.md` + `staging/processed_files.json` (tracking log)
   - **Time:** ~2–5 min per 100 files

2. **scripts/entity_extraction_index.py**
   - Parses all working notes
   - Generates Excel spreadsheet of unique entities
   - One row per entity (persons, texts, locations, concepts)
   - Columns: slug, name, status (NEW/EXISTS), confidence, source, source_file
   - **Usage:** `python scripts/entity_extraction_index.py`
   - **Output:** `staging/entity_extraction_index.xlsx`
   - **Time:** ~2–3 min

### 📁 Artifact Structure

```
staging/
├── working_notes/                    # Per-source working notes
│   ├── note_0001-filename.md
│   ├── note_0002-filename.md
│   └── [4,446 files total]
├── entity_extraction_index.xlsx      # Master index of all unique entities
├── WORKING_NOTES_TEMPLATE.md         # Template for new notes
├── BATCH_[name]_plan.md              # Per-batch enrichment plan
├── BATCH_[name]_persons.json         # Staging: new persons (ready for DB)
├── BATCH_[name]_texts.json           # Staging: new texts
├── BATCH_[name]_concepts.json        # Staging: new concepts
├── BATCH_[name]_events.json          # Staging: new events
├── processed_files.json              # Tracking log (idempotency)
└── PROGRESS.md                       # Weekly progress metrics
```

---

## HOW TO USE: QUICK START

### **Day 1: Extract Entities**

```bash
# 1. Process markdown files (pilot: first 100 files)
cd C:\Dev\ALCHEMYTIMELINEMAP
python scripts/read_markdown_batch.py 100

# 2. Generate entity index
python scripts/entity_extraction_index.py

# 3. Open results
# - staging/working_notes/note_*.md (50 working notes)
# - staging/entity_extraction_index.xlsx (Index of all entities)

# 4. Decide which batch to enrich first
# Open entity_extraction_index.xlsx
# Filter Status column → "NEW" to see what needs enrichment
```

### **Days 2–4: Enrich One Batch**

**Batch template: Late Antique Egypt & Syria (Pilot)**

```bash
# 1. Read and understand enrichment standards
# - Read: ENRICHMENT_WORKFLOW.md (entire file)
# - Keep open: STANDARD_TIMELINE_EVENTS.md
# - Keep open: CONCEPTUAL_FRAMEWORK.md (historiography)

# 2. For each new person identified in working notes:
# - Write 1,200–2,200 word biography
# - Include 8+ references in DGWE format
# - Save as [slug]-biography.md (temporary)

# 3. For each new text:
# - Write 1,000–1,800 word analysis
# - Include transmission history
# - Save as [slug]-text-analysis.md (temporary)

# 4. For each new concept:
# - Write 1,500–2,500 word definition
# - Declare ACTOR_TERM vs. ANALYST_TERM explicitly
# - Save as [slug]-concept-definition.md (temporary)

# 5. For each timeline event:
# - Write 100–250 word description
# - Include scholarly grounding (scholar + citation)
# - Use [LINK:slug] markup for entity links
# - Validate against SCHEMA.json enums
```

### **Day 5: Validate & Submit**

```bash
# 1. Run validation checklist
# - See ENRICHMENT_WORKFLOW.md § 6.2
# - Check: word counts, links, bibliography, confidence, review_status

# 2. Prepare staging JSON
# Create: staging/BATCH_001_enriched_entities.json
# (Contains: persons[], texts[], concepts[], events[])

# 3. Run Python validation
# python scripts/validate_staging_json.py

# 4. Submit to main session
# Output: "Batch 001 [Late Antique Egypt] ready for database insertion"
```

---

## THE 13-BATCH ROADMAP

**Recommended execution order (one batch every 5 days):**

| Week | Batch | Era/Region | Expected Output |
|---|---|---|---|
| Week 1 | 1 (Pilot) | Late Antique Egypt & Syria | 15–20 persons, 8–12 events |
| Week 2 | 2 | Early Islamic Baghdad & Persia | 20–30 persons, 40–50 events |
| Week 3–4 | 3 + 4 | Medieval Islam Spain + Monasteries | 30–40 persons, 65–75 events |
| Week 5–6 | 5 + 6 | Medieval Universities + Byzantium | 20–30 persons, 45–60 events |
| Week 7–8 | 7 + 8 | Renaissance Italy + Low Countries | 30–40 persons, 70–90 events |
| Week 9–10 | 9 + 10 | Early Modern Central Europe + England | 40–50 persons, 90–120 events |
| Week 11–12 | 11 + 12 | Early Modern France + Spain | 25–35 persons, 55–75 events |
| Week 13 | 13 | 18th Century Chemical Revolution | 25–30 persons, 50–70 events |

**Total project time:** 13–16 weeks  
**Estimated final state:**
- 150–180 persons (currently 81 → +70–100)
- 80–100 texts (currently 42 → +38–58)
- 50–60 concepts (currently 30 → +20–30)
- 600–650 timeline events (currently 582 → +20–70)

---

## KEY REFERENCE MATERIALS

**Always available for consultation:**

- **SCHEMA.json** — Valid enum values for era_slug, role, review_status, confidence (check before entering any field)
- **CONCEPTUAL_FRAMEWORK.md** — Historiographical principles (Actor/Analyst distinction, Provenance, Material Culture, Transmission)
- **STANDARD_TIMELINE_EVENTS.md** — Event format (100–250 words, required fields)
- **STANDARD_PERSON_BIOGRAPHIES.md** — Person format (1,200+ words, required sections)
- **STANDARD_TEXT_DESCRIPTIONS.md** — Text format (1,000+ words, transmission history required)
- **STANDARD_CONCEPT_DEFINITIONS.md** — Concept format (1,500+ words, Actor/Analyst explicit)
- **PHASESTATUS.md** — Current phase status and success criteria

---

## QUALITY GATES

Before any entity enters the database, verify:

- [ ] **Provenance:** Source file and modern scholar cited
- [ ] **Word count:** In range per content type
- [ ] **Entity links:** All [LINK:slug] references exist in SCHEMA.json
- [ ] **No markdown artifacts:** No stray `#`, `*`, `**`, `[]`, `{}` in prose
- [ ] **Bibliography:** DGWE format, minimum item count (8 for persons/concepts, 6 for texts)
- [ ] **Historiography:** Actor/Analyst distinction explicit (persons/concepts); scholarly debate named
- [ ] **Confidence & Review:** Flags set (HIGH/MEDIUM/LOW; DRAFT/READY_FOR_REVIEW/REVIEWED)

---

## PROJECT INVARIANTS (MUST MAINTAIN)

From CLAUDE.md:

1. **Provenance on every claim.** Every substantive assertion traces to a named scholar or primary source.
2. **No endorsement of transmutation.** Report historical beliefs accurately; never imply they were true.
3. **Actor/Analyst distinction.** Historical actors used *their* vocabulary; scholars apply *analytical* categories.
4. **All entity links must exist.** Every [LINK:slug] must reference a slug in the database.
5. **Enum values are locked.** No new values without adding to schema first (see SCHEMA.json).

---

## TROUBLESHOOTING

**Q: What if a markdown file is about a broad topic rather than a specific person/text/event?**

A: Decompose it. Extract specific persons, texts, events, concepts mentioned. Don't create a "topic" entry. Every database entry is about a discrete, named entity.

**Q: How do I know if a person already exists?**

A: Check `entity_extraction_index.xlsx`, Status column. "EXISTS" = already in DB; "NEW" = needs enrichment.

**Q: What if dates/attributions conflict across sources?**

A: Note in enriched text. Mark confidence as MEDIUM. "Scholars disagree on dating; Smith argues [date], Newman argues [date]." Trust primary source where available; cite modern scholar's interpretation.

**Q: How do I handle pseudonymous or misattributed texts?**

A: Declare in Text entry. "Attributed to [Person] by tradition; modern scholars argue [Author X] wrote this (see [Citation])."

**Q: Can I skip a batch or do them out of order?**

A: Yes, if necessary. But chronological order (Late Antique → Early Modern → 18th c.) helps earlier periods provide context for later ones. Prioritize by your available expertise.

---

## WHAT HAPPENS AFTER EACH BATCH IS SUBMITTED

1. **Main session validates** staging JSON
2. **Python script inserts** into database (idempotent)
3. **Site rebuilds** with new content
4. **Map updates** with geo-pinned events
5. **GitHub Pages deploys** automatically
6. You move to next batch

---

## SUCCESS: PHASE 3A COMPLETE

When all 13 batches are enriched and inserted:

✅ 4,446 markdown files processed  
✅ 150–180 persons with full biographies  
✅ 80–100 texts with scholarly analyses  
✅ 50–60 concepts with encyclopedia-length definitions  
✅ 600–650 timeline events with scholarly grounding  
✅ 100% entity link validation (zero broken links)  
✅ Database complete; GitHub Pages live  
✅ Interactive map shows all geotagged events  
✅ Scholarly encyclopedia-quality site for history of alchemy & chemistry

---

## 📖 Next Step

**Right now:**

1. Open `staging/WORKING_NOTES_TEMPLATE.md` to understand the structure
2. Run: `python scripts/read_markdown_batch.py 100` (pilot test)
3. Open `staging/entity_extraction_index.xlsx`
4. Read: `ENRICHMENT_WORKFLOW.md` (entire file)
5. Start enriching the first new persons identified

**Questions?**

- Refer to: `ENRICHMENT_WORKFLOW.md` (day-to-day questions)
- Refer to: `INGESTION_EXECUTION_PLAN.md` (pacing, batching, tracking)
- Refer to: `MARKDOWN_INGESTION_STRATEGY.md` (system architecture)
- Refer to: `CONCEPTUAL_FRAMEWORK.md` (historiography)
- Refer to: `STANDARD_*.md` (format specifications)

---

**The system is complete. You can now systematically transform 4,446 scholarly sources into an authoritative interactive historical database.**

*Good luck. 🧪*
