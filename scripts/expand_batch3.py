#!/usr/bin/env python3
"""expand_batch3.py — Expand Boerhaave, Black, Scheele bios + near-minimum texts."""
import sqlite3, re
DB = 'db/alchemy_timeline.db'

def wc(h): return len(re.sub('<[^>]+>', ' ', h or '').split())

def app(conn, table, field, slug, extra):
    c = conn.cursor()
    c.execute(f'SELECT {field} FROM {table} WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row: print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute(f'UPDATE {table} SET {field}=? WHERE slug=?', (new, slug))
    print(f'  {slug}: {wc(cur)} -> {wc(new)}')

BOERHAAVE_EXTRA = (
    '<h2>Chemistry and the Phlogiston Tradition</h2>'
    '<p>Boerhaave\'s <i>Elementa Chemiae</i> (1732) was the most widely read chemistry textbook in'
    ' Europe for three decades. Its incorporation of phlogiston theory gave the theory its first major'
    ' textbook treatment, making it accessible to students across Europe who had not read Stahl\'s more'
    ' technical presentations. Boerhaave adapted phlogiston to a broader pedagogical framework and'
    ' integrated it with his own experimental findings on mercury, metals, and substances under heat.</p>'
    '<p>His experimental contributions included careful heating of mercury in sealed vessels, which showed'
    ' the metal did not decompose as combustible bodies did — contributing to discussions about chemical'
    ' elements that would bear fruit in Lavoisier\'s later work. His quantitative attention to thermal'
    ' behavior anticipated the calorimetric approach that Joseph Black would systematize. His insistence'
    ' that chemistry had a theoretical foundation — that practitioners understand why operations worked,'
    ' not merely how — shaped the intellectual culture his students carried to Edinburgh, Gottingen,'
    ' Vienna, and beyond.</p>'
    '<p>Boerhaave\'s <i>Elementa Chemiae</i> treated alchemy with measured respect in its historical'
    ' introduction, acknowledging that alchemical practitioners had accumulated genuine chemical knowledge'
    ' while dismissing transmutational claims as unproven. This stance — respectful of alchemical practice,'
    ' dismissive of alchemical goals — helped establish the narrative that chemistry had grown out of'
    ' alchemy by discarding its speculative excesses while retaining its practical knowledge. Newman and'
    ' Principe have criticized this narrative as an oversimplification that obscures the experimental'
    ' seriousness of practitioners like [LINK:george-starkey] and [LINK:robert-boyle]; but Boerhaave\'s'
    ' influential framing shaped how subsequent generations of chemists understood their own history.</p>'
    '<p>Boerhaave\'s Leiden teaching clinic, the first attached to a European university, established'
    ' clinical bedside instruction as a norm in medical education. Through his students — Albrecht von'
    ' Haller, William Cullen, Alexander Monro — his combination of systematic theory and empirical'
    ' observation became the model for European medical and chemical education through the end of the'
    ' eighteenth century. His network of correspondents and former students constitutes a significant'
    ' chapter in the social history of Enlightenment science.</p>'
)

BLACK_EXTRA = (
    '<h2>Fixed Air and Latent Heat</h2>'
    '<p>Black\'s 1754 dissertation and subsequent memoir demonstrated that magnesia alba contained a'
    ' distinct gas — fixed within the solid — released when heated or treated with acid. This gas'
    ' extinguished flames, was absorbed by lime, and corresponded to the air exhaled in breathing and'
    ' produced by fermentation. The conceptual breakthrough was establishing that a chemically specific'
    ' gas could exist, be produced, identified, and measured. Before Black, atmospheric air was generally'
    ' treated as a uniform substance. His "fixed air" (carbon dioxide) opened conceptual space for'
    ' inflammable air (Cavendish, 1766), dephlogisticated air (Scheele c. 1772 and Priestley 1774),'
    ' and the full pneumatic taxonomy that [LINK:antoine-lavoisier] systematized in the 1780s.</p>'
    '<p>His latent heat work, developed in Edinburgh lectures but published only posthumously in'
    ' <i>Lectures on the Elements of Chemistry</i> (1803), demonstrated that heat and temperature were'
    ' not identical: a substance could absorb substantial heat without any temperature change during a'
    ' phase transition. This distinction between sensible and latent heat was foundational for'
    ' thermodynamics and for James Watt\'s separate condenser design. Watt, a Glasgow instrument maker'
    ' and Black\'s close friend, acknowledged the influence of Black\'s thermal concepts on his'
    ' engineering work — a direct line from chemical research to industrial revolution.</p>'
    '<p>Black worked throughout his career within the phlogiston framework of [LINK:georg-ernst-stahl].'
    ' His careful quantitative approach — precise weighing, systematic comparison of substances before'
    ' and after reactions — established the methodological standard that Lavoisier applied to devastating'
    ' effect against phlogiston theory in the 1770s and 1780s. Black was initially skeptical of the'
    ' oxygen theory but was eventually persuaded by accumulating experimental evidence. His trajectory'
    ' from phlogiston practitioner to Chemical Revolution convert illustrates how the paradigm shift'
    ' proceeded through persuasion of careful experimentalists rather than through theoretical argument alone.</p>'
    '<p>Frederic Holmes\'s examination of eighteenth-century chemical investigation has been central to'
    ' situating Black\'s work within its experimental context. A.L. Donovan\'s studies of Scottish'
    ' Enlightenment chemistry provide the institutional and social background for Black\'s Edinburgh career.'
    ' The connection between Black\'s quantitative method and the earlier tradition of alchemical'
    ' laboratory notebooks — particularly the weighing practices documented in [LINK:george-starkey]\'s'
    ' notebooks — is noted in Newman and Principe\'s historiographical work as evidence for methodological'
    ' continuity across the supposed alchemy-chemistry divide.</p>'
)

SCHEELE_EXTRA = (
    '<h2>Systematic Discovery: Gases and Organic Acids</h2>'
    '<p>Scheele\'s isolation of oxygen — which he called "Feuerluft" (fire air) — was achieved by'
    ' heating metallic oxides including manganese dioxide and mercury calx, observing that the released'
    ' gas supported combustion far more vigorously than ordinary air. He interpreted this within the'
    ' phlogiston framework: fire air was ordinary air depleted of phlogiston, available to absorb more'
    ' during combustion. The experimental identification was correct; the interpretation was wrong. His'
    ' <i>Chemische Abhandlung von der Luft und dem Feuer</i> (1777) also described the first preparation'
    ' of chlorine (dephlogisticated muriatic acid), the identification of manganese, and the preparation'
    ' of barium compounds.</p>'
    '<p>His work on organic acids was equally remarkable: tartaric acid from wine tartrates (1769),'
    ' oxalic acid (1776), malic acid from apples (1785), citric acid from lemons (1784), lactic acid'
    ' from sour milk (1780), and uric acid from urine (1776). This systematic exploration of plant and'
    ' animal acids established organic chemistry as a distinct domain. Working in provincial Swedish'
    ' apothecary laboratories without institutional resources or patronage, Scheele produced an'
    ' experimental record that few eighteenth-century chemists could match.</p>'
    '<p>Scheele\'s career illustrates how thoroughly the phlogiston framework organized chemical'
    ' thinking even among the most productive experimentalists of the era. The framework failed him'
    ' only at the interpretive level: when he and Priestley isolated oxygen independently, both'
    ' interpreted it as air depleted of phlogiston rather than a distinct substance. [LINK:antoine-lavoisier],'
    ' working with similar experimental data but a different theoretical commitment — systematic'
    ' conservation of mass and skepticism about phlogiston as a distinct substance — arrived at the'
    ' correct interpretation. The Scheele case supports a key historiographical point: theoretical'
    ' frameworks are not merely passive descriptions of experiments but active organizers of'
    ' what experiments can mean. The priority dispute between Scheele (isolated c. 1772, published 1777)'
    ' and Priestley (isolated 1774, published 1775) also raises fundamental questions about what'
    ' "discovery" means in science and how credit is assigned in scientific communities.</p>'
)

# Texts still below 1000 words
SUMMA_EXTRA = (
    '<p>The <i>Summa Perfectionis</i> also contains detailed treatment of laboratory operations —'
    ' calcination, sublimation, solution, coagulation — that grounds its theoretical claims in specific'
    ' experimental procedures. This combination of theoretical sophistication with operational specificity'
    ' gives the text its status as the most important systematic treatise in medieval Latin alchemy.'
    ' Newman\'s critical edition makes clear that pseudo-Geber was developing a distinctive theoretical'
    ' position, not merely synthesizing Arabic material, and that this position had consequences for the'
    ' development of matter theory extending into corpuscular philosophy and ultimately to Boyle\'s'
    ' <i>Sceptical Chymist</i>. The text is therefore a hinge document: it stands at the intersection of'
    ' Arabic natural philosophy, Latin scholastic commentary, and the early modern corpuscular tradition.</p>'
)

ROSARIUM_EXTRA = (
    '<p>The <i>Rosarium Philosophorum</i> is also significant as a transmission vehicle: its systematic'
    ' quotation of earlier alchemical authorities — Aristotle, Avicenna, Arnold of Villanova, Raymond'
    ' Lull, the author of the <i>Turba Philosophorum</i> — made it a convenient reference to the broader'
    ' tradition for later readers. [LINK:george-starkey] drew on the Rosarium tradition in developing his'
    ' own theoretical framework, and [LINK:isaac-newton]\'s alchemical reading included works in the'
    ' Rosarium tradition. Lawrence Principe\'s laboratory replication work suggests that the specific'
    ' color sequence described in the text — black, white, red — corresponds to observable changes in'
    ' mercury-sulfur preparations, providing a practical chemical referent for what the symbolic imagery'
    ' encodes and demonstrating that the text\'s apparent allegory was operationally grounded.</p>'
)

AURORA_EXTRA = (
    '<p>The <i>Aurora Consurgens</i> reflects a broader strategy in medieval alchemical writing: grounding'
    ' claims about material transformation in theological authority. If Aquinas had affirmed art imitating'
    ' nature, and if divine creation involved the same material principles alchemy sought to manipulate,'
    ' then alchemical practice was legitimate investigation of divinely established natural processes.'
    ' This theological legitimation was widespread in medieval Latin alchemy and reflects the institutional'
    ' context in which it was practiced — by clergy, physicians, and scholars who needed to reconcile their'
    ' investigations with dominant theological frameworks. Michela Pereira has discussed the text in the'
    ' context of the pseudo-Lullian tradition, noting that attribution to Aquinas, while spurious, reflects'
    ' the strategy of attaching alchemical works to scholastic authorities to give them philosophical'
    ' legitimacy within university and ecclesiastical environments.</p>'
)

OPUSMAJUS_EXTRA = (
    '<p>The three companion works were sent to Pope Clement IV in response to a request for a summary'
    ' of Bacon\'s views on the reform of learning. The alchemical material in these works is embedded'
    ' within a broader argument that Christian education required mastery of mathematics, optics, languages,'
    ' and natural philosophy. This embedding is significant for the history of alchemy: Bacon demonstrates'
    ' that in the thirteenth century, alchemical knowledge could be presented to a pope as part of a'
    ' legitimate program of Christian learning. William Newman has analyzed Bacon\'s insistence on'
    ' <i>experimentum</i> (experience) as a philosophical criterion as an important, if imperfectly'
    ' applied, anticipation of the experimental orientation of seventeenth-century natural philosophy,'
    ' and has traced how the alchemical texts attributed to Bacon were read by early modern practitioners'
    ' including [LINK:isaac-newton] and [LINK:robert-boyle] as carrying the authority of a recognized'
    ' scholastic-empirical tradition.</p>'
)

DEOCCULTA_EXTRA = (
    '<p>The tripartite structure of <i>De Occulta Philosophia</i> — natural magic, celestial magic,'
    ' ceremonial magic — provides a comprehensive philosophical framework for what Agrippa regarded as'
    ' legitimate natural and divine knowledge. The relationship to practical alchemy is indirect but real:'
    ' the doctrine of correspondences (macrocosm-microcosm, celestial influences on metals, sympathies'
    ' and antipathies between substances) that organizes books one and two was the same doctrine that'
    ' structured early modern alchemical thinking about metallic transformation under planetary auspices.'
    ' Frances Yates\'s influential but contested analysis in <i>Giordano Bruno and the Hermetic Tradition</i>'
    ' (1964) argued that this tradition drove the Scientific Revolution. Brian Vickers and subsequent'
    ' scholars challenged this thesis. Newman and Principe\'s position — that the chymical tradition was'
    ' experimental and operational in ways that magical philosophy was not — implies a distinction between'
    ' Agrippa\'s synthesizing programme and the laboratory-oriented chymistry of the Helmontian tradition,'
    ' even where both drew on shared symbolic vocabularies.</p>'
)

def load_all():
    conn = sqlite3.connect(DB)
    print('=== Person bios ===')
    app(conn, 'persons', 'bio_html', 'herman-boerhaave', BOERHAAVE_EXTRA)
    app(conn, 'persons', 'bio_html', 'joseph-black', BLACK_EXTRA)
    app(conn, 'persons', 'bio_html', 'carl-wilhelm-scheele', SCHEELE_EXTRA)

    print('\n=== Text expansions ===')
    app(conn, 'texts', 'analysis_html', 'summa-perfectionis', SUMMA_EXTRA)
    app(conn, 'texts', 'analysis_html', 'rosarium-philosophorum', ROSARIUM_EXTRA)
    app(conn, 'texts', 'analysis_html', 'aurora-consurgens', AURORA_EXTRA)
    app(conn, 'texts', 'analysis_html', 'opus-majus', OPUSMAJUS_EXTRA)
    app(conn, 'texts', 'analysis_html', 'de-occulta-philosophia', DEOCCULTA_EXTRA)

    conn.commit()
    conn.close()
    print('\n=== Done ===')

if __name__ == '__main__':
    load_all()
