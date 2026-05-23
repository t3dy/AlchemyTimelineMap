# AGENT LOADING STRATEGY — ALCHEMYTIMELINEMAP

**Purpose:** Deterministic task routing. Every agent receives an explicit loading contract: "For task X, read files A, B, C (in this order, this many minutes each)."

---

## QUICK REFERENCE: TASK → LOADING CONTRACT

| Task | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 | Layer 6 | Boot Time | Total Tokens |
|------|---------|---------|---------|---------|---------|---------|-----------|------------|
| **Write Timeline Event** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | — | STANDARD_TIMELINE_EVENTS.md (5m) | SCHEMA.json (1m) | Example (3m) | 5m | 1,200–1,500 |
| **Write Person Biography** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | CONCEPTUAL_FRAMEWORK.md (8m) | STANDARD_PERSON_BIOGRAPHIES.md (7m) | SCHEMA.json (1m) | Example (5m) | 5m | 3,000–3,500 |
| **Write Text Description** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | CONCEPTUAL_FRAMEWORK.md (8m) | STANDARD_TEXT_DESCRIPTIONS.md (5m) | SCHEMA.json (1m) | Example (4m) | 5m | 2,200–2,700 |
| **Write Concept Definition** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | CONCEPTUAL_FRAMEWORK.md (8m) | STANDARD_CONCEPT_DEFINITIONS.md (6m) | SCHEMA.json (1m) | Examples (5m) | 5m | 2,500–3,000 |
| **Enrich Events (Batch, 20–50)** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | — | STANDARD_TIMELINE_EVENTS.md (5m) | CONTEXT_ENGINEERING.md (8m) | — | 5m | 1,600–2,000 |
| **Debug/Fix Invalid Link** | CLAUDE.md (5m) | — | — | — | SCHEMA.json (1m) | — | 5m | 500–800 |
| **Deploy Site (GitHub Pages)** | CLAUDE.md (5m) | PHASESTATUS.md (2m) | — | — | PIPELINE.md (3m) | — | 5m | 800–1,200 |
| **Schema Validation Update** | CLAUDE.md (5m) | — | — | — | SCHEMA.json (1m), CONTRACTS.json (2m) | — | 5m | 600–900 |

---

## DETAILED LOADING CONTRACTS BY TASK

### Task: Write a Single Timeline Event

**Trigger:** "I need to write a new timeline event for [date/event]"

**Loading sequence (16 minutes, 1,200–1,500 tokens):**

1. **Layer 0 (5 min):** Read `CLAUDE.md` (400w)
   - Get mission and core invariants
   - Confirm current phase
   - Understand routing

2. **Layer 1 (2 min):** Read `PHASESTATUS.md` (skim for "What's next" section)
   - Confirm you're in the right phase
   - Check if timeline event enrichment is in scope

3. **Layer 3 (5 min):** Read `STANDARD_TIMELINE_EVENTS.md` (400w)
   - Word count: 100–250 words
   - Required fields: date_label, location, description, persons_involved, texts_involved, concepts_involved
   - Validation checklist
   - Example passing entry

4. **Layer 4 (1 min):** Skim `SCHEMA.json` (just the timeline_event section)
   - Confirm enum values for location, confidence, review_status
   - Confirm word count range matches STANDARD_TIMELINE_EVENTS.md

5. **Layer 6 (3 min, optional):** Read example timeline event from `archive/`
   - See what a passing entry looks like
   - Note how entity links are formatted

**Do NOT load:** Layer 2 (historiography), Layer 7 (archive)

**Quality gate:** Word count check, required fields present, entity slugs valid (check against SCHEMA.json enum)

---

### Task: Write a Person Biography (Historical Alchemist or Scholar)

**Trigger:** "I need to expand the biography of [person name] or write a new biography for [person]"

**Loading sequence (28 minutes, 3,000–3,500 tokens):**

1. **Layer 0 (5 min):** Read `CLAUDE.md` (400w)
   - Mission, invariants, routing

2. **Layer 1 (2 min):** Read `PHASESTATUS.md` (skim for status on person expansion)
   - Confirm phase scope

3. **Layer 2 (8 min):** Read `CONCEPTUAL_FRAMEWORK.md` (2,000w, sections § 1–3, § 5)
   - Project vision and three constituencies
   - Historiographical framework: Actor/Analyst distinction, medieval continuity, material culture
   - Key scholarly authorities
   - **Why:** Person biographies must be grounded in historiographical principles (not hagiography, not esoteric lore)
   - **How:** Use examples from CONCEPTUAL_FRAMEWORK.md to justify editorial choices

4. **Layer 3 (7 min):** Read `STANDARD_PERSON_BIOGRAPHIES.md` (500w)
   - Word count: 1,200–2,200 words
   - Required sections: opening paragraph, main narrative, historiographical disputes, material culture (if applicable), legacy
   - Bibliography format (DGWE model)
   - Validation checklist
   - Example passing biography

5. **Layer 4 (1 min):** Skim `SCHEMA.json` (persons table section)
   - Confirm role_primary enum values (ALCHEMIST, CHEMIST, SCHOLAR, etc.)
   - Confirm era enum values (MEDIEVAL, RENAISSANCE, EARLY_MODERN, etc.)

6. **Layer 6 (5 min, optional):** Read worked example person biography from `archive/`
   - Study how historiographical disputes are presented
   - Note how sources are cited
   - Examine entity links to other persons, texts, concepts

**Do NOT load:** Layer 7 (archive)

**Quality gate:** Word count check, all required sections present, historiographical grounding evident, bibliography format matches DGWE model, entity links valid

---

### Task: Write a Text Description (Primary Source, Commentary, or Scholarship)

**Trigger:** "I need to write a description of [text] or expand the entry for [manuscript/printed work]"

**Loading sequence (22 minutes, 2,200–2,700 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md`

2. **Layer 1 (2 min):** `PHASESTATUS.md` (skim for text expansion status)

3. **Layer 2 (8 min):** `CONCEPTUAL_FRAMEWORK.md` (§ 1–4, focus on historiographical principles for textual transmission)
   - Understand how to describe textual tradition and transmission chains
   - Key authorities for primary source interpretation

4. **Layer 3 (5 min):** `STANDARD_TEXT_DESCRIPTIONS.md` (450w)
   - Word count: varies by type (primary sources: 1,000–1,800w; scholarship: 800–1,200w)
   - Required sections: composition/publication, content summary, historiographical significance, textual tradition
   - Bibliography format
   - Example passing entries

5. **Layer 4 (1 min):** Skim `SCHEMA.json` (texts table section)
   - Confirm text_type enum (PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA)
   - Confirm era enum

6. **Layer 6 (4 min, optional):** Read worked example text description
   - Study how primary sources are contextualized
   - Note how textual tradition is described

**Quality gate:** Word count check, required sections, bibliography formatted, historiographical significance clear, entity links valid

---

### Task: Write a Concept Definition (ACTOR_TERM or ANALYST_TERM)

**Trigger:** "I need to define [alchemy concept] or expand the definition of [operation/theory]"

**Loading sequence (26 minutes, 2,500–3,000 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md`

2. **Layer 1 (2 min):** `PHASESTATUS.md` (skim for concept expansion scope)

3. **Layer 2 (8 min):** `CONCEPTUAL_FRAMEWORK.md` (§ 3, § 5—focus on Actor/Analyst distinction and material culture)
   - Critical: Understand the difference between ACTOR_TERM (historical actor's concept) and ANALYST_TERM (modern scholarly concept)
   - Understand material grounding and embodied knowledge
   - Key authorities for alchemical operations vs. modern chemistry

4. **Layer 3 (6 min):** `STANDARD_CONCEPT_DEFINITIONS.md` (550w)
   - Word count: definition_short 60–120w, definition_long 1,500–2,500w
   - Critical rule: ACTOR_TERM vs. ANALYST_TERM distinction (separate definitions)
   - Required sections (both types): historical usage, scholarly interpretation, relationship to operations
   - For ACTOR_TERMs: grounding in primary sources and material practices
   - For ANALYST_TERMs: historiographical significance and scholarly debates
   - Validation checklist
   - Example entries (both types)

5. **Layer 4 (1 min):** Skim `SCHEMA.json` (concepts table section)
   - Confirm category_type enum (ACTOR_TERM, ANALYST_TERM)

6. **Layer 6 (5 min, optional):** Read worked example concept definitions
   - Study ACTOR_TERM example (e.g., DISTILLATION as historical operation)
   - Study ANALYST_TERM example (e.g., TRANSMUTATION as historiographical category)
   - Note how definitions differ in focus and grounding

**Do NOT load:** Layer 7

**Quality gate:** Word count correct, category_type clear, section requirements met, material grounding present (ACTOR_TERM), historiographical debate discussed (ANALYST_TERM), entity links valid

---

### Task: Enrich Timeline Events in Batch (20–50 events)

**Trigger:** "I need to enrich [20–50 timeline events] with descriptions"

**Loading sequence (21 minutes, 1,600–2,000 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md`

2. **Layer 1 (2 min):** `PHASESTATUS.md` (confirm batch scope)

3. **Layer 3 (5 min):** `STANDARD_TIMELINE_EVENTS.md`
   - Word count per event: 100–250w
   - Required fields
   - Quick validation checklist

4. **Layer 4 (8 min):** `CONTEXT_ENGINEERING.md`
   - Read this FIRST if doing batch enrichment
   - Understand the batch strategy: pre-query entities, load context once, enrich multiple events in sequence
   - Learn the staging pattern (write to staging/*, validate before DB insertion)
   - Learn the 5-step batch workflow

5. **Layer 6 (optional, 1–2 min):** Brief skim of example timeline event

**Do NOT load:** Layer 2 (historiography not needed for bulk enrichment), Layer 7

**Quality gate:** Word count check per event, entity slug validity, consistency across batch, provenance metadata complete (source_method, confidence, review_status)

---

### Task: Debug or Fix Invalid Entity Link

**Trigger:** "I got a validation error: entity link [LINK:slug] does not exist"

**Loading sequence (7 minutes, 500–800 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md` (quick skim for pipeline rules)

2. **Layer 4 (2 min):** `SCHEMA.json` (entity slug format, enum values)
   - Understand slug naming convention (lowercase, hyphens, no special chars)
   - Check if slug exists in database
   - Verify enum value is valid

**Quality gate:** Slug validation, existence check, enum value confirmation

**Next action:** If slug doesn't exist, either:
- Create the entity (new person, text, concept, location)
- Fix the typo in the link
- Confirm with human editor that entity is in scope

---

### Task: Deploy Site to GitHub Pages

**Trigger:** "I need to generate the static site and deploy to GitHub Pages"

**Loading sequence (10 minutes, 800–1,200 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md` (confirm pipeline rules)

2. **Layer 1 (2 min):** `PHASESTATUS.md` (check current phase, event count accuracy)

3. **Layer 4 (3 min):** `PIPELINE.md`
   - Script execution order
   - Database state requirements
   - Output directory (docs/ or site/)
   - Verification steps

**Do NOT load:** Layer 2, 3, 5, 6, 7

**Quality gate:** Pipeline script success, no validation errors, site/ or docs/ directory updated, GitHub Pages deployed

---

### Task: Update Database Schema or Validation Rules

**Trigger:** "I need to add a new enum value, change word count rules, or modify schema"

**Loading sequence (8 minutes, 600–900 tokens):**

1. **Layer 0 (5 min):** `CLAUDE.md` (confirm vocabulary lock rules)

2. **Layer 4 (3 min):** Both `SCHEMA.json` and `CONTRACTS.json`
   - Understand current schema structure
   - Identify where enum is defined
   - Identify what validation contracts need updating

**Action:** 
- Update SCHEMA.json (source of truth for enums and word counts)
- Update ONTOLOGY.md (reference documentation)
- Update scripts/init_db.py CHECK constraints
- Re-run validation script to verify

---

## AUTHORITY RULES FOR LOADING CONTRACTS

**Rule 1: File precedence in loading sequence is authority precedence.**
- If you load Layer 3 (STANDARD_TIMELINE_EVENTS.md) and it says 100–250 words, but Layer 6 example shows 200–300 words, the standard (Layer 3) is authoritative.
- If you load Layer 4 (SCHEMA.json) and it contradicts Layer 3, the schema is authoritative.

**Rule 2: Never skip Layer 0 or Layer 1.**
- Every agent must read CLAUDE.md to understand mission and invariants.
- Every agent must check PHASESTATUS.md to confirm task is in current phase scope.

**Rule 3: Layer 2 (historiography) is required only for substantive editorial decisions.**
- Write timeline event? No Layer 2 (structural task).
- Write person biography? Yes Layer 2 (requires historiographical judgment).
- Write concept definition? Yes Layer 2 (requires understanding of Actor/Analyst distinction).

**Rule 4: Layer 6 (examples) is always optional but strongly recommended.**
- First time writing type X? Load an example.
- Routine batch enrichment? Skip the example.

**Rule 5: Never auto-load Layer 7.**
- Archive files are historical only.
- Only read if explicitly asked "what was the old approach?"

---

## IMPLEMENTATION: AGENT PROMPT INJECTION

When agent starts, inject this contract into system message:

```
You are working on task: [TASK_NAME]

Your loading contract (deterministic, non-negotiable):
1. Read files in this order: [FILE_LIST]
2. Total reading time: [TIME] minutes, [TOKEN_COUNT] tokens
3. Authority hierarchy for this task: [HIERARCHY]
4. Quality gates: [CHECKLIST]

Do not read files outside this contract. Do not ask "should I read X?" The contract is determined by your task type. Follow it.
```

---

## TESTING LOADING CONTRACTS

For each task type, a human should verify:

- [ ] Agent reads exactly the files in the contract (no more, no fewer)
- [ ] Agent completes task in the estimated time
- [ ] Token count is within budget
- [ ] Agent does not ask "should I read..." (contract is explicit)
- [ ] Quality gates are mechanically checkable (no ambiguity)
- [ ] No file is read twice (efficient)
- [ ] All prerequisites are loaded before execution

---

*Next document: TOKEN_ECONOMY_AUDIT.md*
