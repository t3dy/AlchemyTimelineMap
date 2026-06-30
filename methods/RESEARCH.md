# RESEARCH METHOD — sourced enrichment of figures, themes, relations, itineraries

How to find and record facts so they survive the project's invariants. Used by the
biographical-enrichment swarm (see `ORCHESTRATION.md`) and by hand.

## What we are filling (the four data categories)
1. **Biographical core** — already present as `bio_html`; we extend it.
2. **Itinerary** — where a figure was, when, and on what evidence (→ `person_itinerary`).
3. **Relational** — typed ties between people (→ `person_relationships`).
4. **Thematic** — which concepts a person/text embodies (→ `concept_person_refs`,
   `concept_text_refs`, currently empty).

## Source hierarchy (cite the highest tier you can reach)
1. **Primary sources** — the figure's own works, trial records, dedications, letters.
2. **Scholarly monographs / critical editions** — named author + work (DGWE format).
3. **Reference works** — DSB, DGWE, Stanford Encyclopedia, Oxford DNB, encyclopaedias.
4. **Tertiary / web** — acceptable for uncontested dates and place names; never the
   sole basis for an interpretive claim. Record the URL and date accessed.

## Recording rules
- Every fact carries a `source` string (author + work, or URL). No source → it does
  not enter the DB.
- Every record carries `confidence` ∈ {HIGH, MEDIUM, LOW} and `review_status` = `DRAFT`
  for machine/web-gathered data (a human promotes to `REVIEWED`).
- **Itinerary evidence** per stop/leg: `attested` | `approximate` (date uncertain) |
  `inferred` (route reconstructed). Never present a reconstruction as documented.
- **Relational evidence**: `attested` | `inferred`; plus `survives` (does direct
  documentary evidence survive?). Enmity (`polemicized-against`) is a real tie.
- **Actor/analyst**: record the actor's own term in `note`; tag the analyst category
  separately. Do not let "cited" silently become "influence".

## Output contract (what a researcher returns → `staging/research_<slug>.json`)
```json
{ "slug": "giordano-bruno",
  "itinerary": [ {"place":"Geneva","lat":46.20,"lon":6.14,"year_start":1579,"year_end":1579,
                  "dwell":1,"what":"…","evidence":"attested","leg_evidence":"inferred",
                  "source":"Rowland 2008"} ],
  "relationships": [ {"target":"henri-iii","type":"patron-of","direction":true,"weight":2,
                      "evidence":"attested","survives":true,"note":"…","source":"…"} ],
  "concepts": [ {"slug":"hermeticism","confidence":"HIGH","source":"Yates 1964"} ],
  "travel_note_html": "Prose paragraph(s) for bio_html, using [LINK:slug] markup.",
  "sources": ["…full citations…"] }
```
Targets/concepts that are not yet DB slugs are allowed but must be flagged so the main
session can create or map them (do not invent links that won't resolve — Invariant 4).

## Quality gate (before anything loads)
A second agent **verifies** each non-trivial claim against an independent source and
tries to refute it; a claim that cannot be corroborated is dropped to `LOW`/omitted.
See the verifier pattern in `ORCHESTRATION.md`.
