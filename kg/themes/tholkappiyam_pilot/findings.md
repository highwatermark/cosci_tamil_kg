# Tholkappiyam pilot: findings from the first tagging (tags_A)

One tagger (a Claude agent, the same one that wrote the brief) tagged 100 verses, 20 from each book,
by `docs/tholkappiyam-tagging-brief.md`. Nothing here has been checked by a second tagger yet;
`packet.md` is ready for that and `scripts/tholkappiyam_agreement.py` will score it. Read every
number below as one reader's tags, not as measured agreement.

## The source

`kg/core/tholkappiyam.jsonl` holds 1,603 records from Project Madurai's pmuni0100 (sutras only): the
சிறப்புப்பாயிரம், எழுத்ததிகாரம் 483, சொல்லதிகாரம் 463, பொருளதிகாரம் 656 (அகத்திணையியல் 58,
புறத்திணையியல் 30, களவியல் 51, கற்பியல் 53, பொருளியல் 52, மெய்ப்பாட்டியல் 27, உவமயியல் 38,
செய்யுளியல் 235, மரபியல் 112). Numbering is this edition's, per iyal, and every iyal runs 1 to N
with no gap. Source problems fixed in parsing: eleven nurpas printed with the number run into the last
line (col 3.1, 4.3, 6.9; porul 2.26, 3.1, 5.2, 5.4, 6.17, 7.7, 8.6, 9.85), one stray Latin letter
(porul 8.41, மிகுதலுsம் → மிகுதலும்), and one iyal heading inside a broken table (eluttu 9). No
commentary or translation text is in the file.

## What the tags show, book by book

| | Kural | Naladiyar | Tirumanthiram | Thiruppugazh | Siddhar |
|---|---|---|---|---|---|
| akam / mixed | 3 / 0 | 0 / 1 | 0 / 2 | 2 / 0 | 0 / 0 |
| neither (no thinai) | 0 | 0 | 9 | 0 | 5 |
| frame fit native | 5 | 4 | 3 | 20 | 4 |
| main thinai | paadaan 11, vaakai 5 | vaakai 8, paadaan 7, kaanchi 4 | paadaan 5 | paadaan 18 | paadaan 10 |
| no meyppadu | 11 | 8 | 13 | 1 | 6 |
| needed a porul 6.12 state | 8 | 6 | 4 | 1 | 6 |
| comparisons (verses) | 6 (6) | 17 (11) | 9 (7) | 23 (16) | 16 (10) |
| ullurai | 0 | 0 | 5 | 0 | 4 |
| mutal present | 2 | 2 | 2 (both negated) | 11 | 1 |
| relates body and life | 0 | 1 | 5 | 4 | 4 |

## Fields that seem to carry signal across books

1. **The puram sub-thinai separates the didactic books better than akam/puram does.** Akam/puram
   alone is nearly useless here: 93 of 100 verses are not akam. But porul 2.29 puts செவியறிவுறூஉ
   (admonition to a hearer) and வாயுறை வாழ்த்து (wholesome counsel) inside paadaan, and 2.15 to 2.19
   give vaakai (excellence in one's calling, including the ascetic's part) and kaanchi (the world
   that does not stay). With those three the Kural (admonition), the Naladiyar (types of people, and
   impermanence) and the Thiruppugazh (praise and supplication, all 20 native) come apart cleanly.
   The didactic books are puram by extension, but by a nurpa, not by a stretch.

2. **The meyppadu profile is a fingerprint, and the causes matter more than the eight names.** The
   Thiruppugazh has a feeling in 19 of 20 songs, and always the same few: azhugai 7, uvagai 6,
   ilivaral 4, accham 4. That is the song's own shape: delight in women, disgust at the body's
   decay, fear of Death's rope, self-abasement. Porul 6.5 puts இளிவு (humiliation) under azhugai and
   6.6 puts old age and disease under ilivaral, so the tagger has to separate "I am a dog" from "my
   teeth loosen", which the concept list never does. The Siddhars' signature is nakai from எள்ளல்
   (mockery: 5 of 20), the satire on book-carriers, garbed beggars and idol-worshippers. The
   Tirumanthiram mostly has no feeling at all (13 of 20 empty).

3. **The comparison type separates the books; the basis less so.** The Naladiyar compares openly:
   11 of 17 comparisons have a marker, and it is the only book that sets image and subject side by
   side (juxtaposition 3). The Siddhars and the Tirumanthiram compare by metaphor and by ullurai
   (13 of 16 and 6 of 9). The Thiruppugazh's comparisons are about bodies (mey 11, uru 8 of 23):
   eyes like carp, breasts like hills, hair like cotton. Basis (porul 7.1) is easy to assign but adds
   less than type does.

4. **Ullurai is where the Siddhars' cipher fits.** Every ullurai in the sample (9) is in the
   Tirumanthiram or the Siddhar songs: the lotus with no water, the jackal that will not come when
   called, the snake, the lady of fragrant hair, the small house. Porul 1.51 defines ullurai as an
   image whose meaning is completed by matching it with an unstated subject, which is exactly what
   பரிபாஷை does. The Kural and Naladiyar have none: they state their tenor. This one field may be the
   most useful thing the frame offers the Siddhar graph, because it forces a tagger to say which
   words carry the hidden subject and what the subject is.

5. **Mutal survives as the temple town, karu as place-praise.** 11 of 20 Thiruppugazh songs name a
   setting, always a shrine (Palani, Arunai, Puliyur, Vayalur), and the praise sections often paint
   it with the native things of porul 1.20: fields, fish, areca palms, moat (370); the millet field
   and kura grove of the Valli story are kurinji karu (591). The landscape apparatus did not vanish
   from devotional poetry; it moved from the lovers to the god's town.

Fields that carry little: `uri` (7 verses, all akam, as it should be), `iraicchi` (2), and
`frame_fit` beyond what `thinai` already shows.

## The uyir / mey analogy

The letters book calls the twelve vowels life (உயிர்) and the eighteen consonants body (மெய்)
(eluttu 1.8, 1.9), says a vowel joined to a consonant keeps its nature (1.10), that the consonant is
half a measure (1.11), and that in the joined letter the vowel sounds after the consonant (1.18).
What the pilot shows:

- **No verse in the sample uses the letters to talk about soul and body.** The analogy is in the
  vocabulary, not in the verses. 14 of 100 verses relate body and life at all (none in the Kural
  sample), and over the whole corpus உயிர் co-occurs with a body word in 1.4% of Tirumanthiram
  verses and 0.6% of Siddhar verses (a string count, not a reading).
- **Where Tirumular relates them, his model is the grammar's.** tirumanthiram:1790 says the Lord is
  in the soul as life is in flesh (ஊனிது தானுயிர் போல்), and 483 has breath shaping the child: union
  in which neither part loses its nature, which is eluttu 1.10. Four of five Tirumanthiram verses that
  relate them are `union`.
- **The Siddhars split three ways, and none is the grammar's.** Pattinathar is dualist (siddhar:300:
  the body is a stinking cage that ends as burnt bone); Agasthiyar refuses the split outright
  (siddhar:2436: உடலுயிரென் றுரைத்திடாதே, do not say "body and life"); Kakabhusundar sheds the
  sheaths (2377). The Thiruppugazh is dualist or transcending (510: remove this pot).
- **Where the Siddhars do map letters to body and life, the polarity is reversed.** Outside the
  sample, siddhar:2111 says the circle of Om became the body and the mute letter (ஊமை எழுத்து)
  became the life. In the grammar it is the sounding vowel that is life and the half-measure
  consonant that is body. The Siddhar puts life in the silent part.
- **Their letter systems are not Tholkappiyam's.** The mantra verses count the Sanskrit alphabet
  (tirumanthiram:963: fifty-one letters) or the five-letter mantra (siddhar:1485), not the thirty
  letters and three dependants of eluttu 1.1 and 1.2. The shared ground is one word: மெய் means body,
  truth and consonant, and Tirumular plays body against truth (2603 மெய்யென் புரவி; 2604
  மெய்கலந்தான்). The pilot cannot show influence from the grammar; it shows a shared word and, in
  Tirumular, a matching picture.

## Surprises

- **The eight feelings have no place for calm.** 25 verses needed one of the extra states of porul
  6.12 (equanimity, restraint, love, reproach, recollection), most of them in exactly the verses the
  graph cares about. tirumanthiram:423 names and refuses wonder (வியப்பில்லை) at the world's end, and
  2508 ends in உபசாந்தம். The eight were made for love and war poetry; the ninth feeling the
  devotional books want is not among them.
- **Mystic verse keeps the karu and negates the mutal.** tirumanthiram:844 has a lotus with no earth,
  water, stalk or root, and no town, above or below; 1528 has union in the place of no night or day.
  These are not verses without a setting: they deny the setting by name, using the categories of
  porul 1.4 against themselves. `mutal.negated` is a small field with a clear meaning.
- **Porul 2.23 (காமப் பகுதி கடவுளும் வரையார்) licenses the Thiruppugazh's love songs.** 645 and 705
  are ordinary perunthinai, a pining girl, the moon that burns, midnight (kurinji's hour, porul 1.7),
  addressed to Murugan.
- **The Naladiyar borrows akam's apparatus for moral truths.** naladiyar:290 addresses the lord of
  the cool hill country, with waterfall and bees, to say the ruined have no kin. It is kurinji in
  everything but its subject.
- **The comparison markers of porul 7.12 to 7.16 do not predict the basis in these books.** Of 28
  comparisons with a marker the uvamaviyal lists, the marker's class matches the shared quality in 9
  (32%). போல, which porul 7.16 lists among colour-form markers, carries action 8 times out of 12.
  Either the classes describe Sangam usage only, or they were never meant as a rule; the second
  tagger will show whether this is the tagger.

## Is it a better frame?

Not a replacement, on this evidence. It classifies 86 of 100 verses somewhere, but the 14 it
cannot (cosmology, tattva counts, breath technique, signs of death, silence) are the Tirumanthiram's
and Siddhars' core, and there the concept list does the work. What it adds that the concept list
lacks is form: the feeling a verse displays and its cause, how it compares, and what it hides. The
fields worth keeping if the second tagger agrees: puram sub-thinai with thurai, meyppadu with
cause, the porul 6.12 states, comparison type, ullurai with its tenor, and `mutal.negated`.

## Problems and limits

- One tagger, who also wrote the brief. Agreement is untested.
- Thiruppugazh songs were tagged whole (16 to 24 lines each); a song has a plea section and a praise
  section with different feelings and settings, and two taggers may weight them differently.
- 36 of the 60 Tirumanthiram, Thiruppugazh and Siddhar verses (17, 13 and 6) are marked uncertain in
  the graph, and their readings are agent-written. Tags on coded verses (the snake, the lady, the lotus) rest on
  traditional readings the Tamil does not fix.
- The sample has no Tirumanthiram verse from the chapters that most use body-and-life language, so
  the uyir/mey section leans on corpus string counts and two out-of-sample verses.
