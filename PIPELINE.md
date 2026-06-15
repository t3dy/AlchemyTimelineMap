# ALCHEMYTIMELINEMAP Pipeline Execution Order

**The sequence of Python scripts for building and deploying the portal.**

---

## Phase 1: Initialize Database Schema

### 1. `scripts/init_db.py`

Creates SQLite schema with all 8 tables and CHECK constraints.

```bash
python scripts/init_db.py
```

**Output:** `db/alchemy_timeline.db` with empty schema.

**Idempotent:** Creates tables only if they don't exist. Safe to re-run.

---

## Phase 2: Load Seed Data

### 2. `scripts/load_seed_data.py`

Ingest initial persons, texts, concepts, and locations from JSON seed files.

```bash
python scripts/load_seed_data.py
```

**Input:** `data/seed_data.json`

**Output:** Populated persons, texts, concepts, locations tables.

**Preconditions:** `init_db.py` must run first.

---

## Phase 3: Load Timeline Event Skeleton

### 3. `scripts/load_timeline_skeleton.py`

Load 500 timeline event stubs (date, location, involved entities) without descriptions yet.

```bash
python scripts/load_timeline_skeleton.py
```

**Input:** `data/timeline_events_skeleton.json`

**Output:** `timeline_events` table with 500 rows, descriptions NULL.

**Preconditions:** Seed data must be loaded first (persons, texts, concepts, locations already exist).

---

## Phase 4: Enrich Timeline Events via Agent Swarm

### 4. `scripts/pre_query_batch_context.py`

For each batch of events, pre-query all related entities and write batch JSON for agent.

```bash
python scripts/pre_query_batch_context.py --batch_id "Medieval_Islam_Iraq_Persia"
```

**Output:** `staging/batch_Medieval_Islam_Iraq_Persia.json`

**See:** `CONTEXT_ENGINEERING.md` for the full batch strategy.

### Agent Work

Agent reads batch JSON, writes enriched descriptions with `[LINK:slug]` markup to `staging/enriched_events_[batch_id].json`.

### 5. `scripts/enrich_timeline_events.py`

Read enriched event JSON from staging, validate, convert markup, load into DB.

```bash
python scripts/enrich_timeline_events.py --staging_file staging/enriched_events_Medieval_Islam_Iraq_Persia.json
```

**Does:**
- Converts `[LINK:slug]` → `<a href>` tags
- Validates word counts (100–250)
- Validates entity references exist in DB
- Updates `timeline_events.description` and `review_status`

---

## Phase 4b: Consolidate Figure Events (one event per historical figure)

The timeline carries **one canonical "figure event" per historical figure** —
an index-card preview that links to a single long-form essay (the person page).
This phase collapses the many duplicate per-figure events into one each.

Run **in this order** (each step depends on the previous):

```bash
python scripts/merge_duplicate_persons.py      # fold duplicate person records (e.g. muhammad-al-razi -> al-razi)
python scripts/consolidate_figure_events.py    # build one figure event per figure; snapshots raw_timeline_events
python scripts/generate_figure_previews.py     # 3-5 sentence index-card preview per figure (MUST follow consolidate)
python scripts/load_figure_essays.py           # load 3,000-5,000 word essays from staging/figure_essays/<slug>.html
```

**Idempotent:** `consolidate_figure_events.py` snapshots the pristine event
table into `raw_timeline_events` on first run and rebuilds the live table from
that snapshot every run, so the whole sequence is safe to repeat. Because
consolidation recreates the figure events, **always re-run
`generate_figure_previews.py` after it.**

**Essays:** one HTML fragment per figure under `staging/figure_essays/<person-slug>.html`
(3,000-5,000 words, `[LINK:slug]` markup). `load_figure_essays.py` validates word
count and link slugs before writing to `persons.bio_html`.

---

## Phase 5: Static Site Generation

### 6. `scripts/build_site.py`

Read SQLite, generate all static HTML pages and JSON data exports.

```bash
python scripts/build_site.py
```

**Output to `site/`:**
- `index.html`, `timeline.html`, `map.html`
- `persons/[slug].html` (100+ files)
- `texts/[slug].html` (50+ files)
- `concepts/[slug].html` (30+ files)
- `data/data.json`, `timeline.json`, `graph.json`

**WARNING:** This script regenerates the entire `docs/` directory for GitHub Pages. Documentation `.md` files must NOT be stored in `docs/` — they will be deleted on each run.

---

## Phase 6: Deploy to GitHub Pages

```bash
cp -r site/* docs/
git add docs/
git commit -m "Deploy: [summary]"
git push origin main
```

GitHub Pages automatically serves from `docs/` folder.

---

## Standard Full Pipeline

```bash
python scripts/init_db.py
python scripts/load_seed_data.py
python scripts/load_timeline_skeleton.py
# For each batch:
#   python scripts/pre_query_batch_context.py --batch_id [batch]
#   [Agent enriches batch → staging/]
#   python scripts/enrich_timeline_events.py --staging_file staging/enriched_events_[batch].json
python scripts/build_site.py
cp -r site/* docs/
git add docs/ && git commit -m "Deploy" && git push
```

---

## Idempotency

All scripts are idempotent:
- `init_db.py`: Creates tables only if they don't exist
- `load_seed_data.py`: Uses `INSERT OR IGNORE`
- `load_timeline_skeleton.py`: Uses `INSERT OR IGNORE`
- `enrich_timeline_events.py`: Uses `UPDATE OR IGNORE`
- `build_site.py`: Regenerates all HTML on each run

---

## Validation After Each Phase

```bash
sqlite3 db/alchemy_timeline.db ".tables"
sqlite3 db/alchemy_timeline.db "SELECT COUNT(*) FROM timeline_events;"
sqlite3 db/alchemy_timeline.db "SELECT COUNT(*) FROM persons;"
ls site/persons/ | wc -l
```

---

*See `CONTEXT_ENGINEERING.md` for batch enrichment strategy. See `SYSTEM.md` for architecture overview.*
