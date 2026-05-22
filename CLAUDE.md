# Claude Code Instructions — ALCHEMYTIMELINEMAP

**An interactive timeline and map of alchemy and chemistry, 500 events, with relational browsing across persons, texts, and concepts. Coverage: Europe, North Africa, Middle East, Late Antiquity through early modern period.**

---

## MANDATORY FIRST STEPS (in order)

1. **Read `PROMPTS.md` in full.** It is the canonical record of the project vision, historiographical framework, three constituencies, and all architectural decisions.

2. **Read `STYLEGUIDE.md` in full.** It governs all prose fields (`description`, `bio_html`, `analysis_html`, `definition_long`) with precise word counts and required structures.

3. **Read `docs/CONTEXT_ENGINEERING.md`.** It explains how to efficiently query the database for timeline event descriptions without creating context explosion with 500 events.

---

## Project Mission

ALCHEMYTIMELINEMAP is an authoritative, interactive scholarly portal for the history of alchemy and chemistry from Late Antiquity through the early modern period. It combines:
- A **500-event interactive timeline** with chronological browsing and era/region/figure/concept filtering
- A **geo-pinned Leaflet.js map** showing the geographic distribution and clustering of alchemical knowledge
- **Relational entity pages** for persons, texts, and concepts, all cross-linked with no dead ends
- **Rigorous historiographical standards** following William R. Newman, Michela Pereira, Wouter J. Hanegraaff

Not an esoteric resource. Not a guide to practice. A scholarly reference for academic, student, and serious independent researchers.

---

## Current Phase

**PHASE 0: SYSTEM ARCHITECTURE + SEED DATA**

The portal infrastructure and system files are being designed. The current priorities are:

1. **Database schema** (init_db.py): 8 tables (timeline_events, persons, texts, concepts, locations, and reference/link tables)
2. **Seed data** (seed_data.json): Initial persons, texts, concepts, locations (~100 entries each)
3. **Timeline event skeleton** (timeline_events_skeleton.json): 500 event stubs (date, location, involved entities) to enrich
4. **Python pipeline** (idempotent scripts for data loading and static site generation)
5. **System files** (PROMPTS.md, STYLEGUIDE.md, CLAUDE.md, CONTEXT_ENGINEERING.md)

---

## Task Routing — Read This File First

| I need to... | Read this first |
|---|---|
| Understand the full project vision | `PROMPTS.md` ← START HERE |
| Write any prose content | `STYLEGUIDE.md` (word counts, structure, bibliography) |
| Know what's built vs. planned | `PHASESTATUS.md` |
| Know the database schema | `docs/ONTOLOGY.md` |
| Know the pipeline order | `docs/PIPELINE.md` |
| Know how to query efficiently for 500 events | `docs/CONTEXT_ENGINEERING.md` |
| Know the architecture | `docs/SYSTEM.md` |
| Add a timeline event | `STYLEGUIDE.md` → Timeline Events section |
| Add a person entry | `STYLEGUIDE.md` → Person Biographies section + `docs/ONTOLOGY.md` persons table |
| Add a text entry | `STYLEGUIDE.md` → Text Descriptions section |
| Add a concept entry | `STYLEGUIDE.md` → Concept Definitions section |
| Run agent swarms | `PROMPTS.md` → Part VI: Agent Operating Rules |

---

## Key Files

| Purpose | File |
|---------|------|
| **Canonical vision** | `PROMPTS.md` ← READ FIRST |
| **Style mandate** | `STYLEGUIDE.md` ← READ SECOND |
| **Context engineering** | `docs/CONTEXT_ENGINEERING.md` ← READ THIRD for 500-event scale |
| Entry point (this file) | `CLAUDE.md` |
| Phase status | `PHASESTATUS.md` |
| Data ontology | `docs/ONTOLOGY.md` |
| Architecture | `docs/SYSTEM.md` |
| Pipeline order | `docs/PIPELINE.md` |
| Database | `db/alchemy_timeline.db` |
| Seed data | `data/seed_data.json` |
| Timeline skeleton | `data/timeline_events_skeleton.json` |
| Deploy script | `scripts/build_site.py` |
| Database init | `scripts/init_db.py` |

---

## Architecture at a Glance

```
SQLite Database (alchemy_timeline.db)
  ├─ persons (105+ alchemists, chemists, scholars)
  ├─ texts (50+ treatises, translations, scholarship)
  ├─ concepts (30+ chemical operations, theories)
  ├─ locations (20+ cities/regions with coordinates)
  ├─ timeline_events (500 dated, geotagged events)
  ├─ person_event_refs
  ├─ text_event_refs
  └─ concept_event_refs

    ↓
    
Python Pipeline (idempotent scripts)
  ├─ scripts/init_db.py (schema creation)
  ├─ scripts/load_seed_data.py (persons, texts, concepts, locations)
  ├─ scripts/enrich_timeline_events.py (load descriptions from staging/)
  └─ scripts/build_site.py (static HTML generation)

    ↓
    
Static HTML/CSS/JS (site/)
  ├─ index.html (home with timeline viewer)
  ├─ map.html (Leaflet.js map with clustered pins)
  ├─ timeline/ (timeline browsing)
  ├─ persons/ (biography pages)
  ├─ texts/ (text description pages)
  ├─ concepts/ (concept definition pages)
  ├─ data.json (export for JavaScript: timeline events, map pins, relational graph)
  └─ assets/ (CSS, vanilla JS, no frameworks)

    ↓
    
GitHub Pages (docs/ folder)
```

**Key principle:** No frameworks. Vanilla HTML, CSS, JavaScript. SQLite as source of truth. Single Python deploy script generates all static files.

---

## Data Ontology Summary

### Persons Table
All entries cover either (a) historical alchemists/chemists, or (b) modern scholars. Fields:
- `slug`: unique identifier (lowercase, hyphens, no special chars)
- `name`: full name
- `role_primary`: ALCHEMIST, CHEMIST, SCHOLAR, PHILOSOPHER, PHYSICIAN, TRANSLATOR, MATHEMATICIAN, CLERICAL, PATRON
- `era`: ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
- `bio_html`: 1,200–2,200 words
- `source_method`, `review_status`, `confidence`: provenance metadata

### Texts Table
- `slug`: unique identifier
- `title`: full title in original language if known
- `text_type`: PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA
- `original_language`: Latin, Arabic, Greek, Hebrew, English, etc.
- `composition_date`: "c. 1320" or "1250–1300"
- `analysis_html`: 1,000–1,800 words for primary sources; varies for scholarship
- Provenance metadata

### Concepts Table
- `slug`: unique identifier
- `label`: term in primary language (e.g., "Distillation" or "Calcination")
- `category_type`: ACTOR_TERM or ANALYST_TERM
- `definition_short`: 60–120 words (index card)
- `definition_long`: 1,500–2,500 words (encyclopedia page)
- Provenance metadata

### Locations Table
- `slug`: unique identifier
- `place_name`: city or region name
- `latitude`, `longitude`: decimal coordinates
- `region`: broader geographic area (e.g., "Iberia", "Italy", "Iraq")
- `modern_name`: modern country or region

### Timeline_Events Table
- `slug`: unique identifier
- `date_label`: "c. 1320" or "1492–1495"
- `date_start_year`, `date_end_year`: for sorting/filtering
- `location_slug`: foreign key to locations table
- `description`: 100–250 words (the core timeline content)
- `persons_involved`: JSON array of person slugs
- `texts_involved`: JSON array of text slugs
- `concepts_involved`: JSON array of concept slugs
- Provenance metadata

---

## Data Flow: From Seed to Site

1. **Seed data** (`data/seed_data.json` or separate domain files)
2. **Python ingestion** (`scripts/load_seed_data.py` — idempotent INSERT OR IGNORE)
3. **Agent enrichment** (agents write to `staging/` as JSON)
4. **Validation & merge** (main session reads staging/, converts `[LINK:slug]` to `<a href>`, loads into DB)
5. **Static site generation** (`scripts/build_site.py` reads DB, generates HTML + data.json)
6. **Deploy** (output to `site/` or `docs/`)

---

## Pipeline Rules

1. **No ad-hoc data.** All data enters via idempotent Python scripts in `scripts/`.
2. **Provenance on every row.** `source_method`, `review_status`, `confidence` required.
3. **Idempotent scripts.** All scripts use `INSERT OR IGNORE`. Safe to re-run.
4. **Slugs, not row IDs.** Never hardcode database row IDs. Use slugs for all cross-references.
5. **Staging files for agent output.** Agents write to `staging/`, main session validates before DB insertion.
6. **[LINK:slug] markup for agents.** Agents wrap entity names in `[LINK:slug]` markup. Main session converts to `<a href>` tags.
7. **Validate after enrichment.** Run deploy after any ingestion to verify output.
8. **Style before data.** Check prose against `STYLEGUIDE.md` before committing to DB.

---

## Python Conventions

- Python stdlib only (sqlite3, json, re, pathlib)
- All scripts must be idempotent (`INSERT OR IGNORE`, `UPDATE OR IGNORE`)
- DB path: `C:\Dev\ALCHEMYTIMELINEMAP\db\alchemy_timeline.db`
- Seed data: `C:\Dev\ALCHEMYTIMELINEMAP\data\seed_data.json` (or split by domain)
- Deploy command: `python C:\Dev\ALCHEMYTIMELINEMAP\scripts\build_site.py`

---

## Key Scholarly Authorities

These scholars' frameworks govern the portal. Reference them in bibliographies and when defining concepts:

| Scholar | Key Work | Use for... |
|---------|----------|-----------|
| William R. Newman | *Atoms and Alchemy* (Yale, 2006) | Operational chemistry, transmutation theory, alchemical texts |
| Michela Pereira | *The Alchemical Corpus Attributed to Ray Lull* (2007) | Medieval alchemy, especially Catalan tradition |
| Garth Fowden | *The Egyptian Hermes* (1986) | Late Antique roots, Zosimos, Byzantine alchemy |
| Wouter J. Hanegraaff | *Dictionary of Gnosis and Western Esotericism* (2006) | Historiographical framework, Actor/Analyst distinction |
| Lawrence Principe | Works on practical alchemy | Modern reassessment of operations, Boyle and Newton |
| Pamela Smith | *The Business of Alchemy* (2005) | Early modern alchemy, craft knowledge, transmutation |
| Eric John Holmyard | *Alchemy* (1957/2005) | Classic overview, historical narrative |

---

## Vocabulary Lock

All enum values are defined in `scripts/init_db.py` CHECK constraints. Do not invent new values for `era`, `role_primary`, `text_type`, `category_type`, `operation`, `confidence`, or `review_status` without adding them to the schema first.

**Current enums:**

```sql
era: ANTIQUITY | LATE_ANTIQUE | MEDIEVAL | RENAISSANCE | EARLY_MODERN | MODERN
role_primary: ALCHEMIST | CHEMIST | SCHOLAR | PHILOSOPHER | PHYSICIAN | TRANSLATOR | MATHEMATICIAN | POET | PATRON | CLERICAL
text_type: PRIMARY_SOURCE | COMMENTARY | COMPILATION | TREATISE | SCHOLARSHIP | ENCYCLOPEDIA
category_type: ACTOR_TERM | ANALYST_TERM
operation: DISTILLATION | SUBLIMATION | CALCINATION | FERMENTATION | CRYSTALLIZATION | DISSOLUTION | COAGULATION | PUTREFACTION | CIRCULATION
confidence: HIGH | MEDIUM | LOW
review_status: DRAFT | REVIEWED | VERIFIED
source_method: MANUAL | AI_ASSISTED | SCHOLARSHIP_BASED
```

---

## Checking Your Work

Before committing any work:

- [ ] Did I read `PROMPTS.md`, `STYLEGUIDE.md`, and `CONTEXT_ENGINEERING.md`?
- [ ] Does my prose meet the minimum word count for its type?
- [ ] Are all book titles and foreign terms italicized?
- [ ] Are claims grounded in named sources?
- [ ] Does every entry link to at least 3 other entities?
- [ ] Is provenance metadata complete (`source_method`, `review_status`, `confidence`)?
- [ ] Are all enums from the vocabulary lock?

---

## Do Not Auto-Suggest Planning Skills

The user prefers to invoke skills by name. Do not suggest `/plan`, `/phase-gate`, `/scope-check` etc. unless explicitly asked.

---

*This file is the entry point. When in doubt, start with `PROMPTS.md`, then `STYLEGUIDE.md`, then the specific documentation for your task.*
