# ALCHEMYTIMELINEMAP

An interactive timeline and map of alchemy and chemistry, with 500 events spanning Late Antiquity through the early modern period. Coverage: Europe, North Africa, Middle East.

**Status:** Phase 0 (System Architecture + Documentation) — Ready for Python script implementation and seed data creation.

---

## Quick Start

1. **Read the system files (in order):**
   - `PROMPTS.md` — Vision, historiographical framework, constituencies
   - `STYLEGUIDE.md` — Content standards (word counts, structure, bibliography format)
   - `CLAUDE.md` — Routing guide, task breakdown, conventions

2. **Understand the architecture:**
   - `docs/SYSTEM.md` — Data flow, technology stack, design principles
   - `docs/ONTOLOGY.md` — Database schema (8 tables, enums, relationships)
   - `docs/PIPELINE.md` — Script execution order

3. **Learn the batch strategy for 500 events:**
   - `docs/CONTEXT_ENGINEERING.md` — How to efficiently query without context explosion

4. **Check project status:**
   - `PHASESTATUS.md` — What's built, what's planned, next immediate actions

---

## Project Structure

```
ALCHEMYTIMELINEMAP/
├── PROMPTS.md                    # Canonical vision ← START HERE
├── STYLEGUIDE.md                 # Content standards
├── CLAUDE.md                      # Routing + conventions
├── PHASESTATUS.md                # Phase tracking
│
├── docs/
│   ├── SYSTEM.md                 # Architecture overview
│   ├── ONTOLOGY.md               # Database schema
│   ├── PIPELINE.md               # Script execution order
│   └── CONTEXT_ENGINEERING.md    # 500-event batch strategy
│
├── db/
│   └── alchemy_timeline.db       # SQLite (created by init_db.py)
│
├── data/
│   ├── seed_data.json            # Initial persons, texts, concepts, locations
│   └── timeline_events_skeleton.json  # 500 event stubs to enrich
│
├── scripts/
│   ├── init_db.py                # Database schema creation
│   ├── load_seed_data.py         # Load seed JSON
│   ├── load_timeline_skeleton.py # Load 500 event stubs
│   ├── pre_query_batch_context.py # Pre-query entity context for agents
│   ├── enrich_timeline_events.py # Load agent output, validate, load to DB
│   └── build_site.py             # Main deploy: SQLite → static HTML/JSON
│
├── staging/
│   ├── batch_[era]_[region].json (input to agents)
│   └── enriched_events_[era]_[region].json (output from agents)
│
└── site/
    ├── index.html
    ├── timeline.html, map.html
    ├── persons/, texts/, concepts/ (generated HTML pages)
    ├── data/ (JSON exports)
    └── assets/ (CSS, JS)
```

---

## Technology Stack

- **Database:** SQLite (`alchemy_timeline.db`)
- **Data loading:** Python 3 stdlib only (sqlite3, json, re, pathlib)
- **Static site generation:** Python
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **Map visualization:** Leaflet.js (CDN)
- **Relationship graph:** D3.js (CDN)
- **Hosting:** GitHub Pages

---

## Core Architecture

1. **SQLite** is the single source of truth
2. **Python scripts** are fully idempotent (can be re-run safely)
3. **Agent output** goes to `staging/` before validation and DB insertion
4. **Static HTML** is generated from SQLite by `scripts/build_site.py`
5. **GitHub Pages** serves the final static site

**No frameworks. No build tools. No runtime dependencies.**

---

## Content Model

### Timeline Event (Primary Unit)
- 100–250 words
- Dated, geotagged (lat/lon)
- Links to at least 1 person, text, or concept
- Declares historiographical significance

### Person Biography
- 1,200–2,200 words
- Roles: ALCHEMIST, CHEMIST, SCHOLAR, PHYSICIAN, TRANSLATOR, etc.
- Eras: ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
- Requires Literature section (5–12 items)

### Text Analysis
- 1,000–1,800 words
- Types: PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA
- Requires Literature section (5–12 items)

### Concept Definition
- 1,500–2,500 words
- Category: ACTOR_TERM (used by historical actors) or ANALYST_TERM (retrospective scholarly category)
- Required sections: Historical Usage → Scholarly Significance → Related Concepts → Literature
- Requires explicit declaration of Actor/Analyst distinction

---

## Historiographical Framework

**Three scholarly principles:**

1. **Actor/Analyst Distinction** (Hanegraaff methodology)
   - ACTOR_TERMs: Words used by historical alchemists (*distillatio*, *transmutatio*)
   - ANALYST_TERMs: Modern retrospective categories (*Hermeticism*, *alchemy*)
   - Never collapse these registers.

2. **Medieval Continuity**
   - The Renaissance "rediscovery" built on continuous medieval Islamic and Latin traditions
   - Never treat the medieval period as a gap.

3. **Operational Chemistry**
   - Alchemists' practical operations (distillation, sublimation) were real chemical advances
   - Separate operational success from transmutational belief.

---

## Key Authorities

- **William R. Newman** — *Atoms and Alchemy* (Yale, 2006) — master of alchemical texts
- **Michela Pereira** — Medieval alchemy and the Catalan tradition
- **Garth Fowden** — *The Egyptian Hermes* (1986) — Late Antique roots
- **Wouter J. Hanegraaff** — *Dictionary of Gnosis and Western Esotericism* (2006) — methodological framework
- **Lawrence Principe** — Modern reassessment of practical alchemy

---

## Implementation Pipeline

### Phase 0: System Architecture (✅ COMPLETE)
- [x] Create PROMPTS.md, STYLEGUIDE.md, CLAUDE.md, PHASESTATUS.md
- [x] Create SYSTEM.md, ONTOLOGY.md, PIPELINE.md, CONTEXT_ENGINEERING.md
- [ ] Create Python script stubs (init_db.py, load_seed_data.py, etc.)
- [ ] Create seed_data.json (bootstrap entities)
- [ ] Create timeline_events_skeleton.json (500 event stubs)

### Phase 1: Agent Swarm — Event Enrichment
- [ ] Partition 500 events into 25 batches (era + region)
- [ ] For each batch: pre-query context, launch agent, validate, load to DB
- [ ] Result: All 500 events with full descriptions

### Phase 2: Agent Swarm — Persons + Texts
- [ ] Ensure all persons at 1,200+ words
- [ ] Ensure all texts at 1,000+ words
- [ ] Ensure all Literature sections present and properly formatted

### Phase 3: Concept Enrichment
- [ ] Ensure all concepts at 1,500+ words
- [ ] Ensure Actor/Analyst distinction explicit throughout
- [ ] Ensure all Literature sections present

### Phase 4: Static Site Generation + Deployment
- [ ] Implement build_site.py
- [ ] Generate all HTML pages
- [ ] Create timeline/map JavaScript with filtering
- [ ] Deploy to GitHub Pages
- [ ] Test all links and relationships

---

## Next Steps

1. **Create Python scripts** (use `scripts/init_db.py` template below as a starting point)
2. **Create seed_data.json** (bootstrap ~100 persons, ~50 texts, ~30 concepts, ~20 locations)
3. **Create timeline_events_skeleton.json** (500 event stubs with dates, locations, entities)
4. **Test the pipeline** (init_db → load_seed → load_skeleton → check counts)
5. **Launch Agent Swarm Phase 1** (enrich all 500 events)

---

## Archaeology & Material Culture (NEW)

The portal now includes comprehensive research on the material evidence of alchemy:

- **docs/ARCHAEOLOGY_AND_MATERIAL_CULTURE.md** — Hessian crucibles, Tycho Brahe's laboratory, Oberstockstall monastery, the Making and Knowing Project, Pamela Smith's artisanal epistemology framework
- **ARCHAEOLOGY_RESEARCH_SUMMARY.md** — Complete research synthesis with sources and historiographical impact
- **INTEGRATION_GUIDE_ARCHAEOLOGY.md** — How to incorporate archaeological findings into timeline events and encyclopedia entries
- **data/seed_data_archaeology_supplement.json** — 2 new scholars, 6 new concepts, 8 new timeline events, 4 new locations

**Key additions:**
- Pamela H. Smith (artisanal epistemology, Making and Knowing Project)
- Lawrence Principe (experimental reconstruction of alchemy)
- New ANALYST_TERMs: artisanal epistemology, operational chemistry, material culture approach
- New ACTOR_TERMs: mullite, medicamenta tria, tacit knowledge
- 8 new timeline events from medieval Hessian crucibles through 2024 Tycho Brahe analysis

---

## For More Information

- **Full vision and principles:** See `PROMPTS.md`
- **Content standards and format:** See `STYLEGUIDE.md`
- **Database schema and tables:** See `docs/ONTOLOGY.md`
- **Script execution order:** See `docs/PIPELINE.md`
- **Efficient querying for 500 events:** See `docs/CONTEXT_ENGINEERING.md`
- **Routing and file index:** See `CLAUDE.md`
- **Archaeological evidence and material culture:** See `docs/ARCHAEOLOGY_AND_MATERIAL_CULTURE.md`
- **How to integrate archaeology content:** See `INTEGRATION_GUIDE_ARCHAEOLOGY.md`
- **Complete research synthesis:** See `ARCHAEOLOGY_RESEARCH_SUMMARY.md`

---

**Last updated:** 2026-05-22
**Latest addition:** Comprehensive archaeology and material culture research integrated (2026-05-22)
