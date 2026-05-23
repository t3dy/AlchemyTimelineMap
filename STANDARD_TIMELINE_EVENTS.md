# Timeline Event Specification

**Lifetime:** Read when writing or enriching timeline events. Layer 3 (Operational Standards).

**Authority:** If this contradicts `SCHEMA.json`, the schema wins.

---

## Word Count

**100–250 words** (plain text, no HTML tags)

---

## Required Elements

Every timeline event description **must** include all four:

1. **Exact date or date range** — "c. 1320," "1492–1495," "6th century"
2. **Named location** — city preferably; region at minimum
3. **Named actors** — at least one person, text, or institution
4. **Historiographical significance** — final sentence explaining why this matters to alchemy/chemistry history

---

## Structure

```
[Date], [Location]: [Main narrative — what happened, who did it, what was discovered/produced].

[Scholarly contextualization — why it matters]. [Connection to broader developments or transmission].
```

---

## Entity Linking

Mark all entity names with `[LINK:slug]` for the main session to convert to HTML links:

```
...as recorded by [LINK:roger-bacon], who integrated Arabic distillation techniques 
described in [LINK:summa-perfectionis] into Latin scholastic philosophy...
```

Each event must link to at least 1 person, text, or concept. Use slugs exactly as they appear in the database.

---

## Example (Passing Entry)

> c. 1250, Andalusia: The scholar Gerard of Cremona, working in Muslim Spain, completes his Latin translation of the *Kitāb al-Ḥāsib* (attributed to [LINK:jabir-ibn-hayyan]), a foundational Arabic alchemical text teaching distillation of alkalis and mineral acids. This translation represents the first systematic introduction of Arabic practical alchemical knowledge into the Latin West and will circulate widely among European alchemists for the next three centuries. The operations described in Jabir's texts were immediately replicable and produced observable effects, establishing [LINK:distillation] in medieval universities as a legitimate natural philosophy.

Word count: 98. All required elements present.

---

## Validation Checklist

- [ ] Date is specific (exact year or "c. [year]")?
- [ ] Location named with region or city?
- [ ] At least one person, text, or institution named?
- [ ] Final sentence states historiographical significance explicitly?
- [ ] Word count 100–250?
- [ ] No markdown artifacts (`#`, `*`, `**`, `-`, `[]`, `{}`)?
- [ ] At least one `[LINK:slug]` markup present?
- [ ] All slugs in `[LINK:slug]` markup exist in database?
- [ ] Plain text only (no HTML tags)?
- [ ] Provenance metadata attached: `source_method`, `review_status`, `confidence`?

---

## What Fails Validation

- **Under 100 words** — too terse to provide context or significance
- **No historiographical significance** — a description without "why this matters" is a chronicle, not history
- **No named actor** — anonymous events cannot be linked to entities
- **Invented slug** — any `[LINK:slug]` that doesn't exist in the database breaks site generation
- **Markdown in prose** — `*` or `**` instead of HTML; `#` headers; bullet points

---

## Prose Standards

- Third person, authoritative, encyclopedia tone
- Book titles and manuscript names in italics: *Summa Perfectionis*, *Emerald Tablet*
- Foreign terms italicized on first use: *distillatio*, *sublimatio*
- Proper names of persons and places: NOT italicized
- No placeholder text ("to be added," "N/A," "TBD")

---

*For historiographical context, see `CONCEPTUAL_FRAMEWORK.md`. For enum values, see `SCHEMA.json`. For batch enrichment strategy, read `CONTEXT_ENGINEERING.md` first.*
