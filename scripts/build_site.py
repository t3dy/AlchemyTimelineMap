#!/usr/bin/env python3
"""
ALCHEMYTIMELINEMAP main deploy script: SQLite → static HTML/CSS/JS

This script reads the SQLite database and generates all static HTML pages:
- index.html (home)
- timeline.html (timeline viewer)
- map.html (Leaflet.js map)
- persons/[slug].html (100+ biography pages)
- texts/[slug].html (50+ text analysis pages)
- concepts/[slug].html (30+ concept definition pages)
- data/data.json (all entities + relationships)
- data/timeline.json (events + coordinates for JS)

Usage:
    python scripts/build_site.py

Output:
    site/ folder with all generated HTML/CSS/JS

Author: Claude
Date: 2026-05-22
"""

import json
import sqlite3
import sys
import re
from pathlib import Path
from datetime import datetime

# Database and output paths
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
SITE_PATH = Path(__file__).parent.parent / "site"


def convert_links_to_html(text, entity_map):
    """Convert [LINK:slug] markers to proper HTML links with tooltips."""
    if not text:
        return text

    pattern = r'\[LINK:([^\]]+)\]+'

    def normalize_slug(value):
        return re.sub(r"[^a-z0-9-]", "", value.strip().lower().replace("_", "-").replace(" ", "-"))

    def replace_link(match):
        slug = normalize_slug(match.group(1))

        # Determine entity type and get name
        if slug in entity_map.get('concepts', {}):
            entity = entity_map['concepts'][slug]
            href = f"../concepts/{slug}.html"
            title = f"Concept: {entity['label']}"
            name = entity['label']
        elif slug in entity_map.get('persons', {}):
            entity = entity_map['persons'][slug]
            href = f"../persons/{slug}.html"
            title = f"Person: {entity['name']}"
            name = entity['name']
        elif slug in entity_map.get('texts', {}):
            entity = entity_map['texts'][slug]
            href = f"../texts/{slug}.html"
            title = f"Text: {entity['title']}"
            name = entity['title']
        else:
            return match.group(1).strip()

        return f'<a href="{href}" class="dh-link" title="{title}">{name}</a>'

    converted = re.sub(pattern, replace_link, text)
    converted = re.sub(r"(</a>)\]+", r"\1", converted)
    converted = re.sub(r"(?<!\*)\*([^*\n<>]{1,120})\*(?!\*)", r"<i>\1</i>", converted)
    return converted.replace("[", "").replace("]", "")


def extract_concept_tags(html_text, concepts_list):
    """Extract concept slugs from [LINK:*] markers."""
    if not html_text:
        return []

    pattern = r'\[LINK:([^\]]+)\]+'
    tags = []
    for match in re.finditer(pattern, html_text):
        slug = re.sub(r"[^a-z0-9-]", "", match.group(1).strip().lower().replace("_", "-").replace(" ", "-"))
        if slug in concepts_list:
            tags.append(slug)
    return list(dict.fromkeys(tags))  # Deduplicate while preserving order


def init_site_structure():
    """Create output directory structure."""
    print("Initializing site structure...")
    SITE_PATH.mkdir(parents=True, exist_ok=True)
    (SITE_PATH / "persons").mkdir(exist_ok=True)
    (SITE_PATH / "texts").mkdir(exist_ok=True)
    (SITE_PATH / "concepts").mkdir(exist_ok=True)
    (SITE_PATH / "events").mkdir(exist_ok=True)
    (SITE_PATH / "data").mkdir(exist_ok=True)
    (SITE_PATH / "assets").mkdir(exist_ok=True)
    print("  [OK] Directory structure created")


def write_html_page(path, content):
    """Write HTML page to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_index_html():
    """Generate index.html (home page)."""
    print("\nGenerating index.html...")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALCHEMYTIMELINEMAP: Alchemy & Chemistry History</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1>ALCHEMYTIMELINEMAP</h1>
        <p>An interactive timeline and map of alchemy and chemistry history</p>
        <p>500 events spanning Late Antiquity through the early modern period</p>
        <p>Coverage: Europe, North Africa, Middle East</p>
    </header>

    <nav>
        <ul>
            <li><a href="timeline.html">Timeline</a></li>
            <li><a href="map.html">Map</a></li>
            <li><a href="persons/">Persons</a></li>
            <li><a href="texts/">Texts</a></li>
            <li><a href="concepts/">Concepts</a></li>
        </ul>
    </nav>

    <main>
        <section>
            <h2>Welcome</h2>
            <p>This portal presents alchemy and chemistry as a rigorous, practical discipline rooted in craft knowledge and operational success—not mysticism or failed transmutation quests.</p>
            <p>Explore the interactive timeline, browse the geographic map, and discover the persons, texts, and concepts that shaped this tradition.</p>
        </section>

        <section>
            <h2>About</h2>
            <p>Built to the historiographical standards of William R. Newman, Pamela H. Smith, and Wouter J. Hanegraaff, this portal synthesizes:</p>
            <ul>
                <li>Archaeological evidence from excavated alchemical laboratories</li>
                <li>Material culture analysis of apparatus and crucible production</li>
                <li>Experimental reconstruction of historical techniques (Making and Knowing Project)</li>
                <li>Artisanal epistemology: knowledge embodied in craft practice</li>
            </ul>
        </section>
    </main>

    <footer>
        <p>&copy; 2026 ALCHEMYTIMELINEMAP. Generated on {{DATE}}.</p>
    </footer>
</body>
</html>""".replace("{{DATE}}", datetime.now().isoformat())

    write_html_page(SITE_PATH / "index.html", html)
    print("  [OK] index.html created")


def generate_timeline_html():
    """Generate timeline.html (sidebar-filtered timeline with index cards)."""
    print("Generating timeline.html...")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1><a href="./">ALCHEMYTIMELINEMAP</a> &mdash; Timeline</h1>
    </header>

    <nav>
        <ul>
            <li><a href="./">Home</a></li>
            <li><a href="map.html">Map</a></li>
        </ul>
    </nav>

    <main>
        <section class="timeline-page">
            <h2>Timeline of Alchemy &amp; Chemistry</h2>
            <p id="timeline-event-count" class="timeline-info">Loading&hellip;</p>

            <div class="timeline-layout">

                <aside class="timeline-filters">
                    <div class="filter-panel">
                        <div class="filter-panel__header">
                            <h3>Filter events</h3>
                            <button id="clear-filters-btn" class="btn-clear">Reset</button>
                        </div>

                        <details class="filter-group" open>
                            <summary>Era</summary>
                            <div class="era-filter-options"></div>
                        </details>

                        <details class="filter-group">
                            <summary>Person</summary>
                            <input type="search" class="filter-search" placeholder="Search persons&hellip;"
                                   data-search-target="person-filter-options">
                            <div class="person-filter-options"></div>
                        </details>

                        <details class="filter-group">
                            <summary>Concept</summary>
                            <input type="search" class="filter-search" placeholder="Search concepts&hellip;"
                                   data-search-target="concept-filter-options">
                            <div class="concept-filter-options"></div>
                        </details>
                    </div>
                </aside>

                <div id="timeline-container" class="timeline-main">
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; ALCHEMYTIMELINEMAP &mdash; <a href="./">Home</a> | <a href="map.html">Map</a></p>
    </footer>

    <script src="assets/timeline.js"></script>
</body>
</html>"""

    write_html_page(SITE_PATH / "timeline.html", html)
    print("  [OK] timeline.html created (with filter controls)")


def generate_map_html():
    """Generate map.html (Leaflet.js map)."""
    print("Generating map.html...")
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="assets/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
</head>
<body>
    <header>
        <h1><a href="./">ALCHEMYTIMELINEMAP</a> — Map</h1>
    </header>

    <nav>
        <ul>
            <li><a href="./">Home</a></li>
            <li><a href="timeline.html">Timeline</a></li>
        </ul>
    </nav>

    <main>
        <section>
            <div id="map" style="height: 600px; width: 100%;"></div>
        </section>
    </main>

    <footer>
        <p>Map generated on {{DATE}}.</p>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script src="assets/map.js"></script>
</body>
</html>""".replace("{{DATE}}", datetime.now().isoformat())

    write_html_page(SITE_PATH / "map.html", html)
    print("  [OK] map.html created")


def generate_persons_pages(entity_map):
    """Generate persons/[slug].html biography pages with relationship sections."""
    print("\nGenerating persons/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, name, role_primary, era, bio_html FROM persons")
    persons = cursor.fetchall()

    for person in persons:
        slug = person["slug"]
        bio_html = convert_links_to_html(person["bio_html"], entity_map)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{person['name']} | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <header>
        <h1><a href="../">ALCHEMYTIMELINEMAP</a> — {person['name']}</h1>
    </header>

    <nav>
        <ul>
            <li><a href="../">Home</a></li>
            <li><a href="./">Persons</a></li>
        </ul>
    </nav>

    <main>
        <article>
            <h2>{person['name']}</h2>
            <p><strong>Role:</strong> {person['role_primary']} | <strong>Era:</strong> {person['era']}</p>
            <div class="bio">
                {bio_html}
            </div>
        </article>

        <div id="related-concepts"></div>
        <div id="related-texts"></div>
        <div id="related-events"></div>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>

    <script src="../assets/relationships.js"></script>
    <script src="../assets/entity-page-relationships.js"></script>
</body>
</html>"""
        write_html_page(SITE_PATH / "persons" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(persons)} persons pages created")


def generate_texts_pages(entity_map):
    """Generate texts/[slug].html text analysis pages with relationship sections."""
    print("\nGenerating texts/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, title, text_type, original_language, composition_date, analysis_html FROM texts")
    texts = cursor.fetchall()

    for text in texts:
        slug = text["slug"]
        analysis_html = convert_links_to_html(text["analysis_html"], entity_map)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{text['title']} | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <header>
        <h1><a href="../">ALCHEMYTIMELINEMAP</a> — {text['title']}</h1>
    </header>

    <nav>
        <ul>
            <li><a href="../">Home</a></li>
            <li><a href="./">Texts</a></li>
        </ul>
    </nav>

    <main>
        <article>
            <h2><i>{text['title']}</i></h2>
            <p><strong>Type:</strong> {text['text_type']} | <strong>Language:</strong> {text['original_language']} | <strong>Composed:</strong> {text['composition_date']}</p>
            <div class="analysis">
                {analysis_html}
            </div>
        </article>

        <div id="related-concepts"></div>
        <div id="related-persons"></div>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>

    <script src="../assets/relationships.js"></script>
    <script src="../assets/entity-page-relationships.js"></script>
</body>
</html>"""
        write_html_page(SITE_PATH / "texts" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(texts)} texts pages created")


def generate_concepts_pages(entity_map):
    """Generate concepts/[slug].html concept definition pages with relationship sections."""
    print("\nGenerating concepts/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, label, category_type, definition_short FROM concepts")
    concepts = cursor.fetchall()

    for concept in concepts:
        slug = concept["slug"]
        definition_html = convert_links_to_html(concept["definition_short"], entity_map)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{concept['label']} | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <header>
        <h1><a href="../">ALCHEMYTIMELINEMAP</a> — {concept['label']}</h1>
    </header>

    <nav>
        <ul>
            <li><a href="../">Home</a></li>
            <li><a href="./">Concepts</a></li>
        </ul>
    </nav>

    <main>
        <article>
            <h2>{concept['label']}</h2>
            <p><strong>Category:</strong> {concept['category_type']}</p>
            <div class="definition">
                {definition_html}
            </div>
        </article>

        <div id="related-persons"></div>
        <div id="related-texts"></div>
        <div id="related-events"></div>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>

    <script src="../assets/relationships.js"></script>
    <script src="../assets/entity-page-relationships.js"></script>
</body>
</html>"""
        write_html_page(SITE_PATH / "concepts" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(concepts)} concepts pages created")


def era_from_year(year):
    """Derive era label from start year."""
    if year is None:
        return "MEDIEVAL"
    if year < 600:
        return "LATE_ANTIQUE"
    if year < 1400:
        return "MEDIEVAL"
    return "EARLY_MODERN"


ERA_LABELS = {
    "LATE_ANTIQUE": "Late Antiquity (3rd–7th c.)",
    "MEDIEVAL": "Medieval (7th–15th c.)",
    "EARLY_MODERN": "Early Modern (15th–18th c.)",
}


def strip_html(html):
    """Strip HTML tags from text."""
    if not html:
        return ""
    return re.sub(r"<[^>]+>", "", html).strip()


def escapeHtml(text):
    """HTML-escape a string."""
    if not text:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def generate_event_pages(entity_map):
    """Generate events/[slug].html individual encyclopedia pages for all 582 events."""
    print("\nGenerating events/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.slug, t.date_label, t.date_start_year, t.date_end_year,
               t.location_slug, l.place_name, l.region,
               t.description, t.persons_involved, t.texts_involved, t.concepts_involved,
               t.scholarly_grounding,
               t.source_method, t.review_status, t.confidence
        FROM timeline_events t
        LEFT JOIN locations l ON t.location_slug = l.slug
        ORDER BY t.date_start_year NULLS LAST
    """)
    events = cursor.fetchall()

    persons_map = {p["slug"]: p["name"] for p in cursor.execute("SELECT slug, name FROM persons")}
    texts_map = {t["slug"]: t["title"] for t in cursor.execute("SELECT slug, title FROM texts")}
    concepts_map = {c["slug"]: c["label"] for c in cursor.execute("SELECT slug, label FROM concepts")}
    conn.close()

    for event in events:
        slug = event["slug"]
        description_html = event["description"] or ""
        era = era_from_year(event["date_start_year"])
        place_name = event["place_name"] or event["location_slug"].replace("-", " ").title()
        region = event["region"] or ""

        try:
            persons = json.loads(event["persons_involved"] or "[]")
        except (json.JSONDecodeError, TypeError):
            persons = []
        try:
            texts = json.loads(event["texts_involved"] or "[]")
        except (json.JSONDecodeError, TypeError):
            texts = []
        try:
            concepts = json.loads(event["concepts_involved"] or "[]")
        except (json.JSONDecodeError, TypeError):
            concepts = []

        # Build related entities sections
        persons_html = ""
        if persons:
            items = "".join(
                f'<li><a href="../persons/{p}.html" class="dh-link">{persons_map.get(p, p)}</a></li>'
                for p in persons
            )
            persons_html = f'<section class="related-section"><h3>Persons Involved</h3><ul>{items}</ul></section>'

        texts_html = ""
        if texts:
            items = "".join(
                f'<li><a href="../texts/{t}.html" class="dh-link"><i>{texts_map.get(t, t)}</i></a></li>'
                for t in texts
            )
            texts_html = f'<section class="related-section"><h3>Texts</h3><ul>{items}</ul></section>'

        concepts_html = ""
        if concepts:
            items = "".join(
                f'<li><a href="../concepts/{c}.html" class="dh-link">{concepts_map.get(c, c)}</a></li>'
                for c in concepts
            )
            concepts_html = f'<section class="related-section"><h3>Concepts</h3><ul>{items}</ul></section>'

        # Confidence / review badge
        review = event["review_status"] or "DRAFT"
        confidence = event["confidence"] or "LOW"
        scholarly_grounding = event["scholarly_grounding"] or ""

        page_title = f"{event['date_label']}, {place_name}"

        # Scholarly grounding section (if present)
        scholarly_section = ""
        if scholarly_grounding:
            scholarly_section = f"""
            <section class="event-page__scholarly">
                <h3>Scholarly Context</h3>
                <p><em>{escapeHtml(scholarly_grounding)}</em></p>
            </section>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | ALCHEMYTIMELINEMAP</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <header>
        <h1><a href="../">ALCHEMYTIMELINEMAP</a></h1>
    </header>

    <nav>
        <ul>
            <li><a href="../">Home</a></li>
            <li><a href="../timeline.html">← Timeline</a></li>
            <li><a href="../map.html">Map</a></li>
        </ul>
    </nav>

    <main>
        <article class="event-page">
            <div class="event-page__header">
                <span class="event-page__date">{event['date_label']}</span>
                <span class="event-page__era">{ERA_LABELS.get(era, era)}</span>
            </div>

            <h2 class="event-page__location">{place_name}</h2>
            {"<p class='event-page__region'>" + region + "</p>" if region else ""}

            {scholarly_section}

            <div class="event-page__body">
                {description_html}
            </div>

            {persons_html}
            {texts_html}
            {concepts_html}

            <footer class="event-page__provenance">
                <small>Review status: <strong>{review}</strong> &nbsp;|&nbsp; Confidence: <strong>{confidence}</strong></small>
            </footer>
        </article>
    </main>

    <footer>
        <p><a href="../timeline.html">← Back to Timeline</a> &nbsp;|&nbsp; <a href="../map.html">View on Map</a></p>
    </footer>
</body>
</html>"""
        write_html_page(SITE_PATH / "events" / f"{slug}.html", html)

    print(f"  [OK] {len(events)} event pages created")


def extract_tags_for_entities(concepts_dict):
    """Extract and enrich entities with concept tags."""
    print("\nExtracting concept tags from entity content...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    concepts_set = set(concepts_dict.keys())

    # Extract tags for persons
    cursor.execute("SELECT slug, bio_html FROM persons")
    persons_tags = {}
    for row in cursor.fetchall():
        tags = extract_concept_tags(row["bio_html"], concepts_set)
        if tags:
            persons_tags[row["slug"]] = tags

    # Extract tags for texts
    cursor.execute("SELECT slug, analysis_html FROM texts")
    texts_tags = {}
    for row in cursor.fetchall():
        tags = extract_concept_tags(row["analysis_html"], concepts_set)
        if tags:
            texts_tags[row["slug"]] = tags

    conn.close()
    return persons_tags, texts_tags


def build_relationship_indices(persons, texts, concepts, events, persons_tags, texts_tags):
    """Build cross-reference maps for relational browsing."""
    print("Building relationship indices...")

    persons_dict = {p["slug"]: p for p in persons}
    texts_dict = {t["slug"]: t for t in texts}
    concepts_dict = {c["slug"]: c for c in concepts}

    relationships = {
        "person_to_concepts": {},
        "person_to_texts": {},
        "person_to_events": {},
        "text_to_persons": {},
        "text_to_concepts": {},
        "concept_to_persons": {},
        "concept_to_texts": {},
        "concept_to_events": {},
    }

    # Person to concepts (from extracted tags)
    for person_slug, concept_slugs in persons_tags.items():
        relationships["person_to_concepts"][person_slug] = concept_slugs

    # Text to concepts (from extracted tags)
    for text_slug, concept_slugs in texts_tags.items():
        relationships["text_to_concepts"][text_slug] = concept_slugs

    # Person to events, person to texts, concept relationships from events
    for event in events:
        raw_persons = event.get("persons_involved", [])
        raw_concepts = event.get("concepts_involved", [])

        # Accept both pre-parsed lists (from export) and JSON strings (from raw DB rows)
        if isinstance(raw_persons, str):
            try:
                raw_persons = json.loads(raw_persons)
            except (json.JSONDecodeError, ValueError):
                raw_persons = [p.strip() for p in raw_persons.split(";") if p.strip()]
        if isinstance(raw_concepts, str):
            try:
                raw_concepts = json.loads(raw_concepts)
            except (json.JSONDecodeError, ValueError):
                raw_concepts = [c.strip() for c in raw_concepts.split(";") if c.strip()]

        for person_slug in (raw_persons or []):
            if person_slug not in relationships["person_to_events"]:
                relationships["person_to_events"][person_slug] = []
            relationships["person_to_events"][person_slug].append(event["slug"])

        for concept_slug in (raw_concepts or []):
            if concept_slug not in relationships["concept_to_events"]:
                relationships["concept_to_events"][concept_slug] = []
            relationships["concept_to_events"][concept_slug].append(event["slug"])

    # Invert person_to_concepts to create concept_to_persons
    for person_slug, concept_slugs in relationships["person_to_concepts"].items():
        for concept_slug in concept_slugs:
            if concept_slug not in relationships["concept_to_persons"]:
                relationships["concept_to_persons"][concept_slug] = []
            relationships["concept_to_persons"][concept_slug].append(person_slug)

    # Invert text_to_concepts to create concept_to_texts
    for text_slug, concept_slugs in relationships["text_to_concepts"].items():
        for concept_slug in concept_slugs:
            if concept_slug not in relationships["concept_to_texts"]:
                relationships["concept_to_texts"][concept_slug] = []
            relationships["concept_to_texts"][concept_slug].append(text_slug)

    return relationships


def validate_data_integrity():
    """Validate that all timeline_events have valid location_slug references before export."""
    print("\nValidating data integrity...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for orphaned location_slug references
    cursor.execute("""
        SELECT COUNT(*) as orphaned_count
        FROM timeline_events t
        WHERE NOT EXISTS (SELECT 1 FROM locations l WHERE l.slug = t.location_slug)
    """)
    result = cursor.fetchone()
    orphaned_count = result[0] if result else 0

    if orphaned_count > 0:
        print(f"  [ERROR] Found {orphaned_count} events with invalid location_slug references:")
        cursor.execute("""
            SELECT t.slug, t.location_slug, t.date_label
            FROM timeline_events t
            WHERE NOT EXISTS (SELECT 1 FROM locations l WHERE l.slug = t.location_slug)
            ORDER BY t.location_slug
        """)
        for slug, location_slug, date_label in cursor.fetchall():
            print(f"    - Event '{slug}' ({date_label}) references non-existent location '{location_slug}'")
        conn.close()
        sys.exit(1)

    # Get total counts for metadata
    cursor.execute("SELECT COUNT(*) FROM timeline_events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM locations")
    total_locations = cursor.fetchone()[0]

    conn.close()

    print(f"  [OK] All {total_events} events have valid location references")
    print(f"  [OK] Database has {total_locations} locations")

    return {"total_events": total_events, "total_locations": total_locations}


def export_json_data():
    """Export data.json (all entities for JavaScript consumers)."""
    print("\nExporting JSON data...")

    # Validate data integrity first
    validation_meta = validate_data_integrity()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query all entities
    cursor.execute("SELECT * FROM persons")
    persons = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM texts")
    texts = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM concepts")
    concepts = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT slug, place_name, latitude, longitude, region, modern_name,
               alchemical_significance, key_periods
        FROM locations
    """)
    locations = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT t.*, l.place_name, l.region
        FROM timeline_events t
        LEFT JOIN locations l ON t.location_slug = l.slug
        ORDER BY t.date_start_year NULLS LAST
    """)
    raw_events = cursor.fetchall()

    conn.close()

    # Enrich events with era, summary, and parsed entity arrays
    events = []
    for row in raw_events:
        e = dict(row)
        # Derive era from start year
        e["era"] = era_from_year(e.get("date_start_year"))
        # Plain-text summary (first 200 chars) for index card display
        e["summary"] = strip_html(e.get("description") or "")[:200].strip()
        # Parse JSON arrays (stored as strings in SQLite)
        for field in ("persons_involved", "texts_involved", "concepts_involved"):
            val = e.get(field)
            if isinstance(val, str):
                try:
                    e[field] = json.loads(val)
                except (json.JSONDecodeError, ValueError):
                    e[field] = []
            elif val is None:
                e[field] = []
        # Drop full description HTML from index to reduce data.json size
        # Full content is on individual event pages
        e["description"] = e["summary"]
        events.append(e)

    # Extract concept tags and build relationships
    concepts_dict = {c["slug"]: c for c in concepts}
    persons_tags, texts_tags = extract_tags_for_entities(concepts_dict)
    relationships = build_relationship_indices(persons, texts, concepts, events, persons_tags, texts_tags)

    # Enrich persons and texts with concept_tags
    for person in persons:
        person["concept_tags"] = persons_tags.get(person["slug"], [])

    for text in texts:
        text["concept_tags"] = texts_tags.get(text["slug"], [])

    data = {
        "meta": {
            "total_events": validation_meta["total_events"],
            "total_locations": validation_meta["total_locations"],
            "mapped_events": len(events),
            "unmapped_events": validation_meta["total_events"] - len(events),
            "validation_passed": True,
            "generated": datetime.now().isoformat(),
        },
        "persons": persons,
        "texts": texts,
        "concepts": concepts,
        "locations": locations,
        "events": events,
        "relationships": relationships,
    }

    data_path = SITE_PATH / "data" / "data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)

    print(f"  [OK] data.json exported ({len(persons)} persons, {len(texts)} texts, {len(concepts)} concepts, {len(events)} events)")
    print(f"  [OK] concept_tags extracted for {len(persons_tags)} persons, {len(texts_tags)} texts")
    print(f"  [OK] relationship indices built")
    print(f"  [OK] validation metadata included (mapped_events: {len(events)}/{validation_meta['total_events']})")


def build_entity_map():
    """Build entity_map for link conversion."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    entity_map = {"persons": {}, "texts": {}, "concepts": {}}

    cursor.execute("SELECT slug, name FROM persons")
    for row in cursor.fetchall():
        entity_map["persons"][row["slug"]] = {"name": row["name"]}

    cursor.execute("SELECT slug, title FROM texts")
    for row in cursor.fetchall():
        entity_map["texts"][row["slug"]] = {"title": row["title"]}

    cursor.execute("SELECT slug, label FROM concepts")
    for row in cursor.fetchall():
        entity_map["concepts"][row["slug"]] = {"label": row["label"]}

    conn.close()
    return entity_map


def build_site():
    """Main deployment function."""
    print("=" * 60)
    print("ALCHEMYTIMELINEMAP DEPLOYMENT")
    print("=" * 60)

    init_site_structure()
    entity_map = build_entity_map()
    generate_index_html()
    generate_timeline_html()
    generate_map_html()
    generate_persons_pages(entity_map)
    generate_texts_pages(entity_map)
    generate_concepts_pages(entity_map)
    generate_event_pages(entity_map)
    export_json_data()

    print("\n" + "=" * 60)
    print("[SUCCESS] DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"\nOutput: {SITE_PATH}/")
    print("Next step: Copy site/ to docs/ and push to GitHub Pages")


if __name__ == "__main__":
    build_site()
