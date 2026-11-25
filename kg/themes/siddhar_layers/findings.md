# Siddhar reading layers: pilot findings

Pilot of `docs/siddhar-layers-brief.md`, 2026-11-25. Validate with
`python3 -I scripts/siddhar_layers_check.py`. Nothing here has been graded yet: the 41 proposed
links are in a blind packet (`grading/packet.md`, with 6 calibration links of known grade) and the
39 lexicon entries in `grading/lexicon_packet.md`. Every judgment below about the new links is the
proposer's, and should be read again when the grades come back.

## The sample

Chapters were drawn with `random.Random(11).shuffle(range(1, 143))`, taking each chapter in that
order unless its poet was already chosen, until six poets were in:

| chapter | poet | work | verses |
|---|---|---|---|
| 15 | பட்டினத்தார் | இரண்டாவது கோயிற்றிருவகவல் | 301 (one long agaval) |
| 101 | கொங்கணச் சித்தர் | வாலைக் கும்மி (5/5) | 1964-1979 |
| 72 | சிவவாக்கியர் | சிவவாக்கியம் (18/21) | 1389-1413 |
| 87 | அகப்பேய்ச் சித்தர் | பாடல்கள் (1/4) | 1642-1666 |
| 96 | இடைக்காட்டுச் சித்தர் | பாடல்கள் (6/6) | 1857-1863 |
| 118 | நொண்டிச் சித்தர் | நொண்டிச் சிந்து (1/2) | 2293-2317 |

99 verses, 214 layer readings, 41 links (25 new, 14 kept from the old marking with their old
notes, 2 renoted), and 57 old graded links reviewed.

## Counts by layer

| layer | verses | high / med / low | links naming it | of which depend on it alone | readings applying a cipher key |
|---|---|---|---|---|---|
| literal | 99 | 40 / 37 / 22 | 17 | 9 | 2 |
| breath | 40 | 3 / 20 / 17 | 9 | 2 | 22 |
| alchemy | 6 | 2 / 1 / 3 | 4 | 0 | 4 |
| consciousness | 51 | 16 / 31 / 4 | 6 | 4 | 9 |
| social | 18 | 10 / 7 / 1 | 5 | 0 | 0 |

Link types: 19 agrees, 9 same_image, 4 shared_key, 4 tension, 3 qualifies, 1 develops,
1 parallel_domain. Targets: 18 Tirumanthiram, 14 other pilot verses, 5 Thiruppugazh, 4 Kural, 0
Naladiyar. Link confidence: 12 high, 28 med, 1 low.

The breath layer is the least certain (17 of 40 readings low) and is where the keys live (22 of
the 37 keyed readings). The social layer is the most certain and never needs a key. Breath is
often not a cipher at all: Sivavakkiyar's chapter names மூலநாடி, வாசி, அனல், அமுதம், and Nondi
names மூலாதாரம், மணிபூரகம், விசுத்தி, நாசிமுனை; on those verses the breath reading is as plain as
the literal one, and a link on it needs no key.

## 1. How many links depend on only one layer

**15 of 41** name no other layer on which they also hold. They split into two very different
groups:

- **9 rest on the literal layer alone.** These are the robust ones: the plain words carry them and
  no interpretive layer is needed (1400 and Tirumanthiram 1507 on the path-fruit scheme, 1409 and
  Thiruppugazh 1039 on the unfound root and crown, 1655 and Kural 1 on அ as first, the three
  tensions 1658/2184, 1648/2313 and the qualifier 1666/1400). One of them, 2317 and 301, is a
  shared-key link on the literal layer: it needs the nine-gates key to read 301's ஒன்பது.
- **6 rest on a single non-literal layer**, and these are the links a reader should distrust first:
  three shared-key links (1390/1656 on the letter சி, low; 1406/1857 on the upper door; 2307/1651
  on the three lights) and three consciousness links (1859 and Tirumanthiram 1681 on the mirror as
  the mind; 2310/1863, silence as effect against silence as discipline; 2309/1862, the inner
  Shakti-Siva pair as final or as construct).

The other 26 hold on two layers, almost always the named layer plus literal. That is the main
practical result: **when a breath, alchemy or social link also holds on the literal layer, the
layer label is a description, not a dependency.** Under the flat marking such links and the
single-layer cipher links looked alike to graders; here they are separable by one field. If the
grades follow the earlier pattern, the 6 single-non-literal links should grade lower than the 26;
that is the prediction this pilot can test.

## 2. Old links in these chapters that now look like cipher artefacts

Of the 57 graded links that touch the pilot verses, the review gives: 28 hold on the literal
words, 4 hold on a non-literal layer the Tamil supports, 13 are generic, 9 misread a verse, 1 is a
stock attack, and **2 are cipher artefacts**:

- **1656 and Tirumanthiram 885 (weak).** Agappei says outright that ம is maya and impurity; the
  link needed Tirumular's மாவெழுத்து to be the letter ம, a gloss his Tamil does not fix. Tirumanthiram
  975 states the same key in words (மகார மலமாய், சிகாரம் சிவமாய்), so the pair is replaced by a
  literal link that needs no key.
- **2317 and Tirumanthiram 658 (weak).** Nondi's nine gates (ஒன்பது வாசல், openings, shut) were
  joined to Tirumular's nine nadis (channels, stilled): two nines that are different things. A shared
  number is not a shared key. Tirumanthiram 152, where the nine gates are the same nine (shut at
  death), replaces it, and the yogi doing voluntarily what death does is what the pair teaches.

Two more were **partly** artefacts and are renoted rather than dropped: 1404 and Tirumanthiram
1958 (the ascent-then-nectar sequence is in both texts, but the old note matched Sivavakkiyar's
circle and three bolts to Tirumular's throat and moon, which only a key does), and 1859 and
Tirumanthiram 1681 (the old note stated 'the mirror is the mind' as Idaikkadar's own words; it is
the consciousness layer's reading of them).

The layering also shows which **cipher readings not to link on**, because the carrying words do
not fix the key: எட்டும் எட்டும் எட்டு (1389) and எட்டெட்டு (1398) as breath counts, which would
have joined them to 2317's எட்டுத் தலங்கள் on the number alone; விண்நாடி (1858) as the sky-channel;
நடுவறிந்து (1409) as the central channel; the sun (பரிதி) of 1408, which is a simile there and
not the right breath; and ரசபானம் (2309) as mercury. All are recorded as low-confidence layer
readings and none carries a link.

The **stock attack** problem is smaller than the overall numbers suggested in these chapters: only
1966 and 749 is a pure stock attack. The social layer is high-confidence on 10 verses, and the
social links proposed (1390/2071, 1402/1978, 1663/1530, 1965/2045, 1966/Kural 276) each name a
specific shared point (where the sects look, the foot seen within, teaching as a living). Whether
graders agree that is enough is open.

## 3. What the medicine, consciousness and body layers add

**Medicine and alchemy.** The flat marks had no way to say that a verse argues from medical
theory. Pattinathar's body-catalogue (301) is partly built from the three humours (வாதபித்தங்கோழை
குடிபுகுஞ் சீறூர், a village where wind, bile and phlegm lodge), which joins it to the Kural's chapter
on medicine (941: the three counted by the learned, beginning with wind) and to Thiruppugazh 894,
which shares four specific features (the humours, the worms, Brahma as the body's maker, the nine
gates) and not just the genre. Konganar's 1968 makes medicine's promise (long life, no diabetes)
for the goddess's name, as Tirumanthiram 2709 makes the five syllables the alchemist's pill. And
the alchemy layer gives the pilot's one cross-book tension about the body: Nondi's throat centre
'so as not to die' (2308) against Arunagirinathar's foolish yogi who holds the breath and eats herbs
to keep the flesh (Thiruppugazh 355), with Tirumanthiram 581 on Nondi's side. Every alchemy
reading is a claim; no verse in the sample gives a preparation, and none is restated.

**Consciousness.** The layer separates claims that the flat readings ran together: the reflexive
formula for knowing (1399 உணர்வதற்கு உணர்வு, 1858 மெய்யே மெய்யில்) across two poets; silence as a
discipline (Idaikkadar 1863) against silence as the effect of seeing (Nondi 2310); and the inner
Shakti-Siva pair as the goal (Idaikkadar 1862) against the same pair seen and passed as imagination
(Nondi 2309). These are real disagreements inside the corpus that a single 'non-dual' reading would
hide.

**Body.** 51 body places on 99 verses: the central channel 7 times, the root centre 5, the crown 4,
the tattvas and humours 16, and single mentions of the navel, throat, nose-tip and brow (all Nondi) and the ten
nadis and humours. 32 of the 51 places are **named**; the other 19 come from keys. The atlas
field already shows that Nondi names places, Sivavakkiyar names channels, Agappei names tattvas,
and Idaikkadar names only the head. Two verbal fixes came out of locating verses in the body: 1391's
தொக்கு is Sanskrit tvak, skin, so the line lists four senses (the flat marks read it as
'gathered'), and 301's unconstrued நான்முழத்து ஒன்பது பீற்றத் துண்டம் reads, under the nine-gates
key, as a four-cubit rag torn in nine places.

**Knows-by.** Direct experience is claimed 35 times, the teacher or book relied on 13 times and
rejected 5 times, the senses rejected 4 times. The field exposes a disagreement the flat marks
treated as tone: Agappei calls the sastras false (1648) while Nondi lists reading many sastras on
his way to release (2313); that pair is proposed as a tension.

## 4. Stance

Each verse has a stance (one or two of shakta_tantric, saiva_siddhanta, void_nondual,
alchemical_physical, ethical_social, unclear), and every link and old-link review records the
stances of both ends. The stance of non-pilot ends was assigned from their marked readings.

**Are different-stance links the ones graders found weak?** On the 57 old graded links touching
these chapters, somewhat, on a small sample:

| old links | n | sound | weak | forced | sound share |
|---|---|---|---|---|---|
| same main stance | 28 | 18 | 6 | 4 | 64% |
| different main stance | 23 | 11 | 11 | 1 | 48% |
| one end `unclear` | 6 | 1 | 4 | 1 | 17% |

(Counting 'same' as any shared value gives 61% against 50%.) The difference is mostly weak, not
forced: different-stance links are seldom stretched, they are thinner, because two schools that use
the same word (மூலம், மௌனம், the four paths) are rarely saying the same thing. The `unclear` row
is the generic catalogue links (the bubble, the body as hut), which graders already marked down.
Of the 41 new links, 28 join the same stance and 13 do not; the grades will show whether the gap
holds.

**Are some old tensions really stance differences?** Yes, most of them. Of the six old tension
links touching these chapters:

- **1658 and Tirumanthiram 2184 (sound)**: Agappei's void stance calls the fifty-one letters false;
  Tirumular's Siddhanta lists them among the paths by which things came. A stance difference, and a
  real one: graders were right that it is incompatible.
- **1938 and 1967 (sound)**: no god above the Maiden (shakta) against Siva is greater (Siddhanta).
  The conflict is between two stances inside Konganar's own kummi.
- **2324 and 2315 (sound)**: the body kept from perishing in nishtai (alchemical-physical) against
  the body as a false cage (Siddhanta renunciation), inside Nondi's one song. A poet holding two
  stances, not a contradiction to be explained away.
- **1400 and 1666 (weak)** and **1676 and 1400 (weak)**: Agappei's void stance against
  Sivavakkiyar's graded Siddhanta scheme. Graders marked them weak because the notes misstated what
  each verse grants; read as stance differences (one school values the graded fruits, the other
  values nothing short of knowing oneself) they become accurate `qualifies` links, which is how
  1666 and 1400 is kept.
- **2303 and 524 (forced)**: both void stance; not a stance difference, and not a tension.

So the sound tensions are the stance differences, and the forced one is the same-stance pair. Of
the 4 new tensions, 3 cross a stance line (1658/2184 kept, 1648/2313, 2308/Thiruppugazh 355) and
one (2309/1862) is inside the void stance but between a shakta-coloured verse and a void one. A
future pass might add a `stance_difference` note to tension links so a grader can tell 'these two
contradict' from 'these two schools differ'.

## 5. The double-reading lexicon

`cipher_lexicon.json` v0.1 lists **39 words** from the pilot verses that carry two traditional
senses: 23 split literal from breath (வாசி, தாள், வாசல், மண்டலம், நடு, மூலநாடி, தந்தி, அத்தி,
குஞ்சரம், ஒன்பது, எட்டு ...), 6 involve alchemy or medicine (குளிகை, ரசம், மாரணம், செப்பு,
வாதம், கவனக்/கமனக்), 8 involve consciousness (சூனியம், வெளி, மூலம், மெய், the letters சி, ம, அ),
1 the social layer (தீர்த்தம்), and 1 (பாதம், foot and step) has two plain senses that links move between. 52 of the 214 layer readings cite an entry. Corpus counts range
from 2 (விண்நாடி, குளிகை, மாரணம், பெருவழி) to 148 (வெளி); the commonest entries (வெளி, மெய், மூலம்,
நீர்) are common words whose second sense is rare, and their counts are upper bounds.

**Acceptance rate: not yet measurable (0 of 39 reviewed).** All entries are `proposed`. The rate
(accepted / reviewed) will come from the lexicon part of the grading packet; it is the lexicon's
quality metric, on the model of reporting acceptance for an extracted entity list. My expectation,
to be checked: entries whose second sense is printed in the corpus's own glosses (அத்தி, தந்தி) or
stated in a sibling verse (மகாரம், சிகாரம், in Tirumanthiram 975) should be accepted; the readings by
emendation (கவனக் as கமனக்) and the numbers (எட்டு) are the most likely rejections.

## New concepts proposed (not added to concepts.json)

- `mukkuttram` (முக்குற்றம், the three humours வாதம், பித்தம், கபம்/கோழை): label ours; the
  verses name the three (301; Kural 941; Thiruppugazh 894, 196, 441, 487). `noy` and `marundhu`
  exist, but nothing names the humoral theory, and `vaadham` already means alchemy.
- `kuligai` (குளிகை, the alchemist's pill): the verses use the word (2305; Tirumanthiram 2709).
- `kaayasiththi` (the undying body, சாகா நிலை): label ours; the verses say சாகாது இருந்திட (2308),
  ஊனுடல் அழியாமல் (2324), தேகத்துக்கு என்றும் சிதைவில்லை (Tirumanthiram 581).

## Limits

- One agent wrote every layer reading and proposed every link; the grades are the only independent
  check, and graders are Claude without a Tamil lexicon. No Tamil scholar has reviewed this.
- Stance values for non-pilot ends, and for verses that take no position, are rough; `unclear` is
  used freely. The stance comparison rests on 51 classifiable old links.
- Links were restricted to pilot verses and the four marked books, so 22 old links to Siddhar
  verses outside the pilot were reviewed but not re-proposed (`out_of_scope`), including sound ones
  (2317 and 1334, 2312 and 610).
- Chapter 96 has 7 verses and chapter 15 one verse; per-chapter figures are not comparable.
- The packet generator lives outside the repository (the brief limits writes to the listed paths);
  `grading/key.json` records the seed, order, calibration links and the layer readings written for
  the calibration verses.

## Blind grading results (2026-11-25, two graders)

- **Calibration:** both graders matched the known grade on 5 of the 6 hidden old links.
- **New links (41):**
  - Grader 1 rated 46% sound and grader 2 37%. They agreed exactly on 73%. Both rated 13 links sound.
  - That is no better than the flat marking's 53% for links between Siddhar verses. **On link quality,
    the layers did not pay for themselves.**
  - By layer, the share of sound grades averaged over both graders:

    | Layer | Links | Sound |
    |---|---|---|
    | breath | 9 | 61% |
    | literal | 17 | 44% |
    | social | 5 | 40% |
    | alchemy | 4 | 25% |
    | consciousness | 6 | 17% |

  - shared_key links were 25% sound, and so were tensions.
- **Graders say most links hold without their layer:** 36 of 41, by both graders. So the layer
  describes the link more often than it carries it, which confirms what the proposer itself found.
- **The one link graded wrong:** 1017 to Tirumanthiram 866 claimed both verses put the moon on the
  left. Tirumanthiram 866 puts the sun's breath on the left.
- **Cipher lexicon v0.2:** 26 entries were accepted by both graders, 10 rejected by both, and 3 are
  disputed. The graders agreed on 92% of entries. The acceptance rate is 67%, against ThinaiKG's 83%
  from a single reviewer.

**Verdict.** Do not re-mark all 2,701 verses in layers to improve links. Keep:
- the accepted lexicon, as a shared key that marking and grading cite
- the stance field, which explains weak links and the sound tensions
- the body-place field, for the body atlas
- the finding that consciousness and shared-key links are the least reliable. Hold them to a
  stricter bar, or route them to a human Tamil reader.
