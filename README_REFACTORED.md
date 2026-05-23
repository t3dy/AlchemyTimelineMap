# ALCHEMYTIMELINEMAP

An interactive timeline and map of alchemy and chemistry, featuring 480+ events spanning Late Antiquity through the early modern period. Coverage: Europe, North Africa, Middle East.

**Website:** https://t3dy.github.io/AlchemyTimelineMap/

---

## Quick Start

1. **New to the project?** Start with [`CLAUDE.md`](CLAUDE.md) (2 min) for mission, current phase, and task routing.

2. **Writing content?** Read [`STYLEGUIDE.md`](STYLEGUIDE.md) (15 min) for word counts, required sections, and prose standards.

3. **Contributing to a task?** Check [`PHASESTATUS.md`](PHASESTATUS.md) (5 min) to see what's in progress and what's next.

4. **Understanding the vision?** Read [`PROMPTS.md`](PROMPTS.md) (15 min) for historiographical framework and design principles.

5. **Running scripts or modifying architecture?** Consult [`docs/PIPELINE.md`](docs/PIPELINE.md) and [`docs/SYSTEM.md`](docs/SYSTEM.md).

---

## Project Structure

```
ALCHEMYTIMELINEMAP/
├── CLAUDE.md              ← START HERE (boot layer)
├── PHASESTATUS.md         ← What's done, what's next
├── PROMPTS.md             ← Canonical vision & historiography
├── STYLEGUIDE.md          ← Content standards
├── README.md              ← This file
│
├── docs/
│   ├── SYSTEM.md          (Architecture & data flow)
│   ├── ONTOLOGY.md        (Database schema)
│   ├── PIPELINE.md        (Script execution order)
│   ├── CONTEXT_ENGINEERING.md  (500-event batch strategy)
│   ├── agents/            (Task-specific prompts)
│   ├── reference/         (Scholarly profiles, examples)
│   └── archive/           (Session notes, superseded guides)
│
├── db/
│   └── alchemy_timeline.db    (SQLite source of truth)
│
├── data/
│   ├── seed_data.json         (Initial 20 persons, 14 texts, etc.)
│   └── timeline_events_skeleton.json (500 event stubs)
│
├── scripts/
│   ├── init_db.py             (Create schema)
│   ├── load_seed_data.py      (Load entities)
│   ├── load_timeline_skeleton.py
│   ├── pre_query_batch_context.py
│   ├── enrich_timeline_events.py
│   └── build_site.py          (Deploy: SQLite → HTML/JSON)
│
├── staging/               (Agent output before validation)
│
└── site/                  (Generated static HTML)
    ├── index.html, timeline.html, map.html
    ├── persons/, texts/, concepts/ (generated pages)
    ├── data/data.json (entity export)
    └── assets/ (CSS, JS)
```

---

## Technology Stack

- **Database:** SQLite (single file, no server)
- **Backend:** Python 3 stdlib only (sqlite3, json, re, pathlib)
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **Map:** Leaflet.js (CDN)
- **Hosting:** GitHub Pages

---

## Core Principles

1. **Timeline-first:** The 500 timeline events are the primary atoms. Persons, texts, concepts are secondary (linked from events).
2. **No frameworks:** Vanilla HTML/JS only. No npm, webpack, or build tools.
3. **Idempotent scripts:** All Python scripts use `INSERT OR IGNORE` and can be re-run safely.
4. **Scholarly standards:** Every entry cites named scholars. Actor/Analyst distinction is explicit.

---

## Current Status

- **Phase 1:** ✅ Complete (480 timeline events enriched)
- **Phase 2:** 🔄 In Progress (expand persons, texts, concepts)

For full details, see [`PHASESTATUS.md`](PHASESTATUS.md).

---

## Key Authorities

The project is built on historiographical frameworks from:
- **William R. Newman** (*Atoms and Alchemy*)
- **Wouter J. Hanegraaff** (*Dictionary of Gnosis and Western Esotericism*)
- **Michela Pereira** (medieval alchemy)
- **Pamela Smith** (artisanal epistemology, material culture)

---

## Next Steps

See [`PHASESTATUS.md`](PHASESTATUS.md) for current task breakdown.

---

*For detailed instructions, see [`CLAUDE.md`](CLAUDE.md).*
