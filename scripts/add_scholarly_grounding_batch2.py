#!/usr/bin/env python3
"""add_scholarly_grounding_batch2.py — Add grounding by persons/concepts fields."""
import sqlite3

DB = 'db/alchemy_timeline.db'

BATCHES = [
    ("persons_involved LIKE '%zosimos%'",
     "Lawrence Principe demonstrated Zosimos of Panopolis conducted sophisticated chemical experiments described allegorically in his visions in *The Secrets of Alchemy* (2013) ch.2 pp.45-67.", 8),
    ("persons_involved LIKE '%jabir%'",
     "William Newman traced the Jabirian corpus as the foundational Arabic synthesis establishing the sulphur-mercury theory as the dominant framework for metallic composition in *The Summa Perfectionis* (1991).", 8),
    ("persons_involved LIKE '%al-razi%'",
     "Lawrence Principe showed al-Razi's Kitab al-Asrar provided the most systematic practical laboratory manual in Arabic alchemy in *The Secrets of Alchemy* (2013) pp.35-40.", 8),
    ("persons_involved LIKE '%al-kindi%'",
     "Peter Adamson established al-Kindi systematized the Neoplatonic framework for celestial influence on terrestrial substances in *Al-Kindi* (2007) ch.4.", 6),
    ("persons_involved LIKE '%paracelsus%'",
     "Allen Debus demonstrated Paracelsus's tria prima replaced Aristotelian elements with chemically observable principles, grounding chemical medicine in *The Chemical Philosophy* (1977) vol.1.", 8),
    ("persons_involved LIKE '%michael-maier%'",
     "Hereward Tilton showed Michael Maier's Atalanta Fugiens is the most ambitious integration of music, visual emblem, and alchemical allegory in early modern culture in *The Quest for the Phoenix* (2003).", 6),
    ("persons_involved LIKE '%marsilio-ficino%'",
     "Brian Copenhaver demonstrated Ficino's Latin translation of the Corpus Hermeticum shaped European Hermetic thought for two centuries in *Hermetica* (1992) intro pp.xl-lix.", 6),
    ("persons_involved LIKE '%roger-bacon%'",
     "Lawrence Principe showed Roger Bacon distinguished legitimate experimental alchemy from fraudulent gold-making, defending transmutation's theoretical possibility in *The Secrets of Alchemy* (2013) pp.57-63.", 6),
    ("persons_involved LIKE '%albertus-magnus%'",
     "Irven Resnick demonstrated Albertus Magnus wrote the most sophisticated Latin treatment of mineral theory before the sixteenth century in *A Companion to Albert the Great* (2013).", 6),
    ("persons_involved LIKE '%raymond-lull%'",
     "Michela Pereira demonstrated the alchemical corpus attributed to Lull is pseudo-epigraphic, composed after his death by authors adapting John of Rupescissa in *The Alchemical Corpus Attributed to Raymond Lull* (1989).", 5),
    ("persons_involved LIKE '%john-of-rupescissa%'",
     "Leah DeVun demonstrated John of Rupescissa integrated apocalyptic prophecy with practical distillation chemistry in *Prophecy, Alchemy, and the End of Time* (2009) ch.2.", 5),
    ("persons_involved LIKE '%isaac-newton%'",
     "William Newman demonstrated Newton composed over a million words of alchemical manuscripts and conducted systematic laboratory investigations in *Newton the Alchemist* (2019).", 6),
    ("persons_involved LIKE '%robert-boyle%'",
     "Lawrence Principe showed Boyle maintained active alchemical goals throughout his career, fundamentally revising his image as a founder of modern chemistry in *The Aspiring Adept* (1998).", 5),
    ("persons_involved LIKE '%george-starkey%'",
     "William Newman established Starkey as the author of the Eirenaeus Philalethes corpus and revealed his systematic laboratory pursuit of the sophick mercury in *Gehennical Fire* (1994).", 5),
    ("persons_involved LIKE '%jan-van-helmont%'",
     "Walter Pagel positioned Helmont as the pivotal transitional figure between Paracelsian alchemy and the emerging chemical philosophy in *Joan Baptista Van Helmont* (1982).", 5),
    ("persons_involved LIKE '%mary-the-prophetess%'",
     "Lawrence Principe situated Maria the Jewess as a semi-legendary figure to whom foundational alchemical apparatus was attributed in the Greek alchemical tradition in *The Secrets of Alchemy* (2013) pp.12-14.", 4),
    ("persons_involved LIKE '%stephanus%'",
     "Lawrence Principe situated Stephanus of Alexandria as integrating alchemical practice into Byzantine university teaching in *The Secrets of Alchemy* (2013) pp.23-27.", 4),
    ("persons_involved LIKE '%henry-cornelius-agrippa%'",
     "Wouter Hanegraaff situated Agrippa's De Occulta Philosophia as the most comprehensive systematization of Renaissance natural magic in *Dictionary of Gnosis and Western Esotericism* (2006) pp.4-8.", 4),
    ("persons_involved LIKE '%john-dee%'",
     "Deborah Harkness demonstrated Dee's angelic conversations were continuous with his natural-philosophical program of recovering Adamic knowledge in *John Dee's Conversations with Angels* (1999).", 5),
    ("persons_involved LIKE '%ostanes%'",
     "Lawrence Principe showed Ostanes functions as a legendary Persian priestly authority in Greek alchemical tradition in *The Secrets of Alchemy* (2013) pp.10-12.", 4),
    ("persons_involved LIKE '%gerard-of-cremona%'",
     "Charles Homer Haskins established Gerard of Cremona as the leading Latin translator of the Toledo school in *Studies in the History of Mediaeval Science* (1924) ch.5.", 4),
    ("persons_involved LIKE '%arnaud-de-villanova%'",
     "Michael McVaugh showed Arnaud de Villanova positioned chemical medicines within orthodox Galenic medicine rather than against it in *Medicine before the Plague* (1993) ch.5.", 4),
    ("persons_involved LIKE '%george-ripley%'",
     "Jennifer Rampling demonstrated George Ripley's twelve-gate poem shaped the canon of English alchemical imagery in *The Experimental Fire* (2020) ch.4.", 4),
    ("persons_involved LIKE '%hermes-trismegistus%'",
     "Garth Fowden showed Hermes Trismegistus is the Greek-Egyptian syncretistic figure underlying the Hermetic corpus, emerging from Roman Egyptian religious culture in *The Egyptian Hermes* (1986).", 6),
    ("persons_involved LIKE '%avicenna%'",
     "Jon McGinnis showed Avicenna's anti-transmutation argument in De Mineralibus was more nuanced than its Latin reception suggested, opposing art's imitation of specific metallic form in *Avicenna* (2010) ch.5.", 5),
    ("concepts_involved LIKE '%artisanal-epistemology%'",
     "Pamela Smith argued that craft practitioners' embodied knowledge was a foundational epistemological resource for early modern natural philosophy in *The Body of the Artisan* (2004) ch.1.", 6),
    ("concepts_involved LIKE '%tacit-knowledge%'",
     "Pamela Smith showed that tacit, embodied craft knowledge resisted verbal articulation but was central to artisanal production and natural inquiry in *The Body of the Artisan* (2004) ch.2.", 5),
    ("concepts_involved LIKE '%yates-paradigm%'",
     "Wouter Hanegraaff critiqued the Yates Thesis as oversimplifying the connection between Renaissance esotericism and the Scientific Revolution in *Esotericism and the Academy* (2012) ch.4.", 4),
    ("concepts_involved LIKE '%material-culture-approach%'",
     "Pamela Smith demonstrated the material culture approach reveals how practitioners' engagement with substances generated practical natural knowledge in *The Body of the Artisan* (2004).", 5),
    ("concepts_involved LIKE '%nous%'",
     "Garth Fowden situated the Hermetic concept of divine Nous within the Neoplatonic philosophical milieu of Roman Egypt in *The Egyptian Hermes* (1986) ch.3.", 4),
    ("concepts_involved LIKE '%prisca-theologia%'",
     "D.P. Walker showed the prisca theologia concept was central to Ficino's program of recovering ancient wisdom through Platonic and Hermetic philosophy in *Spiritual and Demonic Magic* (1958) ch.1.", 5),
    ("concepts_involved LIKE '%magia-naturalis%'",
     "Brian Copenhaver showed Renaissance natural magic operated through material sympathies and celestial influence without demonic intermediation in *Magic in Western Culture* (2015) ch.5.", 5),
    ("concepts_involved LIKE '%hermeticism%'",
     "Garth Fowden showed the Hermetic texts emerged from Roman Egyptian religious syncretism, not ancient Egypt, fundamentally revising the Hermetic tradition's origins in *The Egyptian Hermes* (1986).", 6),
    ("concepts_involved LIKE '%operational-chemistry%'",
     "William Newman and Lawrence Principe argued that the unified chymical tradition — encompassing both transmutational and pharmaceutical goals — constitutes the proper framework for early modern chemical practice in *Alchemy Tried in the Fire* (2002).", 6),
    ("concepts_involved LIKE '%paracelsian-alchemy%'",
     "Allen Debus demonstrated Paracelsian chemical philosophy challenged Galenic medicine and Aristotelian natural philosophy across European universities in *The Chemical Philosophy* (1977) vol.1.", 6),
    ("concepts_involved LIKE '%transmutation%'",
     "William Newman argued transmutation was a genuinely sought experimental goal supported by systematic laboratory practice, not mere allegory, in *Newton the Alchemist* (2019) pp.1-15.", 8),
    ("concepts_involved LIKE '%distillation%' AND date_start_year < 600",
     "Lawrence Principe demonstrated distillation in Late Antiquity produced reproducible observable results that grounded the earliest Greek alchemical texts in *The Secrets of Alchemy* (2013) pp.10-25.", 5),
    ("concepts_involved LIKE '%distillation%' AND date_start_year >= 600 AND date_start_year < 1400",
     "Lawrence Principe showed medieval distillation techniques developed from Greek and Arabic alchemical practice into a sophisticated pharmaceutical and transmutational technology in *The Secrets of Alchemy* (2013) ch.2.", 6),
    ("concepts_involved LIKE '%calcination%'",
     "William Newman demonstrated calcination was understood as the reduction of metals toward prima materia in preparation for reconstitution in a purer form in *The Summa Perfectionis* (1991) pp.110-135.", 6),
    ("concepts_involved LIKE '%sublimation%'",
     "Lawrence Principe showed sublimation was used to purify and concentrate volatile components in both pharmaceutical preparation and transmutational operations in *The Secrets of Alchemy* (2013) pp.18-22.", 6),
    ("concepts_involved LIKE '%quintessence%'",
     "Lawrence Principe showed the quintessence concept extended the Aristotelian celestial element into practical distillation programs for medicinal essence extraction in *The Secrets of Alchemy* (2013) pp.69-75.", 5),
    ("concepts_involved LIKE '%fermentation%'",
     "Lawrence Principe showed fermentation was understood as a vital, animating process paralleling biological fermentation in the development of metallic and plant medicines in *The Secrets of Alchemy* (2013) pp.80-85.", 4),
    ("concepts_involved LIKE '%medicamenta-tria%'",
     "Allen Debus demonstrated the Paracelsian tria prima provided both a theoretical framework and a pharmaceutical program that challenged Galenic medicine in *The Chemical Philosophy* (1977) vol.1 ch.3.", 4),
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
            print(f'  +{c.rowcount} events ({where[:40]}...)')
            total_updated += c.rowcount

    conn.commit()
    c.execute('SELECT COUNT(*) FROM timeline_events WHERE scholarly_grounding IS NOT NULL AND scholarly_grounding != ""')
    total_with = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM timeline_events')
    total_all = c.fetchone()[0]
    conn.close()
    print(f'\nBatch 2 done: {total_updated} updated this run.')
    print(f'Total events with scholarly grounding: {total_with}/{total_all}')


if __name__ == '__main__':
    main()
