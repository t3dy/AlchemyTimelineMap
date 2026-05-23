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
from pathlib import Path
from datetime import datetime

# Database and output paths
DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"
SITE_PATH = Path(__file__).parent.parent / "site"


def init_site_structure():
    """Create output directory structure."""
    print("Initializing site structure...")
    SITE_PATH.mkdir(parents=True, exist_ok=True)
    (SITE_PATH / "persons").mkdir(exist_ok=True)
    (SITE_PATH / "texts").mkdir(exist_ok=True)
    (SITE_PATH / "concepts").mkdir(exist_ok=True)
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
    """Generate timeline.html (timeline viewer)."""
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
        <h1><a href="./">ALCHEMYTIMELINEMAP</a> — Timeline</h1>
    </header>

    <nav>
        <ul>
            <li><a href="./">Home</a></li>
            <li><a href="map.html">Map</a></li>
        </ul>
    </nav>

    <main>
        <section>
            <h2>Timeline of Alchemy & Chemistry</h2>
            <p>500 events from Late Antiquity through the early modern period.</p>
            <div id="timeline-container">
                <!-- Timeline JS will populate this -->
            </div>
        </section>
    </main>

    <footer>
        <p>Timeline generated on {{DATE}}.</p>
    </footer>

    <script src="assets/timeline.js"></script>
</body>
</html>""".replace("{{DATE}}", datetime.now().isoformat())

    write_html_page(SITE_PATH / "timeline.html", html)
    print("  [OK] timeline.html created")


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


def generate_persons_pages():
    """Generate persons/[slug].html biography pages."""
    print("\nGenerating persons/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, name, role_primary, era, bio_html FROM persons")
    persons = cursor.fetchall()

    for person in persons:
        slug = person["slug"]
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
                {person['bio_html']}
            </div>
        </article>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>
</body>
</html>"""
        write_html_page(SITE_PATH / "persons" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(persons)} persons pages created")


def generate_texts_pages():
    """Generate texts/[slug].html text analysis pages."""
    print("\nGenerating texts/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, title, text_type, original_language, composition_date, analysis_html FROM texts")
    texts = cursor.fetchall()

    for text in texts:
        slug = text["slug"]
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
        </article>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>
</body>
</html>"""
        write_html_page(SITE_PATH / "texts" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(texts)} texts pages created")


def generate_concepts_pages():
    """Generate concepts/[slug].html concept definition pages."""
    print("\nGenerating concepts/ pages...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT slug, label, category_type, definition_short FROM concepts")
    concepts = cursor.fetchall()

    for concept in concepts:
        slug = concept["slug"]
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
                {concept['definition_short']}
            </div>
        </article>
    </main>

    <footer>
        <p><a href="../">Back to home</a></p>
    </footer>
</body>
</html>"""
        write_html_page(SITE_PATH / "concepts" / f"{slug}.html", html)

    conn.close()
    print(f"  [OK] {len(concepts)} concepts pages created")


def export_json_data():
    """Export data.json (all entities for JavaScript consumers)."""
    print("\nExporting JSON data...")
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

    cursor.execute("SELECT * FROM timeline_events")
    events = [dict(row) for row in cursor.fetchall()]

    data = {
        "persons": persons,
        "texts": texts,
        "concepts": concepts,
        "locations": locations,
        "events": events,
        "generated": datetime.now().isoformat(),
    }

    data_path = SITE_PATH / "data" / "data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)

    conn.close()
    print(f"  [OK] data.json exported ({len(persons)} persons, {len(texts)} texts, {len(concepts)} concepts, {len(events)} events)")


def build_site():
    """Main deployment function."""
    print("=" * 60)
    print("ALCHEMYTIMELINEMAP DEPLOYMENT")
    print("=" * 60)

    init_site_structure()
    generate_index_html()
    generate_timeline_html()
    generate_map_html()
    generate_persons_pages()
    generate_texts_pages()
    generate_concepts_pages()
    export_json_data()

    print("\n" + "=" * 60)
    print("[SUCCESS] DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"\nOutput: {SITE_PATH}/")
    print("Next step: Copy site/ to docs/ and push to GitHub Pages")


if __name__ == "__main__":
    build_site()
