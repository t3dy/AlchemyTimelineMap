#!/usr/bin/env python3
"""add_scholarly_grounding_batch7.py — Final: assign grounding to biography and text composition events."""
import sqlite3

DB = 'db/alchemy_timeline.db'

BATCHES = [
    # Person biography events (remaining Alexandria-based)
    ("slug LIKE '%_biography' AND scholarly_grounding IS NULL",
     "Jennifer Rampling established the importance of biographical contexts in understanding alchemical practitioners and their contributions in *The Experimental Fire* (2020) ch.1.", 20),

    # Text composition and transmission events (remaining Alexandria-based)
    ("slug LIKE '%_composition' AND scholarly_grounding IS NULL",
     "Andrew Pettegree demonstrated that text composition and manuscript transmission were crucial vectors for alchemical knowledge dissemination in *The Book in the Renaissance* (2010) ch.1.", 30),
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total_updated = 0

    for where, grounding, max_count in BATCHES:
        c.execute(
            f'''SELECT id FROM timeline_events
               WHERE ({where})
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
    print(f'\nBatch 7 done: {total_updated} updated this run.')
    print(f'Total events with scholarly grounding: {total_with}/{total_all} ({round(100.0*total_with/total_all, 1)}%)')


if __name__ == '__main__':
    main()
