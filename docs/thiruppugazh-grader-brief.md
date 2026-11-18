# Brief: grading links from the Thiruppugazh

You are grading links in a knowledge graph of the meanings and themes of Tamil literature. Most
links in your packet start from a song of the Thiruppugazh of Arunagirinathar (15th century, songs
to Murugan) and point to another Thiruppugazh song (`tp:N`), a Kural couplet (`kural:N`), a
Naladiyar quatrain (`naladiyar:N`) or a verse of the Tirumanthiram (`tirumanthiram:N`). A few join two Kural or Naladiyar verses; grade them the same way.
Another agent proposed each link while reading the book. Your job is an independent, careful
judgment of whether each link holds. Grade on the merits: don't aim for any particular share of
passes or failures.

Each link has a type, the proposer's note, and for both verses the Tamil and a "marked reading"
(Pope's gloss too for the Kural). **For the Thiruppugazh there is no commentary in the corpus:
the marked reading and nuance were written by the same agent that proposed the link,** so they are
a claim to check, not evidence; the same holds for Tirumanthiram readings. Read the Tamil first.
The songs are set to a rhythm, so words are split across line ends and `......` marks the beat;
read across the breaks. A song typically confesses (lust, courtesans, the body's decay, Death's
messengers) and then praises Murugan; check that the link rests on what the song actually says,
not on the stock themes of the genre. Two songs sharing a stock formula or a stock complaint is a
weak link unless the pairing teaches something. Earlier graders were too lenient: a link that
needs a generous reading is weak, not sound. Base-text typos
and corrupt lines exist in this edition; if a verse looks corrupted, say so instead of building on
it. Read only your packet. Do not edit any file in the repository.

## Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. The note should say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in
  different books, domains or chapters).
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain.

## Grades

- sound: the connection is real, the type fits, the note is accurate about both verses, and the
  pairing teaches the reader something.
- weak: a real connection, but thin, generic, or the note overstates it; or it would be sound under
  a different type (give better_type).
- forced: depends on stretching a word, a reading, or a symbolic gloss; or it's only a shared topic
  or shared word dressed up as more.
- wrong: misreads or misdescribes a verse, cites the wrong text, or claims something the verses
  contradict.

Grade the link as written, note included. A true connection with a false claim in the note is weak
or wrong depending on how central the false claim is. A fluent, careful-sounding note is not
evidence: check each claim it makes against the Tamil. Two songs that share lines within the
Thiruppugazh are a real connection; grade whether the note describes them fairly.

## Output

Write a JSON array to the output path you were given, with one object per link, in packet order:

    {"a": "tp:24", "b": "kural:1229", "type": "AGREES", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "reason": "one or two sentences, citing the Tamil words that decide it",
     "text_issue": null or a short note if a verse's text looks corrupted}

Write `a` and `b` exactly as the packet's LINK header shows them, as strings. Every link in the
packet must appear exactly once. Validate that the file parses as JSON and that its count matches
the packet's LINK headers. Then reply with only the counts by grade.
