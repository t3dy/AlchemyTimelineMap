# ALCHEMYTIMELINEMAP — Project System Complete

**Date Created:** 2026-05-22
**Status:** Phase 0 Complete — System architecture, documentation, and template scripts ready for implementation

---

## What Has Been Created

### System Files (Canonical Vision & Standards)

✅ **PROMPTS.md** (1,800 words)
- Canonical project vision
- Three constituencies (scholars, students, independent researchers)
- Historiographical framework (Actor/Analyst distinction, medieval continuity, operational chemistry)
- Content standards by type (timeline events, persons, texts, concepts)
- Agent operating rules and vocabulary lock

✅ **STYLEGUIDE.md** (1,200 words)
- Comprehensive prose standards (no markdown, no bullets, no hashtags)
- Required HTML structure for bio_html, analysis_html, definition_long
- Voice and register requirements
- Italics policy
- Bibliography format (DGWE model)
- Minimum word count specifications (timeline: 100–250 | persons: 1,200–2,200 | texts: 1,000–1,800 | concepts: 1,500–2,500)
- Complete checklist for validating entries

✅ **CLAUDE.md** (800 words)
- Task routing guide
- Key files reference table
- Architecture at a glance
- Data ontology summary (8 tables)
- Data flow diagram
- Python conventions and vocabulary lock
- Key scholarly authorities

✅ **PHASESTATUS.md** (500 words)
- Current phase (Phase 0 complete)
- Remaining work (Python scripts, seed data, timeline events skeleton)
- Planned phases (1–4)
- Success criteria for full project

### Documentation (Technical Architecture)

✅ **docs/SYSTEM.md** (900 words)
- Core technology stack
- Complete data flow diagram
- Design principles (SQLite as source of truth, no frameworks, idempotent ingestion, provenance on every datum)
- Directory structure
- Typical workflow
- Database schema summary
- Deployment checklist

✅ **docs/ONTOLOGY.md** (1,400 words)
- Complete database schema for all 8 tables
- Field-by-field specification with CHECK constraints
- Enum values (vocabulary lock)
- Indexing strategy
- Expected row counts when complete (500 events, 100+ persons, 50+ texts, 30+ concepts)
- SQL examples

✅ **docs/PIPELINE.md** (900 words)
- Script execution order (6 main scripts)
- Phase 1: Initialize database schema
- Phase 2: Load seed data
- Phase 3: Load timeline event skeleton
- Phase 4: Enrich timeline events via agent swarm
- Phase 5: Static site generation
- Phase 6: Deploy to GitHub Pages
- Standard full pipeline (one-shot command sequence)
- Idempotency and safe re-running
- Batch processing schedule

✅ **docs/CONTEXT_ENGINEERING.md** (1,200 words)
- Problem: 500 events × 3–5 related entities = context explosion
- Solution: Batch + pre-query pattern
- 5-step workflow for efficient agent enrichment
- Token efficiency analysis
- Example: Pilot batch (Medieval Islamic, 20 events, 35–50 entities)
- Implementation checklist

✅ **README.md** (500 words)
- Project overview and quick start guide
- Project structure diagram
- Technology stack summary
- Core architecture diagram
- Content model (timeline events, persons, texts, concepts)
- Historiographical framework
- Key authorities
- Implementation pipeline (Phases 0–4)
- Next steps

### Implementation Templates

✅ **scripts/init_db.py** (250 lines)
- Complete database schema creation script
- All 8 tables with proper foreign keys
- All CHECK constraints for enum values
- Index creation
- Idempotent pattern (CREATE TABLE IF NOT EXISTS)
- Fully documented

### Project Structure

✅ **Folder structure created:**
```
C:\Dev\ALCHEMYTIMELINEMAP/
├── PROMPTS.md, STYLEGUIDE.md, CLAUDE.md, PHASESTATUS.md, README.md, PROJECT_SUMMARY.md
├── docs/ (SYSTEM.md, ONTOLOGY.md, PIPELINE.md, CONTEXT_ENGINEERING.md)
├── db/ (alchemy_timeline.db — to be created by init_db.py)
├── data/ (seed_data.json, timeline_events_skeleton.json — to be created)
├── scripts/ (init_db.py — template provided; others to be implemented)
├── staging/ (for agent output)
└── site/ (generated static HTML — will be created by build_site.py)
```

---

## What Remains to Be Implemented

### Immediate (Phase 0b–0c)

1. **Complete Python scripts** (5 remaining, use init_db.py as template):
   - `scripts/load_seed_data.py` — Load seed JSON into DB (idempotent)
   - `scripts/load_timeline_skeleton.py` — Load 500 event stubs (idempotent)
   - `scripts/pre_query_batch_context.py` — Pre-query entity context for agent batches
   - `scripts/enrich_timeline_events.py` — Load agent output, validate, convert markup, load to DB
   - `scripts/build_site.py` — Main deploy: SQLite → static HTML/JSON (most complex)

2. **Create seed_data.json**:
   - ~100 alchemists/chemists/scholars (e.g., Jabir ibn Hayyan, Al-Razi, Zosimos, Roger Bacon, etc.)
   - ~50 key texts (e.g., Summa Perfectionis, Emerald Tablet, Picatrix, etc.)
   - ~30 concepts (e.g., Distillation, Calcination, Transmutation, Quintessence, etc.)
   - ~20 locations with coordinates (Baghdad, Cairo, Bologna, Florence, Antwerp, etc.)
   - All entries with provenance metadata (source_method, review_status, confidence)

3. **Create timeline_events_skeleton.json**:
   - 500 event stubs with:
     - date_label, date_start_year, date_end_year
     - location_slug
     - persons_involved (JSON array of slugs)
     - texts_involved (JSON array of slugs)
     - concepts_involved (JSON array of slugs)
   - No descriptions yet (will be filled by agents)

4. **Test the pipeline**:
   - Run init_db.py → verify schema created
   - Run load_seed_data.py → verify entities loaded
   - Run load_timeline_skeleton.py → verify 500 events loaded
   - Spot-check with sqlite3 CLI

### Phase 1: Event Enrichment via Agent Swarm

- Partition 500 events into ~25 batches (era + region, ~20 events per batch)
- For each batch:
  - Main session: pre-query entity context, write `staging/batch_*.json`
  - Agent Type A (Timeline Event Enricher): read batch, write `staging/enriched_events_*.json`
  - Main session: validate, load into DB

**Expected result:** All 500 timeline events with 100–250 word descriptions

### Phase 2: Enrich Persons and Texts

- Ensure all persons at minimum 1,200 words
- Ensure all texts at minimum 1,000 words
- Ensure all Literature sections present and properly formatted

### Phase 3: Enrich Concepts

- Ensure all concepts at minimum 1,500 words
- Ensure Actor/Analyst distinction explicit throughout
- Ensure Literature sections present with 8–15 items

### Phase 4: Static Site Generation and Deployment

- Implement build_site.py to generate:
  - index.html, timeline.html, map.html
  - 100+ biography pages (persons/)
  - 50+ text pages (texts/)
  - 30+ concept pages (concepts/)
  - data.json, timeline.json, graph.json (for JavaScript)
- Create CSS and vanilla JavaScript for timeline, map, and graph UI
- Deploy to GitHub Pages

---

## Key Design Decisions Baked In

1. **Timeline-First Architecture**: Unlike EmeraldTablet (dictionary-first), ALCHEMYTIMELINEMAP is timeline-first. Events are the primary content unit.

2. **Batch Processing for 500 Events**: With context engineering (docs/CONTEXT_ENGINEERING.md), agents work on 20–30 event batches with pre-loaded entity context, avoiding token explosion.

3. **Provenance on Every Datum**: Every row tracks source_method, review_status, confidence for full audit trail.

4. **Idempotent Pipeline**: All scripts use INSERT OR IGNORE / UPDATE OR IGNORE, safe to re-run multiple times.

5. **Slugs, Never IDs**: All cross-references use human-readable slugs (e.g., "jabir-ibn-hayyan") instead of database row IDs.

6. **Staging Files for Agent Output**: Agents write to staging/, main session validates and loads. Full audit trail, ability to revise.

7. **Vanilla HTML/CSS/JS**: No frameworks, no build tools, no npm. Direct CDN for Leaflet.js and D3.js only.

8. **Historiographical Rigor**: Built on Hanegraaff methodology (Actor/Analyst distinction), William Newman (practical chemistry), and medieval continuity principles.

---

## Expected Final State (When Complete)

| Component | Target | Status |
|-----------|--------|--------|
| Timeline events | 500 | Planned |
| Persons | 100–120 | Planned |
| Texts | 50–60 | Planned |
| Concepts | 30–40 | Planned |
| Locations | 20–25 | Planned |
| HTML biography pages | 100+ | Planned |
| HTML text pages | 50+ | Planned |
| HTML concept pages | 30+ | Planned |
| Interactive map | 1 | Planned |
| Interactive timeline | 1 | Planned |
| Relationship graph | 1 | Planned |
| GitHub Pages site | Live | Planned |

---

## Critical Files to Read Before Starting Implementation

**In order:**
1. `PROMPTS.md` — Vision and historiographical framework
2. `STYLEGUIDE.md` — Content standards and word counts
3. `docs/CONTEXT_ENGINEERING.md` — How to handle 500 events efficiently
4. `docs/ONTOLOGY.md` — Database schema details
5. `docs/PIPELINE.md` — Script execution order

---

## How to Use This System

**For AI agents:**
- Read PROMPTS.md and STYLEGUIDE.md before writing any content
- Use CONTEXT_ENGINEERING.md as the template for timeline event enrichment
- Output to staging/ as JSON; wrap entity names in `[LINK:slug]` markup

**For main session:**
- Use PIPELINE.md to run scripts in order
- Use ONTOLOGY.md to understand database structure
- Use SYSTEM.md to understand overall architecture

**For deployment:**
- Follow PIPELINE.md Phases 1–5 sequentially
- Use PHASESTATUS.md to track progress
- Consult CLAUDE.md for any routing questions

---

## Next Immediate Action

1. **Implement remaining Python scripts** (use init_db.py as template for pattern)
2. **Create seed_data.json** (bootstrap initial entities)
3. **Create timeline_events_skeleton.json** (500 event stubs)
4. **Test the pipeline** (init → load → verify)
5. **Launch Agent Swarm Phase 1** (enrich all 500 events via batch pattern)

---

**Created by:** Claude Code
**Date:** 2026-05-22
**Project Status:** Phase 0 (System Architecture) — ✅ COMPLETE
**Next Phase:** Phase 1 (Agent Swarm Event Enrichment) — Ready to begin
