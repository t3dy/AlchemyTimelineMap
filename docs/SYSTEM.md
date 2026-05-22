# ALCHEMYTIMELINEMAP System Architecture

**Overview of the data flow, technology stack, and design principles.**

---

## Core Stack

- **Database:** SQLite (`alchemy_timeline.db`)
- **Data loading:** Python 3 stdlib only (sqlite3, json, re, pathlib)
- **Static site generation:** Python script (`build_site.py`)
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks, no npm, no build tools)
- **Map:** Leaflet.js (external CDN)
- **Visualization:** D3.js for relationship graph (external CDN)
- **Hosting:** GitHub Pages (`docs/` folder)

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Seed Data (JSON files in data/)                            │
│  ├─ data/seed_data.json (persons, texts, concepts, loc)    │
│  └─ data/timeline_events_skeleton.json (500 stubs)          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  Python Data Loading (scripts/)                             │
│  ├─ scripts/init_db.py (schema + CHECK constraints)         │
│  ├─ scripts/load_seed_data.py (INSERT OR IGNORE)            │
│  └─ scripts/enrich_timeline_events.py (load from staging)   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  SQLite Database (db/alchemy_timeline.db)                   │
│  ├─ timeline_events (500 rows, core content unit)           │
│  ├─ persons (100+ alchemists, chemists, scholars)           │
│  ├─ texts (50+ treatises, scholarship)                      │
│  ├─ concepts (30+ chemical operations, theories)            │
│  ├─ locations (20+ cities/regions with lat/lon)             │
│  └─ Reference tables (person_event_refs, etc.)              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  Agent Enrichment (Staging Pattern)                         │
│  ├─ Main session pre-queries entity context                 │
│  ├─ Main session writes batch JSON to staging/              │
│  ├─ Agent enriches with descriptions, writes to staging/    │
│  └─ Main session reads staging/, loads into DB              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  Static Site Generation (build_site.py)                     │
│  ├─ Read from SQLite                                        │
│  ├─ Generate HTML pages (persons/, texts/, concepts/)       │
│  ├─ Generate timeline JSON (for JavaScript timeline view)   │
│  ├─ Generate map pins JSON (lat/lon for Leaflet)            │
│  ├─ Generate graph JSON (D3.js relationship graph)          │
│  └─ Generate data.json (all entities + relationships)       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│  Static Output (site/ → docs/)                              │
│  ├─ index.html (home)                                       │
│  ├─ timeline.html (timeline viewer with JS filtering)       │
│  ├─ map.html (Leaflet.js map with clustered pins)           │
│  ├─ persons/[slug].html (biography pages, 100+ files)       │
│  ├─ texts/[slug].html (text pages, 50+ files)               │
│  ├─ concepts/[slug].html (concept pages, 30+ files)         │
│  ├─ data.json (all entities + relationships)                │
│  ├─ timeline.json (events + map pins)                       │
│  └─ assets/ (CSS, JS, images)                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
           GitHub Pages
           (t3dy/alchemytimelinemap)
```

---

## Design Principles

### 1. SQLite as Source of Truth

All data lives in the SQLite database. Python scripts are idempotent and can be re-run without corruption. The database is the single source of truth; HTML pages are ephemeral and regenerated on every deploy.

**Implication:** Never edit HTML directly. Always edit the database via Python scripts, then regenerate.

### 2. No Frameworks, No Build Tools

- **Frontend:** Vanilla HTML, CSS, JavaScript only
- **No React, Vue, Svelte**
- **No npm, webpack, or build step**
- **External libraries:** Leaflet.js and D3.js via CDN only

**Implication:** Code is human-readable, directly editable, and requires zero build infrastructure.

### 3. Idempotent Ingestion

All Python scripts use `INSERT OR IGNORE` (for persons, texts, concepts, locations) and `UPDATE OR IGNORE` (for existing records). Scripts can be re-run safely without duplication or corruption.

**Implication:** Safe to run the entire pipeline multiple times. No cleanup needed between iterations.

### 4. Provenance on Every Datum

Every row in the database includes:
- `source_method`: MANUAL, AI_ASSISTED, SCHOLARSHIP_BASED
- `review_status`: DRAFT, REVIEWED, VERIFIED
- `confidence`: HIGH, MEDIUM, LOW

**Implication:** Every statement in the portal is traceable to how it was created and how trustworthy it is.

### 5. Slugs, Never IDs

All cross-references use slugs (human-readable identifiers), never hardcoded database row IDs.

**Implication:** Rows can be deleted, merged, or renumbered without breaking links.

### 6. Staging Files for Agent Output

Agents do not write directly to the database. They write JSON to `staging/`, which the main session validates and loads.

**Implication:** Full audit trail, ability to reject or revise agent output, and clear separation of concerns.

---

## Directory Structure

```
C:\Dev\ALCHEMYTIMELINEMAP/
├── PROMPTS.md                    # Canonical vision
├── STYLEGUIDE.md                 # Content standards
├── CLAUDE.md                      # Routing + conventions (this file)
├── PHASESTATUS.md                # Current phase + progress
│
├── db/
│   └── alchemy_timeline.db       # SQLite database (created by init_db.py)
│
├── data/
│   ├── seed_data.json            # Initial persons, texts, concepts, locations
│   └── timeline_events_skeleton.json  # 500 event stubs to enrich
│
├── scripts/
│   ├── init_db.py                # Create schema with CHECK constraints
│   ├── load_seed_data.py         # Load seed data (idempotent)
│   ├── enrich_timeline_events.py # Load enriched descriptions from staging/
│   └── build_site.py             # Main deploy script: reads DB, generates HTML
│
├── staging/
│   ├── batch_[era]_[region].json (input: pre-queried entity context)
│   ├── enriched_events_[era]_[region].json (output from agents)
│   ├── audit_relational.json     (output from relational auditors)
│   └── ...
│
├── site/
│   ├── index.html
│   ├── timeline.html
│   ├── map.html
│   ├── persons/
│   ├── texts/
│   ├── concepts/
│   ├── data/
│   │   ├── data.json             # All entities + relationships
│   │   ├── timeline.json         # Events + coordinates
│   │   └── graph.json            # D3.js graph data
│   └── assets/
│       ├── style.css
│       ├── timeline.js
│       ├── map.js
│       └── graph.js
│
└── docs/
    ├── SYSTEM.md                 # Architecture (this file)
    ├── ONTOLOGY.md               # Database schema
    ├── PIPELINE.md               # Script execution order
    ├── CONTEXT_ENGINEERING.md    # How to query efficiently for 500 events
    └── ...

# GitHub Pages output (copy site/ to docs/ or configure in deploy)
```

---

## Key Operational Files

| File | Purpose | Frequency |
|------|---------|-----------|
| `db/alchemy_timeline.db` | SQLite source of truth | Persistent |
| `data/seed_data.json` | Initial entity data | Created once, updated as needed |
| `data/timeline_events_skeleton.json` | 500 event stubs (dates, locations, involved entities) | Created once, updated incrementally |
| `staging/batch_*.json` | Pre-queried context for agent batches | Created before each agent run |
| `staging/enriched_events_*.json` | Agent output (enriched descriptions) | Created by agents, read by main session |
| `scripts/build_site.py` | Deploy script: reads DB, generates HTML + JSON | Run after any DB change |
| `site/` | Generated static HTML/CSS/JS | Regenerated on every deploy |
| `docs/` | GitHub Pages output (copy of `site/`) | Synced to GitHub |

---

## Typical Workflow

1. **Initialize database:**
   ```
   python scripts/init_db.py
   python scripts/load_seed_data.py
   ```

2. **Add/update timeline event skeleton:**
   - Edit `data/timeline_events_skeleton.json` (or use Python to bulk-insert)
   - Run `python scripts/init_db.py` again (idempotent)

3. **Enrich timeline events via agent swarm:**
   - Main session: partition 500 events into 20–30 batches
   - Main session: pre-query entity context, write to `staging/batch_*.json`
   - Agent: read batch JSON, write enriched descriptions to `staging/enriched_*.json`
   - Main session: read staging files, validate, load into DB

4. **Generate static site:**
   ```
   python scripts/build_site.py
   ```
   - Reads from `db/alchemy_timeline.db`
   - Generates HTML pages, JSON data exports
   - Writes to `site/`

5. **Deploy to GitHub Pages:**
   - Copy `site/` contents to `docs/`
   - Push to GitHub
   - GitHub Pages auto-publishes `docs/`

---

## Database Schema (Summary)

See `ONTOLOGY.md` for detailed schema. Quick overview:

**Core tables:**
- `timeline_events` (500 rows): date_label, location_slug, description, persons_involved, texts_involved, concepts_involved
- `persons` (100+ rows): slug, name, role_primary, era, bio_html
- `texts` (50+ rows): slug, title, text_type, analysis_html
- `concepts` (30+ rows): slug, label, category_type, definition_long
- `locations` (20+ rows): slug, place_name, latitude, longitude, region

**Reference tables:**
- `person_event_refs`: links persons to events
- `text_event_refs`: links texts to events
- `concept_event_refs`: links concepts to events
- `concept_person_refs`: links concepts to persons
- `concept_text_refs`: links concepts to texts

---

## Deployment Checklist

- [ ] All timeline events enriched (100% descriptions written and loaded)
- [ ] All persons pages at 1,200+ words minimum
- [ ] All texts pages at 1,000+ words minimum
- [ ] All concepts pages at 1,500+ words minimum
- [ ] All biographies have Literature sections (5–12 items)
- [ ] All text analyses have Literature sections (5–12 items)
- [ ] All concept definitions have Literature sections (8–15 items)
- [ ] Every entity page links to at least 3 other entities
- [ ] Map has valid lat/lon for all events (no NULL coordinates)
- [ ] Timeline JSON exports successfully without errors
- [ ] Graph JSON exports successfully without errors
- [ ] Static HTML generates without errors
- [ ] GitHub Pages repo configured to serve from `docs/`

---

*For detailed schema, see `ONTOLOGY.md`. For script execution order, see `PIPELINE.md`.*
