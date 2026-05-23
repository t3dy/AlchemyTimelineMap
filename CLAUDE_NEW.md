# Claude Code Instructions — ALCHEMYTIMELINEMAP

**An interactive timeline and map of alchemy and chemistry: 480+ events across Late Antiquity through the early modern period. Europe, North Africa, Middle East.**

---

## Non-Negotiable Invariants

1. **Actor/Analyst distinction** (Hanegraaff): Historical terms vs. modern categories—never collapse them.
2. **Medieval continuity**: No "dark age" gap. Alchemy is continuous from Late Antiquity through Arabic, Byzantine, and Latin medieval traditions into the Renaissance.
3. **Operational chemistry**: Chemical operations (distillation, sublimation) are real, reproducible, material practices. Separate them from transmutation theory.
4. **Named-source scholarship**: Every substantive claim traces to a cited scholar (Newman, Pereira, Hanegraaff, Smith, Principe, Fowden, etc.).
5. **No esoteric framing**: This is a scholarly reference portal, not a guide to practice or endorsement of transmutation claims.

---

## Current Status

**Phase:** Phase 2 (IN PROGRESS) — Persons, texts, concepts expansion  
**Event count:** 480 enriched, 20 pending to reach 500 target  
**For details:** → `PHASESTATUS.md` (source of truth for project state)

---

## Task Routing (Quick Start)

**What to read depends on your task:**

| I need to… | Read this |
|-----------|----------|
| **Understand my task & prerequisites** | `docs/agents/TASK_ROUTING.md` |
| **Write person biography / text / concept / timeline event** | `STYLEGUIDE.md` (§ for your content type) |
| **Understand historiographical principles** | `PROMPTS.md` (optional, deeper context) |
| **Know project status & what to work on** | `PHASESTATUS.md` |
| **Know allowed enum values** | `docs/VOCABULARY.md` |
| **Run scripts or modify pipeline** | `docs/PIPELINE.md` or `docs/SYSTEM.md` |
| **Fix a schema/database issue** | `docs/ONTOLOGY.md` |
| **See complete worked examples** | `docs/reference/examples/` |
| **Understand why user cares about certain framings** | `docs/reference/SCHOLARLY_PROFILE.md` (optional) |

**First time? Start here:** `docs/agents/TASK_ROUTING.md` → Find your task → Follow prerequisites → Read task prompt

---

## Core Principles

- **Timeline-first:** 500 events are atoms; persons, texts, concepts are secondary.
- **No frameworks:** Vanilla HTML/JS only. SQLite as source of truth.
- **Separation of concerns:** Each file has one purpose. Read only what you need.
- **Idempotent scripts:** All Python code uses `INSERT OR IGNORE`; safe to re-run.

---

## The 8 Tables (30-second overview)

- **timeline_events**: 500 dated, geotagged events (100–250 words each)
- **persons**: Alchemists, chemists, scholars (1,200–2,200 words each)
- **texts**: Treatises, commentaries, scholarship (1,000–1,800 words each)
- **concepts**: Operations, theories (1,500–2,500 words each, ACTOR_TERM vs. ANALYST_TERM distinction)
- **locations**: Cities/regions with coordinates
- **person_event_refs, text_event_refs, concept_event_refs**: Linking tables

For full schema: → `docs/ONTOLOGY.md`

---

## Key Scholarly Authorities

These frameworks govern the portal:

| Scholar | Key Work | Use for |
|---------|----------|---------|
| William R. Newman | *Atoms and Alchemy* (Yale, 2006) | Operational chemistry; transmutation theory; text criticism |
| Wouter J. Hanegraaff | *Dictionary of Gnosis and Western Esotericism* (Brill, 2006) | Actor/Analyst distinction; historiographical methodology |
| Michela Pereira | Medieval alchemy research | Medieval Islamic continuity; Catalan tradition |
| Pamela Smith | *The Business of Alchemy* (U Chicago, 2005) | Material culture; artisanal epistemology; embodied knowledge |
| Garth Fowden | *The Egyptian Hermes* (1986) | Late Antique roots; Byzantine alchemy; Zosimos |
| Lawrence Principe | Practical alchemy & experimental reconstruction | Modern reassessment of operations; hands-on verification |

For more: → `PROMPTS.md` (§ 6)

---

## Vocabulary Lock (Enum Values)

All controlled vocabulary is in **one file:** `docs/VOCABULARY.md`

**Never invent enum values.** Valid options:
- **era:** ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
- **role_primary:** ALCHEMIST, CHEMIST, SCHOLAR, PHILOSOPHER, PHYSICIAN, TRANSLATOR, MATHEMATICIAN, POET, PATRON, CLERICAL
- **text_type:** PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA
- **category_type:** ACTOR_TERM, ANALYST_TERM
- **confidence:** HIGH, MEDIUM, LOW
- **review_status:** DRAFT, REVIEWED, VERIFIED
- **source_method:** MANUAL, AI_ASSISTED, SCHOLARSHIP_BASED

For explanations: → `docs/VOCABULARY.md`

---

## Before You Start

1. **What's my task?** Find it in `docs/agents/TASK_ROUTING.md`
2. **What do I read?** Follow the prerequisites in that file
3. **Write what?** Check `STYLEGUIDE.md` for your content type
4. **What enums can I use?** Check `docs/VOCABULARY.md`
5. **Execute:** Read your task-specific prompt in `docs/agents/PROMPT_*.md`

---

## Checking Your Work

Before committing:

- [ ] Word count meets minimum for type?
- [ ] All required sections present?
- [ ] Book titles italicized, proper names NOT italicized?
- [ ] Claims grounded in named scholars?
- [ ] All entity links valid (≥3 per entry)?
- [ ] No markdown artifacts, hashtags, bullets?
- [ ] Bibliography in DGWE format?
- [ ] Provenance metadata complete (source_method, review_status, confidence)?
- [ ] All enum values from `docs/VOCABULARY.md` (not invented)?
- [ ] ACTOR_TERM/ANALYST_TERM distinction explicit (if concept)?

See `STYLEGUIDE.md` Validation Checklist for full details.

---

## Do Not Auto-Suggest Planning Skills

The user does not want unsolicited `/plan` or `/phase-gate` prompts. Invoke skills only when explicitly asked by name.

---

*For specific task guidance, see `docs/agents/TASK_ROUTING.md`. For historiographical context, see `PROMPTS.md`. For prose standards, see `STYLEGUIDE.md`.*

**Last updated:** 2026-05-22  
**Current phase:** Phase 2 (Persons, texts, concepts expansion)
