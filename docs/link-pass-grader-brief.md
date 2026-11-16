# Brief: grading links between Kural verses

You are grading links between verses of the Thirukkural in a knowledge graph of meanings and themes.
Another agent proposed each link. Your job is an independent, careful judgment of whether each link
holds. Grade on the merits: don't aim for any particular share of passes or failures.

Your packet lists links. Each has a type, a note, and for both verses: the Tamil, Pope's gloss, the
marking agent's reading, Subramuniyaswami's translation where it exists, and the start of up to
three commentaries (Parimelazhagar, Manakkudavar, Kalaignar; long ones are cut off with "…"). If you
need a full commentary, run this from /Users/harilakshmanan/Cursor/cosci_knowledge_graph:
`python3 -I scripts/chapter_marks.py show CHAPTER_NO` (it prints a whole chapter). Do not edit any
file in that repository, and read only your packet and that command's output.

Read the Tamil first. Translations sometimes add ideas the verse doesn't contain. Base-text typos
exist in this edition, so if a verse looks corrupted, say so instead of building on it. Manakkudavar
entries marked [#] may be Parimelazhagar's text used as a filler, so they aren't independent
evidence. Subramuniyaswami's translation is in copyright: use it as one more reading, and never quote
it in your reasons.

## Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. The note should say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in different
  domains or chapters).
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain.

## Grades

- sound: the connection is real, the type fits, the note is accurate about both verses, and the
  pairing teaches the reader something.
- weak: a real connection, but thin, generic, or the note overstates it; or it would be sound under a
  different type (give better_type).
- forced: depends on stretching a word, a reading, or a commentator; or it's only a shared topic or
  shared word dressed up as more.
- wrong: misreads or misdescribes a verse, cites the wrong text, or claims something the verses
  contradict.

Grade the link as written, note included. A true connection with a false claim in the note is weak
or wrong depending on how central the false claim is. A fluent, careful-sounding note is not
evidence: check each claim it makes against the Tamil.

## Output

Write a JSON array to the output path you were given, with one object per link, in packet order:

    {"a": 1192, "b": 11, "type": "PARALLEL_DOMAIN", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "reason": "one or two sentences, citing the Tamil words that decide it",
     "text_issue": null or a short note if a verse's text looks corrupted}

Every link in the packet must appear exactly once. Validate that the file parses as JSON and that
its count matches the packet's LINK headers. Then reply with only the counts by grade.
