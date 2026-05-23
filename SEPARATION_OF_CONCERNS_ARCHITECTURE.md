# Separation of Concerns Architecture for ALCHEMYTIMELINEMAP

**Principle:** Each file has exactly ONE purpose. No duplication. An LLM reads only what it needs for its function.

---

## File-by-Function Map (After Refactoring)

### Layer 1: Entry & Orientation (Read First)

**File: `CLAUDE.md`**
- **Purpose:** Minimal orientation + routing only
- **Scope:** ~400 words
- **Contains:**
  - 1-sentence mission
  - Link to PHASESTATUS.md ("Current phase: see X")
  - Task routing table (task → which file(s) to read)
  - Link to PROMPTS.md ("For historiography: see X")
  - Link to STYLEGUIDE.md ("For writing: see X")
  - DO NOT contain: historiography, content standards, architecture, schema details
- **Reader:** Every Claude session (first file)
- **Use case:** "I'm starting work. What should I read?"

**File: `README.md`**
- **Purpose:** GitHub project overview
- **Scope:** ~200 words
- **Contains:**
  - Project tagline
  - Links to CLAUDE.md, PHASESTATUS.md, key docs
  - Tech stack (1 line)
  - GitHub Pages URL
- **Reader:** Humans browsing the repo on GitHub
- **Use case:** "What is this project?"

---

### Layer 2: Conceptual Foundations (Read Before Creating Content)

**File: `PROMPTS.md`**
- **Purpose:** Historiographical framework + scholarly principles only
- **Scope:** ~2,500 words (trim from current 4,000+)
- **Contains:**
  - Project vision (1 section)
  - Three constituencies (1 section)
  - Historiographical framework (Actor/Analyst, Medieval continuity, operational chemistry, provenance, geography, taxonomy)
  - Key scholarly authorities and their relevance
  - **DO NOT contain:** Content standards (→STYLEGUIDE.md), technical architecture (→docs/SYSTEM.md), pipeline (→docs/PIPELINE.md), vocabulary lock (→docs/VOCABULARY.md)
- **Reader:** Agents creating content; humans understanding project philosophy
- **Use case:** "Why does this project matter? What are the non-negotiable principles?"

**File: `docs/VOCABULARY.md`** [NEW]
- **Purpose:** Single source of truth for all controlled vocabulary
- **Scope:** ~500 words
- **Contains:**
  - All enum values (era, role_primary, text_type, category_type, operation, confidence, review_status, source_method)
  - Why each value exists
  - Examples of each
  - **Referenced by (not duplicated in):** STYLEGUIDE.md, docs/ONTOLOGY.md, agent prompts
- **Reader:** Anyone designing content, writing validation rules, creating agent prompts
- **Use case:** "What enum values are valid? Why?" (One answer, not scattered across 5 files)

---

### Layer 3: Content Standards (Read Before Writing)

**File: `STYLEGUIDE.md`** [CONSOLIDATED]
- **Purpose:** ALL prose writing standards in one place
- **Scope:** ~3,500 words (consolidated from 3 current guides)
- **Contains:**
  - § 1: Core prose standard (no markdown, no bullets, encyclopedia tone)
  - § 2: Person biographies (1,200–2,200 words)
    - § 2.1: Historical alchemists (Works, Alchemical Significance, Transmission, Scholarly Debates)
    - § 2.2: Modern scholars (Central Thesis, Key Works, Approach, Disputes)
    - § 2.3: Example openings
  - § 3: Text descriptions (1,000–1,800 words)
    - § 3.1: Primary sources (Content, Composition, Modern Scholarship)
    - § 3.2: Commentaries & scholarship
    - § 3.3: Example openings
  - § 4: Timeline events (100–250 words)
    - Required elements, structure, example
  - § 5: Concept definitions (1,500–2,500 words)
    - ACTOR_TERM vs. ANALYST_TERM distinction, sections, examples
  - § 6: Bibliography format (DGWE model with examples)
  - Appendix A: Complete example entries (William R. Newman, Summa Perfectionis, etc.)
  - Appendix B: Validation checklist
  - **References but does NOT duplicate:** VOCABULARY.md (for enum values)
  - **References but does NOT duplicate:** PROMPTS.md (for historiography context)
- **Reader:** Anyone writing content (persons, texts, concepts, events)
- **Use case:** "I'm writing a person biography. What are the requirements?"

**Rationale:** Single source of truth. No competing guides (STYLE_GUIDE_ALCHEMISTS.md, STYLE_GUIDE_SCHOLARS_AND_TEXTS.md archived). An agent reads STYLEGUIDE.md once and knows all prose requirements.

---

### Layer 4: Project State (Read to Understand Current Status)

**File: `PHASESTATUS.md`** [PROMOTED]
- **Purpose:** Single source of truth for what's done, what's in progress, what's next
- **Scope:** ~1,200 words
- **Contains:**
  - Phase completion summary (Phase 0 ✅, Phase 1 ✅, Phase 2 🔄, Phase 3 ⏳)
  - Detailed status for current phase only (Phase 2 detail: persons, texts, concepts scope + immediate next actions)
  - Event count accuracy (480 enriched, 20 pending)
  - Known issues flagged
  - Success criteria
  - **DO NOT contain:** Historiography (→PROMPTS.md), prose standards (→STYLEGUIDE.md), architecture (→docs/SYSTEM.md)
- **Reader:** Anyone asking "What's the status? What do I work on next?"
- **Use case:** "What should I do today? What's finished? What's in progress?"

---

### Layer 5: Technical Architecture (Read Before Modifying Systems)

**File: `docs/SYSTEM.md`**
- **Purpose:** Data flow diagram + design principles (SQLite, idempotent, no frameworks)
- **Scope:** ~800 words (already fairly clean)
- **Contains:**
  - Core stack (SQLite, Python stdlib, vanilla HTML/JS)
  - Data flow diagram (seed JSON → scripts → DB → HTML)
  - Design principles (SQLite as source of truth, no frameworks, idempotent scripts)
  - Typical workflow (seed → load → enrich → deploy)
  - Directory structure
  - **DO NOT contain:** Full schema (→docs/ONTOLOGY.md), script execution order (→docs/PIPELINE.md), batch strategy (→docs/CONTEXT_ENGINEERING.md)
- **Reader:** Engineers modifying the data pipeline or architecture
- **Use case:** "How does data flow from seed to site? What are the non-negotiable design principles?"

**File: `docs/ONTOLOGY.md`**
- **Purpose:** Database schema—ONLY schema, nothing else
- **Scope:** ~1,200 words (already exists)
- **Contains:**
  - 8 table definitions (fields, types, constraints)
  - Foreign key relationships
  - CHECK constraints (references docs/VOCABULARY.md for enum values)
  - Indexes
  - SQL examples
  - **DO NOT contain:** Data flow (→docs/SYSTEM.md), script order (→docs/PIPELINE.md), design philosophy (→docs/SYSTEM.md)
- **Reader:** Anyone adding/modifying database tables or queries
- **Use case:** "What is the schema for the persons table?"

**File: `docs/PIPELINE.md`**
- **Purpose:** Python script execution order—ONLY orchestration, nothing else
- **Scope:** ~800 words (already exists)
- **Contains:**
  - 6 main scripts in order (init_db → load_seed → load_skeleton → pre_query → enrich → build_site)
  - What each script does (1 sentence)
  - Dependencies between scripts
  - Idempotency guarantees
  - How to run the full pipeline
  - **DO NOT contain:** Script implementation details, database schema (→docs/ONTOLOGY.md), data flow philosophy (→docs/SYSTEM.md), batch strategy (→docs/CONTEXT_ENGINEERING.md)
- **Reader:** Anyone running or debugging the deployment pipeline
- **Use case:** "In what order do I run these scripts? What happens if I re-run one?"

**File: `docs/CONTEXT_ENGINEERING.md`**
- **Purpose:** Batch pattern strategy for 500-event scale—ONLY this, nothing else
- **Scope:** ~1,000 words (already exists)
- **Contains:**
  - Problem: 500 events × 5 entities = context explosion
  - Solution: batch + pre-query pattern
  - 5-step workflow
  - Token efficiency analysis
  - Example (pilot batch)
  - **DO NOT contain:** General architecture (→docs/SYSTEM.md), script details (→docs/PIPELINE.md)
- **Reader:** Agents enriching timeline events in batches; anyone working on Phase 1 continuation
- **Use case:** "How do I efficiently enrich 500 events without blowing up my context?"

---

### Layer 6: Task Routing (Read Before Starting a Specific Task)

**File: `docs/agents/TASK_ROUTING.md`** [NEW]
- **Purpose:** Route from "I have task X" to "Read file A, file B, file C, then execute prompt Z"
- **Scope:** ~400 words
- **Contains:**
  - Matrix: Task → Prerequisites (PROMPTS? STYLEGUIDE? PHASESTATUS?) → Task-specific prompt file
  - Examples:
    - Task: "Write a person biography" → Read STYLEGUIDE.md § 2, optionally PROMPTS.md § 1, then execute PROMPT_BIOGRAPHY_ENRICHER.md
    - Task: "Enrich timeline events" → Read CONTEXT_ENGINEERING.md, STYLEGUIDE.md § 4, then execute PROMPT_EVENT_ENRICHER.md
    - Task: "Deploy to live site" → Read PIPELINE.md, then execute build_site.py
  - **DO NOT contain:** Full historiography, full style guide, full pipeline—just links to those files
- **Reader:** An agent starting work, asking "What do I read first?"
- **Use case:** "I'm enriching persons. What are the prerequisites?"

---

### Layer 7: Task-Specific Prompts (Read When Executing a Task)

**Files: `docs/agents/PROMPT_*.md`** [NEW, <500 words each]

Example structure for `PROMPT_BIOGRAPHY_ENRICHER.md`:

```markdown
# Task: Expand Person Biography

## Prerequisites
Before starting, read:
- STYLEGUIDE.md § 2 (person biography requirements)
- Optionally: PROMPTS.md § 2 (historiographical framework)

## Your Task
Expand the biography of [PERSON] from current word count to 1,200–2,200 words.

## Requirements
- Opening paragraph: 200–350 words
- 2–4 `<h2>` sections per STYLEGUIDE.md § 2.1 (historical) or § 2.2 (modern scholar)
- Literature section: 5–12 references in DGWE format
- Pass STYLEGUIDE.md Appendix B checklist

## Context
[Pre-queried: person's authored texts, events involving them, relationships to other figures]

## Success Criteria
- Word count: 1,200–2,200 (excluding Literature)
- All sections present
- No markdown artifacts
- review_status: REVIEWED or VERIFIED

---

**DO NOT repeat:**
- Full prose standards (read STYLEGUIDE.md instead)
- Historiographical framework (read PROMPTS.md instead)
- Enum values (read docs/VOCABULARY.md instead)
```

---

### Layer 8: Reference & Context (Read Only When Relevant)

**File: `docs/reference/SCHOLARLY_PROFILE.md`**
- **Purpose:** Ted Hand's scholarly values and methodological commitments (context for understanding user intent)
- **Scope:** ~1,500 words
- **Reader:** Optional—useful for understanding why the user cares about certain framings
- **Use case:** "Why does this user emphasize ludic translation? Material grounding? Actor/analyst distinction?"
- **Note:** Not required reading; provides context for editorial decisions.

**Directory: `docs/reference/examples/`**
- **Purpose:** Complete, worked examples of good entries
- **Contains:**
  - Full person biography (William R. Newman, ~900 words)
  - Full text description (Summa Perfectionis, ~1,200 words)
  - Full concept definition (Distillation, ~1,800 words)
  - Timeline event (good example, ~150 words)
- **Reader:** Optional—useful for writers who want to see a complete example
- **Use case:** "Show me what a finished person biography looks like"

**Directory: `docs/reference/archaeology/`**
- **Purpose:** Domain-specific research on material culture and alchemical artifacts
- **Contains:**
  - ARCHAEOLOGY_AND_MATERIAL_CULTURE.md (hessian crucibles, Tycho Brahe, Making and Knowing)
  - ARCHAEOLOGY_RESEARCH_SUMMARY.md (complete synthesis)
  - INTEGRATION_GUIDE_ARCHAEOLOGY.md (how to use in Phase 2)
- **Reader:** Optional—useful when enriching persons/texts/concepts related to material culture
- **Use case:** "I'm writing about 16th-century alchemical laboratories. What physical evidence exists?"

---

### Layer 9: Archive (Do Not Read, Just for Reference)

**Directory: `docs/archive/`**
- **Purpose:** Superseded or replaced files (kept for history, not active use)
- **Contains:**
  - SONNETSCHOLARLYPROFILE.md (superseded by SCHOLARLY_PROFILE.md)
  - STYLE_GUIDE_ALCHEMISTS.md (consolidated into STYLEGUIDE.md)
  - STYLE_GUIDE_SCHOLARS_AND_TEXTS.md (consolidated into STYLEGUIDE.md)
  - PROJECT_SUMMARY.md (superseded by PHASESTATUS.md)
  - SESSION_SUMMARY.md (session working notes, not canonical)
  - REFACTOR_AUDIT_REPORT.md (audit documentation)
  - REFACTOR_SUMMARY.md (audit summary)
  - STYLEGUIDE_CONSOLIDATION_PLAN.md (consolidation plan)
- **Note:** Each archived file includes a header explaining why it was archived

---

## Reading Paths by Function

### "I'm a new agent starting work on ALCHEMYTIMELINEMAP"
1. Read: `CLAUDE.md` (400w) — Orientation
2. Look up: `docs/agents/TASK_ROUTING.md` — Find your task
3. Follow task prerequisites (e.g., STYLEGUIDE.md § 2 for biographies)
4. Read: Your task-specific prompt (300w)
5. Execute: Write content

**Total reading: ~1,000–2,000 words depending on task. No excess.**

### "I'm writing a person biography"
1. Read: `STYLEGUIDE.md § 2` (~800 words) — All requirements
2. Optionally read: `docs/reference/examples/WILLIAM_NEWMAN_EXAMPLE.md` (900 words) — Concrete model
3. Optionally read: `PROMPTS.md § 2` (~500 words) — Historiographical context for depth decisions
4. Execute: Write biography

**Total reading: 800–2,200 words depending on depth needed. No duplication.**

### "I'm enriching timeline events in a batch"
1. Read: `docs/CONTEXT_ENGINEERING.md` (~1,000 words) — Batch pattern for scale
2. Read: `STYLEGUIDE.md § 4` (~300 words) — Event requirements
3. Read: `docs/agents/PROMPT_EVENT_ENRICHER.md` (300 words) — Task specifics
4. Execute: Write batch of 20–50 events

**Total reading: ~1,600 words. No excess. Context-efficient.**

### "I need to deploy the site"
1. Read: `docs/PIPELINE.md` (~800 words) — Script order
2. Execute: Run scripts in sequence

**Total reading: 800 words. Focused.**

### "I need to understand the current project state"
1. Read: `PHASESTATUS.md` (~1,200 words) — All status info
2. Optionally: Link to task from `docs/agents/TASK_ROUTING.md`

**Total reading: ~1,200 words. Single source of truth.**

### "I'm modifying the database schema"
1. Read: `docs/ONTOLOGY.md` (~1,200 words) — Current schema
2. Read: `docs/SYSTEM.md` (~800 words) — Design principles
3. Consult: `docs/VOCABULARY.md` (~500 words) — Enum values

**Total reading: ~2,500 words. Focused on technical layer.**

---

## Separation of Concerns Checklist

✅ **Each file has exactly ONE purpose**
- PROMPTS.md = historiography only
- STYLEGUIDE.md = prose standards only
- PHASESTATUS.md = project state only
- SYSTEM.md = architecture & data flow only
- ONTOLOGY.md = schema only
- PIPELINE.md = script order only
- VOCABULARY.md = enum values only
- CLAUDE.md = routing only (mostly links)

✅ **No duplication**
- Historiography: PROMPTS.md only
- Prose standards: STYLEGUIDE.md only
- Enums: docs/VOCABULARY.md only
- Architecture: docs/SYSTEM.md only
- Schema: docs/ONTOLOGY.md only
- Status: PHASESTATUS.md only

✅ **An LLM reads only what it needs**
- Writing person bio? Read STYLEGUIDE.md § 2 + task prompt. (~1,100 words total)
- Enriching events? Read CONTEXT_ENGINEERING.md + STYLEGUIDE.md § 4 + task prompt. (~1,600 words)
- Understanding status? Read PHASESTATUS.md only. (~1,200 words)
- No "read 5 files hoping one applies" situation.

✅ **Cross-references instead of duplication**
- STYLEGUIDE.md says: "For vocabulary, see docs/VOCABULARY.md" (does NOT repeat enums)
- Task prompts say: "Read STYLEGUIDE.md § X" (do NOT repeat prose standards)
- PHASESTATUS.md says: "For historiography, see PROMPTS.md" (does NOT repeat framework)

✅ **Boot file is minimal routing**
- CLAUDE.md: ~400 words of orientation + routing table
- Everything else is "read X for [purpose]"

---

## File Sizes After Refactoring

| File | Current | Refactored | Rationale |
|------|---------|-----------|-----------|
| CLAUDE.md | 2,600w | 400w | Boot only (routing + minimal orientation) |
| README.md | 500w | 200w | GitHub overview only |
| PROMPTS.md | 4,000w | 2,500w | Trim duplicate content standards, agent rules (now in task prompts) |
| STYLEGUIDE.md | 2,000w | 3,500w | Consolidate 3 guides; add examples |
| docs/VOCABULARY.md | — | 500w | NEW: single source of truth for enums |
| PHASESTATUS.md | 800w | 1,200w | Keep as canonical status source |
| docs/SYSTEM.md | 1,200w | 800w | Remove duplicate architecture detail |
| docs/ONTOLOGY.md | 1,400w | 1,200w | Schema only (slightly trimmed) |
| docs/PIPELINE.md | 900w | 800w | Pipeline order only (slightly trimmed) |
| docs/CONTEXT_ENGINEERING.md | 1,200w | 1,000w | Batch strategy only (slightly trimmed) |
| docs/agents/TASK_ROUTING.md | — | 400w | NEW: task → prerequisites → prompt router |
| docs/agents/PROMPT_*.md | ~3,000w (7 files) | ~3,500w | Refactored to <500w each; focus on task specifics, not preamble |

---

## Summary: Separation of Concerns

| Concern | File | Purpose |
|---------|------|---------|
| **Orientation** | CLAUDE.md | Where to start, what to read next |
| **Historiography** | PROMPTS.md | Why this project matters, core principles |
| **Prose Standards** | STYLEGUIDE.md | How to write all content types |
| **Vocabulary** | docs/VOCABULARY.md | Allowed enum values, no duplication |
| **Project State** | PHASESTATUS.md | What's done, what's in progress |
| **Architecture** | docs/SYSTEM.md | How data flows, design principles |
| **Schema** | docs/ONTOLOGY.md | Database tables & relationships |
| **Pipeline** | docs/PIPELINE.md | Script execution order |
| **Batch Strategy** | docs/CONTEXT_ENGINEERING.md | How to enrich 500 events efficiently |
| **Task Routing** | docs/agents/TASK_ROUTING.md | Given task X, read files A, B, C |
| **Task Prompts** | docs/agents/PROMPT_*.md | Task-specific instructions |
| **Context** | docs/reference/ | Examples, scholarly profile, archaeology |
| **History** | docs/archive/ | Superseded files (kept for reference) |

---

*This architecture ensures each file has exactly one concern and LLMs read only what they need.*
