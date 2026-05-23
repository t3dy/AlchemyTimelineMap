# CRITICAL ARCHITECTURE AUDIT — ALCHEMYTIMELINEMAP

**Date:** 2026-05-22  
**Scope:** Examination of documentation system as operational environment for AI agents  
**Approach:** Ruthless assessment of layer design, authority, routing, token economy

---

## EXECUTIVE SUMMARY

The current system exhibits **layer bleed, router ambiguity, and token waste** despite previous consolidation efforts. It is still designed as "a documentation project that AI sometimes reads" rather than "an operating environment for AI-assisted development."

**Key findings:**
- 8+ versions of key files exist (CLAUDE.md, CLAUDE_NEW.md, CLAUDE_REFACTORED.md, etc.)
- Historiographical framework repeated across 4+ files
- Prose standards scattered across 3+ files
- No deterministic task routing; agents must infer
- Agent prompts still contain boilerplate instead of being execution contracts
- Token overhead for boot is still 1,000–2,000 words (could be <300)
- Validation rules exist in prose, not in executable form
- Staging/validation workflow is informal (no contracts, checksums, or checkpoints)
- Session summaries and scholarly profiles occupy valuable repo space
- No distinction between "read once at project start" and "read per task"

**Critical insight:** The architecture still prioritizes human readability and conceptual completeness over deterministic routing and token efficiency. It reads like "onboarding documentation" rather than "a compiler pipeline."

---

## CURRENT STATE: LAYER ANALYSIS

### What Actually Exists (Honest Assessment)

**Root directory files (15+ active):**
- CLAUDE.md, CLAUDE_NEW.md, CLAUDE_REFACTORED.md (3 versions of same file; no clear winner)
- PROMPTS.md (4,000+ words; unreduced, contains vision + historiography + standards + agent rules)
- STYLEGUIDE.md, STYLEGUIDE_CONSOLIDATED.md (2 versions)
- PHASESTATUS.md, PHASESTATUS_REFACTORED.md (2 versions)
- README.md, PROJECT_SUMMARY.md, SESSION_SUMMARY.md (3 status documents, overlapping)
- ARCHAEOLOGY_RESEARCH_SUMMARY.md, ARCHAEOLOGY_AND_MATERIAL_CULTURE.md (archaeology docs)
- INTEGRATION_GUIDE_ARCHAEOLOGY.md (archaeology integration)
- CONTENT_EXPANSION_SUMMARY.md (session notes)
- CHANGELOG.md, IMPLEMENTATION_COMPLETE.md (meta-documentation)
- SCHOLARLYPROFILE.md, SONNETSCHOLARLYPROFILE.md (user context, 2 versions)

**docs/ directory files (12+):**
- docs/SYSTEM.md, docs/ONTOLOGY.md, docs/PIPELINE.md, docs/CONTEXT_ENGINEERING.md (architecture)
- docs/VOCABULARY.md (enums)
- docs/agents/TASK_ROUTING.md, docs/agents/PROMPT_*.md (agent routing & tasks)
- docs/ARCHAEOLOGY_AND_MATERIAL_CULTURE.md, docs/MULTIREGISTER_EXAMPLES.md
- docs/reference/, docs/archive/ (directories)

**agent prompts (7 files):**
- AGENT_PROMPT_*.md (root level)
- docs/agents/PROMPT_*.md (refactored versions)

### The Real Problem: Layer Bleed

**What should be boot layer (read once per session):**
- Mission + core invariants: 50 words
- Current phase pointer: 10 words
- Task routing decision tree: 300 words
- **Total: ~360 words, <2 min read**

**What currently IS boot layer:**
- CLAUDE.md: 2,600 words (historiography, standards summary, architecture diagram, vocabulary)
- README.md: 500+ words (overlaps CLAUDE, PROMPTS, PHASESTATUS)
- IMPLIED requirement to read PROMPTS.md: 4,000+ words
- **Total: ~7,100 words, 20+ min read**

**Ratio of actual-to-needed:** 20x bloat

---

### The Authority Problem

| Concept | Appears In | Status |
|---------|-----------|--------|
| **Historiographical framework** (Actor/Analyst, medieval continuity, operational chemistry) | PROMPTS.md § 3, CLAUDE.md implied, PROMPTS_REFACTORED.md, agent prompts (preambles) | FRAGMENTED across 4+ files; no single canonical source |
| **Prose standards** (word counts, required sections, italics, bibliography) | STYLEGUIDE.md, STYLE_GUIDE_ALCHEMISTS.md, STYLE_GUIDE_SCHOLARS_AND_TEXTS.md, PROMPT_*.md | SPLIT across 5+ files; task prompts duplicate rules |
| **Enum values** (era, role_primary, text_type, category_type, operation, confidence, review_status, source_method) | PROMPTS.md § VII, CLAUDE.md, docs/VOCABULARY.md, scripts/init_db.py | 4 instances; contradiction risk high |
| **Current phase** | PHASESTATUS.md, CLAUDE.md, README.md, PROJECT_SUMMARY.md, SESSION_SUMMARY.md | 5 instances; Phase description in CLAUDE is stale |
| **Content model** (timeline event, person, text, concept definitions) | PROMPTS.md § IV, STYLEGUIDE.md, README.md, CLAUDE.md | 4 instances |
| **Schema** | docs/ONTOLOGY.md, scripts/init_db.py, implied in CLAUDE.md | 2 instances (prose + code; no JSON schema) |
| **Pipeline order** | docs/PIPELINE.md, CLAUDE.md § Data Flow, README.md | 3 instances |
| **Key authorities** (Newman, Pereira, Hanegraaff, etc.) | PROMPTS.md, CLAUDE.md, SCHOLARLYPROFILE.md | 3 instances |

**Contradiction risk:** CLAUDENEW says Phase 0, PHASESTATUS says Phase 2 (conflict persists)

---

## ROUTING AMBIGUITY ANALYSIS

### Current Task Routing (Implicit)

Agent arrives with task "Write person biography."

**Current implicit flow:**
1. Start reading (where? CLAUDE? PROMPTS? README?)
2. Find task routing (scattered across multiple files)
3. Discover prerequisites (STYLEGUIDE § 2, PROMPTS § 3, VOCABULARY, TASK_ROUTING.md)
4. Read all prerequisites (1,200–3,300 words depending on interpretation)
5. Read task prompt (300 words, maybe duplicate of step 4)
6. Execute task

**Decision points where agent can get lost:**
- "Is historiography mandatory or optional?" (PROMPTS is marked "read before new agent tasks" but not per-task)
- "Do I read full STYLEGUIDE or just § 2?" (Unclear)
- "What if STYLEGUIDE § 2 and PROMPT_BIOGRAPHY_ENRICHER.md say different things?" (No arbitration rule)
- "Are enum values in docs/VOCABULARY.md or should I trust STYLEGUIDE § 6?" (Multiple sources)

**Token waste:** Agent might read 3,000 words to find out they only need 1,000.

---

## TOKEN ECONOMY AUDIT

### Current Boot Cost

**Scenario: New agent, first task**

Reading path 1 (conservative):
- CLAUDE.md: 2,600w
- TASK_ROUTING.md: 600w
- STYLEGUIDE.md § relevant: 1,000w
- PROMPTS.md (inferred as necessary): 4,000w
- **Total: 8,200 words**

Reading path 2 (aggressive):
- Just CLAUDE.md: 2,600w
- Task prompt: 300w
- Execute (hope for the best)
- **Total: 2,900 words + high error risk**

**Ideal boot cost:**
- Routing file: 300w
- Task-specific requirements: 400w
- **Total: 700 words, 5 min**

**Current-to-ideal ratio:** 12x bloat (8,200 ÷ 700)

### Duplication Cost

**Historiography:**
- PROMPTS.md § 3 (1,200 words)
- CLAUDE.md § (implied, 400 words)
- Task prompts (preambles, 200 words × 7 = 1,400 words)
- PROMPTS_REFACTORED.md (written separately)
- **Total wasted: ~3,000 words of redundant historiography**

**Prose standards:**
- STYLEGUIDE.md (2,000 words)
- STYLE_GUIDE_ALCHEMISTS.md (1,000 words)
- STYLE_GUIDE_SCHOLARS_AND_TEXTS.md (1,500 words)
- Task prompt preambles (200 words × 4)
- **Total wasted: ~4,700 words of scattered standards**

**Enum values:**
- PROMPTS.md § VII (300 words)
- CLAUDE.md (200 words)
- docs/VOCABULARY.md (500 words)
- scripts/init_db.py (not counted, but authoritative)
- **Total wasted: ~1,000 words of enum documentation**

**Total duplication tax:** ~8,700 words of repeated/scattered material

---

## LAYER BLEED PROBLEMS

### Conceptual Material Leaking Into Operational Docs

**CLAUDE.md (should be boot + routing only):**
- Contains full Data Ontology Summary (belongs in ONTOLOGY.md)
- Contains pipeline rules (belongs in PIPELINE.md or schema)
- Contains "Key Scholarly Authorities" (belongs in PROMPTS.md, not boot)
- Contains Architecture at a Glance (belongs in SYSTEM.md)

**PROMPTS.md (should be historiography only):**
- Contains "Part IV: Content Standards" (belongs in STYLEGUIDE.md)
- Contains "Part VI: Agent Operating Rules" (belongs in agent contracts, not a prose file)
- Contains "Vocabulary Lock" (belongs in executable schema)

**Task prompts (should be execution contracts only):**
- Contains preamble repeating STYLEGUIDE.md rules (should reference only)
- Contains duplicated historiography context (should reference PROMPTS.md)
- Not structured as JSON contracts (should be executable validation rules)

**STYLEGUIDE.md (should be writing standards only):**
- Contains DGWE bibliography examples (okay)
- Contains Actor/Analyst examples (duplicates PROMPTS.md § 5)
- Contains validation checklist (should be in executable schema, not prose)

### Conceptual vs Operational Confusion

**Example: Word count rules**

Currently:
- Timeline event: 100–250 words (STYLEGUIDE § 4)
- Person bio: 1,200–2,200 words (STYLEGUIDE § 2)
- Repeated in PROMPT_BIOGRAPHY_ENRICHER.md
- Mentioned in PROMPTS.md § IV
- Implied in README.md

Should be:
- Single JSON schema file with fields: content_type, min_words, max_words
- Executable validation on data entry
- Referenced by STYLEGUIDE.md, not embedded
- Checked programmatically, not by reading prose

---

## ROUTING PRECISION PROBLEMS

### Current Task Routing Matrix (Inferred)

The TASK_ROUTING.md file exists, but:
1. It's not listed in CLAUDE.md boot sequence
2. It requires finding docs/agents/ directory (not obvious)
3. It doesn't have enforcement (agents can ignore it)
4. It doesn't specify optional vs. mandatory reads
5. It doesn't specify contradiction resolution

### Missing Routing Decisions

Questions agents must answer themselves:
- "If STYLEGUIDE § 5 conflicts with PROMPT_CONCEPT_ENRICHER.md, which wins?" (No arbiter)
- "If docs/VOCABULARY.md and PROMPTS.md § VII list different enum values, which is current?" (No authority order)
- "Should I read historiography (PROMPTS) for every task, or just once?" (Unclear)
- "If task prompt says 'read STYLEGUIDE § 2' but I'm not writing a person biography, what should I read?" (No conditional logic)

---

## VALIDATION & STAGING PROBLEMS

### Current Validation (Entirely Prose-Based)

**Word counts:**
- "100–250 words" for timeline events mentioned in STYLEGUIDE.md
- Checked manually by humans reading the text
- No programmatic validation
- No checksum verification
- Error discovered after writing (too late)

**Required sections:**
- "Opening paragraph (200–350 words)" mentioned in STYLEGUIDE.md
- Checked manually by reading prose
- No JSON schema definition
- No automated linting
- Easy to skip unknowingly

**Enum usage:**
- "Use only values from docs/VOCABULARY.md" mentioned in STYLEGUIDE.md
- No validation on database insert
- Relies on agent remembering
- Scripts don't enforce CHECK constraints

**Entity linking:**
- "[LINK:slug]" markup mentioned in task prompts
- No validation that slug exists
- No checksum of reference integrity
- Breaks silently

### Missing Staging Contracts

Current staging workflow (informal):
1. Agent writes content to staging/ directory
2. Main session reads and validates manually
3. If errors found, ask agent to fix
4. Load to database
5. No record of what was checked
6. No formal handoff

**Should be:**
1. Agent writes to staging/ with manifest
2. Manifest contains: hash, content_type, word_count, enum_usage, entity_links
3. Validation script checks manifest against schema
4. Report: pass/fail with specific violations
5. Only passing entries move to database
6. Audit trail recorded

---

## CONTRADICTION RISK ASSESSMENT

### Known Active Contradictions

| Issue | Source A | Source B | Risk |
|-------|----------|----------|------|
| **Current phase** | CLAUDE.md: "Phase 0" | PHASESTATUS.md: "Phase 2" | HIGH: Agents confused about project state |
| **Event count** | PHASESTATUS.md: "480 current, 20 pending" | README.md: "500-event target" | MEDIUM: Unclear if target is reached |
| **Enum values (era)** | PROMPTS.md: LATE_ANTIQUE | docs/VOCABULARY.md: LATE_ANTIQUE | LOW: Consistent but documented twice |
| **Historiography significance** | PROMPTS.md § 3.4 says "provenance on every claim" | STYLEGUIDE.md § 1 does NOT explicitly require final significance sentence | MEDIUM: Agents unsure if required |
| **ACTOR_TERM definition** | PROMPTS.md § 5 | docs/VOCABULARY.md | MEDIUM: Different levels of detail |

### Contradiction Sources

1. Multiple versions of same file (CLAUDE.md, CLAUDE_NEW.md, CLAUDE_REFACTORED.md)
2. Prose rules scattered across files (no authority order)
3. Stale content not updated after project progresses (Phase 0 in CLAUDE.md)
4. Enum values documented in multiple places (source of truth unclear)
5. No deprecation mechanism (old files remain, confuse agents)

---

## WHAT SHOULD BE EXECUTABLE, NOT PROSE

### Rules Currently in Prose That Should Be Schema/Validation

**Word count rules:**
```json
{
  "timeline_event": {"min": 100, "max": 250},
  "person_biography": {"min": 1200, "max": 2200},
  "text_description": {"min": 1000, "max": 1800},
  "concept_definition": {"min": 1500, "max": 2500}
}
```

**Required sections:**
```json
{
  "person_biography": [
    "opening_paragraph",
    "main_sections_2_to_4",
    "literature_section"
  ],
  "timeline_event": [
    "date",
    "location",
    "named_actors",
    "historiographical_significance"
  ]
}
```

**Enum validation:**
```python
# In scripts/init_db.py or validation schema
CHECK (era IN ('ANTIQUITY', 'LATE_ANTIQUE', 'MEDIEVAL', 'RENAISSANCE', 'EARLY_MODERN', 'MODERN'))
CHECK (role_primary IN ('ALCHEMIST', 'CHEMIST', ...))
```

**Bibliography format:**
```json
{
  "format": "author_lastname. title. publisher, year.",
  "regex": "^[A-Z][a-z]+(, [A-Z][a-z]+)*\\. .*\\. .*\\d{4}\\.$"
}
```

**Entity link validation:**
```python
# Validate [LINK:slug] references exist in database
def validate_entity_links(text, session):
    for link in re.findall(r'\[LINK:(\w+)\]', text):
        if not session.query(Entity).filter_by(slug=link).exists():
            raise ValidationError(f"Unknown entity slug: {link}")
```

**Current state:** All of the above are in prose only. No programmatic enforcement. Errors discovered after writing.

---

## AGENT PROMPT DESIGN PROBLEM

### Current Design (Onboarding Essay Model)

Each agent prompt contains:
1. 200-word preamble repeating historiography
2. 300-word section on prose standards
3. 200-word section on entity linking
4. 100-word section on enum usage
5. 200 words of actual task-specific instructions

**Reality:** 80% preamble, 20% task-specific. Token waste.

### Ideal Design (Execution Contract Model)

Each agent prompt should be:
```
# Task: [name]

## Prerequisites (links only)
- STYLEGUIDE.md § [X]
- docs/VOCABULARY.md
- PROMPTS.md § [Y] (optional for depth)

## Execution Contract
- Input: [schema]
- Output: [schema]
- Word count: [min–max]
- Required sections: [list]
- Validation: [what fails the contract]

## Example
[concrete example of passing input/output]
```

**Word count per prompt:** 300–400 words (not 1,000+)
**Boilerplate:** 0% (all rules reference STYLEGUIDE.md)
**Task-specific:** 100% of content

---

## SCHOLARLY PROFILE & SESSION NOTES PROBLEM

### Current Situation

**SCHOLARLYPROFILE.md** (1,500 words):
- Documents Ted Hand's scholarly values, methodologies, preferences
- Contains useful context for editorial decisions
- Currently in root directory
- Every agent must consider whether to read it
- Used rarely, takes up mental real estate

**SONNETSCHOLARLYPROFILE.md** (duplicate, superseded)

**SESSION_SUMMARY.md, PROJECT_SUMMARY.md:**
- Session working notes, not canonical
- Overlaps PHASESTATUS.md
- Takes up root directory space
- Decay risk (becomes stale, outdated)

**ARCHAEOLOGY_RESEARCH_SUMMARY.md, INTEGRATION_GUIDE_ARCHAEOLOGY.md:**
- Domain-specific research
- Useful for Phase 2 enrichment
- Not needed for every task
- Takes up root directory space

### The Real Problem

These files are **genuinely useful context** but **not operational instructions**. They shouldn't live in the boot layer. They should be:
- Optional references, not mandatory reads
- Organized by task (e.g., "expanding person biographies" → links to scholarly profile)
- Not duplicating information in task contracts
- Clearly marked as "context" or "reference," not "requirements"

---

## WHAT DOESN'T WORK (Honest Assessment)

1. **CLAUDE.md as a router:** Still too big (2,600 words), tries to be comprehensive, duplicates other files.

2. **PROMPTS.md as a single document:** 4,000+ words mixing vision, historiography, content standards, and agent rules. Should be split.

3. **Task routing via README + TASK_ROUTING.md + agent prompts:** Fragmented. Agents don't know which to consult first.

4. **STYLEGUIDE.md as the single prose standard:** Still 3,500+ words (post-consolidation). Contains sections that should be in task contracts or executable schema.

5. **Multiple versions of the same files:** CLAUDE.md, CLAUDE_NEW.md, CLAUDE_REFACTORED.md. No clear deprecation. Creates confusion.

6. **Prose-only validation:** Word counts, sections, enum usage all documented in prose. No programmatic enforcement.

7. **No token budget per file:** PROMPTS.md can be 4,000 words because there's no constraint. Bloat results.

8. **Versioning of docs via copy-paste:** Instead of deprecating CLAUDE.md, we created CLAUDE_NEW.md. Git history unclear.

---

## WHAT WOULD WORK BETTER

1. **Layered loading with strict token budgets.**
2. **Single authoritative source per concept, with reference links everywhere else.**
3. **Deterministic routing that agents follow without decision-making.**
4. **Task contracts as JSON schemas, not prose essays.**
5. **Validation enforced mechanically, not by agent reading prose.**
6. **Progressive disclosure: start with ~300 tokens, load more only if needed.**
7. **Clear distinction: "Read once" vs. "Read per task" vs. "Reference only" vs. "Archival."**
8. **Deprecation mechanism: mark files as superseded, move to archive/.**
9. **No competing versions of the same file.**
10. **Staging as a formal validation checkpoint with checksums.**

---

## CONCLUSION

The current system has been improved but is still designed as "documentation that agents read" rather than "an execution environment for agents to operate in."

The next iteration should treat the repo as a compiler pipeline with:
- Explicit layers
- Token budgets per layer
- Deterministic routing contracts
- Executable validation
- No duplication of authority
- Progressive revelation

The goal: agents never ask "what should I read?" or "which file is authoritative?" They receive a loading contract, execute it, and move forward.

---

*Next document: LAYERED ARCHITECTURE DESIGN*
