# Brief: the refinement pass (links and concepts) for the Tirumanthiram and the Thiruppugazh

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph is a knowledge graph of the
meanings, themes and threads of Tamil literature. Four books are marked: the Thirukkural, the
Naladiyar, the Tirumanthiram and the Thiruppugazh. The first pass over the Tirumanthiram and the
Thiruppugazh linked only about 30% of their verses (the Kural, after its own link pass, links 99%),
and tagged many verses with broad concepts. This pass fixes both for the verses you are given.

Every verse ID is written `book:N`: `kural:1061`, `naladiyar:42`, `tirumanthiram:1823`,
`thiruppugazh:355` (Thiruppugazh verses are whole songs).

## Inputs (all paths under the scratchpad folder below unless they start with scripts/)

Scratchpad: `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/refine/`

- Your verses: read them a few at a time with `verse.py` (below); `book_marks.py show` prints whole
  chapters and overflows. Your chapters' current marks are in `kg/themes/BOOK/chNNN.json` (read only).
  `python3 -I scripts/book_marks.py BOOK chapters` lists every chapter's verse range.
- Any verse of any book, with its Tamil, reading, nuance and concepts:
  `python3 -I scripts/verse.py kural:1061 tirumanthiram:725 ...` (several per call); add `-r` for the
  reading and concepts only, one line each, to scan candidates quickly.
- A pair inside your own set: propose it once, from either end.
- `hints_tm.txt` / `hints_tp.txt`: for each verse, the verses sharing its rarest concepts and words,
  first from its own book, then a few from each other book; each hint shows in brackets the two
  rarest things the pair shares. Hints only: most are not real links, and
  many real links will not be in them.
- `index.txt`: one line per verse of all four books (`id | concepts | reading`). It is large: grep
  it for ideas, images, words and concept ids rather than reading it whole.
- `existing_links.txt`: every link already in the graph (`a b type grade`). Don't propose a pair
  that is already there in either direction; check with `python3 -I .../refine/exists.py A B [A B ...]`.
- `kg/themes/concepts.json`: the shared concept list.

## For each of your verses

1. **Concepts.** Read the verse's current concepts. Replace them only if they are wrong or too
   broad for what the verse is about; otherwise leave them (write `null`). Rules:
   - A concept says what the verse is *about*, not every name in it. Don't tag `sivam`, `iraivan`
     or `thiruvadi` merely because Siva, the Lord or the feet are named; tag them when the verse
     is about Siva's nature, the soul becoming Siva, or the feet as refuge or goal.
   - Prefer the specific concept that exists (`praanan` over `yogam` for a breath verse,
     `varaivinmagalir` over `kaamam` when the courtesan's trade is the point).
   - Propose a new concept only when an idea recurs across several verses and nothing fits. Name
     what the text names (lowercase romanized Tamil id, Tamil word, short gloss, `label_source`
     "text" or "marker"). Murugan's own stories (the vel, Valli, the defeat of Sura, the peacock)
     may get concepts now if a song is *about* one, not when it is stock praise. Tag a new concept
     only on your own verses; it is applied elsewhere later.
   - 1 to 4 concepts, most central first.
2. **Links.** Find what each verse truly connects to across all four books. Shortlist from the
   hints and by grepping the index; then, **before proposing any link, read the Tamil of both
   verses** with `verse.py`. Readings in the index are other agents' summaries, not the text.
   - Up to 3 new links per verse. Aim for every verse to have at least one link, counting the links
     it already has; a verse that is already well linked needs a new one only if it is worth it.
     "No link" is a respectable answer with a one-line reason when nothing teaches the reader
     anything.
   - Value links across books, and within the book across distant chapters. A link to a near
     neighbour is fine only if it is more than the chapter's shared topic.
   - Two songs or verses that share a stock formula or a stock complaint are a weak link unless the
     pairing teaches something; don't propose those.
   - A near-repeat of the same verse elsewhere in the book is worth an `agrees` link: say so.

## Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. Say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something.
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain.

Notes are two or three sentences: what each verse says, from the Tamil, then what the pairing
shows, citing the deciding Tamil words. No superlatives or motives the text doesn't give. Neither
the Tirumanthiram nor the Thiruppugazh has commentary in the corpus; don't look for one (no web).

## Output

Write one JSON object to the output path you were given:

    {"new_concepts": [{"id": "vel", "tamil": "வேல்", "gloss": "...", "label_source": "text"}],
     "verses": [
       {"verse": "tirumanthiram:725", "concepts": null,
        "links": [{"b": "naladiyar:47", "type": "tension", "note": "..."}], "no_link_reason": null},
       ...]}

One entry per verse of yours, in order. `concepts` is `null` to keep the current ones, or the full
new list. Validate with
`python3 -I /private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/refine/refine_check.py OUT BOOK CH CH ...`
until it says valid. Do not edit any repository file and do not commit. Reply with only: links
proposed (within the book, to each other book), verses with no link, concept changes, new concept
ids.
