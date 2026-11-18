# Brief: marking Thiruppugazh chapters

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. The Thirukkural, the Naladiyar and the
Tirumanthiram are marked and linked. You are marking songs of the Thiruppugazh of Arunagirinathar
(15th century): 1,326 songs to Murugan, most of them sung at a shrine (தலம்) and grouped under its
name, the rest general songs (பொதுப்பாடல்கள்).

## Read first

- `kg/themes/SCHEMA.md`: the marking rules. Follow them exactly, with the changes below.
- `kg/themes/tirumanthiram/ch004.json` and `kg/themes/naladiyar/ch038.json`: worked examples. (The
  Naladiyar chapter on courtesans is the closest earlier treatment of a frequent Thiruppugazh theme.)
- `kg/themes/concepts.json`: the shared concept list (240 concepts). Reuse these ids. Add a concept
  only when none fits, and name what the text names.

## Commands (from the repository root)

- Your chapters' songs: `python3 -I scripts/book_marks.py thiruppugazh show 12 13`
- Validate your files: `python3 -I scripts/book_marks.py thiruppugazh check 12 13`
- Kural verses in full: `python3 -I scripts/link_pass.py verse 1061`; a Naladiyar chapter:
  `python3 -I scripts/naladiyar_marks.py show 38`; a Tirumanthiram chapter:
  `python3 -I scripts/book_marks.py tirumanthiram show 151` (running chapter number)
- One line per marked verse of those three books, with concepts and a reading, to search for links:
  `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/books_index.txt`
  (lines start `kural:N`, `naladiyar:N` or `tirumanthiram:N`; grep it rather than reading it whole)

## How to read a song

- The unit you mark is a whole song (a "verse" in the schema). Keys are song numbers.
- The text is set to a rhythm (சந்தம்): words are split across line ends and `......` marks the
  beat. Read across the breaks; the split pieces are one word.
- Most songs move in two halves. The first is the poet's plea or confession: the lure of women
  (often courtesans), the body's decay, Death's messengers, wasted life, and a prayer for the
  Lord's feet or grace. The second praises Murugan through epithets and myths (Valli, Devayanai,
  Surapadman, the Krauncha hill, the vel, the peacock, Siva's son taught the meaning of Om, Vishnu's
  nephew) and ends at the shrine with பெருமாளே. Some songs are only praise.
- `reading`: two or three sentences in your own words: what the plea asks or confesses, what the
  praise centres on, and the shrine if named. Not a line-by-line translation.
- `concepts`: what the song is about, not every epithet. Murugan's praise alone is not a reason for
  a concept in every song; mark what is distinctive.
- The descriptions of lovemaking are frank. Read them as the poet does, as the confession the song
  turns away from, and summarise them plainly and briefly.

## What the pilot (songs 1-35, chapters 1-5, already marked) found

- Concepts for recurring themes: `kootru` for Death and his servants coming with noose and club on
  the buffalo, or Yama's palm-leaf summons (சமனோலை), where the plea is for Murugan to come at that
  hour; `thiruvadi` for the feet; `thondu` (new) for devotional service (தொண்டு, அடிமை, வழியடிமை),
  never `adimai`, which means bondage; `mayal` (new) for the poet's infatuation (மயல்).
- Courtesans: use `varaivinmagalir` only when money or deceit is named (wealth taken, "come to our
  house", the man thrown out when his money ends); otherwise `kaamam`, or `punarchi` for the explicit
  scenes. The poet's self-abuse (சிறியன், புலையன், நிர்மூடன்) is `kutram` or `pedhaimai`.
- One myth earns concepts: Murugan teaching Siva the meaning of Om and binding Brahma for not
  knowing it (`guru`, `piranavam`; `gnaanam` if Om is not explicit). Valli and the millet field,
  Vishnu or Rama as uncle, the vel against Sura and Krauncha, and battle scenes are stock praise:
  leave them out of concepts unless a song is about them.
- Battle scenes are sung in drum syllables (தெனன, டுடுடு, குகுகு). They are rhythm, not words.
- Watch for Murugan identified with Tamil saints (the Tamil mouth that impaled the Jains, i.e.
  Sambandar; the teacher of Tamil to Agastya).
- Some songs are akam love poems in another voice (a mother's lament for her lovesick daughter, a
  courtesan's own speech), not the poet's confession. Say whose voice it is.
- Expect corrupt glyphs that `CORRUPT_CHARS` does not flag; the bad glyph ஡ often stands for ஊ, and
  ஡ண for ரீ. Record them in `source_issues`.
- Read the pilot's files (`kg/themes/thiruppugazh/ch004.json`, `ch005.json`) for depth and style.

## Changes from the Kural schema

- Files go in `kg/themes/thiruppugazh/chNNN.json`, numbered by the tool's running chapter numbers
  (1 to 261, shown by `show`). Long runs under one heading are split into chapters of up to 15
  songs; `chapter_theme` describes your chapter's songs.
- **There is no commentary or translation in the corpus, and you must not look for one** (no web
  search; modern meanings of the Thiruppugazh are in copyright). Readings rest on the Tamil alone,
  so there are no `positions` and no `contested` marks. Instead:
  - Mark `uncertain` when the sense depends on how a run of syllables splits into words, on an
    obscure Sanskrit or Tamil word, on an allusion you can't identify, or on a corrupt line.
  - In `nuance`, say which words carry the meaning and which allusion or doctrine they point to.
    Name a myth only when the text names it or its unmistakable details.
  - Don't invent precision. A short, true reading beats a full, confident one.
- `links` may point within the Thiruppugazh (`"b": 512`), to the Kural (`"kural:913"`), the
  Naladiyar (`"naladiyar:371"`) or the Tirumanthiram (`"tirumanthiram:1823"`). At most three
  links per song, and only links that teach something; most songs need none. Likely ground: the
  courtesan (Kural chapter 92, Naladiyar chapter 38), the body's decay (Naladiyar chapters 3 and
  5), Death's messengers and the Lord's feet (Tirumanthiram), and repeated formulas within the
  book. Read the other verse before linking. Test every `tension` as SCHEMA.md says.
- Record corrupt lines (the `CORRUPT_CHARS` field shows where the source had bad characters) and
  heading problems in `source_issues`.

## Rules

- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within, to the Kural, to the Naladiyar, to the Tirumanthiram), how many songs you marked
  uncertain, and text problems.
