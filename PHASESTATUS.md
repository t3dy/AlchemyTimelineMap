# ALCHEMYTIMELINEMAP Phase Status

**Updated:** 2026-05-22
**Current Phase:** PHASE 0 — SYSTEM ARCHITECTURE + SEED DATA

---

## What Is PLANNED (Phase 0)

| Task | Status | Notes |
|------|--------|-------|
| Create PROMPTS.md | ✅ COMPLETE | Canonical vision, historiographical framework, agent operating rules |
| Create STYLEGUIDE.md | ✅ COMPLETE | Content standards for all prose fields (timeline events, persons, texts, concepts) |
| Create CLAUDE.md | ✅ COMPLETE | Routing guide, key files, vocabulary lock, conventions |
| Create SYSTEM.md | ✅ COMPLETE | Architecture overview, data flow, design principles |
| Create ONTOLOGY.md | ✅ COMPLETE | Database schema (8 tables, CHECK constraints, enums) |
| Create PIPELINE.md | ✅ COMPLETE | Script execution order (6 main scripts) |
| Create CONTEXT_ENGINEERING.md | ✅ COMPLETE | How to efficiently query for 500 timeline events (batch pattern) |
| Create project folder structure | ✅ COMPLETE | db/, scripts/, docs/, data/, staging/, site/, assets/ |
| Design Python scripts (stub templates) | ⏳ NEXT | init_db.py, load_seed_data.py, load_timeline_skeleton.py, etc. |
| Create seed_data.json (initial entities) | ⏳ NEXT | ~100 persons, ~50 texts, ~30 concepts, ~20 locations |
| Create timeline_events_skeleton.json | ⏳ NEXT | 500 event stubs (date, location, involved entities) |

---

## Remaining Work

### Phase 0b (Immediate): Python Script Stubs

Create the following Python scripts with idempotent patterns:

1. **`scripts/init_db.py`** — Database schema creation
2. **`scripts/load_seed_data.py`** — Ingest seed JSON
3. **`scripts/load_timeline_skeleton.py`** — Ingest 500 event stubs
4. **`scripts/pre_query_batch_context.py`** — Pre-query entity context for agent batches
5. **`scripts/enrich_timeline_events.py`** — Load agent output, validate, convert markup, update DB
6. **`scripts/build_site.py`** — Main deploy: SQLite → static HTML/JSON

All scripts must:
- Use stdlib only (sqlite3, json, re, pathlib)
- Be fully idempotent (INSERT OR IGNORE, CREATE TABLE IF NOT EXISTS)
- Include docstrings and validation
- Output to standard locations (db/, staging/, site/)

### Phase 0c: Seed Data Creation

Create:
- **`data/seed_data.json`** — Initial 100 persons, 50 texts, 30 concepts, 20 locations (bootstrapping the database)
- **`data/timeline_events_skeleton.json`** — 500 event stubs with:
  - date_label, date_start_year, date_end_year
  - location_slug
  - persons_involved, texts_involved, concepts_involved (as JSON arrays of slugs)
  - No descriptions yet (will be filled by agent swarm)

**Key principle:** Seed data should include the most important/high-confidence entities so that all 500 events can reference existing persons, texts, concepts (no dangling references).

**Suggested bootstrap sources:**
- Use EmeraldTablet database (query persons/texts/concepts, adapt to alchemy domain)
- Use Claudiens database (query persons from Maier scholarship, adapt)
- Manually define ~15 canonical alchemists (Jabir, Al-Razi, Zosimos, etc.)
- Manually define ~10 canonical texts (Summa Perfectionis, Emerald Tablet, etc.)
- Define major cities/regions with coordinates (Baghdad, Cairo, Iberia, Italy, etc.)

---

### Phase 1: Agent Swarm I — Event Enrichment

**Goal:** Enrich all 500 timeline events with full descriptions (100–250 words each).

**Approach:** 
- Partition 500 events into ~25 batches (era + region)
- For each batch:
  - Main session: pre-query entity context, write `staging/batch_*.json`
  - Agent Type A (Timeline Event Enricher): read batch, write `staging/enriched_events_*.json`
  - Main session: validate, load into DB

**Success criteria:**
- [ ] All 500 events have descriptions (100–250 words)
- [ ] All descriptions link to at least 1 person, text, or concept
- [ ] All descriptions declare historiographical significance (final sentence)
- [ ] All entity links resolve to existing persons/texts/concepts
- [ ] All event dates and locations are valid

**Estimated time:** 8–10 hours (25 batches × 5 minutes per batch + validation)

---

### Phase 2: Agent Swarm II — Persons + Texts Enrichment

**Goal:** Ensure all persons and texts are at minimum word counts.

**Person biographies (bio_html):**
- Minimum: 1,200–2,200 words
- Required sections: opening para + 2–4 `<h2>` sections + Literature

**Text analyses (analysis_html):**
- Minimum: 1,000–1,800 words
- Required sections: opening para + Content/Theory + Transmission + Modern Scholarship + Literature

**Approach:**
- Query persons/texts with word counts < minimum
- Batch by era/role for narrative coherence
- Agent Type B (Biography Enricher): receive pre-queried context (texts they wrote, events involving them), write full biographies
- Validate and load

**Success criteria:**
- [ ] All 100+ persons at 1,200+ words with Literature section
- [ ] All 50+ texts at 1,000+ words with Literature section
- [ ] All biographies cite ≥2 named scholars
- [ ] All Literature sections have 5–12 items in DGWE format

---

### Phase 3: Concept Definitions

**Goal:** Ensure all concepts have encyclopedia-length definitions.

**Concept definitions (definition_long):**
- Minimum: 1,500–2,500 words
- Required sections: opening + Historical Usage + Scholarly Significance + (Transmission) + Related Concepts + Literature

**Approach:**
- Agents write encyclopedia-length entries following STYLEGUIDE.md
- Batch by category (ACTOR_TERM vs. ANALYST_TERM, or by chemical operation type)

**Success criteria:**
- [ ] All 30+ concepts at 1,500–2,500 words
- [ ] All declare Actor/Analyst distinction explicitly
- [ ] All cite ≥3 named scholars in Scholarly Significance
- [ ] All Literature sections have 8–15 items
- [ ] All Related Concepts sections link to 3–5 other concepts

---

### Phase 4: Static Site Generation + Deployment

**Goal:** Generate all static HTML pages and deploy to GitHub Pages.

**Tasks:**
- [ ] Implement `scripts/build_site.py` to generate:
  - `index.html` (home)
  - `timeline.html` (timeline viewer with filtering)
  - `map.html` (Leaflet.js map with geo-pins)
  - `persons/[slug].html` (100+ biography pages)
  - `texts/[slug].html` (50+ text pages)
  - `concepts/[slug].html` (30+ concept pages)
  - `data/data.json` (all entities + relationships)
  - `data/timeline.json` (events + coordinates)
  - `data/graph.json` (D3.js graph)
- [ ] Create CSS and vanilla JavaScript for timeline, map, and graph UI
- [ ] Test all links and relationships
- [ ] Deploy to GitHub Pages (push site/ → docs/)

**Success criteria:**
- [ ] All 500 events appear on timeline with correct dates
- [ ] All events appear on map with correct coordinates
- [ ] All entity pages render without errors
- [ ] All internal links are valid
- [ ] GitHub Pages site is live and responsive

---

## Expected Database Row Counts (When Complete)

| Table | Target | Status |
|-------|--------|--------|
| timeline_events | 500 | ⏳ Planned |
| persons | 100–120 | ⏳ Planned |
| texts | 50–60 | ⏳ Planned |
| concepts | 30–40 | ⏳ Planned |
| locations | 20–25 | ⏳ Planned |
| person_event_refs | 200–300 | ⏳ Calculated |
| text_event_refs | 150–200 | ⏳ Calculated |
| concept_event_refs | 300–400 | ⏳ Calculated |

---

## Key Files Status

| File | Purpose | Status |
|------|---------|--------|
| PROMPTS.md | Canonical vision | ✅ Complete |
| STYLEGUIDE.md | Content standards | ✅ Complete |
| CLAUDE.md | Routing guide | ✅ Complete |
| PHASESTATUS.md | This file | ✅ Complete |
| docs/SYSTEM.md | Architecture | ✅ Complete |
| docs/ONTOLOGY.md | Database schema | ✅ Complete |
| docs/PIPELINE.md | Script execution order | ✅ Complete |
| docs/CONTEXT_ENGINEERING.md | 500-event batch strategy | ✅ Complete |
| data/seed_data.json | Initial entities | ⏳ Pending |
| data/timeline_events_skeleton.json | 500 event stubs | ⏳ Pending |
| scripts/*.py | All Python scripts | ⏳ Pending |
| site/ | Generated static HTML | ⏳ Pending |

---

## Next Immediate Actions

1. **Create Python script stubs** (init_db.py, load_seed_data.py, etc.)
   - Copy template patterns from EmeraldTablet if available
   - Adapt to ALCHEMYTIMELINEMAP schema
   - Test each script in isolation

2. **Create seed_data.json**
   - Bootstrap ~100 alchemists/chemists/scholars
   - Bootstrap ~50 key texts
   - Bootstrap ~30 concepts
   - Bootstrap ~20 cities/regions with coordinates
   - Ensure all have provenance metadata (source_method, review_status, confidence)

3. **Create timeline_events_skeleton.json**
   - Define 500 event stubs with dates, locations, and involved entities
   - No descriptions yet (will be filled by agents)
   - Ensure all person/text/concept slugs reference existing seed data

4. **Test full pipeline**
   - Run init_db.py → verify schema
   - Run load_seed_data.py → verify entity counts
   - Run load_timeline_skeleton.py → verify 500 events loaded
   - Spot-check database with sqlite3 CLI

5. **Launch Agent Swarm Phase 1**
   - Create pilot batch (e.g., "Medieval_Islam_Iraq_Persia", 20 events)
   - Pre-query entity context, write staging JSON
   - Run Timeline Event Enricher agent on pilot batch
   - Load results, validate
   - Repeat for remaining ~24 batches

---

## Success Criteria (Full Project)

- [ ] All 500 timeline events have 100–250 word descriptions
- [ ] All 100+ persons have 1,200–2,200 word biographies with Literature sections
- [ ] All 50+ texts have 1,000–1,800 word analyses with Literature sections
- [ ] All 30+ concepts have 1,500–2,500 word definitions with Actor/Analyst distinction explicit
- [ ] Every entity page links to at least 3 other entities
- [ ] Map shows all 500 events geotagged with valid coordinates
- [ ] Timeline shows all 500 events chronologically with era/region filtering
- [ ] All internal links are valid
- [ ] All bibliographies follow DGWE format (author last name, full title, full publication data)
- [ ] GitHub Pages site is live, responsive, and indexed

---

*For questions about next steps, see CLAUDE.md Task Routing.*
