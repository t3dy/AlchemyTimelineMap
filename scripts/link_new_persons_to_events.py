#!/usr/bin/env python3
"""link_new_persons_to_events.py — Link newly added persons to relevant events."""
import sqlite3

DB = 'db/alchemy_timeline.db'

# Mapping: person_slug -> list of (description, event_filter_sql)
NEW_PERSON_EVENT_LINKS = [
    # 18th-century chemistry revolution figures
    ("georg-ernst-stahl", [
        ("Phlogiston theory and Stahlian chemistry", "description LIKE '%phlogiston%' OR description LIKE '%stahl%' OR concepts_involved LIKE '%combustion%'"),
        ("Early 18th century chemistry", "date_start_year >= 1700 AND date_start_year <= 1730"),
    ]),

    ("herman-boerhaave", [
        ("Boerhaave's medical and chemical synthesis", "description LIKE '%boerhaave%' OR description LIKE '%iatrochemistry%'"),
        ("Early 18th century medical chemistry", "date_start_year >= 1700 AND date_start_year <= 1738"),
    ]),

    ("joseph-black", [
        ("Black's quantitative chemistry and fixed air", "description LIKE '%black%' OR description LIKE '%fixed air%' OR description LIKE '%carbon%'"),
        ("Mid-18th century quantitative chemistry", "date_start_year >= 1750 AND date_start_year <= 1800"),
    ]),

    ("carl-wilhelm-scheele", [
        ("Scheele's discovery of oxygen and acids", "description LIKE '%scheele%' OR description LIKE '%chlorine%' OR description LIKE '%organic acid%'"),
        ("Late 18th century pneumatic chemistry", "date_start_year >= 1770 AND date_start_year <= 1800"),
    ]),

    ("antoine-lavoisier", [
        ("Lavoisier's oxygen theory and chemical revolution", "description LIKE '%lavoisier%' OR description LIKE '%oxygen theory%' OR description LIKE '%chemical revolution%'"),
        ("Late 18th century chemistry reform", "date_start_year >= 1770 AND date_start_year <= 1800"),
    ]),

    ("jons-jacob-berzelius", [
        ("Berzelius and atomic weight determination", "description LIKE '%berzelius%' OR description LIKE '%atomic weight%'"),
        ("Early 19th century chemistry", "date_start_year >= 1800 AND date_start_year <= 1850"),
    ]),

    ("friedrich-wohler", [
        ("Wohler's urea synthesis and organic chemistry", "description LIKE '%wohler%' OR description LIKE '%urea%' OR description LIKE '%organic synthesis%'"),
        ("Early 19th century organic chemistry", "date_start_year >= 1820 AND date_start_year <= 1880"),
    ]),

    ("justus-von-liebig", [
        ("Liebig's agricultural chemistry", "description LIKE '%liebig%' OR description LIKE '%agricultural%' OR description LIKE '%nitrogen%'"),
        ("19th century applied chemistry", "date_start_year >= 1830 AND date_start_year <= 1880"),
    ]),

    # Medieval and Renaissance figures
    ("jabir-ibn-aflah", [
        ("Islamic mathematics and astronomy", "date_start_year >= 1100 AND date_start_year <= 1200 AND location_slug IN ('al-andalus', 'cordoba', 'seville')"),
    ]),

    ("gerbert-of-aurillac", [
        ("Medieval transmission of Islamic learning", "date_start_year >= 950 AND date_start_year <= 1003 AND location_slug IN ('reims', 'ravenna', 'rome')"),
    ]),

    ("robert-grosseteste", [
        ("Oxford experimental natural philosophy", "date_start_year >= 1230 AND date_start_year <= 1260 AND location_slug = 'oxford'"),
    ]),

    ("nicholas-of-cusa", [
        ("Renaissance Neoplatonic natural philosophy", "date_start_year >= 1450 AND date_start_year <= 1464"),
    ]),

    ("juan-huarte-de-san-juan", [
        ("Spanish Renaissance natural philosophy", "date_start_year >= 1560 AND date_start_year <= 1590 AND location_slug IN ('madrid', 'seville')"),
    ]),

    ("franciscus-patricius", [
        ("Renaissance Neoplatonism and esotericism", "date_start_year >= 1560 AND date_start_year <= 1597"),
    ]),

    ("thomas-hobbes", [
        ("Mechanical philosophy and corpuscularism", "description LIKE '%hobbes%' OR description LIKE '%mechanical philosophy%' OR concepts_involved LIKE '%corpuscular%'"),
        ("Mid-17th century natural philosophy", "date_start_year >= 1640 AND date_start_year <= 1680"),
    ]),

    ("christiaan-huygens", [
        ("Wave theory of light and matter physics", "description LIKE '%huygens%' OR description LIKE '%light theory%' OR description LIKE '%elasticity%'"),
        ("Late 17th century physics", "date_start_year >= 1660 AND date_start_year <= 1700"),
    ]),

    ("jacob-grimm", [
        ("Folklore and mystical traditions", "description LIKE '%myth%' OR description LIKE '%folklore%' OR description LIKE '%esoteric%'"),
    ]),
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total_linked = 0

    for person_slug, patterns in NEW_PERSON_EVENT_LINKS:
        # Check if person exists
        c.execute('SELECT id FROM persons WHERE slug = ?', (person_slug,))
        person = c.fetchone()
        if not person:
            print(f"  ! Person not found: {person_slug}")
            continue

        for description, event_filter in patterns:
            # Find matching events that aren't already linked
            c.execute(f'''
                SELECT slug FROM timeline_events
                WHERE {event_filter}
                AND NOT EXISTS (
                    SELECT 1 FROM person_event_refs
                    WHERE person_slug = ? AND event_slug = timeline_events.slug
                )
                LIMIT 5
            ''', (person_slug,))

            events = c.fetchall()
            if events:
                for (event_slug,) in events:
                    c.execute(
                        'INSERT OR IGNORE INTO person_event_refs (person_slug, event_slug) VALUES (?, ?)',
                        (person_slug, event_slug)
                    )
                print(f"  +{len(events)} {description:50} > {person_slug}")
                total_linked += len(events)

    conn.commit()
    conn.close()
    print(f'\n[OK] Linked {total_linked} new person-event relationships')


if __name__ == '__main__':
    main()
