# PROGRESSIVE REVELATION CRITIQUE — ALCHEMYTIMELINEMAP

**Purpose:** Analyze whether the refactored architecture truly supports progressive disclosure (start simple, add complexity only when needed). Identify where conceptual material still leaks into operational docs, where onboarding contains unnecessary philosophy, where technical docs duplicate historiography.

---

## DEFINITION: PROGRESSIVE REVELATION

A system supports progressive revelation when:

1. **Boot layer is minimal.** Agent can start with 300–500 words and understand task routing.
2. **Each layer adds context only for that layer's decisions.** No philosophy in operational standards; no standards in conceptual framework.
3. **Optional complexity is marked optional.** Agent never wonders "should I read this?"
4. **No layer duplicates information from another layer.** Single source of truth for each concept.
5. **Agent can complete most tasks by reading 1,200–1,500 tokens total.** Less than 5 minutes of reading.

---

## CURRENT SYSTEM: PROGRESSIVE REVELATION FAILURE ANALYSIS

### Layer 0 (Boot) — CURRENT STATE

**File:** CLAUDE.md (2,600w)

**Content analysis:**
- § 1 Mission + core invariants (200w) ← **CORRECT, 5 min read**
- § 2 Task routing (300w) ← **CORRECT, minimal**
- § 3 Project vision (400w) ← **LEAK: Should be in Layer 2**
- § 4 Historiographical principles (700w) ← **LEAK: Should be in Layer 2**
- § 5 Key authorities (200w) ← **LEAK: Should be in Layer 2**
- § 6 Architecture diagram (300w) ← **LEAK: Should be in Layer 4 (docs/SYSTEM.md)**
- § 7 Data flow (200w) ← **LEAK: Should be in Layer 4 (docs/PIPELINE.md)**
- § 8 Vocabulary lock (300w) ← **LEAK: Should be in Layer 4 (docs/VOCABULARY.md)**
- § 9 Schema summary (200w) ← **LEAK: Should be reference only (docs/ONTOLOGY.md)**
- § 10 Checking your work (100w) ← **CORRECT for boot**

**Progressive revelation failure:** 
- Agent arrives and reads 2,600 words when they only need 500 words to get started
- Historiography (§ 3–5) adds 1,300 words for agents who don't need it (timeline event writers)
- Architecture details (§ 6–7) add 500 words for agents who won't modify the system
- Vocabulary definitions (§ 8–9) add 600 words when they should reference external doc

**Cognitive cost:** Agent must filter out 2,100 words of "not needed for my task" context

---

### Layer 1 (Project State) — CURRENT STATE

**File:** PHASESTATUS.md (1,200w) + PROJECT_SUMMARY.md (500w) + SESSION_SUMMARY.md (500w)

**Problem:** Three files, same information at different times
- PHASESTATUS.md: current state (correct)
- PROJECT_SUMMARY.md: Phase 0/1 snapshot (stale, from earlier work)
- SESSION_SUMMARY.md: working notes from previous session (archival)

**Progressive revelation failure:**
- Agent doesn't know which file to trust
- Dates are implicit (SESSION_SUMMARY is stale, doesn't state when)
- Has to read all three to understand what's canonical

**Fix:** PHASESTATUS.md is only source of truth; move others to archive

---

### Layer 2 (Conceptual Framework) — CURRENT STATE

**Files:** PROMPTS.md (4,000w) + scattered historiographical preambles in agent prompts

**Content analysis:**
- § 1 Project vision (200w) ← **CORRECT**
- § 2 Three constituencies (300w) ← **CORRECT**
- § 3 Historiographical principles (1,200w) ← **CORRECT**
- § 4 Key authorities (200w) ← **CORRECT**
- § 5 Actor/Analyst distinction (500w) ← **CORRECT**
- § 6 Agent operating rules (400w) ← **LEAK: Should be in Layer 3 task prompts**
- § 7 Vocabulary lock (200w) ← **LEAK: Should be in Layer 4**
- § 8 Detailed examples (1,000w) ← **LEAK: Should be in Layer 6**
- § 9 Content standards (500w) ← **LEAK: Should be in Layer 3**

**Progressive revelation failure:**
- Timeline event writers don't need historiography, but it's baked into PROMPTS.md
- Agent must read full 4,000w to understand task-specific standards (mixed with historiography)
- No clear boundary between "conceptual" (historiography) and "operational" (standards, rules)

**Why this matters:** A timeline event enrichment task should NOT require understanding historiographical principles about medieval continuity. But current PROMPTS.md mixes both.

---

### Layer 3 (Operational Standards) — CURRENT STATE

**Files:** STYLEGUIDE.md (2,000w consolidated, or scattered across 3 files)

**Content analysis:**
- § 1 General prose principles (300w) ← **CORRECT**
- § 2 Person biographies (800w) ← **CORRECT for person bio task**
- § 3 Text descriptions (600w) ← **CORRECT for text task**
- § 4 Timeline events (400w) ← **CORRECT for timeline task**
- § 5 Concept definitions (700w) ← **CORRECT for concept task**
- § 6 Bibliography format (200w) ← **LEAK: Applies to all; not task-specific**

**Progressive revelation failure:**
- All tasks must read full STYLEGUIDE.md
- Bibliography rules are repeated in § 2, 3, 5 (duplication)
- Agent writing timeline events reads 2,000w of STYLEGUIDE when only 400w is relevant
- Agent gets lost in § 1 (general prose) when they need specific rules (§ 4)

---

### Layer 4 (Technical Contracts & Schema) — CURRENT STATE

**Files:** docs/ONTOLOGY.md (1,400w prose) + docs/VOCABULARY.md (500w) + scattered in CLAUDE.md (§ 9)

**Content analysis:**
- docs/ONTOLOGY.md: Prose schema with mixed explanation (should be JSON schema)
- docs/VOCABULARY.md: Enum reference (should be derived from schema, not separate)
- CLAUDE.md § 9: Duplicate enum list (should reference docs/VOCABULARY.md)

**Progressive revelation failure:**
- Enums are defined in 3 places (duplication)
- No single machine-readable source of truth
- Agent must cross-reference prose + reference + CLAUDE.md to verify valid values
- Schema is embedded in prose (hard to validate programmatically)

**Why this matters:** Validation rules are interpretive rather than mechanical

---

### Layer 5 (Executable Validation) — CURRENT STATE

**Status:** Does not exist

**Progressive revelation failure:**
- No validation scripts
- All rules are prose
- Agents are trusted to read rules and follow them
- Inconsistencies aren't caught until database ingestion fails

---

### Layer 6 (Examples & Reference) — CURRENT STATE

**Files:** Mostly absent (need creation)

**Progressive revelation failure:**
- No worked examples
- Agent has no concrete "show me what good looks like"
- Agents must infer from descriptions in prose standards

---

### Layer 7 (Archive & History) — CURRENT STATE

**Status:** Not organized; files scattered

**Progressive revelation failure:**
- Old versions clutter root directory
- Agent is tempted to read OLD CLAUDE_NEW.md instead of understanding it's superseded
- No clear deprecation notices

---

## POST-REFACTOR SYSTEM: PROGRESSIVE REVELATION SUCCESS ANALYSIS

### Progressive Revelation Path 1: Write Timeline Event

**Reading:**
1. CLAUDE.md (400w, 5 min) ← Layer 0
2. PHASESTATUS.md (skim, 2 min) ← Layer 1
3. STANDARD_TIMELINE_EVENTS.md (400w, 5 min) ← Layer 3
4. docs/SCHEMA.json (timeline section, 100w, 1 min) ← Layer 4
5. Example (optional, 3 min) ← Layer 6

**Total:** 16 minutes, 1,200–1,500 tokens

**Progressive revelation achieved:**
- ✓ Agent starts with 400w (clear mission)
- ✓ Agent confirms phase (2 min)
- ✓ Agent learns task-specific standards only (400w, not 2,000w)
- ✓ Agent skims schema for enums (1 min)
- ✓ Agent optionally sees example
- ✓ Agent never reads historiography (not needed)
- ✓ Agent never reads person bio standards (not relevant)
- ✓ No decision ambiguity (contract is explicit)

---

### Progressive Revelation Path 2: Write Person Biography

**Reading:**
1. CLAUDE.md (400w, 5 min) ← Layer 0
2. PHASESTATUS.md (skim, 2 min) ← Layer 1
3. CONCEPTUAL_FRAMEWORK.md (2,000w, 8 min) ← Layer 2 **[REQUIRED for editorial depth]**
4. STANDARD_PERSON_BIOGRAPHIES.md (500w, 7 min) ← Layer 3
5. docs/SCHEMA.json (persons section, 100w, 1 min) ← Layer 4
6. Example (optional, 5 min) ← Layer 6

**Total:** 28 minutes, 3,000–3,500 tokens

**Progressive revelation achieved:**
- ✓ Agent starts with 400w (mission)
- ✓ Agent confirms phase (2 min)
- ✓ Agent reads historiography ONLY because they need it for biography depth (8 min)
- ✓ Agent then learns task-specific standards (500w, not full 2,000w STYLEGUIDE.md)
- ✓ Agent skims schema
- ✓ No reading of timeline event standards (not relevant)
- ✓ No reading of text standards (not relevant)
- ✓ Historiography is in one place (CONCEPTUAL_FRAMEWORK.md), linked but optional for timeline events

**Key insight:** Agent reads historiography BECAUSE THEY NEED IT, not because it's contaminating boot layer

---

### Progressive Revelation Path 3: Deploy Site

**Reading:**
1. CLAUDE.md (400w, 5 min) ← Layer 0
2. PHASESTATUS.md (skim, 2 min) ← Layer 1
3. docs/PIPELINE.md (900w, 3 min) ← Layer 4

**Total:** 10 minutes, 800 tokens

**Progressive revelation achieved:**
- ✓ Agent reads ONLY pipeline order (no historiography, no content standards)
- ✓ Boot layer doesn't bloat with "deployment details"
- ✓ No reading of person bio or timeline standards (not relevant)

---

## LAYER BLEED ANALYSIS

### Definition: Layer Bleed

Layer bleed occurs when information from one layer appears in another layer where it shouldn't belong.

| Bleed Type | Current | Post-Refactor | Status |
|-----------|---------|---------------|--------|
| **Historiography in Layer 0 (boot)** | CLAUDE.md § 3–5 (1,300w) | Removed → CONCEPTUAL_FRAMEWORK.md | **FIXED** |
| **Architecture in Layer 0 (boot)** | CLAUDE.md § 6–7 (500w) | Removed → docs/SYSTEM.md, docs/PIPELINE.md | **FIXED** |
| **Enum definitions in Layer 0 (boot)** | CLAUDE.md § 8–9 (600w) | Removed → docs/VOCABULARY.md, docs/SCHEMA.json | **FIXED** |
| **Agent rules in Layer 2 (conceptual)** | PROMPTS.md § 6 (400w) | Removed → task-specific prompts | **FIXED** |
| **Standards in Layer 2 (conceptual)** | PROMPTS.md § 9 (500w) | Removed → Layer 3 STANDARD_*.md | **FIXED** |
| **Examples in Layer 2 (conceptual)** | PROMPTS.md § 8 (1,000w) | Removed → Layer 6 docs/reference/examples/ | **FIXED** |
| **All standards in Layer 3 (operational)** | STYLEGUIDE.md (2,000w all at once) | Split into 4 task-specific files | **FIXED** |
| **Historiography preambles in agent prompts** | Each task prompt (300w × 4) | Removed → link to CONCEPTUAL_FRAMEWORK.md | **FIXED** |
| **Vocabulary in multiple places** | PROMPTS.md + CLAUDE.md + docs/VOCABULARY.md (4 places) | Single source: docs/SCHEMA.json | **FIXED** |
| **Phase status in multiple places** | PHASESTATUS.md + PROJECT_SUMMARY.md + SESSION_SUMMARY.md + CLAUDE.md | Single source: PHASESTATUS.md | **FIXED** |

---

## CONCEPTUAL MATERIAL LEAKAGE: DETAILED EXAMPLES

### Example 1: Historiography Bleeding into Boot

**Current system (CLAUDE.md):**

```
# CLAUDE.md

## § 3: Project Vision (400w)
ALCHEMYTIMELINEMAP is an authoritative scholarly portal based on...
The Actor/Analyst distinction is fundamental...
Medieval continuity thesis states that...
Operationalism in alchemy refers to...
Pamela Smith's framework emphasizes material culture...

## Task Routing Table
...
```

**Problem:** A timeline event writer arrives, reads CLAUDE.md, and encounters 400 words of historiography before getting to task routing.

**Post-refactor fix (CLAUDE.md NEW):**

```
# CLAUDE.md

## Mission
ALCHEMYTIMELINEMAP is an interactive timeline and map of alchemy (500 events, Late Antiquity–early modern).

## Core Invariants
1. No frameworks endorsed; historical phenomena reported
2. Provenance required on all entries
3. All entity links must exist
4. Historiographical grounding for person biographies
5. Material culture emphasized where applicable

## Task Routing
[Simple table, 8 common tasks]

## Links to Other Layers
- Historiography: CONCEPTUAL_FRAMEWORK.md (read for editorial decisions on person/concept definitions)
- Project state: PHASESTATUS.md
- Task-specific standards: AGENT_LOADING_STRATEGY.md
```

**Improvement:** Boot is now 5 minutes instead of 12 minutes. Historiography is still available (CONCEPTUAL_FRAMEWORK.md) but not mandatory for timeline events.

---

### Example 2: Architecture Details Bleeding into Boot

**Current system (CLAUDE.md § 6–7):**

```
## § 6: Architecture at a Glance (300w)

SQLite Database (alchemy_timeline.db)
  ├─ persons (105+ alchemists)
  ├─ texts (50+ treatises)
  ├─ concepts (30+ operations)
  ├─ locations (20+ cities/regions)
  ├─ timeline_events (500 dated events)
  ├─ person_event_refs
  ├─ text_event_refs
  └─ concept_event_refs
    ↓
Python Pipeline (idempotent scripts)
  ├─ scripts/init_db.py
  ...
    ↓
Static HTML/CSS/JS (site/)
  ...
```

**Problem:** An agent writing a timeline event doesn't need to understand SQLite schema or pipeline architecture. This is for developers, not content creators.

**Post-refactor fix:** Remove from CLAUDE.md, keep in docs/SYSTEM.md (Layer 4). Agents only read it when modifying the system.

---

### Example 3: Standards Scattered Across Layer 3

**Current system (STYLEGUIDE.md):**

An agent writing timeline events must read:
- § 1 (General prose, 300w) — general principles, not specific to timeline events
- § 4 (Timeline events, 400w) — actual standards
- § 6 (Bibliography, 200w) — applies to all but repeated in each section

**Problem:** Agent must read 900w to get 400w of relevant standards. Must mentally filter out § 1 (general, can skip), § 2 (person bio), § 3 (text), § 5 (concept), § 6 (maybe needed?).

**Post-refactor fix (STANDARD_TIMELINE_EVENTS.md):**

```
## Timeline Event Specification

### Word Count
100–250 words

### Required Fields
- date_label
- location
- description (the timeline event prose)
- persons_involved
- texts_involved
- concepts_involved

### Bibliography (if applicable)
Not required for timeline events. If you cite a source, use DGWE format.

### Validation Checklist
- [ ] Word count within 100–250 range
- [ ] All required fields present
- [ ] All entity slugs exist in database
- [ ] Location is valid (check docs/SCHEMA.json locations enum)
- [ ] Confidence level assigned (HIGH, MEDIUM, LOW)

### Example Passing Entry
[Worked example, 150w]

### What Fails Validation
- Word count < 100 or > 250
- Missing required fields
- Entity slug doesn't exist
- Confidence not in (HIGH, MEDIUM, LOW)
```

**Improvement:** Agent reads 400w of ONLY relevant standards. No mental filtering.

---

## DECISION CLARITY ANALYSIS

### Current System: Decision Ambiguity

**Scenario:** Agent is asked to "expand the person biography of Ibn Sina"

**Current questions agent might ask:**
- "Should I read PROMPTS.md for historiographical context?" (implicit, not stated)
- "Should I read the full STYLEGUIDE.md or just § 2?" (unclear)
- "Are there examples somewhere?" (no clear pointer)
- "How do I validate my work?" (no validation rules specified)
- "Should I use CLAUDE.md § 8 (vocabulary) or docs/VOCABULARY.md?" (duplicated, confusing)
- "Is this the right phase for biography expansion?" (must check PHASESTATUS.md, but not told to)

**Outcome:** Agent must infer prerequisites. Some will be read unnecessary files; some will miss required files.

### Post-Refactor System: Decision Clarity

**Same scenario:**

**AGENT_LOADING_STRATEGY.md says explicitly:**

```
## Task: Write Person Biography

Loading sequence (28 minutes, 3,000–3,500 tokens):

1. CLAUDE.md (5m)
2. PHASESTATUS.md (2m)
3. CONCEPTUAL_FRAMEWORK.md (8m) [REQUIRED for editorial depth]
4. STANDARD_PERSON_BIOGRAPHIES.md (7m)
5. docs/SCHEMA.json (1m)
6. Example (5m, optional)

Do NOT load: Layer 2 (other content types), Layer 7 (archive)

Quality gate: Word count check, sections check, historiographical grounding evident
```

**Outcome:** Agent has explicit contract. No ambiguity. No wasted reading.

---

## ONBOARDING PHILOSOPHY ANALYSIS

### Current System: Onboarding Contains Unnecessary Philosophy

**CLAUDE.md § 3–5 (1,300w of philosophy):**

```
## § 3: Project Vision

ALCHEMYTIMELINEMAP is an interactive timeline and map of alchemy and chemistry...
Coverage: Europe, North Africa, Middle East, Late Antiquity through early modern period...
The portal combines:
- A 500-event interactive timeline...
- A geo-pinned Leaflet.js map...
- Relational entity pages...
- Rigorous historiographical standards...

## § 4: Historiographical Principles

The Actor/Analyst Distinction: This project treats "alchemy" as a historical phenomenon...
Medieval Continuity: We reject the notion that alchemy suddenly appeared...
Operational Chemistry: Historical alchemists engaged in real chemical operations...
Transmission and Misreading: How ideas travel and transform...

## § 5: Key Scholarly Authorities

William R. Newman...
Michela Pereira...
Garth Fowden...
```

**Problem:**
- Agent writing timeline events doesn't need to understand historiographical principles
- Agent deploying the site doesn't need to understand three constituencies
- Boot layer becomes a "lore dump" for context that's optional for most tasks

**Post-refactor fix:** Boot layer becomes minimalist (mission, invariants, routing). Philosophy is in Layer 2, read only when needed.

---

## TECHNICAL DOCS DUPLICATION ANALYSIS

### Current System: Vocabulary Defined in 4 Places

**Duplication of enum values:**

1. **PROMPTS.md § VII: Vocabulary Lock (400w)**
   ```
   era: ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
   role_primary: ALCHEMIST, CHEMIST, SCHOLAR, PHILOSOPHER, PHYSICIAN, ...
   ```

2. **CLAUDE.md § 8: Vocabulary Lock (300w)**
   ```
   [Same enums repeated]
   ```

3. **docs/VOCABULARY.md (500w)**
   ```
   [Same enums with explanation]
   ```

4. **docs/ONTOLOGY.md (embedded, 400w)**
   ```
   [Same enums in schema prose]
   ```

**Problem:**
- If a new enum is added, 4 places must be updated
- Agent must verify which version is current
- No machine-readable source of truth

**Post-refactor fix:**
- Single source: docs/SCHEMA.json (JSON schema)
- docs/VOCABULARY.md references it (no duplication)
- Validation scripts load from SCHEMA.json
- No prose duplication

---

## SUMMARY: PROGRESSIVE REVELATION IMPROVEMENTS

| Metric | Current | Post-Refactor | Improvement |
|--------|---------|---------------|-------------|
| **Boot time (Layer 0)** | 12 min (read 2,600w CLAUDE.md) | 5 min (read 400w CLAUDE.md) | **60% faster** |
| **Timeline event total reading** | 18 min (boot + STYLEGUIDE + implicit schema) | 5 min (boot + STANDARD_TIMELINE_EVENTS.md + schema) | **72% faster** |
| **Person biography total reading** | 28 min (boot + PROMPTS.md § 1–3 + STYLEGUIDE.md § 2 + schema) | 28 min (boot + CONCEPTUAL_FRAMEWORK.md + STANDARD_PERSON_BIOGRAPHIES.md + schema) | **Same time, clearer path** |
| **Historiography bleeding into boot** | 1,300w leaked into Layer 0 | 0w (CONCEPTUAL_FRAMEWORK.md is separate layer) | **100% fixed** |
| **Architecture bleeding into boot** | 500w leaked into Layer 0 | 0w (docs/SYSTEM.md is Layer 4) | **100% fixed** |
| **Enum duplication** | 4 places (PROMPTS, CLAUDE, VOCABULARY, ONTOLOGY) | 1 place (SCHEMA.json) | **75% deduplication** |
| **Task routing ambiguity** | Agent must infer prerequisites | Explicit contract (AGENT_LOADING_STRATEGY.md) | **100% clarity** |
| **Optional vs. required unclear** | No distinction (PROMPTS.md § 1–5 all included?) | Explicit (Layer 2 optional for timeline events, required for person biographies) | **100% clarity** |
| **Cognitive overhead (filtering)** | ~1,000 tokens of "not needed" context per task | ~0 tokens (only reads needed context) | **Eliminate cognitive tax** |

---

*Next document: HUMAN_AI_COLLABORATION_MODEL.md*
