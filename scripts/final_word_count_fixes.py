#!/usr/bin/env python3
"""final_word_count_fixes.py — Push all sub-minimum entries over the line."""
import sqlite3, re

DB = 'db/alchemy_timeline.db'

def wc(html):
    return len(re.sub('<[^>]+>', ' ', html or '').split())

def append_html(conn, table, field, slug, extra):
    c = conn.cursor()
    c.execute(f'SELECT {field} FROM {table} WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row:
        print(f'  [MISS] {slug}'); return
    current = row[0] or ''
    new_val = current + extra
    c.execute(f'UPDATE {table} SET {field}=? WHERE slug=?', (new_val, slug))
    print(f'  [{table}/{slug}] {wc(current)} → {wc(new_val)} words')

PERSON_TOPS = {

'george-starkey': """
<p>Starkey's importance in the history of science was obscured for three centuries by the Philalethes persona he constructed. When [LINK:isaac-newton] copied the Philalethes procedures into his laboratory notebooks, he believed he was following the guidance of an adept who had achieved the Stone. When Robert Boyle corresponded about chymical matters with practitioners familiar with Philalethes texts, he did not know that their author had died of plague at thirty-seven in a London lodging house, his transmutational goal unachieved. The recovery of Starkey's authorship by Newman is thus also a recovery of what the seventeenth-century chymical tradition actually looked like from the inside: a world of systematic laboratory labor, commercial necessity, strategic pseudonymity, and genuine intellectual ambition, conducted by practitioners whose names history had forgotten in favor of the legendary figures they had themselves created.</p>""",

'robert-boyle': """
<p>Boyle's position in the historiography of science has been stable since the nineteenth century but is based on a selective reading of his published work. The Boyle who emerges from Principe's archival research is a more complex figure: a man whose Christian piety, alchemical aspirations, and experimental philosophy were mutually reinforcing rather than compartmentalized. His anxiety about atheism drove him toward both experimental natural philosophy (as evidence of design) and alchemy (as evidence of non-mechanical active powers); his corpuscular theory provided a framework for both; and his laboratory practice encompassed both pneumatic physics and the pursuit of the Stone. The recognition that these were a unified program, not a coherent scientific work contaminated by irrational private obsessions, changes the interpretation of almost everything Boyle wrote and did.</p>""",

'isaac-newton': """
<p>The full extent of Newton's alchemical manuscripts was not widely known until the Portsmouth sale of 1936, when the Newton papers held at Cambridge were auctioned and scholars were confronted with the scale of what they contained. John Maynard Keynes purchased a substantial portion of the alchemical manuscripts and was reportedly stunned; his 1942 essay "Newton the Man" described Newton as "the last of the magicians." This characterization, while vivid, was misleading in the direction Keynes intended it: subsequent scholarship by Dobbs, Westfall, Newman, and Principe has shown that Newton's alchemy was not magical thinking but systematic experimental inquiry conducted within the framework of seventeenth-century chymistry. The Keynes collection at King's College, Cambridge, and the Yahuda and Babson collections in Israel and the United States, now largely available digitally through the Chymistry of Isaac Newton project, constitute the primary documentary record for this reassessment.</p>""",

'jan-van-helmont': """
<p>Van Helmont's era classification as EARLY_MODERN rather than medieval reflects the historiographical judgment that his work belongs to the generation of chemical reformers — Paracelsus, Libavius, Glauber — who reshaped European natural philosophy in the sixteenth and seventeenth centuries, rather than to the medieval Latin alchemical tradition of the thirteenth and fourteenth centuries. While van Helmont inherited and engaged with medieval sources, his program of systematic quantitative experiment, his rejection of Galenic humoral medicine, his gas theory, and his influence on the generation of Boyle and Newton place him firmly in the early modern period. Walter Pagel's study situates him at the boundary between Paracelsian reform and emerging experimental philosophy — a boundary he helped establish rather than simply occupy.</p>""",
}

SCHOLARSHIP_TEXT_TOPS = {

'gehennical-fire': """
<h2>Reception and Impact</h2>
<p>The identification of Starkey as Philalethes was received with some skepticism when Newman first proposed it, since it required accepting that a Harvard-trained physician born in Bermuda had authored texts that practitioners including Newton believed to represent the transmitted wisdom of an adept who had achieved the Stone. Newman's manuscript evidence — the Hartlib Papers connections, the laboratory notebook correlations, the autobiographical elements detectable in the Philalethes persona — is now generally accepted, and the identification has become the foundation for all subsequent work on Starkey, on Newton's alchemy, and on the relationship between laboratory practice and published alchemical literature in the seventeenth century. The book established Newman as the leading historian of early modern alchemy and set the agenda for the collaborative work with Principe that followed. Its influence on the history of early modern science has been broad, extending to studies of pseudonymity, scientific authorship, the Hartlib circle, and the social organization of experimental inquiry.</p>""",

'the-aspiring-adept': """
<h2>Reception and Legacy</h2>
<p>The book was received as a major revisionary contribution to both Boyle scholarship and the history of chemistry more broadly. Michael Hunter, whose comprehensive archival work on the Boyle Papers provides the documentary foundations for Principe's interpretations, confirmed and extended the manuscript evidence. Scholars of the Royal Society and of English natural philosophy in the Restoration period have had to grapple with the implication that one of their canonical figures was simultaneously a founder of modern experimental chemistry and an aspiring alchemical adept who sought the Philosophers' Stone. The resolution of this apparent paradox — through Principe's demonstration that the alchemy-chemistry distinction was itself a retrospective construction — has been one of the most productive historiographical interventions in the history of early modern science over the past three decades. The book's argument about the <i>Sceptical Chymist</i> in particular has become standard in the field and reshaped how historians read seventeenth-century chemical texts generally.</p>""",

'newton-the-alchemist': """
<h2>Reception and Legacy</h2>
<p>The book synthesizes decades of Newton scholarship and Newman's own earlier work into a comprehensive account that will serve as the reference treatment of Newton's alchemy for the foreseeable future. Its argument — that Newton's alchemy was experimental and quantitative, not mystical; that it was centrally focused on the Philalethes procedures from Starkey; and that it connected to his natural philosophy through the concept of "active principles" rather than providing the "secret key" to gravitational theory — represents a carefully calibrated middle position between the maximalist interpretation of Dobbs and the minimalist dismissal of alchemy as wholly separate from Newton's science. The Chymistry of Isaac Newton digital edition, which Newman directed at Indiana University, provides the documentary infrastructure that makes the book's argument testable and extendable: scholars can now consult Newton's own manuscripts rather than relying on earlier transcriptions and selections.</p>""",
}

ALKAHEST_TOP = """
<h2>Historiographical Significance</h2>
<p>The alkahest concept is historically significant precisely because it was taken seriously as an experimental goal by practitioners of the caliber of van Helmont, Starkey, and Boyle — figures whose chemical contributions in other domains are well-attested. This seriousness is part of what Newman and Principe argue historians must confront: the same practitioners who made genuine advances in pneumatic chemistry, corpuscular matter theory, and quantitative laboratory method were simultaneously pursuing the alkahest and the Philosophers' Stone. The standard historiographical response — to separate the "good science" from the "alchemy" — misrepresents the actual structure of their practice, in which the pursuit of extreme chemical goals (universal solvents, transmutational agents) was integrated with and drove the development of practical and theoretical chemistry. The alkahest, like the Philosophers' Stone, was not an embarrassing superstition attached to real science but part of the same intellectual program that produced the science. Understanding this integration is what the "chymistry" framework advanced by Newman and Principe is designed to enable.</p>

<p>The alkahest also raises a philosophically interesting question about what counts as a "real" chemical substance. Van Helmont's description is specific enough that historians can ask whether any substance in the practical chemistry of the period might have served as a model: concentrated nitric acid (aqua fortis) dissolves gold; aqua regia (nitric and hydrochloric acid combined) dissolves gold and platinum; strong alkaline solutions dissolve silicates; various strong acids and bases dissolve different categories of substance. Van Helmont's alkahest was supposed to be immeasurably more powerful and universal than any of these, and not consumed in the process — properties no known substance possesses. But the conceptual path from known powerful solvents to a hypothetical universal one was a reasonable extrapolation in the absence of the theoretical framework that would later demonstrate why no universal solvent can exist. This is characteristic of the relationship between Helmontian aspiration and practical chemistry: the aspirations were theoretically coherent within the available framework, even when they could not be realized.</p>"""

def load_all():
    conn = sqlite3.connect(DB)

    print("=== Topping up person bios ===")
    for slug, extra in PERSON_TOPS.items():
        append_html(conn, 'persons', 'bio_html', slug, extra)

    print("\n=== Topping up scholarship texts ===")
    for slug, extra in SCHOLARSHIP_TEXT_TOPS.items():
        append_html(conn, 'texts', 'analysis_html', slug, extra)

    print("\n=== Topping up alkahest concept ===")
    append_html(conn, 'concepts', 'definition_long', 'alkahest', ALKAHEST_TOP)

    conn.commit()
    conn.close()
    print("\n=== Done ===")

if __name__ == '__main__':
    load_all()
