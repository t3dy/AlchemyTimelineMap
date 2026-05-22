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
# Pseudo-code for main session
batch_id = "Medieval_Islam_Iraq_Persia"
events = db.query(
    "SELECT slug, date_label, location, persons_involved, texts_involved, concepts_involved 
     FROM timeline_events WHERE batch_id = ? ORDER BY date_start_year", 
    [batch_id]
)

# Fetch all unique entities involved in this batch
person_slugs = set()
text_slugs = set()
concept_slugs = set()
for event in events:
    person_slugs.update(json.loads(event['persons_involved']))
    text_slugs.update(json.loads(event['texts_involved']))
    concept_slugs.update(json.loads(event['concepts_involved']))

# Query full data for these entities
persons = db.query(
    "SELECT slug, name, role_primary, era FROM persons WHERE slug IN (?)",
    [person_slugs]
)
texts = db.query(
    "SELECT slug, title, text_type FROM texts WHERE slug IN (?)",
    [text_slugs]
)
concepts = db.query(
    "SELECT slug, label, category_type FROM concepts WHERE slug IN (?)",
    [concept_slugs]
)

# Build compact JSON context
context = {
    "batch_id": batch_id,
    "events": events,
    "entities": {
        "persons": persons,
        "texts": texts,
        "concepts": concepts,
        "locations": db.query("SELECT slug, place_name FROM locations")  # all for reference
    }
}

# Save to JSON file for agent
with open("staging/batch_Medieval_Islam_Iraq_Persia.json", "w") as f:
    json.dump(context, f)
```

---

## Step 3: Agent Receives Focused Context

The agent receives a JSON file like:

```json
{
  "batch_id": "Medieval_Islam_Iraq_Persia",
  "instructions": "For each event stub, write a 100–250 word description...",
  "events": [
    {
      "slug": "event_000042",
      "date_label": "c. 850",
      "location_slug": "baghdad",
      "persons_involved": ["jabir-ibn-hayyan", "al-kindi"],
      "texts_involved": ["kitab-al-hasib"],
      "concepts_involved": ["distillation", "sublimation"]
    },
    ...
  ],
  "entities": {
    "persons": [
      {"slug": "jabir-ibn-hayyan", "name": "Jabir ibn Hayyan", "role_primary": "ALCHEMIST", "era": "MEDIEVAL"},
      {"slug": "al-kindi", "name": "Al-Kindi", "role_primary": "PHILOSOPHER", "era": "MEDIEVAL"},
      ...
    ],
    "texts": [
      {"slug": "kitab-al-hasib", "title": "Kitāb al-Ḥāsib", "text_type": "PRIMARY_SOURCE"},
      ...
    ],
    "concepts": [
      {"slug": "distillation", "label": "Distillation", "category_type": "ACTOR_TERM"},
      {"slug": "sublimation", "label": "Sublimation", "category_type": "ACTOR_TERM"},
      ...
    ],
    "locations": [
      {"slug": "baghdad", "place_name": "Baghdad"},
      ...
    ]
  }
}
```

**Agent task:**
> "For each event stub, write a 100–250 word description incorporating the context provided. When mentioning a person, text, or concept that exists in the entity list, wrap it in `[LINK:slug]` markup. Output to `staging/enriched_events_Medieval_Islam_Iraq_Persia.json`."

---

## Step 4: Agent Output Format

The agent writes back:

```json
{
  "batch_id": "Medieval_Islam_Iraq_Persia",
  "enriched_events": [
    {
      "slug": "event_000042",
      "description": "c. 850, Baghdad: The natural philosopher [LINK:al-kindi] and the alchemist [LINK:jabir-ibn-hayyan] collaborate in Baghdad's House of Wisdom, discussing the principles of distillation described in the [LINK:kitab-al-hasib]. Their work establishes [LINK:distillation] as a reproducible operation yielding measurable products, shifting alchemy from mystical speculation toward empirical practice. This collaboration represents the apex of early Islamic alchemical science and will influence Latin translations centuries later."
    },
    ...
  ],
  "metadata": {
    "timestamp": "2026-05-22T14:00:00Z",
    "confidence": "MEDIUM",
    "review_status": "DRAFT",
    "agent_type": "Timeline Event Enricher"
  }
}
```

---

## Step 5: Main Session Processes and Loads

The main session:

1. Reads the enriched JSON from staging
2. Converts `[LINK:slug]` to `<a href="../persons/[slug].html">[name]</a>` (using entity context to look up names)
3. Validates word counts, historiographical significance, entity references
4. Loads descriptions into `timeline_events.description` field
5. Updates `timeline_events.review_status` to "REVIEWED" or flags for human review if any issues

```python
# Pseudo-code for main session
with open("staging/enriched_events_Medieval_Islam_Iraq_Persia.json") as f:
    enriched = json.load(f)

for event in enriched['enriched_events']:
    slug = event['slug']
    description = event['description']
    
    # Convert [LINK:slug] to <a> tags
    def replace_links(text):
        pattern = r'\[LINK:(\w+)\]'
        def resolve(match):
            entity_slug = match.group(1)
            # Look up entity name from context
            entity = find_entity_by_slug(entity_slug)
            entity_type = entity['type']  # 'person', 'text', 'concept'
            entity_name = entity['name']
            href = f"../{entity_type}s/{entity_slug}.html"
            return f'<a href="{href}">{entity_name}</a>'
        return re.sub(pattern, resolve, text)
    
    description_html = replace_links(description)
    
    # Validate
    word_count = len(description.split())
    if word_count < 100 or word_count > 250:
        print(f"WARNING: {slug} is {word_count} words (should be 100-250)")
        review_status = "DRAFT"
    else:
        review_status = "REVIEWED"
    
    # Load into DB
    db.execute(
        "UPDATE timeline_events SET description = ?, review_status = ? WHERE slug = ?",
        [description_html, review_status, slug]
    )
    
    db.commit()
```

---

## Token Efficiency Analysis

**Without batching (all 500 events at once):**
- Agent receives: ~500 events + all persons/texts/concepts
- Tokens for context: ~50,000–80,000 (wasted on repetition)
- Response quality: Lower (agent loses track across 500 events)

**With batching (20 events + entity context):**
- Agent receives: ~20 events + 35–50 unique entities
- Tokens for context: ~5,000–8,000 (focused, reusable)
- Response quality: Higher (agent can focus on coherent historical narratives)
- Total tokens for all 500 events: 5,000 × 25 batches = 125,000 (lower cost than single pass, higher quality)

**Key win:** The 20-event batches allow narrative coherence (related events in same region/era create natural storytelling context). The agent can write descriptions that reference earlier events in the batch, creating a flowing historical narrative.

---

## Implementation Checklist

- [ ] Define batch partitions (era + region combinations)
- [ ] Create partition assignment for 500 event stubs (which batch each event belongs to)
- [ ] Write main session script to pre-query entity context for each batch
- [ ] Create agent prompt template for Timeline Event Enricher with example batch JSON
- [ ] Define output validation rules (word count, entity link coverage, historiographical significance)
- [ ] Create conversion script for `[LINK:slug]` → `<a href>` tags
- [ ] Test with pilot batch (e.g., 20 Medieval Islamic events) before full swarm

---

## Example: Pilot Batch

**Batch:** Medieval_Islam_Iraq_Persia (c. 750–1050)
**Events:** 20 stubs
**Unique entities:** 12 persons, 8 texts, 6 concepts

**Persons involved:** Jabir ibn Hayyan, Al-Kindi, Al-Razi, Abu Ma'shar, etc.
**Texts:** Kitāb al-Ḥāsib, Risālat al-Asrār, etc.
**Concepts:** Distillation, Sublimation, Calcination, Transmutation, etc.

**Token budget for batch:** ~8,000 tokens (5,000 for context + 3,000 for response)

---

*For each batch, use this pattern. Scale to all 500 events via ~25 batches over several sessions.*
