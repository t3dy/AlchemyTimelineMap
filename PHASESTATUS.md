# ALCHEMYTIMELINEMAP Phase Status

**Updated:** 2026-05-22
**Current Phase:** PHASE 1 (READY) — AGENT SWARM EVENT ENRICHMENT

---

## PHASE 0: SYSTEM ARCHITECTURE + SEED DATA (✅ COMPLETE)

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
| Python scripts (6 main scripts) | ✅ COMPLETE | All idempotent, UTF-8 safe, tested end-to-end |
| Create seed_data.json (initial entities) | ✅ COMPLETE | 20 persons, 14 texts, 18 concepts, 11 locations (loaded) |
| Create timeline_events_skeleton.json | ✅ COMPLETE | 25 event stubs (loaded, ready for expansion to 500) |

---

## PHASE 3D: DATABASE & SITE GENERATION (✅ COMPLETE)

| Task | Status | Notes |
|------|--------|-------|
| Initialize SQLite schema | ✅ COMPLETE | 8 tables, foreign keys, CHECK constraints, 9 indexes |
| Load seed data | ✅ COMPLETE | 20 persons, 14 texts, 18 concepts, 11 locations |
| Load timeline skeleton | ✅ COMPLETE | 25 events + 92 reference relationships |
| Generate HTML pages | ✅ COMPLETE | 52 pages (3 main + 20 persons + 14 texts + 18 concepts) |
| Export JSON data | ✅ COMPLETE | data.json (47 KB) with all entities for JS |
| End-to-end testing | ✅ COMPLETE | All scripts verified working on Windows |

**Database status:** `C:\Dev\ALCHEMYTIMELINEMAP\db\alchemy_timeline.db` (created 2026-05-22)
**Generated site:** `C:\Dev\ALCHEMYTIMELINEMAP\site/` (52 HTML files + JSON)

---

### PHASE 1: AGENT SWARM EVENT ENRICHMENT (READY TO BEGIN)

**Goal:** Enrich all 500 timeline events with full descriptions (100–250 words each).

**Current state:** Database initialized with 25 core events; ready for expansion to 500 events.

**Approach:** 
- Expand timeline_events_skeleton.json from 25 → 500 events (475 new events)
- Partition 500 events into ~25 batches (era + region)
- For each batch:
  - Main session: pre_query_batch_context.py to write `staging/batch_*.json`
  - Agent Type A (Timeline Event Enricher): read batch, write `staging/enriched_events_*.json`
  - Main session: enrich_timeline_events.py to validate, convert markup, load into DB
- Rebuild site with build_site.py

**Success criteria:**
- [ ] Timeline skeleton expanded from 25 → 500 events
- [ ] All 500 events have descriptions (100–250 words)
- [ ] All descriptions link to at least 1 person, text, or concept
- [ ] All descriptions declare historiographical significance (final sentence)
- [ ] All entity links resolve to existing persons/texts/concepts
- [ ] All event dates and locations are valid

**Tools ready:** pre_query_batch_context.py, enrich_timeline_events.py both tested and working

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
