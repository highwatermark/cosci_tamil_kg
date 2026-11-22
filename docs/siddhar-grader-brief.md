# Brief: grading Siddhar links

You are grading links in a knowledge graph of the meanings and themes of Tamil literature. Each
link in your packet starts from a verse of the Siddhar songs (`siddhar:N`, where N is the verse's
running number in `kg/core/siddhar.jsonl`; the packet also prints the verse's own id, such as
`siddhar:sivavakkiyam:285`, its poet and its work) and points to another Siddhar verse or to a
verse of the Kural (`kural:N`), the Naladiyar (`naladiyar:N`), the Tirumanthiram
(`tirumanthiram:N`) or the Thiruppugazh (`thiruppugazh:N`). A few links join two Kural or
Naladiyar verses; grade them the same way. Another agent proposed each link while reading the
book. Your job is an independent, careful judgment of whether each link holds. Grade on the
merits: don't aim for any particular share of passes or failures.

Each link has a type, the proposer's note, and for both verses the Tamil and a "marked reading"
(Pope's gloss too for the Kural). **The Siddhar songs, the Tirumanthiram and the Thiruppugazh have
no commentary in the corpus: the marked reading and nuance were written by Claude agents, and for
the Siddhar verse by the same agent that proposed the link,** so they are a claim to check, not
evidence. Read the Tamil first.

The Siddhars write in cipher (பரிபாஷை: sun and moon for the breaths, the horse for the breath,
the serpent, numbers, salt, body-places) and in refrain. A link that holds only on a symbolic
reading the Tamil doesn't fix is weak or forced unless the note names that reading and it is a
fair, traditional one. The Siddhars attack ritual, caste, temple images and book-learning in
stock phrases; two verses sharing a stock attack, or a verse sharing a stock attack with the
Tirumanthiram's தவ நிந்தை chapters, is a weak link unless the pairing teaches something specific.
Sivavakkiyar's near-repeats of his own verses are a real connection; grade whether the note
describes them fairly. Earlier graders were too lenient: a link that needs a generous reading is
weak, not sound. Base-text misprints and corrupt lines are common in this edition; if a verse
looks corrupted, say so in `text_issue` instead of building on it. Read only your packet. Do not
edit any file in the repository.

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
evidence: check each claim it makes against the Tamil.

## Output

Write a JSON array to the output path you were given, with one object per link, in packet order:

    {"a": "siddhar:1285", "b": "tirumanthiram:668", "type": "AGREES", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "reason": "two or three sentences citing the deciding Tamil words",
     "text_issue": null or a short note on a corrupt line}

Write `a` and `b` exactly as the packet's LINK header shows them, as strings. Every link in the
packet must appear exactly once. Validate that the file parses as JSON and that its count matches
the packet's LINK headers. Then reply with only the counts by grade.
