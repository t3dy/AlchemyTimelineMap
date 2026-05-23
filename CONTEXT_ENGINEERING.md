# Context Engineering for ALCHEMYTIMELINEMAP

**How to efficiently query and enrich 500 timeline events without context explosion.**

---

## The Problem

500 timeline events × 3–5 related entities per event = 1,500–2,500 entity references. If an agent receives all 500 event stubs plus full entity descriptions in a single prompt, the context window explodes. Even if it fits, token efficiency suffers.

**Solution:** Batch processing with pre-loaded entity context.

---

## The Pattern: Batch + Pre-Query

Instead of:
```
Agent: "Here are 500 events. Enrich them."  ← Context explosion
```

We do:

```
Main session: "Here are 20 events from MEDIEVAL IBERIA."
              "Here are the 35 persons/texts/concepts involved."
              "Enrich these 20 events with descriptions."
                ↓
Agent: Receives focused batch + complete entity context
       Writes 20 event descriptions to staging/
                ↓
Main session: Reads staging/, converts [LINK:slug] to <a href>, loads into DB
```

---

## Step 1: Partition Timeline Events into Batches

Group the 500 events by **era + region** for efficient processing:

**Batches (example):**
- `Late_Antique_Egypt_Syria` (25 events)
- `Medieval_Islam_Iraq_Persia` (40 events)
- `Medieval_Islam_Iberia` (30 events)
- `Medieval_Latin_Europe` (35 events)
- `Renaissance_Italy` (40 events)
- `Early_Modern_Central_Europe` (45 events)
- `Early_Modern_England` (30 events)
- `Early_Modern_Low_Countries` (45 events)
- ... (10–15 total batches)

Each batch should have **15–30 events** (not 500 at once).

---

## Step 2: Pre-Query Entity Context for Each Batch

Before sending a batch to an agent, the main session queries the database for all entities involved:

```python
batch_id = "Medieval_Islam_Iraq_Persia"
events = db.query(
    "SELECT slug, date_label, location_slug, persons_involved, texts_involved, concepts_involved "
    "FROM timeline_events WHERE batch_group = ? ORDER BY date_start_year",
    [batch_id]
)

person_slugs = set()
text_slugs = set()
concept_slugs = set()
for event in events:
    person_slugs.update(json.loads(event['persons_involved'] or '[]'))
    text_slugs.update(json.loads(event['texts_involved'] or '[]'))
    concept_slugs.update(json.loads(event['concepts_involved'] or '[]'))

persons = db.query("SELECT slug, name, role_primary, era FROM persons WHERE slug IN (?)", [person_slugs])
texts = db.query("SELECT slug, title, text_type FROM texts WHERE slug IN (?)", [text_slugs])
concepts = db.query("SELECT slug, label, category_type FROM concepts WHERE slug IN (?)", [concept_slugs])

context = {
    "batch_id": batch_id,
    "events": events,
    "entities": {"persons": persons, "texts": texts, "concepts": concepts,
                 "locations": db.query("SELECT slug, place_name FROM locations")}
}

with open(f"staging/batch_{batch_id}.json", "w") as f:
    json.dump(context, f)
```

---

## Step 3: Agent Receives Focused Context

The agent receives a JSON file with 20–30 event stubs and all entity names/slugs it needs:

```json
{
  "batch_id": "Medieval_Islam_Iraq_Persia",
  "events": [
    {"slug": "event_000042", "date_label": "c. 850", "location_slug": "baghdad",
     "persons_involved": ["jabir-ibn-hayyan", "al-kindi"],
     "texts_involved": ["kitab-al-hasib"],
     "concepts_involved": ["distillation", "sublimation"]}
  ],
  "entities": {
    "persons": [{"slug": "jabir-ibn-hayyan", "name": "Jabir ibn Hayyan", "role_primary": "ALCHEMIST"}],
    "texts": [{"slug": "kitab-al-hasib", "title": "Kitāb al-Ḥāsib", "text_type": "PRIMARY_SOURCE"}],
    "concepts": [{"slug": "distillation", "label": "Distillation", "category_type": "ACTOR_TERM"}]
  }
}
```

---

## Step 4: Agent Output Format

```json
{
  "batch_id": "Medieval_Islam_Iraq_Persia",
  "enriched_events": [
    {
      "slug": "event_000042",
      "description": "c. 850, Baghdad: [LINK:jabir-ibn-hayyan] and [LINK:al-kindi] collaborate at the House of Wisdom, developing techniques of [LINK:distillation] and [LINK:sublimation] documented in the [LINK:kitab-al-hasib]..."
    }
  ],
  "metadata": {"confidence": "MEDIUM", "review_status": "DRAFT", "source_method": "AI_ASSISTED"}
}
```

---

## Step 5: Main Session Processes and Loads

1. Read enriched JSON from staging/
2. Convert `[LINK:slug]` to `<a href="../persons/[slug].html">[name]</a>`
3. Validate word counts (100–250), historiographical significance, entity references
4. Load descriptions into `timeline_events.description`
5. Update `review_status` to REVIEWED or flag for human review

---

## Token Efficiency

**Without batching (all 500 events at once):**
- Context tokens: ~50,000–80,000
- Quality: Lower (agent loses track)

**With batching (20 events + entity context):**
- Context tokens: ~5,000–8,000 per batch
- Total for 500 events: 25 batches × 8,000 = 200,000 (but distributed across sessions, higher quality)

---

## Implementation Checklist

- [ ] Define batch partitions (era + region combinations)
- [ ] Assign each of 500 events to a batch
- [ ] Write main session pre-query script
- [ ] Create agent prompt template with example batch JSON
- [ ] Define output validation rules
- [ ] Create `[LINK:slug]` → `<a href>` conversion script
- [ ] Test with pilot batch (20 Medieval Islamic events) before full run

---

*For detailed schema see `ONTOLOGY.md`. For pipeline execution order see `PIPELINE.md`.*
