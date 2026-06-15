# Figure Essay Brief — write ONE 3,000–5,000 word essay

You are writing the single long-form essay for one historical figure on the
ALCHEMYTIMELINEMAP. The figure now has exactly one timeline index card that
links to this essay (rendered from `persons.bio_html`). Your essay supersedes
the scattered per-figure events, so it must be the complete account.

## Output
Write a single HTML fragment to: `staging/figure_essays/<person-slug>.html`
(the slug is given to you). Do not edit the database; the loader does that.

## Hard requirements (the loader rejects essays that fail these)
1. **Word count 3,000–5,000** (counted as text with HTML tags stripped). Aim ~3,600.
2. **HTML fragment only** — use `<p>`, `<h2>`, `<i>` tags. No `<html>/<body>/<head>`,
   no markdown (`#`, `*`, `-`, `**`), no `<ul>`/`<li>`.
3. **`[LINK:slug]` markup** for every entity you name that exists in the database.
   The slug MUST exist. Get the full valid list with:
   `python3 -c "import sqlite3;c=sqlite3.connect('db/alchemy_timeline.db');[print(r[0]) for t in ('persons','texts','concepts') for r in c.execute(f'SELECT slug FROM {t}')]"`
   Only link slugs from that list. Do NOT link the subject to their own page.

## Content requirements
Open with the figure's name (not "This figure…"), with dates, origin, role, era,
and one sentence of significance. Then cover, in `<h2>` sections (250–450 words each):
- **Life and historical context**
- **Works / texts written** — name the actual treatises (use `[LINK:slug]` for texts in the DB)
- **Operational / chemical contribution** — material grounding: apparatus, substances,
  observable results, hazards. What was actually done in the laboratory or workshop?
- **Relationships and collaborators** — teachers, students, patrons, rivals, correspondents
  (e.g. Zosimos↔Theosebeia). Link people who exist in the DB.
- **Transmission and reception** — how the work circulated and who it influenced
- **Scholarly debates and modern historiography** — name specific modern scholars
  (e.g. Principe, Newman, Pereira, Smith, Hanegraaff, Copenhaver) and their positions
- End with `<h2>Literature</h2>`: 5–12 references, DGWE format, one per `<p>`:
  `Author Last, First. Title. Publisher, Year.` (title text plain; alphabetized; no URLs)

## Editorial invariants (mandatory)
- **Provenance:** every substantive claim traces to a named scholar or primary source.
- **No endorsement of transmutation:** report historical beliefs accurately; never imply
  metals were actually transmuted or that the philosophers' stone was real.
- **Actor/Analyst distinction:** historical actors used their own vocabulary; modern
  scholars apply analytical categories — never conflate them.
- Scholarly, encyclopedic, third-person tone. Text titles italicized with `<i>`; proper
  names not italicized. Accuracy over fluency — do not invent texts, dates, or scholars.

## Source material
Read the figure's existing biography to reuse accurate facts, then EXPAND and restructure
to the full length and section plan above (do not merely pad):
`python3 -c "import sqlite3;c=sqlite3.connect('db/alchemy_timeline.db');print(c.execute('SELECT bio_html FROM persons WHERE slug=?',('<person-slug>',)).fetchone()[0])"`

## Self-check before finishing
Run this and fix any problem it reports (must print OK):
```
python3 - <<'PY'
import re
p="staging/figure_essays/<person-slug>.html"
h=open(p).read()
import sqlite3;c=sqlite3.connect('db/alchemy_timeline.db')
slugs={r[0] for t in ('persons','texts','concepts') for r in c.execute(f'SELECT slug FROM {t}')}
wc=len(re.sub(r'<[^>]+>',' ',h).split())
bad=sorted({m for m in re.findall(r'\[LINK:([^\]]+)\]',h) if m.strip() not in slugs})
print('WORDS',wc,'OK' if 3000<=wc<=5000 else 'OUT-OF-RANGE')
print('BAD LINKS',bad if bad else 'OK')
PY
```
Return only a one-line status (figure slug, word count, OK/issues). Do not print the essay.
