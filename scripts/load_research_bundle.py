#!/usr/bin/env python3
"""
load_research_bundle.py — load staging/research_<slug>.json bundles into the DB.

Writes to person_itinerary, person_relationships, concept_person_refs, and appends a
provenance-marked Travels/Connections block to persons.bio_html (idempotent — replaces
an existing block rather than stacking). Everything lands as review_status=DRAFT.

Validates: person exists; concept slugs exist; relationship targets are DB persons or
carry a target_label; [LINK:slug] markup in prose resolves. Reports unresolved links.

Usage: python load_research_bundle.py [slug ...]   (default: all staging/research_*.json)
"""
import sqlite3, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "alchemy_timeline.db"
STAGING = ROOT / "staging"
SOURCE_METHOD = "research_swarm_2026_06_29"
START, END = "<!--TRAVELS:START-->", "<!--TRAVELS:END-->"


def main():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    persons = {r["slug"] for r in c.execute("select slug from persons")}
    concepts = {r["slug"] for r in c.execute("select slug from concepts")}
    locations = {r["slug"] for r in c.execute("select slug from locations")}
    texts = {r["slug"] for r in c.execute("select slug from texts")}
    all_slugs = persons | concepts | locations | texts

    args = sys.argv[1:]
    files = ([STAGING / f"research_{s}.json" for s in args] if args
             else sorted(STAGING.glob("research_*.json")))
    if not files:
        print("No research bundles found in staging/."); return

    summary = []
    for f in files:
        if not f.exists():
            print(f"  [SKIP] {f.name}: not found"); continue
        b = json.loads(f.read_text(encoding="utf-8"))
        slug = b.get("slug")
        if slug not in persons:
            print(f"  [SKIP] {f.name}: person '{slug}' not in DB"); continue

        warns = []
        # ---- itinerary (replace) ----
        c.execute("delete from person_itinerary where person_slug=?", (slug,))
        for i, st in enumerate(b.get("itinerary", []), 1):
            loc = st.get("location_slug")
            if loc and loc not in locations:
                warns.append(f"itinerary location_slug '{loc}' not in DB (kept as name)"); loc = None
            c.execute("""insert into person_itinerary
                (person_slug,seq,place_name,location_slug,latitude,longitude,year_start,year_end,
                 dwell,what,evidence,leg_evidence,source,confidence,review_status,source_method)
                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'DRAFT', ?)""",
                (slug, i, st.get("place"), loc, st.get("lat"), st.get("lon"),
                 st.get("year_start"), st.get("year_end"), st.get("dwell"), st.get("what"),
                 st.get("evidence", "attested"), st.get("leg_evidence"),
                 st.get("source", "(unsourced)"), st.get("confidence", "MEDIUM"), SOURCE_METHOD))

        # ---- relationships (upsert) ----
        for r in b.get("relationships", []):
            tgt = r.get("target"); label = r.get("target_label")
            if tgt and tgt in concepts:
                warns.append(f"rel target '{tgt}' is a concept, not a person (skipped)"); continue
            if tgt and tgt not in persons and not label:
                label = tgt.replace("-", " ").title()
                warns.append(f"rel target '{tgt}' not a DB person (kept as label)")
            c.execute("""insert or replace into person_relationships
                (source_slug,target_slug,target_label,rel_type,direction,weight,evidence,survives,
                 note,source,date_start,date_end,confidence,review_status,source_method)
                values(?,?,?,?,?,?,?,?,?,?,?,?,?, 'DRAFT', ?)""",
                (slug, tgt or label, label, r.get("type"), 1 if r.get("direction") else 0,
                 r.get("weight", 1), r.get("evidence", "attested"), 1 if r.get("survives", True) else 0,
                 r.get("note"), r.get("source", "(unsourced)"), r.get("date_start"), r.get("date_end"),
                 r.get("confidence", "MEDIUM"), SOURCE_METHOD))

        # ---- concept links (thematic) ----
        for cl in b.get("concepts", []):
            cs = cl.get("slug") if isinstance(cl, dict) else cl
            if cs not in concepts:
                warns.append(f"concept '{cs}' not in DB (skipped)"); continue
            exists = c.execute("select 1 from concept_person_refs where concept_slug=? and person_slug=?", (cs, slug)).fetchone()
            if not exists:
                c.execute("insert into concept_person_refs(concept_slug,person_slug) values(?,?)", (cs, slug))

        # ---- bio_html travels block (idempotent) ----
        note = b.get("travel_note_html", "").strip()
        if note:
            def _resolve(mt):
                s = mt.group(1)
                if s in all_slugs:
                    return mt.group(0)
                warns.append(f"prose [LINK:{s}] unresolved -> plain text")
                return s.replace("-", " ").title()
            note = re.sub(r"\[LINK:([a-z0-9\-]+)\]", _resolve, note)
            row = c.execute("select bio_html from persons where slug=?", (slug,)).fetchone()
            bio = row["bio_html"] or ""
            block = f"{START}\n<h3>Travels and Connections</h3>\n{note}\n{END}"
            if START in bio and END in bio:
                bio = re.sub(re.escape(START) + r".*?" + re.escape(END), block, bio, flags=re.DOTALL)
            else:
                bio = bio.rstrip() + "\n\n" + block
            c.execute("update persons set bio_html=?, review_status='DRAFT' where slug=?", (bio, slug))

        c.commit()
        summary.append((slug, len(b.get("itinerary", [])), len(b.get("relationships", [])),
                        len(b.get("concepts", [])), len(warns)))
        print(f"  [OK] {slug}: {summary[-1][1]} stops, {summary[-1][2]} rels, {summary[-1][3]} concepts"
              + (f"  [{len(warns)} warnings]" if warns else ""))
        for w in warns:
            print(f"        - {w}")

    print(f"\nLoaded {len(summary)} bundles. Run: python scripts/build_site.py  to regenerate pages.")
    c.close()


if __name__ == "__main__":
    main()
