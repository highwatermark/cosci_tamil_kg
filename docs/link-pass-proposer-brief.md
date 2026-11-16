# Brief: proposing links between Kural verses

You are finding connections between verses of the Thirukkural for a knowledge graph of its meanings
and themes. You are given one or two chapters. For each of their verses, look for the verses anywhere
in the whole Kural that it truly connects to.

Work from /Users/harilakshmanan/Cursor/cosci_knowledge_graph. Do not edit anything there. Read ONLY
the files and commands named below. In particular do not open anything under kg/kural/ or kg/themes/,
and do not read docs/ or git history: they contain earlier link work, and this exercise tests what can
be found independently.

## Inputs

- Index of all 1,330 verses, one line each (number | chapter | concepts | a one-sentence reading in
  English): `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/full/index.txt`
  Read all of it first. It is your map of the book.
- Hints: `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/full/hints.txt`
  For each verse, 10 verses that share words with it. These are weak hints from word overlap. Most
  real connections are thematic and will NOT be in the hints, so search the index yourself; use grep
  on the index for ideas and images.
- Your own chapters in full, with three commentaries: `python3 -I scripts/chapter_marks.py show N`
- Any verses, yours included (Tamil, Pope's gloss, Subramuniyaswami's translation where it exists,
  and the start of Parimelazhagar and Kalaignar): `python3 -I scripts/link_pass.py verse 327 550 ...`
  Several numbers per call is fine.

Subramuniyaswami's translation covers verses 1 to 1080 and is in copyright. Use it, like Pope, as one
more reading of a verse. Never quote it in a note. If his reading matters to a link, describe it in
your own words and attribute it to him.

## Method, for each of your verses

1. Shortlist candidate verses from the index, across all three books. Think about what the verse
   claims, its image, and where the book says the opposite, limits it, or repeats its logic in
   another domain.
2. Before proposing any link, read the Tamil and commentary of BOTH verses with the commands above.
   Read the Tamil first: translations sometimes add ideas the verse doesn't contain, and the index
   readings are a model's summaries, not the text. This edition has typos; if a verse looks
   corrupted, say so and don't build on it.
3. Propose at most 3 links per verse, only ones that would teach a reader something. A link to a
   verse in the same chapter is allowed when it is a real connection, not just the chapter's shared
   topic. "No link" is a valid and respectable answer: give a one-line reason.

Chapters 109 to 133 are the Book of Love, whose verses are dramatised speeches by lovers. A speaker's
claim in the moment is not the book's teaching, so be careful before calling a link from or to those
chapters a tension.

## Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. Say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in different
  domains).
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain.

## Notes

Each note is two or three sentences: say what each verse says (accurately, from the Tamil), then what
the pairing shows. Cite the deciding Tamil words. Attribute anything that comes from a commentator or
translator to them. Don't inflate: no superlatives or motives the text doesn't give.

## Output

Write a JSON array to the output path you were given, with exactly one object per verse of yours, in
order:

    {"verse": 3, "links": [{"b": 10, "type": "agrees", "note": "..."}], "no_link_reason": null}

Use `"links": []` and a reason string when you propose none. `b` must be a verse number from 1 to
1330 other than the verse itself. Validate that the file parses, has one entry per verse, at most 3
links per verse, and every type is one of the six names. Then reply with only: how many links you
proposed, how many verses got none, and any verse-text problems you saw (verse numbers only, one line).
