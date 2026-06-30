# methods/ — the working method system

One tight layer over the project's scattered process docs. Each file here is the
**entry point** for one kind of work; it points to the canonical authority rather than
duplicating it. When in doubt, start here.

| Area | File | Canonical sources it organizes |
|------|------|-------------------------------|
| **Style** (how output looks/reads) | `STYLE.md` | `STYLEGUIDE_CONSOLIDATED.md`, `STANDARD_*.md`, `../MAPRESEARCH/research/MAPTYPES_FRAMEWORK.md` |
| **Orchestration** (how we run agents) | `ORCHESTRATION.md` | `AGENT_LOADING_STRATEGY.md`, `CONTEXT_ENGINEERING.md`, `AGENT_PROMPT_*.md` |
| **Research** (how we find & source facts) | `RESEARCH.md` | `ENRICHMENT_WORKFLOW.md`, `CONCEPTUAL_FRAMEWORK.md` (invariants) |
| **Writing** (how facts become prose/metadata) | `WRITING.md` | `STANDARD_PERSON_BIOGRAPHIES.md`, `STANDARD_TIMELINE_EVENTS.md`, `ONTOLOGY.md` |

## The five non-negotiables (from CLAUDE.md, restated for every method)
1. **Provenance on every claim** — a named scholar or primary source.
2. **No endorsement of transmutation** — report beliefs; never imply truth.
3. **Actor/analyst distinction** — actors' vocabulary ≠ analysts' categories.
4. **All entity links must resolve** — every `[LINK:slug]` exists in the DB.
5. **Enums are locked** — no new values without `SCHEMA.json` first.

## The data-ontology gaps these methods exist to close (2026-06, from AUDIT)
- `concept_person_refs` and `concept_text_refs` are **empty** → thematic links missing.
- **No person-to-person relationships** → relational data missing.
- **No itinerary/travels** anywhere → itinerary data missing.
See `RESEARCH.md` + `WRITING.md` for the protocol that fills them, and
`docs/DATA_GAP_STUDY.md` for the current worklist.
