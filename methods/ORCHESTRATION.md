# ORCHESTRATION — running agents to enrich the corpus

How to fan work out to subagents safely. Pairs with `RESEARCH.md` (what they gather)
and `WRITING.md` (how results become prose/metadata).

## The core pattern: research → verify → stage → validate → load → rebuild
```
[research agents]  → staging/research_<slug>.json   (parallel, one per figure)
        ↓
[verifier agents]  → adversarially check each claim; drop the uncorroborated
        ↓
 main session      → validate slugs/enums/provenance; load to DB via a loader script
        ↓
 build_site.py     → regenerate the website
```
The main session is the only thing that writes to the DB. Agents only write to
`staging/`. (This mirrors the existing pipeline; see `PIPELINE.md`.)

## Tool choice
- **Agent tool (subagents)** — default for research/verification fan-out. Each gets
  `WebSearch`/`WebFetch`. Launch a batch in one message so they run concurrently.
- **Workflow tool** — only when the user has explicitly opted into multi-agent
  orchestration; encodes the loop above deterministically (fan-out research, pipeline
  through verify, barrier to dedup, then load). Do not invoke without that opt-in.

## Roles
- **Researcher** — given one figure + the `RESEARCH.md` output contract, returns sourced
  itinerary + relationships + concept tags + a travel-note paragraph. Cites everything.
- **Verifier** — given a researcher's claims, tries to *refute* each against an
  independent source; returns per-claim {corroborated, confidence, note}. Default to
  skeptical: uncertain → drop or mark LOW.
- **Integrator (main session)** — validates against `SCHEMA.json` enums + existing
  slugs, resolves/creates link targets, loads, rebuilds, spot-checks.

## Batching & provenance discipline
- Prioritise by leverage: figures with the most events but no itinerary first (see
  `docs/DATA_GAP_STUDY.md`).
- Everything machine/web-gathered loads as `review_status = DRAFT`, `source_method` set
  to the agent/run id, so a human can audit and promote.
- Never bulk-load unverified interpretive claims. Dates and place names may pass on a
  single good source; interpretation needs the verifier.

## Sandboxing research agents (lesson, 2026-06-29)
Research agents run with broad tools and CAN reach the DB. In the first runs an agent
wrote two bare person records directly to `persons` (harmless, valid figures, but
off-process). Until per-call tool restriction is available, every research prompt MUST
state plainly: **use Write ONLY for your one `staging/research_<slug>.json`; do NOT run
Bash/python/sqlite or modify the database or any other file; research via WebSearch/
WebFetch only.** The integrator then audits `persons` for unexpected new slugs after a
batch (compare counts before/after) and confirms all structured rows carry the run's
`source_method`.

## Prompt templates
Reusable researcher/verifier prompts live in `AGENT_PROMPT_BIOGRAPHY_ENRICHER.md` and
the other `AGENT_PROMPT_*.md` files; extend those rather than writing ad-hoc prompts.
