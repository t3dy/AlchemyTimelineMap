# WRITING METHOD — turning research into prose, metadata, and website pages

How a verified research bundle (`staging/research_<slug>.json`) becomes durable content.
Pairs with `STANDARD_PERSON_BIOGRAPHIES.md` (the binding prose spec).

## Three destinations for one finding
1. **Metadata (structured)** → the new tables `person_itinerary`, `person_relationships`,
   and `concept_person_refs`. Machine-queryable; powers the maps in `../MAPRESEARCH`.
2. **Prose (bio_html)** → a "Travels" / "Connections" passage appended to the figure's
   biography, in `[LINK:slug]` markup. Rendered by `build_site.py`.
3. **Website** → regenerated automatically from bio_html when `build_site.py` runs.

## The Travels passage (bio_html)
- One to three short paragraphs, present-historical voice, matching the existing bio's
  register (see `STANDARD_PERSON_BIOGRAPHIES.md` for word counts and tone).
- Name places in order with dates; mark uncertainty in prose ("by an undocumented
  route", "around 1579") — never smooth a gap into false certainty.
- Link people and places with `[LINK:slug]`; every slug must already resolve
  (Invariant 4). If a target lacks a page, name it in plain text instead.
- No markdown artifacts in prose (no `#`, `*`, `-`, `[]`, `{}`); HTML only.
- End interpretive sentences with their warrant where natural (the scholar/source),
  consistent with the provenance invariant.

## Metadata writing rules
- Coordinates are real places (decimal degrees). Stops in chronological order.
- Carry `evidence`, `confidence`, `source` on every row; `review_status = DRAFT` for
  newly gathered data.
- `person_relationships`: `direction = true` only for asymmetric ties (patron-of,
  taught, cited); keep the actor's own language in `note`.

## Procedure
1. Validate the staged bundle (slugs exist or are flagged; enums legal; sources present).
2. Load metadata via the loader (`scripts/load_research_bundle.py`).
3. Append the `travel_note_html` to `bio_html` under a `<h3>Travels</h3>` /
   `<h3>Connections</h3>` heading (idempotent: replace an existing such block, don't
   stack duplicates).
4. Run `build_site.py`; spot-check the regenerated `site/persons/<slug>.html`.
5. Leave `review_status = DRAFT` until a human promotes it.

## Don't
- Don't paste raw research notes or citations as prose — synthesise.
- Don't add a travel claim that isn't also in the metadata (prose and data must agree).
- Don't promote to `REVIEWED` automatically.
