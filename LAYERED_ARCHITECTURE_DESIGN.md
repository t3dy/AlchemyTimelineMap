# LAYERED ARCHITECTURE DESIGN — ALCHEMYTIMELINEMAP

**Design Philosophy:** Treat the documentation and context system as a compiler pipeline with explicit layers, token budgets, authority hierarchy, and deterministic loading contracts.

---

## LAYER ARCHITECTURE (7 Explicit Layers)

```
Layer 0: BOOT/ROUTING (300–500 tokens)
  ↓
Layer 1: PROJECT STATE (1,000 tokens)
  ↓
Layer 2: CONCEPTUAL FRAMEWORK (2,000 tokens, optional per-task)
  ↓
Layer 3: OPERATIONAL STANDARDS (1,500 tokens, task-specific)
  ↓
Layer 4: TECHNICAL CONTRACTS (1,000 tokens, schema-based)
  ↓
Layer 5: EXECUTABLE VALIDATION (code/JSON)
  ↓
Layer 6: EXAMPLES & REFERENCE (on-demand)
  ↓
Layer 7: ARCHIVE & HISTORY (never auto-load)
```

---

## LAYER 0: BOOT/ROUTING

**Purpose:** Agent arrives, determines task, receives deterministic loading contract.

**Token budget:** 300–500 words  
**Intended reader:** Every agent, every session, first thing  
**Lifetime:** Read once per session  
**Should contain:**
- Mission statement (1 sentence)
- Core invariants (3–5 bullets, non-negotiable)
- Single task routing decision tree
- Pointer to Layer 1 (project state)
- Pointer to Layer 3 (task-specific standards)

**Should NOT contain:**
- Historiography (→ Layer 2)
- Writing standards (→ Layer 3)
- Schema details (→ Layer 4)
- Examples (→ Layer 6)
- Project history (→ Layer 7)

**Current files assigned:**
- CLAUDE.md (currently 2,600w; needs to be shrunk to 400w)

**Design:** Replace CLAUDE.md with a 400-word routing-only file that:
```
1. States mission (40 words)
2. Lists core invariants (200 words)
3. Provides task routing decision tree (100 words)
4. Links to Layer 1, Layer 3, Layer 4 docs
```

**Anti-patterns:**
- Summarizing entire historiography
- Explaining architecture in boot layer
- Repeating vocabulary lock
- Including "Key Scholarly Authorities"

---

## LAYER 1: PROJECT STATE

**Purpose:** Single source of truth for "what's the current state?"

**Token budget:** 1,000 words  
**Intended reader:** Any agent asking "what's in progress? what's next?"  
**Lifetime:** Consulted per session as needed  
**Should contain:**
- Current phase (which phase, what's the scope)
- Completed deliverables (per phase)
- Known issues flagged for resolution
- Immediate next steps
- Event count accuracy
- Database row counts
- Links to entities needing expansion (Phase 2)

**Should NOT contain:**
- Historiography
- Writing standards
- Architecture diagrams
- Project history/session notes

**Current files assigned:**
- PHASESTATUS.md (currently accurate; keep as-is)

**Design:** PHASESTATUS.md is already correct. Make it the ONLY source of phase/status truth.

**Anti-patterns:**
- Duplicating phase description in CLAUDE.md, README.md, or agent prompts
- Including session notes in PHASESTATUS.md
- Mixing historical project snapshots with current state
- Stale information not updated post-phase

---

## LAYER 2: CONCEPTUAL FRAMEWORK

**Purpose:** Historiographical principles, scholarly authorities, methodological commitments.

**Token budget:** 2,000 words  
**Intended reader:** 
  - Agents creating substantive content (per-task decision)
  - Humans understanding "why does this project exist?"
  - New team members onboarding (optional, not mandatory)
**Lifetime:** Read once per session if task requires deep editorial decisions; optional otherwise  
**Should contain:**
- Project vision (why alchemy history matters)
- Three constituencies (scholars, students, independent researchers)
- Historiographical principles: Actor/Analyst distinction, medieval continuity, operational chemistry, provenance, geography, taxonomy
- Key scholarly authorities and their relevance
- Why transmutation theory is treated as historical phenomenon, not endorsed claim
- Material culture & embodied knowledge (Pamela Smith framework)
- Transmission and misreading (how ideas travel and transform)

**Should NOT contain:**
- Word count rules (→ Layer 3)
- Prose standards (→ Layer 3)
- Enumvalue definitions (→ Layer 4)
- Validation rules (→ Layer 5)
- Examples (→ Layer 6)

**Current files assigned:**
- PROMPTS.md (currently 4,000w; trim to 2,000w by removing standards, agent rules, vocabulary)
- PROMPTS_REFACTORED.md (use as basis for trimmed version)

**Design:** Create CONCEPTUAL_FRAMEWORK.md (2,000 words):
```
§ 1: Project vision (200w)
§ 2: Three constituencies (300w)
§ 3: Historiographical principles (1,000w)
§ 4: Key authorities (200w)
§ 5: Materiality and embodied knowledge (300w)
```

**Anti-patterns:**
- Repeating historiography in task prompts
- Mixing conceptual with operational material
- Making this mandatory for every task
- Keeping it in PROMPTS.md where it gets confused with standards

---

## LAYER 3: OPERATIONAL STANDARDS

**Purpose:** Task-specific writing rules, requirements, validation checklist.

**Token budget:** Task-specific: 400–800 words per task  
**Intended reader:** Agent executing a specific task  
**Lifetime:** Read when task is determined  
**Should contain (per task):**
- What content type this is (timeline event, person bio, text, concept)
- Word count range
- Required sections
- Validation rules (what passes, what fails)
- Entity linking requirements
- Bibliography format
- Example passing entry
- Checklist before submission

**Should NOT contain:**
- Historiographical context (→ Layer 2)
- Enum definitions (→ Layer 4)
- General prose principles (→ Reference layer)

**Current files assigned:**
- Task-specific prompt files in docs/agents/PROMPT_*.md (refactored to 400–500w each)

**Design:** Each task has a deterministic "standard file":
- STANDARD_TIMELINE_EVENTS.md (400w)
- STANDARD_PERSON_BIOGRAPHIES.md (500w)
- STANDARD_TEXT_DESCRIPTIONS.md (450w)
- STANDARD_CONCEPT_DEFINITIONS.md (550w)

Each contains ONLY:
```
## [Content Type] Specification

### Word Count
min: X, max: Y

### Required Sections
1. [section name] (word range)
2. [section name] (word range)

### Validation Checklist
- [ ] Word count within range
- [ ] All required sections present
- [ ] [specific rule 1]
- [ ] [specific rule 2]

### Example (Passing Entry)
[Concrete example]

### What Fails Validation
[Concrete failure examples]
```

**Anti-patterns:**
- Including historiography as "context for depth decisions"
- Repeating vocabulary lock
- Including "pre-queried context" instructions (→ execution contract)
- Making it 1,000+ words

---

## LAYER 4: TECHNICAL CONTRACTS & SCHEMA

**Purpose:** Executable specifications for validation, schema, data model, pipeline.

**Token budget:** Mostly code/JSON; prose <500w total  
**Intended reader:** 
  - Execution agents (deterministic contracts)
  - Developers building validation
  - Pipeline orchestration
**Lifetime:** Loaded once per environment; referenced by validation  
**Should contain:**
- Database schema (as JSON schema, not verbose prose)
- Enum definitions (AUTHORITY SOURCE for all enum values)
- Content type specifications (word count, required sections as schema)
- Pipeline contracts (input/output types, validation gates)
- Staging manifest format
- Entity slug conventions
- Entity link validation contract

**Should NOT contain:**
- Historiographical explanation
- Writing style guidance
- Examples

**Current files assigned:**
- docs/ONTOLOGY.md (currently prose; needs JSON schema version)
- docs/VOCABULARY.md (correct as enum reference, but also needs JSON schema)
- NEW: docs/SCHEMA.json (machine-readable schema)
- NEW: docs/CONTRACTS.json (pipeline contracts)

**Design:**

**docs/SCHEMA.json:**
```json
{
  "content_types": {
    "timeline_event": {
      "word_count": {"min": 100, "max": 250},
      "required_fields": ["date", "location", "description", "significance"],
      "validation_rules": [...]
    },
    "person_biography": {
      "word_count": {"min": 1200, "max": 2200},
      "required_sections": [
        {"name": "opening_paragraph", "min": 200, "max": 350},
        {"name": "main_section_1", "min": 250, "max": 400},
        ...
      ]
    }
  },
  "enums": {
    "era": ["ANTIQUITY", "LATE_ANTIQUE", "MEDIEVAL", "RENAISSANCE", "EARLY_MODERN", "MODERN"],
    "role_primary": [...]
  }
}
```

**docs/CONTRACTS.json:**
```json
{
  "staging_manifest": {
    "required_fields": ["content_type", "entity_slug", "word_count", "entity_links", "checksum"],
    "validation": {
      "word_count_matches_actual": true,
      "entity_links_exist_in_db": true,
      "enum_values_valid": true
    }
  },
  "timeline_event_contract": {
    "input": {"type": "timeline_event_stub"},
    "output": {"type": "timeline_event_enriched", "validation": "passes_schema"},
    "error_codes": ["word_count_too_low", "missing_section", "invalid_entity_link"]
  }
}
```

**Anti-patterns:**
- Keeping prose documentation of schema
- Multiple versions of enum definitions
- No machine-readable authority

---

## LAYER 5: EXECUTABLE VALIDATION

**Purpose:** Code that enforces rules mechanically, not by agent reading prose.

**Format:** Python scripts, SQL constraints, JSON schema validators  
**Intended reader:** Validation pipeline, pre-commit hooks, ingestion scripts  
**Should contain:**
- Word count validation
- Required section validation
- Enum value validation
- Entity link existence checking
- Bibliography format regex
- Staging manifest checksum verification

**Should NOT contain:** Prose (all enforcement is code)

**Current files assigned:**
- NEW: scripts/validate_content.py (word count, sections, enum validation)
- NEW: scripts/validate_staging_manifest.py (manifest checksums, entity links)
- Existing: scripts/init_db.py (add CHECK constraints for enums)

---

## LAYER 6: EXAMPLES & REFERENCE

**Purpose:** Concrete examples, worked models, scholarly context, optional reads.

**Token budget:** Unlimited (reference material, consulted as-needed)  
**Intended reader:** Agents wanting to see a concrete example; humans learning  
**Lifetime:** Consulted when agent says "show me what this looks like"  
**Should contain:**
- Worked example: person biography (900w)
- Worked example: text description (1,200w)
- Worked example: concept definition ACTOR_TERM (1,800w)
- Worked example: concept definition ANALYST_TERM (1,600w)
- Worked example: timeline event (150w)
- Scholarly profile (user context)
- Archaeology research (domain context)
- Actor/analyst distinction examples
- Material grounding examples

**Should NOT contain:** Operational rules (those are in Layer 3)

**Current files assigned:**
- docs/reference/examples/ (worked examples)
- docs/reference/SCHOLARLY_PROFILE.md
- docs/reference/ARCHAEOLOGY_*.md
- docs/reference/ACTOR_ANALYST_EXAMPLES.md

**Design:** Clearly marked as reference/examples; never auto-loaded.

---

## LAYER 7: ARCHIVE & HISTORY

**Purpose:** Git history, superseded files, session notes.

**Token budget:** N/A (never loaded)  
**Intended reader:** Historical research only  
**Lifetime:** Never auto-loaded; consulted if explicitly seeking history  
**Should contain:**
- Superseded files (CLAUDE.md versions, PROMPTS.md versions, etc.)
- Session summaries and project snapshots
- Refactoring audit reports
- Previous consolidation attempts
- Deprecated agent prompts

**Should NOT contain:** Anything operational

**Current files assigned:**
- docs/archive/ (all old versions, refactoring docs)
- CHANGELOG.md (what changed and why)

---

## LAYER LOADING DECISIONS (Deterministic Routing)

### By Task Type

#### Task: Write Timeline Event

```
Load:
  - Layer 0: BOOT (find task routing) → 5 min
  - Layer 1: PROJECT STATE (understand phase) → 2 min
  - Layer 3: STANDARD_TIMELINE_EVENTS.md → 5 min
  - Layer 4: docs/SCHEMA.json (word count, required fields) → 1 min
  - Layer 6: Example timeline event → 3 min (if agent requests)

Total: 16 min, 1,200–1,500 tokens
Do NOT load: Layer 2 (historiography), Layer 7 (archive)
```

#### Task: Write Person Biography

```
Load:
  - Layer 0: BOOT → 5 min
  - Layer 1: PROJECT STATE → 2 min
  - Layer 2: CONCEPTUAL_FRAMEWORK.md (for editorial depth decisions) → 8 min
  - Layer 3: STANDARD_PERSON_BIOGRAPHIES.md → 7 min
  - Layer 4: docs/SCHEMA.json → 1 min
  - Layer 6: Example person biography → 5 min (if agent requests)

Total: 28 min, 3,000–3,500 tokens
Optional: Layer 6 (scholarly profile for context)
Do NOT load: Layer 7 (archive)
```

#### Task: Deploy Site to GitHub Pages

```
Load:
  - Layer 0: BOOT → 5 min
  - Layer 1: PROJECT STATE (verify phase) → 2 min
  - Layer 4: docs/PIPELINE.md → 3 min

Total: 10 min, 800 tokens
Do NOT load: Layer 2, 3, 5, 6, 7
```

#### Task: Debug Invalid Entity Link

```
Load:
  - Layer 0: BOOT → 5 min
  - Layer 4: docs/SCHEMA.json (entity slug format) → 1 min
  - Layer 4: Entity link validation contract → 1 min
  - Layer 5: scripts/validate_staging_manifest.py → 3 min

Total: 10 min, 500 tokens
Do NOT load: Layer 2, 3, 6, 7
```

---

## TOKEN BUDGET PER LAYER

| Layer | Ideal Max | Purpose | Rule |
|-------|-----------|---------|------|
| 0 | 400w | Boot/routing | Never exceed; trim ruthlessly |
| 1 | 1,000w | Project state | Fixed; one file only |
| 2 | 2,000w | Conceptual | Optional per-task; can exceed for optional reads |
| 3 | 500w per task | Operational standards | Strict per-task budget; never duplicate |
| 4 | Code/schema | Execution contracts | No prose limit (executable) |
| 5 | Code only | Validation | No prose |
| 6 | Unlimited | Reference | On-demand, never auto-loaded |
| 7 | N/A | Archive | Never auto-loaded |

---

## AUTHORITY HIERARCHY (Explicit)

**For any concept, this is the authority order:**

1. **Executable schema (Layer 4, Layer 5)** — Code/JSON is authoritative
   - Word count range from docs/SCHEMA.json wins
   - Enum values from docs/VOCABULARY.md (as JSON) win
   - Validation rules in Python validation scripts win

2. **Operational standards (Layer 3)** — Task-specific prose
   - If STANDARD_TIMELINE_EVENTS.md contradicts something in Layer 6, use STANDARD_TIMELINE_EVENTS.md
   - If STANDARD_PERSON_BIOGRAPHIES.md and STANDARD_TIMELINE_EVENTS.md disagree on bibliography format, ERROR (they shouldn't)

3. **Conceptual framework (Layer 2)** — Context for understanding WHY
   - Never overrules Layer 3 operational rules
   - Provides interpretation guidance, not authority

4. **Reference examples (Layer 6)** — Illustrative only
   - If an example contradicts Layer 3 standard, the standard wins
   - Examples should be verified against standards before creation

5. **Archive (Layer 7)** — Never authoritative
   - Old versions are historical records only
   - New content should never reference archive files

**Rule:** If two files conflict, the higher layer wins. Conflicts indicate a bug (duplication/contradiction).

---

## DESIGN PRINCIPLES FOR THIS LAYER SYSTEM

1. **No duplication across layers.** If a rule appears in Layer 2 and Layer 3, one is wrong.

2. **Progressive disclosure.** Agent reads minimum to start (Layer 0), adds context (Layer 1), then task-specific (Layer 3, Layer 4).

3. **Deterministic loading.** No agent should ever ask "should I read this?" Task determines loading contract.

4. **Executable authority.** If something can be checked mechanically, it should be. Prose rules are interpretable; code rules are not.

5. **Single source per concept.** Historiography appears once (Layer 2). Prose standards appear once per task (Layer 3). Enums defined once (Layer 4).

6. **Token budgets enforced.** Layer 0 cannot exceed 400 words. Layer 3 cannot exceed 600 words per task. If you need more, split into another file.

7. **Lifetime clarity.** Every file's header states "read once," "read per-task," "on-demand," or "never auto-load."

---

## WHAT THIS ELIMINATES

- Multiple versions of the same file (CLAUDE.md, CLAUDE_NEW.md, CLAUDE_REFACTORED.md → one file)
- Scattered historiography (PROMPTS.md + preambles in agent prompts → one file)
- Repeated prose standards (STYLEGUIDE.md, STYLE_GUIDE_*.md, task prompt preambles → one file per task)
- Enum duplication (PROMPTS.md + CLAUDE.md + docs/VOCABULARY.md → one JSON source)
- Implicit routing (scattered across README, CLAUDE, TASK_ROUTING → explicit contract)
- Prose-only validation (read STYLEGUIDE § 2 and hope you remember → executable schema)
- Decision ambiguity (should I read X or Y → deterministic loading contract)

---

## WHAT THIS ENABLES

- New agent reads 400w (Layer 0) to understand routing
- Specific task loads 400–800w of rules (Layer 3) + schema (Layer 4)
- Total boot per task: 1,000–1,500 tokens (vs. current 8,000–9,000)
- Validation is mechanical, not interpretive
- No contradictions (authority hierarchy is clear)
- Long-session maintainability (rules don't scatter)
- Deterministic agent onboarding (no guessing)

---

*Next document: FILE AUTHORITY MAP*
