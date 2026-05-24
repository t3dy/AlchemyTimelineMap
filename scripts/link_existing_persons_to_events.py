#!/usr/bin/env python3
"""link_existing_persons_to_events.py — Link existing persons to relevant events via keyword matching."""
import sqlite3

DB = 'db/alchemy_timeline.db'

# Mapping: person_slug -> list of (keyword_patterns, event_filter_sql)
PERSON_EVENT_LINKS = [
    # Isaac Newton - events about alchemy, transmutation, natural philosophy in late 1600s
    ("isaac-newton", [
        ("Newton's alchemical studies", "description LIKE '%newton%' OR description LIKE '%gravity%' OR description LIKE '%optics%'"),
        ("Late 17th century natural philosophy", "date_start_year >= 1670 AND date_start_year <= 1730 AND location_slug IN ('london', 'cambridge')"),
    ]),

    # Robert Boyle - events about air, pressure, experimental philosophy, 1650-1700
    ("robert-boyle", [
        ("Boyle's law and vacuum experiments", "description LIKE '%boyle%' OR description LIKE '%vacuum%' OR description LIKE '%air%' OR description LIKE '%pressure%'"),
        ("Experimental philosophy 1650-1700", "date_start_year >= 1640 AND date_start_year <= 1700 AND (location_slug = 'london' OR location_slug = 'oxford')"),
    ]),

    # Jan van Helmont - events about iatrochemistry, medical alchemy, 1600-1650
    ("jan-van-helmont", [
        ("Helmont's medical and chemical work", "description LIKE '%helmont%' OR description LIKE '%gas%' OR description LIKE '%medical%' OR concepts_involved LIKE '%medicamenta%'"),
        ("Early 17th century iatrochemistry", "date_start_year >= 1600 AND date_start_year <= 1650 AND (location_slug IN ('brussels', 'antwerp', 'amsterdam'))"),
    ]),

    # John Dee - Renaissance polymath, mathematics, natural magic, 1550-1600
    ("john-dee", [
        ("Dee's natural magic and mathematics", "description LIKE '%dee%' OR description LIKE '%magic%' OR description LIKE '%mathematics%'"),
        ("Renaissance court natural philosophy", "date_start_year >= 1550 AND date_start_year <= 1605 AND (location_slug IN ('london', 'prague', 'vienna'))"),
    ]),

    # John of Rupescissa - medieval alchemist, 1300-1370, distillation and quintessence
    ("john-of-rupescissa", [
        ("Rupescissa's distillation and quintessence work", "description LIKE '%rupescissa%' OR description LIKE '%aqua vitae%' OR concepts_involved LIKE '%quintessence%'"),
        ("14th century Franciscan alchemy", "date_start_year >= 1340 AND date_start_year <= 1370"),
    ]),

    # Raymond Lull - medieval polymath, logic, alchemy, 1232-1315
    ("raymond-lull", [
        ("Lull's combinatorial and alchemical work", "description LIKE '%lull%' OR description LIKE '%combinatorial%'"),
        ("Late medieval Iberian philosophy", "date_start_year >= 1270 AND date_start_year <= 1315"),
    ]),

    # George Ripley - Renaissance English alchemist, 15th century
    ("george-ripley", [
        ("Ripley's alchemical writings", "description LIKE '%ripley%'"),
        ("15th century English alchemy", "date_start_year >= 1400 AND date_start_year <= 1500 AND location_slug IN ('london', 'england')"),
    ]),

    # Michael Sendivogius - early modern alchemist, 1550-1620
    ("michael-sendivogius", [
        ("Sendivogius and the Hermetic tradition", "description LIKE '%sendivogius%' OR description LIKE '%hermetic%'"),
        ("Early 17th century transmutation", "date_start_year >= 1580 AND date_start_year <= 1620"),
    ]),

    # Robert Fludd - Renaissance polymath, natural magic, Neoplatonism, 1574-1637
    ("robert-fludd", [
        ("Fludd's magical and natural philosophy", "description LIKE '%fludd%' OR description LIKE '%rosicrucian%' OR concepts_involved LIKE '%hermeticism%'"),
        ("Early 17th century court patronage", "date_start_year >= 1590 AND date_start_year <= 1640 AND location_slug IN ('london', 'prague')"),
    ]),

    # George Agricola - mining, metallurgy, practical chemistry, 1490-1555
    ("george-agricola", [
        ("Agricola's mining and metallurgy work", "description LIKE '%agricola%' OR description LIKE '%mining%' OR description LIKE '%metallurg%'"),
        ("16th century practical chemistry", "date_start_year >= 1530 AND date_start_year <= 1555"),
    ]),

    # Heinrich Khunrath - alchemist, mystic, emblematic illustrations, 1560-1605
    ("heinrich-khunrath", [
        ("Khunrath's Amphitheatre and emblematic alchemy", "description LIKE '%khunrath%' OR description LIKE '%amphitheatre%'"),
        ("Late 16th century Prague alchemy", "date_start_year >= 1580 AND date_start_year <= 1605 AND location_slug = 'prague'"),
    ]),

    # Hildegard of Bingen - medieval mystic, natural philosophy, medicine, 1098-1179
    ("hildegard-of-bingen", [
        ("Hildegard's natural philosophy and medical knowledge", "description LIKE '%hildegard%' OR concepts_involved LIKE '%pharmaceutical%'"),
        ("12th century monastic natural philosophy", "date_start_year >= 1140 AND date_start_year <= 1179 AND location_slug IN ('rhineland', 'rome')"),
    ]),

    # Francis Bacon - philosophy of natural inquiry, empiricism, 1561-1626
    ("francis-bacon", [
        ("Bacon's empirical natural philosophy", "description LIKE '%bacon%' OR description LIKE '%empirical%' OR description LIKE '%method%'"),
        ("Early 17th century natural inquiry", "date_start_year >= 1590 AND date_start_year <= 1626"),
    ]),

    # Thomas Aquinas - medieval theology and philosophy, 1225-1274
    ("thomas-aquinas", [
        ("Thomas Aquinas and scholastic natural philosophy", "description LIKE '%aquinas%' OR description LIKE '%scholastic%'"),
        ("13th century university natural philosophy", "date_start_year >= 1240 AND date_start_year <= 1274 AND location_slug IN ('paris', 'oxford')"),
    ]),

    # George Starkey - early modern alchemist, laboratory practice, 1628-1665
    ("george-starkey", [
        ("Starkey's systematic laboratory work", "description LIKE '%starkey%' OR description LIKE '%sophick%'"),
        ("Mid-17th century English alchemy", "date_start_year >= 1650 AND date_start_year <= 1665 AND location_slug IN ('london', 'cambridge')"),
    ]),

    # William Backhouse - English alchemist, mentor to Ashmole, 1600-1662
    ("william-backhouse", [
        ("Backhouse and English alchemical tradition", "description LIKE '%backhouse%'"),
        ("17th century English alchemy", "date_start_year >= 1640 AND date_start_year <= 1662 AND location_slug = 'london'"),
    ]),

    # Elias Ashmole - alchemist, antiquarian, collector, 1617-1692
    ("elias-ashmole", [
        ("Ashmole's alchemical and antiquarian collecting", "description LIKE '%ashmole%'"),
        ("Late 17th century English alchemy", "date_start_year >= 1660 AND date_start_year <= 1692"),
    ]),

    # Robert of Chester - medieval translator of al-Khwarizmi, 12th century
    ("robert-of-chester", [
        ("Robert's translation of Arabic alchemy", "description LIKE '%chester%' OR description LIKE '%translator%'"),
        ("12th century translation from Arabic", "date_start_year >= 1140 AND date_start_year <= 1180"),
    ]),

    # Avicenna (Ibn Sina) - major medical and philosophical authority, 980-1037
    ("avicenna", [
        ("Avicenna's medical and natural philosophy", "description LIKE '%avicenna%' OR description LIKE '%ibn sina%' OR description LIKE '%canon%'"),
        ("Early Islamic medical and chemical knowledge", "date_start_year >= 1000 AND date_start_year <= 1050"),
    ]),

    # Albertus Magnus - medieval polymath, alchemy, natural philosophy, 1200-1280
    ("albertus-magnus", [
        ("Albert the Great's natural philosophy", "description LIKE '%albertus%' OR description LIKE '%albert the great%'"),
        ("13th century scholastic alchemy", "date_start_year >= 1240 AND date_start_year <= 1280 AND location_slug IN ('paris', 'cologne')"),
    ]),
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total_linked = 0

    for person_slug, patterns in PERSON_EVENT_LINKS:
        # Check if person exists
        c.execute('SELECT id FROM persons WHERE slug = ?', (person_slug,))
        person = c.fetchone()
        if not person:
            print(f"  ⚠ Person not found: {person_slug}")
            continue

        person_id = person[0]

        for description, event_filter in patterns:
            # Find matching events that aren't already linked
            c.execute(f'''
                SELECT id, slug FROM timeline_events
                WHERE {event_filter}
                AND NOT EXISTS (
                    SELECT 1 FROM person_event_refs
                    WHERE person_slug = ? AND event_slug = timeline_events.slug
                )
                LIMIT 5
            ''', (person_slug,))

            events = c.fetchall()
            if events:
                for event_id, event_slug in events:
                    c.execute(
                        'INSERT OR IGNORE INTO person_event_refs (person_slug, event_slug) VALUES (?, ?)',
                        (person_slug, event_slug)
                    )
                print(f"  +{len(events)} {description:45} > {person_slug}")
                total_linked += len(events)

    conn.commit()
    conn.close()
    print(f'\n[OK] Linked {total_linked} person-event relationships')


if __name__ == '__main__':
    main()
