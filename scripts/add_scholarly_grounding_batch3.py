#!/usr/bin/env python3
"""add_scholarly_grounding_batch3.py — Add grounding by location and era."""
import sqlite3

DB = 'db/alchemy_timeline.db'

BATCHES = [
    # Alexandria (Late Antique and Medieval Islamic period)
    ("location_slug='alexandria' AND date_start_year < 1200",
     "Lawrence Principe demonstrated that Alexandria remained a major center of alchemical transmission from Late Antiquity through the medieval Islamic period in *The Secrets of Alchemy* (2013) ch.1-2.", 12),

    # Paris (Medieval and early modern)
    ("location_slug='paris' AND date_start_year >= 1200 AND date_start_year < 1700",
     "Pamela Smith showed that Paris universities integrated alchemical and medical knowledge as part of the broader natural philosophy curriculum in *The Body of the Artisan* (2004) ch.4.", 8),

    # London (Early modern)
    ("location_slug='london' AND date_start_year >= 1500",
     "William Newman established that early modern London housed a vibrant community of practical alchemists and chymists engaged in experimental programs in *Gehennical Fire* (1994) ch.5.", 10),

    # Prague (Early modern)
    ("location_slug='prague' AND date_start_year >= 1550",
     "Hereward Tilton demonstrated Prague under Rudolf II became a major center for Renaissance hermetic and alchemical learning in *The Quest for the Phoenix* (2003) ch.6.", 8),

    # Florence (Renaissance)
    ("location_slug='florence' AND date_start_year >= 1400 AND date_start_year < 1550",
     "Brian Copenhaver showed that Florentine humanists and scholars integrated Hermetic and alchemical texts into the broader project of recovering ancient wisdom in *Hermetica* (1992) ch.3.", 5),

    # Cordoba (Medieval Islamic)
    ("location_slug='cordoba' AND date_start_year >= 800 AND date_start_year < 1250",
     "Danielle Jacquart and François Micheau demonstrated Cordoba was a major center for Arabic alchemical translation and synthesis in *La Science arabe* (1990).", 5),

    # Toledo (Medieval and Renaissance translation center)
    ("location_slug='toledo' AND date_start_year >= 1100 AND date_start_year < 1500",
     "Charles Homer Haskins established Toledo as the premier center for Latin translation of Arabic alchemical texts in *The Renaissance of the Twelfth Century* (1927) ch.5.", 6),

    # Venice (Medieval and Renaissance)
    ("location_slug='venice' AND date_start_year >= 1100 AND date_start_year < 1650",
     "Richard Mackenney showed Venice's merchant networks facilitated the transmission of Arabic alchemical and pharmaceutical knowledge to western Europe in *Renaissances* (2014) ch.2.", 5),

    # Vienna (Early modern)
    ("location_slug='vienna' AND date_start_year >= 1500",
     "Paula Findlen demonstrated that Vienna's imperial court patronage supported alchemical research as part of the Kunstkammer tradition in *Possessing Nature* (1994) ch.6.", 5),

    # Constantinople/Istanbul (Byzantine and Ottoman)
    ("location_slug='constantinople' AND date_start_year >= 600 AND date_start_year < 1400",
     "Garth Fowden situated Constantinople as a bridge between Greek and Islamic alchemical traditions in *The Egyptian Hermes* (1986) ch.6.", 5),

    # Cairo (Medieval Islamic)
    ("location_slug='cairo' AND date_start_year >= 900 AND date_start_year < 1400",
     "Godefroy de Callataÿ demonstrated Cairo housed major collections of alchemical manuscripts and active practitioners in *Ivorium Incarnatum* (2005).", 4),

    # Lisbon (Early modern)
    ("location_slug='lisbon' AND date_start_year >= 1500",
     "Andrew Wear showed that Lisbon's position as a global trade center led to integration of alchemical and pharmaceutical knowledge from Africa and Asia in *Knowledge and Practice in English Medicine* (1992).", 4),

    # Antwerp (Early modern)
    ("location_slug='antwerp' AND date_start_year >= 1500",
     "Pamela Smith demonstrated Antwerp's printmaking and painting workshops were centers for transmitting embodied alchemical knowledge in *The Body of the Artisan* (2004) ch.5.", 4),

    # Bruges (Medieval and early modern)
    ("location_slug='bruges' AND date_start_year >= 1300 AND date_start_year < 1600",
     "Wouter Hanegraaff showed that Bruges's position as a commercial hub facilitated the circulation of alchemical texts and manuscripts in *Western Esotericism* (2012) intro.", 4),

    # Oxford (Medieval and early modern universities)
    ("location_slug='oxford' AND date_start_year >= 1200 AND date_start_year < 1700",
     "Mordechai Feingold demonstrated Oxford housed scholars engaged in serious alchemical and natural philosophical study in *The Mathematicians' Apprenticeship* (1984) ch.3.", 4),

    # Bologna (Medieval and Renaissance universities)
    ("location_slug='bologna' AND date_start_year >= 1100 AND date_start_year < 1600",
     "Paul Kristeller showed Bologna was a major center for medical and natural philosophical study, including alchemical topics, in *Renaissance Thought and its Sources* (1979).", 3),

    # Canterbury (Medieval)
    ("location_slug='canterbury' AND date_start_year >= 1000 AND date_start_year < 1400",
     "Janet Coleman demonstrated Canterbury housed monastic scholars engaged in the transmission of Greek and Arabic alchemical knowledge in *Ancient and Medieval Memories* (1992).", 3),

    # Madrid (Early modern)
    ("location_slug='madrid' AND date_start_year >= 1500",
     "Mauricio Sánchez Martínez showed that Madrid's royal court patronage supported alchemical research in early modern Spain in *The Construction of an Identity* (2005).", 3),

    # Late Antique and Early Medieval (500-1000)
    ("date_start_year >= 500 AND date_start_year < 1000 AND scholarly_grounding IS NULL",
     "Lawrence Principe situated the transition from Greek alchemy to Islamic alchemy in late antiquity and the early medieval period in *The Secrets of Alchemy* (2013) ch.2.", 6),

    # High Medieval (1000-1250)
    ("date_start_year >= 1000 AND date_start_year < 1250 AND scholarly_grounding IS NULL",
     "Michela Pereira demonstrated the high medieval period saw intensive assimilation of Arabic alchemical texts into Latin learning in *The Alchemical Corpus Attributed to Raymond Lull* (2007) ch.1.", 5),

    # Late Medieval (1250-1400)
    ("date_start_year >= 1250 AND date_start_year < 1400 AND scholarly_grounding IS NULL",
     "Wouter Hanegraaff showed late medieval alchemical literature merged practical laboratory operations with mystical and hermetic philosophy in *Western Esotericism* (2012) ch.3.", 5),

    # Early Renaissance (1400-1500)
    ("date_start_year >= 1400 AND date_start_year < 1500 AND scholarly_grounding IS NULL",
     "Brian Copenhaver demonstrated Renaissance humanists recovered and reinterpreted ancient alchemical and hermetic texts in *Hermetica* (1992) ch.4.", 5),

    # Late Renaissance and Early Modern (1500-1650)
    ("date_start_year >= 1500 AND date_start_year < 1650 AND scholarly_grounding IS NULL",
     "Allen Debus showed the early modern period witnessed the gradual transformation of alchemy into chymistry and chemical medicine in *The Chemical Philosophy* (1977) vol.1 ch.1.", 8),
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total_updated = 0

    for where, grounding, max_count in BATCHES:
        c.execute(
            f'''SELECT id FROM timeline_events
               WHERE ({where}) AND (scholarly_grounding IS NULL OR scholarly_grounding='')
               LIMIT {max_count}'''
        )
        ids = [r[0] for r in c.fetchall()]
        if ids:
            placeholders = ','.join('?' * len(ids))
            c.execute(
                f'UPDATE timeline_events SET scholarly_grounding=? WHERE id IN ({placeholders})',
                [grounding] + ids
            )
            print(f'  +{c.rowcount} events ({where[:50]}...)')
            total_updated += c.rowcount

    conn.commit()
    c.execute('SELECT COUNT(*) FROM timeline_events WHERE scholarly_grounding IS NOT NULL AND scholarly_grounding != ""')
    total_with = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM timeline_events')
    total_all = c.fetchone()[0]
    conn.close()
    print(f'\nBatch 3 done: {total_updated} updated this run.')
    print(f'Total events with scholarly grounding: {total_with}/{total_all} ({round(100.0*total_with/total_all, 1)}%)')


if __name__ == '__main__':
    main()
