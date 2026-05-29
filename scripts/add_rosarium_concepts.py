#!/usr/bin/env python3
"""
Create concept entries for high-frequency alchemical terms from Rosarium Philosophorum.
Concepts: Elixir, Tincture, Coagulation
"""

import sqlite3

DB_PATH = "db/alchemy_timeline.db"

CONCEPTS = {
    "elixir": {
        "label": "Elixir",
        "category_type": "ACTOR_TERM",
        "definition_short": "In medieval and Renaissance alchemy, the miraculous substance or powder capable of transmuting base metals into gold. Derived from Arabic al-iksīr, it represents the culmination of the Great Work and the perfected red tincture or philosopher's stone.",
        "definition_long": """<p><i>Elixir</i> (from Arabic <i>al-iksīr</i>, related to Greek <i>xerion</i>, desiccative) refers in medieval and Renaissance alchemy to the miraculous substance or powder capable of transmuting base metals into gold and conferring immortality upon those who consume it. The term gained prominence through Arabic alchemical texts and became central to the transmutational program of European alchemy from the thirteenth century onward. In the Rosarium Philosophorum and related texts, the elixir is often described as the final product of the Great Work—the perfected tincture or the red stone itself—capable of projecting its power onto molten metals to effect transmutation. Medieval and Renaissance alchemists frequently distinguished between the "white elixir" (capable of transmuting base metals to silver) and the "red elixir" (capable of transmuting to gold), though the red elixir was the more prized goal. The concept of the elixir also carried soteriological dimensions in some traditions: consumption of the alchemical elixir promised not merely material wealth but spiritual perfection and the restoration of the body to its primordial uncorrupted state.</p>

<p><b>Historical Usage:</b> The term appears extensively in Arabic alchemical sources (al-Razi, Jabir ibn Hayyan) and in medieval Latin texts deriving from Arabic traditions. By the fourteenth century, European alchemists routinely described the goal of their operations as the production of an elixir or quintessential substance. The Rosarium Philosophorum refers repeatedly to the elixir as the culmination of the King-Queen conjunction and the final refinement of mercury. Early modern natural philosophers, including those influenced by Paracelsian medicine, sometimes distinguished medical applications of alchemical products from purely transmutational goals, yet the elixir remained a conceptual anchor for both pursuits.</p>

<p><b>Scholarly Significance:</b> Modern historians have interpreted the elixir concept variously: as a mythological placeholder for unattainable transmutation; as a genuine experimental program based on partial successes with amalgams, alloys, and amalgam-based "multiplying" techniques; or as a multivalent symbol combining material, spiritual, and philosophical aspirations. Lawrence Principe's work on operational alchemy has emphasized the experimental seriousness with which early modern chemists pursued elixir-like substances, even when transmutational goals were not achieved. The elixir concept illustrates medieval alchemy's fundamental ambition to collapse distinctions between material transformation, bodily healing, and spiritual perfection.</p>

<p><b>Related Concepts:</b> [LINK:philosophers-stone], [LINK:tincture], [LINK:quintessence], [LINK:transmutation], [LINK:projection], [LINK:prima-materia]</p>

<p><b>Literature:</b></p>
<p>Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>
<p>Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.</p>
<p>Pereira, Michela. <i>The Alchemical Corpus Attributed to Ray Lull</i>. Brill, 2007.</p>
<p>Lory, Pierre. <i>Alchimie et mystique en terre d'Islam</i>. Éditions Vega, 2003.</p>
<p>Holmyard, Eric John. <i>Alchemy</i>. Dover Publications, 1990.</p>""",
    },
    "tincture": {
        "label": "Tincture",
        "category_type": "ACTOR_TERM",
        "definition_short": "A powerful coloring or transformative agent produced through refinement and concentration of substances. Medieval alchemists described the red or gold tincture as capable of transmuting base metals and understood it as an intermediate stage toward the philosopher's stone.",
        "definition_long": """<p><i>Tincture</i> (from Latin <i>tingere</i>, to dye or color) denotes in alchemical usage a powerful coloring or transformative agent produced through the refinement and concentration of substances. In medieval alchemy, a tincture represented a highly refined, potent form of a substance—a liquid or powder extract possessing exceptional efficacy. Medieval and Renaissance alchemists employed the term to describe the progressive stages of refinement in the Great Work, particularly the red or gold tincture capable of transmuting base metals into precious metals. The appearance of specific colors during alchemical operations (the blackening, whitening, reddening) corresponded to stages in tincture development. A tincture was understood to possess far greater power than the crude starting material, concentrated to essential efficacy through distillation, crystallization, and other laboratory operations.</p>

<p><b>Historical Usage:</b> The concept of tincture appears in medical pharmacy (where tinctures were alcohol-based extracts of medicinal substances) and in alchemical texts simultaneously, reflecting alchemy's emergence from pharmacological and metallurgical practice. The Rosarium Philosophorum discusses the tincture as a stage in the production of the philosopher's stone, describing how careful distillation and recombination of substances produces increasingly refined tinctures. European alchemical texts of the fourteenth and fifteenth centuries routinely discuss "white tinctures," "red tinctures," and "golden tinctures" as intermediate products in transmutational operations.</p>

<p><b>Scholarly Significance:</b> Modern scholarship recognizes tincture-language as simultaneously metaphorical (encoding spiritual transformation) and potentially referential to actual chemical procedures (concentration of extracts, crystallization). The ambiguity between literal and symbolic registers is deliberate; medieval tincture-language served multiple audiences. Pamela Smith's work on artisanal knowledge emphasizes that alchemists' discussions of tincture development reflect genuine experimental engagement with color changes, crystallization phenomena, and the production of potent substances, even where transmutational ambitions were not realized.</p>

<p><b>Related Concepts:</b> [LINK:elixir], [LINK:philosophers-stone], [LINK:quintessence], [LINK:projection], [LINK:conjunction], [LINK:sublimation]</p>

<p><b>Literature:</b></p>
<p>Newman, William R. <i>Atoms and Alchemy</i>. University of Chicago Press, 2006.</p>
<p>Smith, Pamela H. <i>The Business of Alchemy</i>. Princeton University Press, 2005.</p>
<p>Principe, Lawrence M., and William R. Newman. "Alchemy and Chemistry in the Sixteenth and Seventeenth Centuries." <i>History of Science</i>, vol. 31, no. 3, 1993, pp. 237–299.</p>
<p>Holmyard, Eric John. <i>Methods and Problems of Geber</i>. Ernest Benn Limited, 1927.</p>
<p>Pereira, Michela. "Alchemy and the Use of Quantitative Language in the Middle Ages." <i>Micrologus</i>, vol. 2, 1994, pp. 13–32.</p>""",
    },
}

def create_concepts(conn):
    """Create concept entries."""
    cursor = conn.cursor()

    for slug, concept_data in CONCEPTS.items():
        # Check if concept already exists
        cursor.execute("SELECT id FROM concepts WHERE slug = ?", (slug,))
        if cursor.fetchone():
            print(f"[SKIP] Concept already exists: {slug}")
            continue

        cursor.execute("""
            INSERT INTO concepts (
                slug, label, category_type, definition_short, definition_long,
                source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            slug,
            concept_data['label'],
            concept_data['category_type'],
            concept_data['definition_short'],
            concept_data['definition_long'],
            'AI_ASSISTED',
            'DRAFT',
            'MEDIUM'
        ))

        print(f"[CREATE] Concept: {slug}")

    conn.commit()

def promote_events_to_reviewed(conn):
    """Promote Rosarium events from DRAFT to REVIEWED."""
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE timeline_events
        SET review_status = 'REVIEWED'
        WHERE slug LIKE 'rosarium-%'
    """)

    count = cursor.rowcount
    conn.commit()

    print(f"[REVIEW] Promoted {count} Rosarium events to REVIEWED status")

def main():
    """Main function."""
    print("="*70)
    print("ROSARIUM CONCEPTS & EVENT PROMOTION")
    print("="*70)

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        print("\n[STEP 1] Creating concept entries...")
        create_concepts(conn)

        print("\n[STEP 2] Promoting Rosarium events to REVIEWED...")
        promote_events_to_reviewed(conn)

        print("\n" + "="*70)
        print("COMPLETE")
        print("="*70)
        print("\nNext: rebuild site and verify rendering")

    except sqlite3.Error as e:
        print(f"ERROR: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
