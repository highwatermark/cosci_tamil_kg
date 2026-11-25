# Methods review: ThinaiKG and "An Introduction to the Tamil Siddhas"

Reviewed 2026-11-25. Both works are in copyright. This note summarises their methods in our own words
and quotes neither.

## ThinaiKG (Simon Peter J, M.Tech dissertation, BITS Pilani WILP, 2025-26; project report Sept 2026)

**What it built.**
- Corpus: 1,891 akam verses from the seven Project Madurai akam texts: Ainkurunuru 498, Kuruntokai 401,
  Natrinai 399, Akananuru 396, Kalittokai 149, and Kurinjippattu and Mullaippattu cut into 27 and 21 pieces.
- Each verse is classified into one of the five thinai.
- A lexicon of named things grew from 176 seed terms to 417.
- The graph has 2,313 nodes and 21,950 edges, exported as OWL, GraphML and JSON. It is published at
  sangamtamil.com.

**Method.**
1. Strip commentary and metadata. Normalise Unicode. Deliberately do not lemmatise, because inflected
   word forms carry the cues.
2. Build a balanced ground truth of 500 verses, 100 per thinai, "manually verified".
3. Baseline: TF-IDF over 10,000 n-grams, SMOTE and an RBF SVM gave macro F1 0.52. Dropping Marutham
   did not help, so the features were the problem, not the class.
4. The turning point was to keep only karupporul words (Tholkappiyam's native things) as features.
   F1 rose to 0.68 with 145 entities and to 0.82 with the grown lexicon. The model is a one-vs-rest
   linear SVM.
5. The lexicon was grown with a human in the loop:
   - take verses classified with confidence above 0.95
   - score each term as SVM coefficient times summed TF-IDF, keeping terms with coefficient above 0.7
     and frequency of at least 3
   - a human accepts or rejects each term
   - retrain and repeat
   Sixteen versioned lexicons, an acceptance rate of 83%, and a filtered set of 237 entities that
   performed within 1% of a 1,000-term set.
6. IndicBERT v2 peaked at 58.6%: too little data, and the tokenizer fragments archaic words.
7. Ontology: Thinai, Verse, Entity and Category, with APPEARS_IN, BELONGS_TO, HAS_CATEGORY and a derived
   CHARACTERIZES edge. An entity enters the graph only with "double confirmation": a high-confidence
   verse and a significant weight.

**Results.** Accuracy 82.3%, macro F1 0.82. Per thinai: Neytal 0.87, Kurinji 0.84, Marutham 0.80,
Mullai 0.80, Palai 0.79 (precision 0.74), because drought can turn any landscape into Palai.

**Cautions before using it as ground truth.**
- *Where the gold labels come from.* Most akam poems already carry a thinai in their colophon, and for
  Akananuru the thinai follows from the poem's number. The report does not say whether the 500 gold
  labels are colophon labels or a person's judgment. For validation we should treat the colophon as
  the authority and their classifier's output as a second opinion.
- *Possible leakage.* The report does not describe a held-out split. The same 500 verses are used "for
  training and evaluation", and the lexicon was grown from model weights over the same corpus. So
  0.82 is probably optimistic.
- *Theory.* Tholkappiyam lets the native things (karu) and the setting (mutal) cross landscapes
  (திணை மயக்கம்), and treats the human situation (uri) as what settles the thinai. An entity-only model
  reads only the weakest signal, which fits its Palai errors. Our Tholkappiyam pilot tags uri and the
  eight feelings, so it complements their work rather than repeating it.
- *Review.* A single reviewer accepted the terms, and no agreement between reviewers is reported.
- *Coverage.* Akam only: no Puram, and only 2 of the 10 Pattupattu poems. Akananuru has 396 of 400
  poems and Kalittokai 149 of 150, so a few poems were lost in parsing.

**What we adopt.**
1. *Domain theory as features.* Use Tholkappiyam's categories as the tagging frame for the Sangam books,
   and a cipher lexicon for the Siddhars. The concept list stays as a separate layer.
2. *A versioned lexicon with an acceptance loop.* Agents propose terms, blind graders accept or reject
   them, and we report the acceptance rate and growth per cycle. A human Tamil reader remains the final
   check; none has reviewed anything yet.
3. *An interpretable model as a discovery engine.* A stdlib classifier (naive Bayes or logistic) over
   lexicon features, predicting thinai for Sangam verses or the reading layer for Siddhar verses. Its
   weights propose new lexicon terms. It is never the final judge.
4. *Double confirmation before an edge enters the graph.* We already require a blind grade. Science
   links will also need two graders.
5. *Experiment log and negative results.* Add docs/experiment-log.md and record what failed.
6. *Validation.* Score our Sangam marking against the colophon thinai first, then against their
   classifier and their entity mentions (scripts/sangam_validate.py, being written).

## Layne Little, "An Introduction to the Tamil Siddhas" (Indian Folklife 2:4, 2003)

A short survey essay by a Berkeley doctoral candidate, not a peer-reviewed study.

**Method.** A thematic and historical survey:
- places the Tamil Siddhas inside the pan-Indian tantric, Nath and Rasa Siddha movements
- reads sectarian history, especially the conflict between the Siddhas and Saiva Siddhanta:
  interpolation in the Tirumanthiram, hostility to Sivavakkiyar's songs, and the controversy over
  Ramalingar
- translates a few verses closely: Tirumanthiram 730 and 801, Auvaiyar's Vinayagar Agaval, and Bhogar
- uses philology on double meanings, e.g. துதிக்கை as both "hand of worship" and "elephant's trunk",
  which places Ganesha at the base centre

**Claims that matter for us.**
- *No single doctrine.* The Siddhas hold no common doctrine and often set incompatible views side by
  side. This argues against reading them all as monists. → Add a **stance** field to each verse:
  shakta-tantric, saiva-siddhanta, void non-dual, alchemical, ethical-social. Some of our "tension"
  links may be stance differences, not errors.
- *Layered imagery.* Each image is meant to be read on its own, in sequence, and as part of the whole
  verse. → Readings should be checked at three scales: word, line and verse.
- *Double readings carry the cipher.* → Build a **double-reading lexicon**, citing each entry and
  counting how often it occurs across the corpus. This joins ThinaiKG's lexicon loop.
- *Uncertain attribution and dates.* Many Siddha "traditions" are modern inventions, and Bhogar's
  hagiography is legendary. → Keep the attribution field and add attribution confidence. Treat claims
  about lineage as tradition, not history.
- *Alchemy as inner and outer work.* The alchemists read the kundalini process and the chemical work as
  mirror images of each other. This fits our separate alchemy and breath layers. It also fits what the
  science comparison found: several Siddhar verses themselves call outward gold-making fraud.

Both additions, the stance field and the double-reading lexicon, have been sent to the reading-layers
pilot that is in progress.
