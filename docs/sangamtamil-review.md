# Review: sangamtamil.com and the ThinaiKG dissertation

Written 2026-11-25 for the Purananuru, Akananuru and Pattupattu passes. Everything below is a
summary in our own words. Nothing from the site's prose, its English translations or the
dissertation is copied into the repository. The site's text and labels were read as data only.

## How the site was read

- The crawl stayed on sangamtamil.com, made one request per second with a plain User-Agent, and
  followed every link and every `data/*.js` file that a page loads. Some of those files are
  loaded by script (`data/verses/<id>.js`, `data/texts/<id>.js`), so their URLs were built from
  the registry in `data/corpus.js`. There is no robots.txt or sitemap; both return 404.
- **453 requests in all**: 430 returned 200, 20 returned 404 (link guesses from script strings
  that do not exist) and 3 returned 403 (directory listings). The 430 are 132 pages and data
  files, the 11 MB report PDF and 297 entity images. The cache (56 MB) is at
  `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/sangamtamil_crawl/`.
  The extracted tables (all entities, all 8,082 mentions, per-verse labels, the poets file and
  the landscape table) are in its `_extracted/` folder. The crawl log is
  `.../scratchpad/stc_crawl_log.tsv`, and the parsing scripts are in `.../scratchpad/stc_tools/`.
- The report PDF was read with a small standard-library PDF text extractor, because neither
  pdftotext nor pypdf is installed. It extracted cleanly except for Tamil vowel-sign order in one
  example on page 5.

## 1. What the site contains

The site is a static reading edition. Its registry, `data/corpus.js`, lists 47 texts in six
groups, each with a canonical extent, the extent on the site, a status (`reader` for the full
text, `partial`) and a note on any gap. The Sangam texts come from Vaidehi Herbert's translation
site: Tamil text, English translation and colophon labels, held per collection in
`data/verses/<id>.js`. The other texts are built from Project Madurai e-texts and held in
`data/texts/<id>.js`. Kural data is in `data/kural_data.js`.

### Sangam: the eight anthologies (Ettuthogai)

| Text | Canonical | On site | Status | Units in data | Thinai label per unit | Units with entities |
|---|---|---|---|---|---|---|
| Natrinai | 400 | 399 | reader (234 lost) | 399 | all 399 (colophon) | 362 (91%) |
| Kuruntokai | 401 | 401 | reader | 401 | all 401 (colophon) | 305 (76%) |
| Ainkurunuru | 500 | 498 | reader | 498 | all 498 (by the hundreds) | 349 (70%) |
| Patirruppattu | 80 | 80 | reader (decads 1 and 10 lost) | 80 | none | 77 (96%) |
| Paripadal | 70 | 22 | partial | 22 | none | 22 (100%) |
| Kalittokai | 150 | 150 | reader | 150 | all 150 (by section) | 140 (93%) |
| Akananuru | 400 | 400 | reader | 400 | all 400 (by number) | 395 (99%) |
| Purananuru | 400 | 398 | partial (267, 268 lost) | 398 | none | 347 (87%) |

### Sangam: the ten idylls (Pattupattu)

Each idyll is cut into segments of a few to about twenty lines, with a line span and an English
heading. The idylls count lines, not poems.

| Idyll | Lines | Segments | Thinai on segments | Segments with entities | Site gap |
|---|---|---|---|---|---|
| Thirumurugatruppadai | 317 | 32 | none | 18 | |
| Porunaratruppadai | 248 | 20 | none | 16 | |
| Sirupanatruppadai | 269 | 51 | none | 33 | lines 219-220 untranslated, Tamil from Project Madurai |
| Perumpanatruppadai | 500 | 41 | none | 38 | |
| Mullaippattu | 103 | 18 | mullai | 11 | |
| Maduraikkanchi | 782 | 65 | none | 50 | lines 453-460 and 700-709 untranslated |
| Nedunalvadai | 188 | 27 | none | 19 | |
| Kurinjippattu | 261 | 28 | kurinji | 21 | |
| Pattinappalai | 301 | 40 | none | 30 | |
| Malaipadukadam | 583 | 44 | none | 35 | lines 561-583 untranslated |

### The rest of the corpus

- **Grammar**: Tolkappiyam, partial, 1,546 of the 1,611 nurpa the tradition counts (Project Madurai pmuni0100).
- **Eighteen minor works**: Thirukkural (1,330, full, with three Tamil commentaries); Naladiyar
  398/400; Nanmanikkadigai 106/104; Inna Narpathu 39/40; Iniyavai Narpathu 40; Kar Narpathu 40;
  Kalavazhi Narpathu 40/41; Ainthinai Aimpathu 50; Thinaimozhi Aimpathu 49/50; Ainthinai
  Ezhupathu 65/70; Thinaimalai Nurraimpathu 152/153; Thirikadugam 100; Acharakkovai 97/100;
  Pazhamozhi Nanuru 385/400; Sirupanchamoolam 97/100; Muthumozhikkanchi 102/100; Elathi 79/80;
  Kainnilai 60. Several "on site" figures exceed the canonical count because the edition's
  units differ from the tradition's.
- **Epics and later kavyas**: Silappathikaram (5,327 lines against the canonical 5,270),
  Manimekalai 4,730/4,861 lines, Civaka Cintamani 2,124/3,145, Valayapathi 69/72, Kundalakesi
  18/19, Soolamani 1,567/2,131, Neelakesi 899/894, Naga Kumara Kaviyam 169/1,114, Udayana Kumara
  Kaviyam 338/367, Yasodhara Kaviyam 741/330 verses.
- **Knowledge graph** (`knowledge/index_with_images.html`): 1,483 entity records, 8,082
  verse mentions over 2,268 of the 2,714 Sangam units. See section 4.
- **Other pages**: a Sangam primer (`sangam.html`), five landscape pages (`thinai_detail.html`,
  with Tolkappiyam's first things and native things per landscape), a poets index built from the
  colophons (656 name spellings), the research page, and games (Thinai Quest, a Kural quiz, a
  loanword game, trivia).

### Data formats

Every data file is a JavaScript assignment (`var name = {...}`) whose body is strict JSON, so it
parses with `json.JSONDecoder().raw_decode` after the `=`. The main records are:

- **Sangam verse** (`data/verses/*.js` and the merged `data/all_verses_data.js`): `verse_id`
  (`Akananuru:56`), `text_name`, `verse_number`, `thinai` (lower-case romanized, or empty),
  `verse_text` (lines separated by `\n`), `translation`, `poet` (romanized), `turai` (an English
  speech situation for akam; a romanized thurai name for puram), `patron` (puram only), and for
  idyll segments `lines` and `heading`. A `source` field marks the few lines whose Tamil comes
  from Project Madurai.
- **Entity** (`data/entity_metadata.js`): keyed by the Tamil word as it appears in a verse, with
  `tamil1`/`tamil2` (modern Tamil glosses), `english1`/`english2` (English glosses, sometimes a
  Latin binomial), `category` (Flora, Fauna, Food, Occupations, Arts), `image`, `imageCredit`,
  `imagePage`, and `canonical` (the root form) on 560 of the 1,483 records.
- **Mention** (`data/entities_verse.js`): keyed by verse id, a list of `{word, category, line}`.
  `line: 0` means the source put the entity in the verse but the word could not be found.
- **Texts from Project Madurai** (`data/texts/*.js`): `verses` with `n`, `seq`, `text`, optional
  `lines`, `part`, and a `source` block naming the pmuni file and a `translations` block.

### Licences and terms

The site states no licence for its own data, code or prose. The footer says the Tamil texts are
public domain and that translations are credited to their translators. The research page calls
the translations public-domain, but that does not hold for the Sangam translations, which are
Vaidehi Herbert's modern work. Translators and the rights stated for each:

| Texts | Translator | Rights as stated on the site | Our reading |
|---|---|---|---|
| All Sangam anthologies and idylls | Vaidehi Herbert (sangamtranslationsbyvaidehi.com), credited in the footer and on the primer page, not per verse | none stated per verse | in copyright; do not copy |
| Thirukkural | G. U. Pope, 1886 (verse); W. H. Drew and John Lazarus, 1840 and 1885 (prose) | public domain | public domain |
| Thirukkural Tamil commentaries | Mu. Varadarajan, Salamon Pappaiya, Mu. Karunanidhi | not stated | modern, in copyright |
| Naladiyar | credited to "G. U. Pope and F. W. Ellis, 1893" | public domain | Pope 1893 is public domain; the Ellis credit is doubtful |
| Silappathikaram | V. R. Ramachandra Dikshitar, 1939, uncorrected OCR, per canto | public domain in India | public domain in India only |
| Other Project Madurai texts | no translation | | Tamil is public domain |
| Entity images | Wikimedia Commons with per-image credit and licence (203 credited: CC BY-SA 3.0 68, CC BY-SA 4.0 53, public domain 26, CC BY 4.0 13, others); 94 more images have no credit; landscape pages use Unsplash photos | as credited | images are not copied to the repo |

The primer also cites A. K. Ramanujan (1985), George L. Hart (1975) and Kamil Zvelebil (1973) as
reading, but the site does not reproduce their translations.

## 2. The dissertation (ThinaiKG)

Simon Peter J, M.Tech in AI and ML, BITS Pilani WILP. It ran over 16 weeks (October 2025 to
January 2026), had its viva in February 2026, and was compiled as a 21-page report in September
2026.

**Task.** Assign each akam poem one of the five landscapes using only the cues a reader uses.

**Corpus.** 1,891 verses from Project Madurai: Ainkurunuru 498, Kuruntokai 401, Natrinai 399,
Akananuru 396, Kalittokai 149, and Kurinjippattu and Mullaippattu split into 27 and 21 pieces.
Commentary and metadata were stripped and nothing was lemmatised. The class mix is palai 27.9%,
kurinji 27.0%, neytal 18.1%, marutham 13.6% and mullai 13.4%. A 500-verse ground truth was hand
verified, 100 per landscape, and a 176-term seed lexicon was compiled from scholarly sources.

**Method.**
1. Baseline: TF-IDF over 10,000 word 1-3-grams, SMOTE oversampling and an RBF SVM. It reached
   macro F1 0.52, with kurinji at 0.32. Dropping marutham did not help.
2. Keep only karupporul words in each verse (flora, fauna, land, occupations, food) and train five
   one-vs-rest linear SVMs on TF-IDF of those tokens. With 145 curated entities, F1 was 0.68.
3. Grow the lexicon by self-training. On unlabelled verses predicted with confidence above 0.95,
   score each term by SVM coefficient times summed TF-IDF, and propose terms with a coefficient
   above 0.7 seen at least three times. A reviewer accepts or rejects each one. Over 16 lexicon
   versions this reached 417 entities with 83% of proposals accepted. A strict filter cut a
   1,000-term set to 237 with under 1% loss.
4. Build a four-class OWL ontology (Thinai, Verse, Entity, Category) with APPEARS_IN,
   BELONGS_TO, HAS_CATEGORY and a derived CHARACTERIZES (entity to landscape). The graph has
   2,313 nodes and 21,950 edges, exported as OWL, GraphML and JSON. An entity entered the graph
   only when a high-confidence classification and a significant weight agreed.

**Results.** On the 500-verse set: accuracy 82.3%, macro precision 0.83, recall 0.81, F1 0.82.
Per class F1: neytal 0.87, kurinji 0.84, mullai 0.80, marutham 0.80, palai 0.79 (precision 0.74,
recall 0.85). IndicBERT v2 fine-tuned four ways peaked at 58.6% with KG features, and a frozen
encoder with a linear head reached 53.6%.

**Errors, as the report explains them.** The seashore has the most distinctive vocabulary.
Marutham and mullai share farmland and pasture words. Palai draws in false positives because its
images are borrowed from the other landscapes. Versions 5 to 9 fell to about 78% after
over-aggressive cleaning.

**Limitations it admits.** Akam only, with puram and later works out of scope. Linear boundaries
and a curated dictionary miss interactions. It depends on one expert reviewer. The graph supports
traversal but not inference.

**Limitations it does not discuss**, which matter for us:
- **Label leakage and circularity.** The report says the same balanced 500 verses served for
  training and evaluation, and it describes no held-out split or cross-validation. The 16 lexicon
  versions were tuned against that set. The lexicon grew from the model's own confident
  predictions, so it drifts toward what the model already believes. The 83% acceptance is
  reviewer approval, not accuracy, and the 82.3% should be read as an optimistic upper bound.
- **The labels were already known.** Every akam poem carries its thinai in the colophon, and in
  Akananuru, Ainkurunuru and Kalittokai the arrangement itself fixes it. A rule on the poem
  number scores 100% on Akananuru. The classifier's real value is its cue analysis and its
  disagreements with the colophon. It is not useful for labelling.
- **Presence is not role.** A flower in a garland, a flower in a simile, a flower named as absent
  and a flower that sets the scene all count the same. Tolkappiyam itself allows native things of
  one land to appear in a poem of another (திணை மயக்கம்; அகத்திணையியல் 14 and 21 say that flowers
  and birds that come into another land take on that land's import). It also makes the situation of love
  (உரிப்பொருள்), not the native things, decide the thinai: palai has no land of its own and is
  defined by separation. The weak palai precision is what that theory predicts.
- No inter-annotator agreement is reported for the ground truth or the entity review, no
  confusion matrix is published, and the BERT accuracy is set against the baseline's F1.
- The entity unit is a surface word-form. It keeps the signal, but it multiplies entities: the
  site's 1,483 records hold many inflections of one word.

**What it got right about reading akam poems.**
- It treats the landscape as an inference from named things, as a trained reader makes it, not as
  a topic word.
- A small core of concrete nouns (trees, flowers, birds, beasts, trades, food) carries most of the
  signal. Domain theory beat bulk n-grams by 30 points of F1.
- It does not lemmatise. Inflected poetic forms are evidence, so keep the form found in the line.
- It stays interpretable. Every decision traces to named entities, every entity to verses, and
  (on the site) every mention to a line.
- It keeps a human in the loop and versions every lexicon change. That is the right discipline for
  a curated vocabulary.
- Its error profile follows the grammar: neytal is easiest, and palai is hardest.

## 3. Ideas to adopt in our marking

1. **Karupporul as a structured field, per verse.** For each native thing record the Tamil form
   as it stands in the line, its stem, the line number and its class. Use Tolkappiyam's own list
   of native things (அகத்திணையியல் 20: deity, food, beast, tree, bird, drum, occupation, lute
   and music, and others) rather than the site's five categories. Keep the first things (முதல்:
   land, season, hour) as a separate field. The site's scheme has no deity, drum, water or
   settlement class. It also files யாழ் and பறை under Arts and mixes trades with tribes and with
   people (bards, dancers) under Occupations.
2. **The role of each native thing in the poem**, which the site cannot express:
   `setting`, `ullurai` (a nature scene that mirrors the human one), `iraicchi` (a detail whose
   import goes beyond the stated sense), `simile` (with its marker, e.g. போல, அன்ன), `ornament`
   (a garland), `gift_or_food`, `place_name`, and `negated` (the dried spring, the withered tree).
   This is where the meaning is, and it is what the Tholkappiyam pilot already tags.
3. **Thinai and thurai as tags with a source.** Store the colophon's thinai and thurai verbatim as
   facts with their source. Store our own inferred thinai separately, with the native things and
   the situation that support it, and a `mixed` flag when native things of another landscape
   appear. Never overwrite a colophon label with an inference.
4. **The akam thurai as a speech situation.** Record speaker, addressee, overhearer (சிறைப்புறம்)
   and occasion (stage of களவு or கற்பு, departure, delay, the courtesan) as fields drawn from the
   Tamil colophon. `facts.jsonl` gives the site's speaker and addressee in this coded form for
   Akananuru.
5. **Puram labels.** Use the puram thinai (வெட்சி to பாடாண், பொதுவியல், கைக்கிளை,
   பெருந்திணை) and thurai from our own Tamil colophons, which the site lacks. Add entity types
   the akam scheme does not need: king or chief, patron, poet, battle, town, river, hill, and the
   hero-stone.
6. **Entity types for our graph**: `karu` (with the Tolkappiyam class), `place`, `person` (poet,
   patron, king), `deity`, `artefact` (drum, lute, weapon, chariot), `practice` (rite, custom),
   plus the landscape and situation nodes. Each entity is linked to verses through a mention that
   carries the form, the line and the role.
7. **Show uncertainty and ambiguity on the entity**: words with two common senses (மா, ஏறு,
   கலை, அன்ன, இல, மை) need a sense chosen per verse, never one fixed gloss for the word.

## 4. Where the site disagrees with or adds to our data

### Purananuru text: site against `kg/core/purananuru.jsonl`

Both have 398 poems with the same numbering (267 and 268 lost). Compared on Tamil letters only,
ignoring spacing and punctuation, 35 poems are identical (one of them, 55, only breaks its lines
differently, so it also appears in the table below), 304 differ only inside lines, and 59 differ
in their lines.

- **Our text drops the vowel sign ொ in the case ending -ஒடு**, writing யடு and ளடு for யொடு
  and ளொடு: 77 cases of யடு and 7 of ளடு. This is a known Project Madurai encoding fault and the
  most frequent real defect in our text. A rule-based repair is safe.
- **37 of our poems contain stray non-Tamil glyphs** (¨ ¡ ¦ _ and the like): 24, 56, 69, 100, 152,
  154, 155, 159, 160, 161, 165, 198, 201, 202, 203, 208, 210, 211, 212, 214, 283, 285, 289, 290,
  291, 298, 299, 310, 314, 315, 316, 318, 321, 343, 346, 352, 373. The site has none.
- Most other in-line differences are editorial conventions, not variants. Our text keeps sandhi
  (-ிற், -ாற், -ுங்), and the site splits words and restores the base form (-ின், -ால், -ும்),
  writes the vowel lengthening of a long syllable out in full (ுஉ), and separates compounds
  (புஇல, ைஆய). Treat these as one reading in two spellings.
- **Line-level differences**: in 29 poems the site lacks our opening line or lines, and in 24 we
  lack lines the site has. A few rows are the same text broken into lines differently
  (55, 58, 230, 366, 377, 383, 384); check those by eye before treating them as losses.

| Poem | Our lines | Site lines | Difference |
|---|---|---|---|
| 9 | 11 | 10 | site lacks our opening line(s) 1 |
| 17 | 40 | 39 | site lacks our opening line(s) 1 |
| 28 | 17 | 15 | site lacks our opening line(s) 1,2 |
| 30 | 15 | 14 | site lacks our line(s) 2 |
| 36 | 13 | 11 | site lacks our opening line(s) 1,2 |
| 48 | 8 | 9 | we lack site line(s) 6 |
| 49 | 6 | 5 | site lacks our opening line(s) 1 |
| 55 | 23 | 21 | site lacks our line(s) 7,8,9,10; we lack site line(s) 7,8 (line breaks differ) |
| 57 | 11 | 10 | site lacks our opening line(s) 1 |
| 58 | 30 | 31 | site lacks our line(s) 1,26; we lack site line(s) 25,26,27 |
| 64 | 7 | 6 | site lacks our opening line(s) 1 |
| 72 | 18 | 17 | site lacks our opening line(s) 1 |
| 74 | 7 | 6 | site lacks our opening line(s) 1 |
| 77 | 10 | 13 | we lack site line(s) 8,10,12 |
| 83 | 6 | 7 | we lack site line(s) 1 |
| 86 | 5 | 6 | we lack site line(s) 2 |
| 88 | 5 | 6 | we lack site line(s) 5 |
| 95 | 9 | 8 | site lacks our opening line(s) 1 |
| 99 | 14 | 13 | site lacks our opening line(s) 1 |
| 100 | 11 | 9 | site lacks our opening line(s) 1,2 |
| 101 | 10 | 9 | site lacks our opening line(s) 1 |
| 113 | 9 | 8 | site lacks our opening line(s) 1 |
| 116 | 18 | 19 | we lack site line(s) 10 |
| 117 | 10 | 9 | site lacks our opening line(s) 1 |
| 122 | 10 | 9 | site lacks our opening line(s) 1 |
| 124 | 5 | 3 | site lacks our opening line(s) 1,2 |
| 126 | 22 | 23 | site lacks our opening line(s) 1; we lack site line(s) 1,2 |
| 142 | 6 | 5 | site lacks our opening line(s) 1 |
| 160 | 28 | 30 | we lack site line(s) 8,17 |
| 163 | 9 | 8 | site lacks our opening line(s) 1 |
| 183 | 10 | 9 | site lacks our opening line(s) 1 |
| 187 | 4 | 2 | site lacks our opening line(s) 1,2 |
| 209 | 18 | 19 | we lack site line(s) 17 |
| 218 | 7 | 6 | site lacks our opening line(s) 1 |
| 223 | 6 | 5 | site lacks our opening line(s) 1 |
| 226 | 6 | 5 | site lacks our opening line(s) 1 |
| 230 | 15 | 16 | site lacks our line(s) 13; we lack site line(s) 13,14 |
| 235 | 19 | 20 | we lack site line(s) 11 |
| 275 | 9 | 8 | site lacks our opening line(s) 1 |
| 283 | 13 | 13 | line 12 read differently on each side |
| 296 | 5 | 4 | site lacks our opening line(s) 1 |
| 306 | 7 | 6 | site lacks our opening line(s) 1 |
| 325 | 13 | 15 | we lack site line(s) 14,15 |
| 338 | 12 | 11 | site lacks our opening line(s) 1 |
| 355 | 3 | 5 | we lack site line(s) 4,5 (the site has two more lines before the gap) |
| 357 | 9 | 9 | line 6 read differently on each side |
| 361 | 22 | 23 | we lack site line(s) 23 |
| 366 | 22 | 23 | site lacks our line(s) 12,21; we lack site line(s) 12,21,22 |
| 370 | 27 | 27 | lines 1,2 read differently on each side |
| 371 | 25 | 27 | we lack site line(s) 1,2 (our poem starts at its third line) |
| 373 | 39 | 39 | lines 13,18,22 read differently on each side |
| 374 | 18 | 18 | line 10 read differently on each side |
| 377 | 29 | 30 | site lacks our line(s) 22; we lack site line(s) 10,23 |
| 378 | 23 | 24 | we lack site line(s) 17 |
| 379 | 18 | 18 | lines 14,15 read differently on each side |
| 382 | 22 | 23 | we lack site line(s) 11 |
| 383 | 23 | 25 | site lacks our line(s) 19; we lack site line(s) 6,15,21 |
| 384 | 22 | 24 | site lacks our line(s) 9; we lack site line(s) 5,10,22 |
| 386 | 24 | 25 | we lack site line(s) 21 |
| 393 | 25 | 25 | line 22 read differently on each side |

Our lines are counted without blank and dotted gap lines. Where we lack lines, check
Duraisamy Pillai's edition (already used in `kg/core/purananuru.jsonl` and
`kg/core/sangam_text_flags.jsonl`) before adding anything. The site is not an edition we should
copy from.

### Purananuru colophons

- **Thurai**: 370 of 389 comparable poems agree once the site's romanization is mapped back to
  Tamil. Two of the differences are errors in our data: poem 5 reads வெவியறிவுறூஉ for
  செவியறிவுறூஉ, and poem 336 reads பாற் பாற் காஞ்சி where the site and the usual reading have
  மகட்பாற் காஞ்சி. Real disagreements to check: 149 (we have பரிசில், the site Iyan Mozhi), 229
  (we have கையறுநிலை, the site a different label), 370 (we have மறக்களவழி, the site a
  different label), and 159, 160, 198 (we have பரிசில் கடாநிலை, the site Parisil). The site's
  thurai field for 244 is a note, not a label.
- **Poets**: 15 (we have கபிலர், with Kapilar's patron for poem 14; the site has Nettimaiyar, the
  usual attribution, so our colophon looks shifted from 14); 144 and 145 (we have கபிலர், the
  site Paranar; our own 145 notes that some call it Paranar's). Our poet field for 60 has verse
  words in it, and for 78 it holds the patron. The site's own slips: the poet field for 20, 21,
  25 and 205 carries the patron; the field for 1 carries a dating note; the field for 112 starts
  with a stray "s:".
- **Thinai**: the site gives no puram thinai at all, so our colophon thinai (394 poems) adds to
  it.

### Akananuru

- The site's thinai matches our colophon (`kg/core/akananuru.jsonl`) on all 400 poems, and the
  numbering rule on all 400. The site has no invocation; ours has it as poem 0.
- Speaker labels: a rough parse of our Tamil thurai agrees with the site's speaker on about 92%
  of the poems it could score (336 of 366). Most of the rest are parser misses. Two are worth
  reading: 72 (ours: the heroine speaks to the friend while the hero overhears; the site: the
  friend to the heroine) and 214 (ours: the heroine to her heart at the war camp; the site, more
  plausibly given the camp, the hero).
- The site keeps only one of the alternative thurai readings that our colophons number (1), (2),
  (3), as in poem 38.

### What the site adds

- 8,082 entity mentions, 4,216 of them in our three books, most with line numbers. That is a
  ready recall check for our native-thing tags (section 6).
- English speech-situation labels for all akam anthologies, and Natrinai and Kuruntokai
  colophon thinai, which we have not ingested yet.
- A poets index across six anthologies (656 spellings), useful for merging poet names.

### Errors in the site's knowledge graph

Measured on the 8,082 mentions: 5,988 are the exact word in the stated line; 1,053 are the start
of a longer word (usually a case form, which is fine); 447 are found only inside a longer word;
228 are not on the stated line; and 366 are unlocated (`line: 0`). Specific faults:

- **Wrong sense fixed on an ambiguous word.** மா (162 mentions) is typed Food and glossed mango,
  but the located uses are mostly the beast or horse (மா, மாவே, கடுமா, வயமா), and 7 sit inside
  மாலை (evening). ஏறு (53) is glossed male hawk, but is mostly the bull. கலை (43) is glossed male
  monkey while its root is given as கலைமான் (stag).
- **Function words taken as entities**: அன்ன (the particle of comparison) as swan; இல (not) as
  the silk-cotton tree; and one- and two-letter fragments (அர, இய, இர, சே, கோ, ஆ) matched inside
  unrelated words, for example ஆ in ஆயமொடு and கலை in போகலை.
- **Roots that run backwards**: some `canonical` values are inflected forms. வண்டு points to
  வண்டினும், and கரும்பு's variants all point to கரும்பினும்.
- **Category inconsistency**: யாழ் and பறை are Arts, while the drums and lutes of Tolkappiyam's
  list are native things. There is no deity or land class, although the report lists land as a
  category.
- **Coverage is uneven**: one or two mentions per poem in Ainkurunuru and Kuruntokai, against
  4.5 in Akananuru, and only 11 of 18 Mullaippattu segments have any. An absent mention is not
  evidence of an absent thing.
- **Landscape tables**: the palai flora on the summary card includes cactus, a New World plant
  unknown to the poems. The kurinji and marutham sample verses are real (Kuruntokai 40,
  Ainkurunuru 1); I could not find the mullai, neytal and palai samples in the site's corpus.
- The verse counts in the report (Akananuru 396, Kalittokai 149, Kurinjippattu 27, Mullaippattu
  21 pieces) do not match the current site (400, 150, 28, 18), so the published graph is not the
  graph that was evaluated.

`kg/sangam/site_kg.jsonl` carries a `site_flags` list on the 188 entity records where these
faults apply.

## 5. Tolkappiyam's theory of meaning: இறைச்சி and உள்ளுறை

For the parallel pilot (`kg/themes/tholkappiyam_pilot/`):

- The site names both devices on its primer page, with a one-line gloss each, but tags neither
  on any verse. Its graph records only that a native thing occurs. It never records what the
  thing does in the poem.
- Tolkappiyam builds both devices out of native things. உள்ளுறை takes any native thing except
  the deity as its vehicle (அகத்திணையியல் 50). இறைச்சி stands outside the situation of love
  itself (பொருளியல் 33), a further meaning can be born from it for readers who know how
  (பொருளியல் 34), and சொல்லதிகாரம் பெயரியல் 42 notes that native names used for இறைச்சி
  point to the land, not to a person. So the site's
  located mentions are the right candidate list for the carriers of both. A pilot tagger can
  start from the mentions in a verse and decide, for each one, whether it is setting, உள்ளுறை,
  இறைச்சி, explicit simile or mere ornament.
- The site's noise shows exactly where carrier detection fails: the comparison particle அன்ன
  tagged as a bird; ambiguous nouns (மா, ஏறு, கலை) whose sense changes what the scene mirrors.
  These are good test items for the pilot's `comparisons` and `layers` fields.
- The dissertation's palai errors are a uri-over-karu effect. When separation is the situation,
  the native things of any land can be present, so a verse can be correctly palai with kurinji
  things in it. Our marks should keep "what the things say" (karu) apart from "what the situation
  is" (uri). The pilot already has both fields, and its `mutal.negated` covers the withered land.
- The speaker field matters for இறைச்சி: the same scene reads differently from the friend and
  from the heroine. Join the pilot's layers to the colophon's speaker, which the site gives in
  English and our Tamil colophons give in full.

## 6. Validation plan

**Kinds of label on the site, and what each is worth as ground truth**

| Label | Where | Kind | Worth |
|---|---|---|---|
| Thinai, Akananuru | `thinai` | traditional, fixed by poem number; 400/400 match the rule and our colophon | the tradition's reading; exact |
| Thinai, Ainkurunuru and Kalittokai | `thinai` | traditional, by the anthology's sections (Kalittokai poem 1, the invocation, is labelled palai) | exact except the invocation |
| Thinai, Natrinai and Kuruntokai | `thinai` | colophon, through the translated source | good; spot-check against Project Madurai when those books are ingested |
| Thinai, Kurinjippattu and Mullaippattu | `thinai` | the whole poem's traditional label copied to every segment | poem-level only |
| Thinai, puram and the other idylls | none | | none |
| Thurai, akam | `turai` | the colophon rendered in English by the translator | good for speaker and addressee; one reading of several |
| Thurai, puram | `turai` | the colophon's name romanized | good; about 5% differ from ours |
| Poet, patron | `poet`, `patron` | colophon, romanized | good, with the slips listed above |
| Classifier thinai | not published | the dissertation's predictions are not in the site's data; the landscape shown on each verse is the traditional one | none available |
| Entity to landscape (CHARACTERIZES) | not published | the page recomputes it from the verse labels | derived, not evidence |
| Entity list, categories, glosses, images | `entity_metadata.js` | hand-curated: began as the classifier-proposed, reviewer-approved lexicon (417); now 1,483 records. The footer credits sangamliteraturefacts.wordpress.com for the entities, and some glosses carry verse references. | curated but noisy; see flags |
| Entity to verse mentions | `entities_verse.js` | a curated list placed in verses by script, then line numbers fixed by script | high recall for concrete nouns in Akananuru and Natrinai, uneven elsewhere; precision weak on short words |
| First and native things per landscape | `thinai_detail.html` | hand-curated textbook table | reference only |

**Coverage per book**: see the tables in section 1. For our three books the site gives
Akananuru 1,804 mentions (395 of 400 poems), Purananuru 1,218 (347 of 398) and the Pattupattu
1,194 over 271 of 366 segments.

**Checks to run after each marking batch** (`scripts/sangam_validate.py`):

1. **Native things: precision and recall against the site's mentions**, per verse, by default
   leaving out unlocated mentions and one- and two-letter words. Read the result this way:
   - *Low recall* on a type (for example occupations, arts) shows either that we are not tagging
     that class or that the site counts people and instruments we treat differently. Decide the
     policy once and record it.
   - *Site words we miss*, verse by verse: each is either a real omission (fix it) or a site false
     positive (check `site_flags`; these should become a stop list).
   - *Words only we tag*: either a site coverage gap (likely in Ainkurunuru, Kuruntokai,
     Mullaippattu), a tag of ours that is not a native thing, or a lemma our matcher misses.
   - Recall below about 0.7 on Akananuru or Natrinai, where the site is dense, is a signal to
     re-read our batch. Below that on Ainkurunuru or Kuruntokai, it is not.
2. **Thinai: ours against the colophon and against the site**, with a confusion matrix and kappa.
   - Ours = colophon = site: nothing to do.
   - Ours = colophon ≠ site: a site error. None was found for Akananuru; for the anthologies
     ingested later, record it.
   - Ours ≠ colophon: either our inference followed native things of another land (expected for
     palai and for mixed poems; record `mixed` and keep the colophon), or the colophon gives
     alternatives (keep both), or our colophon parse is wrong (fix the text).
   - Off-diagonal cells concentrated in palai mean we are reading karu over uri. Cells between
     marutham and neytal or mullai often mean the shared water and pasture words.
3. **Speaker and addressee** (Akananuru): compare our parsed Tamil thurai with
   `thurai_speech` in `facts.jsonl`. Differences are either our parse, an alternative reading in
   our colophon, or one of the slips listed in section 4.
4. **Text**: before marking a Purananuru poem, check it against the line-difference table above
   and `kg/core/sangam_text_flags.jsonl`.

There are no classifier labels to compare against. If we want an independent machine check, the
dissertation's method is easy to reproduce on our own marks: a linear model on our native-thing
tags, cross-validated, with its disagreements with the colophon sent for reading.

## 7. Sites and datasets the site cites that we should look at

- **Project Madurai** (projectmadurai.org): the dissertation's corpus source. It names
  pmuni0028 as an example; the site's texts name pmuni0016, 0024, 0025, 0027, 0029, 0035, 0036,
  0046, 0047, 0048, 0051, 0056, 0062, 0100, 0111, 0141, 0507, 0508, 0538, 0597, 0601, 0602,
  0664, 0670 and 0672. We already mirror it.
- **sangamliteraturefacts.wordpress.com**: credited in the footer for the knowledge-graph
  entities. Probably per-verse flora and fauna lists with verse references, which would be the
  real source of the mention list. Worth reading for its identifications. Check its terms before
  using anything beyond facts.
- **Vaidehi Herbert, sangamtranslationsbyvaidehi.com**: the source of the site's Sangam text,
  colophon renderings and translations. Useful to check readings; the translations are in
  copyright.
- **Tamil Virtual Academy** (tamilvu.org): cited as a source; it has the standard editions with
  commentaries, a good arbiter for the Purananuru line differences.
- **github.com/tk120404/thirukkural**: the Kural JSON the site used, with Pope, Drew-Lazarus and
  three commentaries. The site found 26 couplets where the prose field held Pope's verse instead,
  a warning if we ever take Kural data from it.
- **IndicBERT v2** (AI4Bharat): the transformer the dissertation tried. It is only relevant if we
  ever train a model.
- From the report's references: Sandeep et al., word segmentation of ancient Tamil text (ICON
  2025), which may help sandhi splitting for our matcher; Ramachandran, a survey of the thinai
  system (Tamil Studies Journal, 2018); Li et al. on ontologies of traditional ecological
  knowledge (Semantic Web, 2020); and CIDOC-CRM, if the graph is ever exported for heritage use.

## Files

- `kg/sangam/facts.jsonl`: 1,164 records, all public-domain facts. Akananuru has 400 poems and
  1,804 native-thing mentions, Purananuru 398 and 1,218, and the Pattupattu 366 site segments and
  1,194. The segments by idyll are Maduraikkanchi 65, Sirupanatruppadai 51, Malaipadukadam 44,
  Perumpanatruppadai 41, Pattinappalai 40, Thirumurugatruppadai 32, Kurinjippattu 28,
  Nedunalvadai 27, Porunaratruppadai 20 and Mullaippattu 18. Each record has the book, number
  (and line span for segments), poet, patron, thinai with its provenance, the thurai
  (Purananuru: the romanized name; Akananuru: coded speaker and addressee, not the English
  wording), the native things with type, line and form, and any `site_flags`. No Tamil verse
  text, translation or heading is copied.
- `kg/sangam/site_kg.jsonl`: 1,483 entity records with id, type, Tamil word, root, short
  identification glosses, Tamil glosses and every verse mention (book, number, line, form).
  There are no images and no prose.
- `scripts/sangam_validate.py`: scores our marks against the two files above and our colophons.
