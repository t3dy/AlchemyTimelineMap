# Ingestion Execution Plan — ALCHEMYTIMELINEMAP

**Purpose:** Day-to-day execution guide for processing 4,446 markdown files from `e:\pdf\alchemy`.

**Updated:** 2026-06-14  
**Status:** Ready for Phase 3A (Markdown Enrichment)

---

## OVERVIEW: THREE-STEP WORKFLOW

```
STEP 1: Read & Extract
[Run Python scripts on markdown batch]
↓ Creates: Working notes + Entity Index

STEP 2: Enrich
[Write full descriptions, biographies, concepts]
↓ Creates: Staging JSON files with complete entries

STEP 3: Validate & Insert
[Main session validates, inserts into database]
↓ Updates: timeline_events, persons, texts, concepts tables
```

---

## STEP 1: READ & EXTRACT (Batch 1–30)

### Running the Batch Reader

**Command:**
```bash
cd C:\Dev\ALCHEMYTIMELINEMAP
python scripts/read_markdown_batch.py 100
```

**Parameters:**
- `100` = Process first 100 markdown files as a pilot test
- Omit parameter to process entire directory (4,446 files)

**Output:**
- `staging/working_notes/note_*.md` (one per source)
- `staging/processed_files.json` (tracking log)

**Expected runtime:** ~2–5 minutes per 100 files

### Generate Entity Index

**Command:**
```bash
python scripts/entity_extraction_index.py
```

**Output:**
- `staging/entity_extraction_index.xlsx`
  - One row per unique entity (person, text, location, concept)
  - Filter by Status=NEW to prioritize new entities
  - Sort by Entity Type to batch by content

**What to do next:**
1. Open `staging/entity_extraction_index.xlsx`
2. Filter Status column to "NEW"
3. Count new persons, texts, concepts
4. Organize by region/era for enrichment batches

---

## STEP 2: ORGANIZE INTO BATCHES

### Recommended Batch Structure

Organize markdown files (and their working notes) by **era/region**:

| Batch # | Era/Region | Time Period | Expected Entities | Notes |
|---|---|---|---|---|
| **1** | Late Antique Egypt & Syria | 1st–4th centuries | 10–20 persons, 5–10 texts, 20–30 events | Foundation of alchemy tradition |
| **2** | Early Islamic Baghdad & Persia | 8th–10th centuries | 15–30 persons, 10–20 texts, 30–50 events | Golden age of alchemy; Jabir, Al-Razi |
| **3** | Medieval Islam: Spain & Iberia | 9th–15th centuries | 10–20 persons, 8–15 texts, 25–40 events | Al-Andalus transmission; Gerard of Cremona |
| **4** | Medieval Latin Europe: Monasteries | 6th–12th centuries | 8–15 persons, 5–10 texts, 15–25 events | Monastic alchemy; Hildegard, Albertus Magnus |
| **5** | Medieval Latin Europe: Universities | 12th–14th centuries | 15–25 persons, 10–15 texts, 25–40 events | University scholasticism; Roger Bacon |
| **6** | Medieval Byzantium | 6th–15th centuries | 5–10 persons, 3–8 texts, 10–20 events | Greek alchemy preservation |
| **7** | Renaissance Italy: Florence & Venice | 14th–16th centuries | 15–25 persons, 12–20 texts, 30–50 events | Hermetic revival; Ficino, Pico |
| **8** | Renaissance Low Countries | 15th–16th centuries | 10–15 persons, 8–12 texts, 20–35 events | Printing revolution; alchemical texts |
| **9** | Early Modern Central Europe | 16th–17th centuries | 20–30 persons, 15–25 texts, 40–60 events | Paracelsus circle; Rudolf II's Prague |
| **10** | Early Modern England | 16th–17th centuries | 15–25 persons, 10–20 texts, 30–50 events | Newton, Boyle, Ashmole |
| **11** | Early Modern France | 16th–17th centuries | 10–20 persons, 8–15 texts, 25–40 events | Institutional chemistry; pharmacy |
| **12** | Early Modern Spain & Portugal | 16th–18th centuries | 10–15 persons, 8–12 texts, 20–30 events | Expansion period; colonial alchemy |
| **13** | 18th Century Chemical Revolution | 18th century | 20–30 persons, 15–25 texts, 40–60 events | Lavoisier, Berzelius, transition to chemistry |

---

## EXECUTING A SINGLE BATCH

### Batch Template: [ERA/REGION]

**Timeline:** 3–5 days per batch (reading + enrichment)

### Phase A: Preparation (0.5 day)

**Task A1: Identify source files**
```bash
# Find markdown files matching era/region pattern
Get-ChildItem "e:\pdf\alchemy" -Recurse -Filter "*[keyword]*" | Select-Object Name
```

**Task A2: Create enrichment plan**

Write `staging/BATCH_[name]_plan.md`:

```markdown
# Enrichment Plan: [Era/Region]

**Batch ID:** [BATCH_001]
**Era/Region:** [Name]
**Time Period:** [Date range]
**Source files:** [Count and list]
**Expected entities:** [X persons, Y texts, Z concepts, W events]

## Source Files Included

- source_file_1.md
- source_file_2.md
- [etc.]

## Historiographical Context

[2–3 sentences on why this era/region matters to alchemy/chemistry history]

## Success Criteria

- [ ] All working notes created (staging/working_notes/)
- [ ] All persons described: 1,200+ words each
- [ ] All texts described: 1,000+ words each
- [ ] All concepts defined: 1,500+ words each
- [ ] All events written: 100–250 words each
- [ ] Validation passes (0 broken links, 0 markdown artifacts)
- [ ] Staging JSON ready for main session

## Batch Metadata

**Created:** [ISO date]
**Enriched by:** [Name/Agent]
**Status:** Planning / In Progress / Complete
```

### Phase B: Reading (1 day)

**Task B1: Run markdown batch reader**

```bash
python scripts/read_markdown_batch.py
# Process all markdown files for this batch
```

**Task B2: Create working notes**

Output: `staging/working_notes/note_*.md` for each source file

**Task B3: Review working notes quality**

- [ ] All persons identified with roles
- [ ] All locations identified with periods
- [ ] All concepts identified with definitions
- [ ] Event candidates listed with dates

### Phase C: Enrichment (3–4 days)

**Task C1: Create person biographies**

For each new person identified:
- Write 1,200–2,200 word biography
- Include 8+ bibliography items
- Target HIGH confidence where possible

**Task C2: Create text descriptions**

For each new text identified:
- Write 1,000–1,800 word analysis
- Include transmission history
- Include 6+ bibliography items

**Task C3: Create concept definitions**

For each new concept identified:
- Write 1,500–2,500 word definition
- Declare ACTOR_TERM vs. ANALYST_TERM explicitly
- Include 8+ bibliography items
- Link to 3+ related concepts

**Task C4: Create timeline events**

For each event candidate:
- Write 100–250 word description
- Include scholarly grounding (named scholar + citation)
- Link to persons, texts, concepts
- Validate date, location, era

### Phase D: Validation (0.5 day)

**Task D1: Run validation checklist**

See ENRICHMENT_WORKFLOW.md § 6.2

**Task D2: Prepare staging JSON**

Create: `staging/BATCH_[name]_enriched_entities.json`

Files included:
- `staging/BATCH_[name]_persons.json` (if new persons created)
- `staging/BATCH_[name]_texts.json` (if new texts created)
- `staging/BATCH_[name]_concepts.json` (if new concepts created)
- `staging/BATCH_[name]_events.json` (all new events)

**Task D3: Handoff to main session**

Notify: Batch [NAME] ready for validation and database insertion.

---

## MONITORING PROGRESS

### Weekly Metrics

Track in `staging/PROGRESS.md`:

```markdown
# Ingestion Progress

**As of:** [ISO date]

## Batches Completed

| Batch # | Name | Working Notes | Persons | Texts | Concepts | Events | Status |
|---|---|---|---|---|---|---|---|
| 1 | Late Antique Egypt | 45 | 18 | 8 | 12 | 35 | ✅ COMPLETE |
| 2 | Early Islamic Baghdad | 52 | 22 | 15 | 18 | 48 | 🔄 IN PROGRESS |

## Totals

| Metric | Target | Progress | % |
|---|---|---|---|
| Markdown files processed | 4,446 | 850 | 19% |
| Persons created | 150 | 40 | 27% |
| Texts created | 80 | 23 | 29% |
| Concepts created | 50 | 30 | 60% |
| Events created | 600 | 83 | 14% |

## Velocity

- Files per day: 85
- Persons per day: 4.2
- Events per day: 8.3
- Estimated completion: [ISO date at current pace]

## Blockers

- [Any challenges, bottlenecks, or questions]

## Next Batch

**Starting:** [Batch name]
**ETA:** [ISO date]
```

---

## QUICK START: RUNNING BATCH 1 (Pilot)

### Day 1: Extract & Plan

```bash
# 1. Run batch reader on pilot sample (first 100 files)
cd C:\Dev\ALCHEMYTIMELINEMAP
python scripts/read_markdown_batch.py 100

# 2. Generate entity index
python scripts/entity_extraction_index.py

# 3. Open entity index and filter for this batch
# staging/entity_extraction_index.xlsx → Filter Status=NEW

# 4. Create enrichment plan
# Copy template: staging/BATCH_001_plan.md
# Customize with entity counts
```

### Days 2–4: Enrich

**For each new person:**
```markdown
Read: STANDARD_PERSON_BIOGRAPHIES.md (format)
Read: CONCEPTUAL_FRAMEWORK.md (historiography)
Write: 1,200–2,200 word biography with 8+ references
```

**For each new text:**
```markdown
Read: STANDARD_TEXT_DESCRIPTIONS.md
Write: 1,000–1,800 word analysis with 6+ references
```

**For each new concept:**
```markdown
Read: STANDARD_CONCEPT_DEFINITIONS.md
Write: 1,500–2,500 word definition with Actor/Analyst distinction
```

**For each event candidate:**
```markdown
Read: STANDARD_TIMELINE_EVENTS.md
Write: 100–250 word description with scholarly grounding
```

### Day 5: Validate & Submit

```bash
# 1. Run validation checklist (ENRICHMENT_WORKFLOW.md § 6.2)
# 2. Prepare staging JSON files
# 3. Run: python scripts/validate_staging_json.py
# 4. Commit to staging/ directory
# 5. Notify main session: "Batch 1 ready for insertion"
```

---

## BATCH EXECUTION SCHEDULE

**Suggested pacing:**

| Week | Batch | Phase |
|---|---|---|
| Week 1 | 1 (Late Antique) | Pilot: extract + enrich + validate |
| Week 2 | 2 (Early Islamic Baghdad) | Extract + enrich |
| Week 3 | 2 (continued) + 3 (Medieval Islam Spain) | Parallel: finish batch 2, start batch 3 |
| Week 4 | 3 + 4 (Medieval Monasteries) | Parallel enrichment |
| Week 5–12 | Remaining batches | 2 batches per week |
| Week 13 | Cleanup + final validation | Ensure 100% coverage |

**Total estimated time:** 12–16 weeks at this pace

---

## TOOLS & REFERENCES

### Key Files

- **MARKDOWN_INGESTION_STRATEGY.md** — Overall architecture (read once)
- **ENRICHMENT_WORKFLOW.md** — Day-to-day enrichment tasks (reference constantly)
- **STANDARD_TIMELINE_EVENTS.md** — Event format (keep open while writing)
- **STANDARD_PERSON_BIOGRAPHIES.md** — Person format
- **STANDARD_TEXT_DESCRIPTIONS.md** — Text format
- **STANDARD_CONCEPT_DEFINITIONS.md** — Concept format
- **CONCEPTUAL_FRAMEWORK.md** — Historiographical principles
- **SCHEMA.json** — Valid enum values and entity definitions

### Python Scripts

- `scripts/read_markdown_batch.py` — Extract entities from markdown (5–10 min)
- `scripts/entity_extraction_index.py` — Create XLSX entity index (2–3 min)
- `scripts/validate_staging_json.py` — Validate JSON before insertion (1 min)

### Workflow Documents

- `staging/BATCH_[name]_plan.md` — Per-batch enrichment plan
- `staging/entity_extraction_index.xlsx` — Live index of all entities
- `staging/PROGRESS.md` — Weekly progress tracking
- `staging/BATCH_STATUS.md` — Status of completed batches

---

## TROUBLESHOOTING

### Q: How do I know if a person already exists in the database?

**A:** Check `entity_extraction_index.xlsx`, Status column. "EXISTS" = already in DB. "NEW" = needs to be created.

### Q: What if I encounter conflicting information about a date or event?

**A:** 
1. Note the disagreement in the working note
2. Mark confidence as MEDIUM
3. In enriched text, note the dispute: "Scholars disagree on dating; Smith argues [date], Newman argues [date]"
4. Trust the primary source date if available; cite modern scholar's interpretation

### Q: How do I handle pseudonymous or misattributed texts?

**A:** Declare the attribution issue in the Text entry:
- Actual author unknown; attributed to [Person] by tradition
- Modern scholars argue [Author X] wrote this; see [Citation]

### Q: What if a markdown file is about a topic (e.g., "alchemy in 12th-century Spain") rather than a specific person/text/event?

**A:** Extract the specific facts:
- Named persons mentioned? → Create person entries
- Specific texts referenced? → Create text entries
- Specific events/discoveries? → Create event entries
- General concepts? → Create concept entries

Don't create a "topic" entry; decompose it into facts.

### Q: How do I prioritize which batches to do first?

**A:** 
1. **Historical importance:** Late Antique foundations → Islamic Golden Age → Medieval → Renaissance → Early Modern → Chemical Revolution
2. **Source density:** Batches with more markdown files may have more entities (use PROGRESS.md)
3. **Chronological ordering:** Earlier periods provide context for later periods

---

## SUCCESS CRITERIA (FULL INGESTION)

When all 4,446 markdown files have been processed:

- [ ] 4,446 working notes created in `staging/working_notes/`
- [ ] Entity extraction index complete (XLSX with all unique entities)
- [ ] 150+ new persons with biographies (1,200+ words each)
- [ ] 80+ new texts with analyses (1,000+ words each)
- [ ] 50+ new concepts with definitions (1,500+ words each)
- [ ] 600+ timeline events with descriptions (100–250 words each)
- [ ] 100% scholarly grounding on events (every event cites a modern scholar)
- [ ] Zero broken entity links (`[LINK:slug]` validation passes)
- [ ] All bibliographies in DGWE format
- [ ] All staging JSON files validated
- [ ] Database updated with all new entries
- [ ] GitHub Pages site regenerated with new content
- [ ] Map updated with all new events (geo-pinned)

---

*For detailed reference material, see ENRICHMENT_WORKFLOW.md. For questions about standards, see STANDARD_*.md and CONCEPTUAL_FRAMEWORK.md.*
