# Marking a Kural chapter

The graph is for meaning: themes, philosophy, nuance, and threads across books. Each chapter
has one file, `kg/themes/kural/chNNN.json`. `ch038.json` is the worked example, so match its
depth and style.

## Commands

Show a chapter's verses and commentaries:

```bash
python3 -I scripts/chapter_marks.py show 38
```

Validate a chapter's marks:

```bash
python3 -I scripts/chapter_marks.py check 38
```

## Fields

| Field | Required | Meaning |
|---|---|---|
| `chapter_no` | Yes | Chapter number |
| `chapter_theme` | Yes | What the chapter argues as a whole, in one or two sentences |
| `structure_note` | No | How the chapter is organized, if a commentator or the verses show it |
| `verses` | Yes | One entry per verse, keyed by verse number |
| `links` | No | Connections to other verses, anywhere in the Kural |
| `new_concepts` | No | Concepts missing from `kg/themes/concepts.json` |
| `source_issues` | No | Problems found in the sources, as strings |

Each verse has:

| Field | Required | Meaning |
|---|---|---|
| `reading` | Yes | One sentence on what the verse says, in your own words |
| `concepts` | Yes | 1 to 4 concept ids, most central first |
| `nuance` | No | What a quick reader would miss. Omit it unless there is something real to say. |
| `contested` | No | `true` if commentators differ in substance |
| `positions` | If contested | A commentator's view: `by`, `position` and an exact `quote` |
| `uncertain` | No | `true` if you aren't confident in your reading |

Each link has `a`, `b`, `type` and `note`. The types are `tension`, `agrees`, `develops`,
`qualifies`, `same_image` and `parallel_domain`.

Each new concept has `id`, `tamil`, `gloss` and `label_source`. The source says whether the
verses use the Tamil word or the label is yours. Ids are lowercase romanized Tamil.

## Rules

- **Read the Tamil first.** Translations can add ideas: Pope's glosses often add "through fate"
  where the verse doesn't say it.
- **Readings are your own words.** Don't copy Pope or a commentator.
- **Quotes are exact.** Copy from the `show` output. Kalaignar's quotes have at most 14 words,
  and the others at most 30, because Kalaignar's commentary is modern.
- **Mark `contested` only for differences in substance:** who is meant, what a key word means, or
  a different worldview. Rewording doesn't count. Most verses shouldn't be contested.
- **Don't resolve a contested verse.** Record the positions without choosing a winner.
- **Say what the verse does and doesn't say.** Don't present a commentator's theology as the
  verse's own claim. A `nuance` is your interpretation, so offer it as one.
- **Keep links few and worthwhile.** Prefer ones between chapters. Don't link verses merely for
  sharing a topic. Each one must teach the reader something, and a real `tension` is the most
  valuable. Check the other verse's text before linking to it.
- **Reuse concepts.** Add one only when nothing existing fits, and name what the text names.
- **Don't invent certainty.** Use `uncertain` when you are unsure. An honest gap is better than a
  smooth guess.
- **Report misaligned sources.** Commentaries were aligned automatically. If one is about a
  different verse, don't use it, and record it in `source_issues`.
