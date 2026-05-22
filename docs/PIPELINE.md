# ALCHEMYTIMELINEMAP Pipeline Execution Order

**The sequence of Python scripts for building and deploying the portal.**

---

## Phase 1: Initialize Database Schema

### 1. `scripts/init_db.py`

**Purpose:** Create SQLite schema with all 8 tables and CHECK constraints.

```python
# Usage
python scripts/init_db.py

# Does:
# - Creates db/alchemy_timeline.db
# - Creates all 8 tables (timeline_events, persons, texts, concepts, locations, + reference tables)
# - Defines all CHECK constraints for enums
# - Creates indexes for efficient querying
# - Idempotent: creates tables only if they don't exist
```

**Output:** `db/alchemy_timeline.db` with empty schema.

**Preconditions:** None.

**Next step:** Load seed data.

---

## Phase 2: Load Seed Data

### 2. `scripts/load_seed_data.py`

**Purpose:** Ingest initial persons, texts, concepts, and locations from JSON seed files.

```python
# Usage
python scripts/load_seed_data.py

# Does:
# - Reads data/seed_data.json (or separate domain files if split)
# - Inserts persons, texts, concepts, locations (INSERT OR IGNORE)
# - Updates all reference tables (person_event_refs, etc.) if seed includes event relations
# - Idempotent: safe to re-run
```

**Input files:**
- `data/seed_data.json` (or split into `data/persons.json`, `data/texts.json`, etc.)
- Expected format: JSON with keys "persons", "texts", "concepts", "locations"

**Output:** Populated persons, texts, concepts, locations tables.

**Preconditions:** 
- `scripts/init_db.py` must be run first
- `data/seed_data.json` must exist

**Next step:** Load timeline event skeleton (without descriptions yet).

---

## Phase 3: Load Timeline Event Skeleton

### 3. `scripts/load_timeline_skeleton.py` (optional, alternative approach)

**Purpose:** Load 500 timeline event stubs (date, location, involved entities) WITHOUT descriptions yet.

```python
# Usage
python scripts/load_timeline_skeleton.py

# Does:
# - Reads data/timeline_events_skeleton.json
# - Inserts timeline_events with NULL descriptions initially
# - Sets description field to "STUB" or empty
# - Inserts rows into person_event_refs, text_event_refs, concept_event_refs
# - Idempotent: safe to re-run
```

**Input file:** `data/timeline_events_skeleton.json`

**Example format:**
```json
{
  "events": [
    {
      "slug": "event_000001",
      "date_label": "c. 850",
      "date_start_year": 840,
      "date_end_year": 860,
      "location_slug": "baghdad",
      "persons_involved": ["jabir-ibn-hayyan", "al-kindi"],
      "texts_involved": ["kitab-al-hasib"],
      "concepts_involved": ["distillation", "sublimation"]
    },
    ...
  ]
}
```

**Output:** `timeline_events` table with 500 rows, all with NULL or "STUB" descriptions.

**Preconditions:**
- Seed data must be loaded first (so persons, texts, concepts, locations already exist)
- `data/timeline_events_skeleton.json` must exist

**Next step:** Enrich timeline events with descriptions via agent swarm.

---

## Phase 4: Enrich Timeline Events via Agent Swarm

### 4. `scripts/pre_query_batch_context.py` (main session)

**Purpose:** For each batch of events, pre-query all related entities and write batch JSON for agent.

```python
# Usage (manually called for each batch, or wrapped in a loop)
python scripts/pre_query_batch_context.py \
    --batch_id "Medieval_Islam_Iraq_Persia" \
    --output staging/batch_Medieval_Islam_Iraq_Persia.json

# Does:
# - Selects all events in the batch from timeline_events
# - Queries all unique persons, texts, concepts, locations involved
# - Constructs compact JSON context with full entity details
# - Writes to staging/batch_[batch_id].json
```

**Output:** `staging/batch_*.json` files (one per batch of ~20–30 events).

**Preconditions:**
- Timeline event skeleton must be loaded
- Events must be partitioned into batches (era + region)

**Next step:** Agent enriches each batch.

---

### Agent Work: Enrich Event Descriptions

**Agent Type:** Timeline Event Enricher (per PROMPTS.md Part VI)

**Input:** `staging/batch_[batch_id].json` (pre-queried context)

**Task:** Write 100–250 word descriptions for each event, wrapping entity names in `[LINK:slug]` markup.

**Output:** `staging/enriched_events_[batch_id].json`

```json
{
  "batch_id": "Medieval_Islam_Iraq_Persia",
  "enriched_events": [
    {
      "slug": "event_000001",
      "description": "c. 850, Baghdad: The natural philosopher [LINK:al-kindi] and the alchemist [LINK:jabir-ibn-hayyan]..."
    },
    ...
  ],
  "metadata": {
    "confidence": "MEDIUM",
    "review_status": "DRAFT"
  }
}
```

---

### 5. `scripts/enrich_timeline_events.py` (main session)

**Purpose:** Read enriched event JSON from staging, validate, convert markup, load into DB.

```python
# Usage (after each agent batch completes)
python scripts/enrich_timeline_events.py \
    --staging_file staging/enriched_events_Medieval_Islam_Iraq_Persia.json \
    --batch_id "Medieval_Islam_Iraq_Persia"

# Does:
# - Reads enriched JSON from staging/
# - Converts [LINK:slug] → <a href>...</a> tags
# - Validates word counts (100–250)
# - Validates entity references exist in DB
# - Updates timeline_events.description and review_status
# - Moves processed file to staging/PROCESSED_enriched_events_*.json
```

**Input:** `staging/enriched_events_[batch_id].json` (from agent)

**Output:** Updated `timeline_events` table with descriptions.

**Preconditions:**
- Agent must have completed batch enrichment
- Staging file must be present

**Next step:** Repeat for next batch, or move to site generation when all batches complete.

---

## Phase 5: Static Site Generation

### 6. `scripts/build_site.py` (main deploy script)

**Purpose:** Read SQLite, generate all static HTML pages and JSON data exports.

```python
# Usage
python scripts/build_site.py

# Does:
# - Reads all tables from db/alchemy_timeline.db
# - Generates index.html (home page)
# - Generates timeline.html (timeline viewer)
# - Generates map.html (Leaflet.js map)
# - For each person: generates persons/[slug].html
# - For each text: generates texts/[slug].html
# - For each concept: generates concepts/[slug].html
# - Generates data/data.json (all entities + relationships for JS)
# - Generates data/timeline.json (events + map pins for timeline/map views)
# - Generates data/graph.json (D3.js relationship graph)
# - Writes all output to site/
```

**Input:** `db/alchemy_timeline.db` (fully populated)

**Output:** 
- `site/index.html`
- `site/timeline.html`, `site/map.html`
- `site/persons/[slug].html` (100+ files)
- `site/texts/[slug].html` (50+ files)
- `site/concepts/[slug].html` (30+ files)
- `site/data/data.json`, `timeline.json`, `graph.json`
- `site/assets/` (CSS, JS)

**Preconditions:**
- All timeline events must have descriptions
- All persons, texts, concepts must have full content (bio_html, analysis_html, definition_long)
- All tables must be fully populated

**Next step:** Copy to `docs/` and push to GitHub.

---

## Phase 6: Deploy to GitHub Pages

### 7. Copy to `docs/` and Push

```bash
# Copy all generated files from site/ to docs/
cp -r site/* docs/

# Commit and push
git add docs/
git commit -m "Deploy: [phase/batch summary]"
git push origin main
```

**GitHub Pages automatically serves from `docs/` folder.**

---

## Standard Full Pipeline (One-Shot)

```bash
# Phase 1: Initialize schema
python scripts/init_db.py

# Phase 2: Load seed data
python scripts/load_seed_data.py

# Phase 3: Load timeline skeleton
python scripts/load_timeline_skeleton.py

# Phase 4: Agent swarm loop
# For each batch:
#   - python scripts/pre_query_batch_context.py --batch_id [batch]
#   - [Agent enriches batch]
#   - python scripts/enrich_timeline_events.py --staging_file [file]

# Phase 5: Generate static site
python scripts/build_site.py

# Phase 6: Deploy
cp -r site/* docs/
git add docs/
git commit -m "Deploy: 500 events enriched, Phase X complete"
git push origin main
```

---

## Idempotency and Safe Re-Running

All scripts are idempotent:

- `init_db.py`: Creates tables only if they don't exist
- `load_seed_data.py`: Uses `INSERT OR IGNORE` — won't duplicate existing rows
- `load_timeline_skeleton.py`: Uses `INSERT OR IGNORE` — won't duplicate
- `enrich_timeline_events.py`: Uses `UPDATE OR IGNORE` — overwrites existing descriptions safely
- `build_site.py`: Deletes stale HTML files before regenerating (configurable)

**Safe to re-run any script multiple times.**

---

## Debugging and Validation

After each script, validate:

```bash
# Check schema created correctly
sqlite3 db/alchemy_timeline.db ".tables"
sqlite3 db/alchemy_timeline.db "SELECT COUNT(*) FROM timeline_events;"

# Check JSON exports generated
ls -la site/data/

# Check HTML files generated
ls -la site/persons/ | wc -l  # should be ~100
ls -la site/texts/ | wc -l    # should be ~50
ls -la site/concepts/ | wc -l # should be ~30
```

---

## Typical Batch Processing Schedule

**Estimate:** 25 batches of 20 events each = 500 total

**Time per batch:** 
- Pre-query (main): ~30 seconds
- Agent enrichment: ~2–5 minutes (depending on model, batch size)
- Load into DB (main): ~30 seconds
- **Total per batch:** ~3–6 minutes

**Full pipeline:** 25 batches × 5 minutes = 125 minutes (~2 hours) for event enrichment + deployment.

---

*Refer to `CONTEXT_ENGINEERING.md` for detailed batch strategy. Refer to `SYSTEM.md` for architecture overview.*
