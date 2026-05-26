#!/usr/bin/env python3
"""
expand_helmontian_content.py

Expands word counts on the helmontian-era content batch to meet minimum requirements:
- Concepts: 1,500 words minimum
- Person bios: 1,200 words minimum
- Texts: PRIMARY_SOURCE 1,000 words; SCHOLARSHIP 800 words
"""

import sqlite3
import re

DB = 'db/alchemy_timeline.db'

def wc(html):
    text = re.sub('<[^>]+>', ' ', html or '')
    return len(text.split())

def append_html(conn, table, field, slug, extra_html):
    c = conn.cursor()
    c.execute(f'SELECT {field} FROM {table} WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row:
        print(f'  [MISS] {slug} not found')
        return
    current = row[0] or ''
    new_val = current + extra_html
    c.execute(f'UPDATE {table} SET {field}=? WHERE slug=?', (new_val, slug))
    print(f'  [{table}/{slug}] {wc(current)} → {wc(new_val)} words')

def load_expansions():
    conn = sqlite3.connect(DB)

    print("=== Expanding helmontian-chymistry concept ===")
    append_html(conn, 'concepts', 'definition_long', 'helmontian-chymistry', """
<h2>The Fate of the Tradition</h2>
<p>Newman and Principe's subtitle — "the Fate of Helmontian Chymistry" — captures an important argument: the Helmontian tradition did not simply become obsolete or fail on its own terms. It was displaced through a combination of theoretical competition and deliberate disciplinary boundary-drawing. Stahl's phlogiston theory was the immediate theoretical successor, explicitly positioning itself against Helmontian vitalism while retaining structural analogies to Helmontian chemical practice. As phlogiston theory became dominant in European academic chemistry through the early eighteenth century — codified in Boerhaave's influential textbooks and institutionalized in the teaching curricula of universities from Edinburgh to Vienna — the distinctively Helmontian elements were marginalized.</p>

<p>The institutional dimension was equally important. The Académie Royale des Sciences in Paris, from its foundation in 1666, was cautious about transmutational claims; by the early eighteenth century, it had effectively excluded them from its purview. As chemistry sought academic respectability — through professorships, journals, royal patronage, and systematic curricula — the transmutational and vitalistic dimensions of Helmontian chymistry became liabilities. Practitioners who might previously have combined laboratory practice with transmutational aspiration now had to choose between institutional legitimacy and the older program. The construction of "alchemy" as a stigmatized category — associated with fraud, secrecy, and credulity — in early eighteenth-century texts and polemics served to make this choice easier and more socially enforced. Newman and Principe identify this construction as an "anti-alchemical propaganda" campaign that succeeded in rewriting the history of chemistry, consigning Starkey and Helmont to the pre-scientific past rather than recognizing them as the serious experimental philosophers they were. The twentieth-century recovery of their significance — through manuscript analysis, laboratory replication, and historiographical revision — represents the reversal of this process.</p>""")

    print("\n=== Expanding phlogiston concept ===")
    append_html(conn, 'concepts', 'definition_long', 'phlogiston', """
<h2>Continuity and Rupture</h2>
<p>Historians of science have debated whether the overthrow of phlogiston by Lavoisier represents a genuine "revolution" — a discontinuous break with prior practice — or a transformation within a continuous experimental tradition. Thomas Kuhn's paradigm-shift model, applied to this case in his analysis of the Chemical Revolution, emphasized discontinuity: the phlogiston paradigm was incommensurable with the oxygen paradigm, and the transition was a replacement rather than a revision. More recent historians, including Newman, Principe, and Frederic Holmes, have emphasized continuities: the experimental techniques developed within the phlogiston tradition — pneumatic troughs, eudiometry, calorimetry — were carried forward into Lavoisier's chemistry, and many of the empirical findings of phlogiston-era chemistry were reinterpreted rather than discarded. Holmes's detailed studies of Lavoisier's laboratory notebooks showed that Lavoisier's "revolution" was built on years of incremental experimental work rather than a single dramatic reorientation.</p>

<p>From the perspective of Newman and Principe's broader argument, the phlogiston episode is part of a longer story about the progressive disciplinary separation of chemistry from alchemy. Phlogiston theory was a step in this separation — it was materialist rather than vitalist, it could be taught in universities and measured in laboratories, and it made no transmutational claims. Lavoisier's Chemical Revolution completed the separation, establishing a chemistry defined by quantitative composition, systematic nomenclature, and institutional integration that explicitly excluded the residues of the alchemical tradition. The Chemical Revolution was not only a change in theory but a change in the social definition of what chemistry was and who was a chemist — a redefinition that excluded the Helmontian tradition as surely as it excluded phlogiston itself.</p>""")

    print("\n=== Expanding Lavoisier bio ===")
    append_html(conn, 'persons', 'bio_html', 'antoine-lavoisier', """
<p>Lavoisier's personal trajectory illuminates the social embedding of the Chemical Revolution. As a fermier général — a tax farmer collecting revenues on behalf of the crown — he was both wealthy and politically exposed. The Gunpowder Administration, which he directed from 1775, gave him access to industrial-scale chemical operations and significant practical influence over French military capacity. His laboratory at the Arsenal in Paris, funded by his administrative income, was among the best-equipped in Europe. The intersection of his scientific and administrative roles enabled extraordinary research productivity but also made him a target: after 1789 the Revolutionary government viewed the fermiers généraux as parasites on the poor, and Lavoisier's scientific reputation offered him no protection. His execution in 1794 — reportedly preceded by a request for a brief reprieve to complete an experiment, denied — became one of the iconic stories of the conflict between science and political power, though historians have shown that the story of the denied reprieve is apocryphal. The mathematician Joseph-Louis Lagrange reportedly commented: "It took only a moment to cut off that head, and a hundred years may not give us another like it." Within a decade, the entire chemistry world had adopted Lavoisier's oxygen framework.</p>""")

    print("\n=== Expanding Stahl bio ===")
    append_html(conn, 'persons', 'bio_html', 'georg-ernst-stahl', """
<p>Stahl's lasting influence operated through two distinct channels. In chemistry, phlogiston theory structured experimental practice and chemical education for eighty years, creating the conceptual framework within which the pneumatic chemistry of the 1770s and 1780s developed — the discoveries that, ironically, led to its overthrow. In medicine, Stahl's animism — the doctrine that a rational soul directed all physiological processes — was influential in German-speaking medicine throughout the eighteenth century and fed into the vitalist traditions that shaped German Romantic Naturphilosophie, including the work of Friedrich Schelling and Johann Friedrich Blumenbach. The tension in Stahl's thought between chemical materialism (phlogiston as a transferable substance) and medical vitalism (the soul as the director of physiological process) reflects deeper tensions in early eighteenth-century natural philosophy between mechanical and vital explanations of natural phenomena — tensions that remained productive throughout the century and were not resolved until the biological sciences developed a more rigorous experimental basis in the nineteenth century. From the perspective of the historiography of alchemy and chemistry, Stahl represents the moment at which the Helmontian program of experimental chymistry was absorbed into a systematic academic chemistry that no longer acknowledged — or even recognized — its alchemical origins.</p>""")

    print("\n=== Expanding alchemy-tried-in-the-fire text ===")
    append_html(conn, 'texts', 'analysis_html', 'alchemy-tried-in-the-fire', """
<p>The book also contains an important methodological manifesto for the history of alchemy. Newman and Principe argue that the proper historical study of alchemy requires treating alchemical texts as technical documents whose language can be decoded through a combination of close reading, comparative manuscript analysis, and laboratory replication. This approach contrasts with earlier historiographies that treated alchemical texts as allegories for spiritual or psychological experience (the Jungian approach associated with C.G. Jung and his followers) or as straightforward fraud and delusion (the positivist dismissal). Newman and Principe demonstrate that alchemical cover names corresponded to specific chemical operations and substances — that "our mercury" in a Philalethes text denoted a specific chemical preparation that could be reproduced in a modern laboratory, not a symbol or metaphor. This methodological position has been influential and contested: it has been criticized for potentially underweighting the genuine symbolic dimensions of alchemical discourse, but it has also opened new lines of historical inquiry that the purely symbolic approach foreclosed.</p>""")

    print("\n=== Expanding ortus-medicinae text ===")
    append_html(conn, 'texts', 'analysis_html', 'ortus-medicinae', """
<p>The <i>Ortus Medicinae</i> also contains van Helmont's claim to have personally witnessed metallic transmutation — a claim he presented as direct empirical evidence, framed with the same observational language he applied to his gas experiments. He describes receiving a small quantity of the Philosophers' Stone from an anonymous stranger and using it to transmute mercury into gold, weighing the product. Whether or not this account is credible, its form is significant: van Helmont presented it as an observable, measurable experimental result, subject to the same standards he applied to his laboratory work on gases and fermentation. Lawrence Principe has argued that this framing should be taken seriously as evidence for how empirical norms operated in seventeenth-century natural philosophy: for van Helmont, the claim to have witnessed transmutation was not a departure from his empirical program but an extension of it. The <i>Ortus Medicinae</i> thus represents a text in which the classical alchemical goal — the Philosophers' Stone and metallic transmutation — was integrated into, rather than separated from, a sophisticated empirical natural philosophy. This integration is precisely what Newman and Principe's category of "Helmontian chymistry" is designed to capture: a tradition in which the alchemical and the experimental were not opposed but mutually constitutive.</p>""")

    print("\n=== Expanding sceptical-chymist text ===")
    append_html(conn, 'texts', 'analysis_html', 'sceptical-chymist', """
<p>The text's relationship to transmutational alchemy is also clarified by Boyle's other writings and manuscripts. Principe's reconstruction of Boyle's "lost" <i>Dialogue on the Transmutation and Melioration of Metals</i> from manuscript fragments scattered in the Boyle Papers at the Royal Society demonstrates that Boyle maintained an active interest in transmutation throughout his life, sought witnesses to alleged transmutations, attempted to have English legislation against gold-making repealed specifically to facilitate alchemical practice, and believed he had personally witnessed metallic transmutation on at least one occasion. These activities are irreconcilable with the received interpretation of the <i>Sceptical Chymist</i> as an anti-alchemical text. Boyle's use of nine different ciphers to conceal alchemical accounts in his private manuscripts — identified by Principe — underscores the sensitivity surrounding his alchemical pursuits in an increasingly public scientific culture, not a private rejection of the tradition. The <i>Sceptical Chymist</i> is thus best understood as a philosophical argument about the foundations of chemical theory, not a disciplinary manifesto separating chemistry from alchemy. Its historical significance lies precisely in how it was misread: the nineteenth-century construction of Boyle as an anti-alchemical hero was itself a significant historiographical event that shaped the subsequent history of the discipline.</p>""")

    conn.commit()
    conn.close()
    print("\n=== Expansions complete ===")


if __name__ == '__main__':
    load_expansions()
