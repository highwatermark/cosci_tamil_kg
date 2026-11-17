# Brief: auditing Kural threads

A thread is a claim about how the Thirukkural treats one theme across chapters or books, resting on
several audited links between verses. Another agent wrote the threads in your packet. You judge
whether each claim is true of the verses it cites, and whether the links carry it. Grade on the
merits; don't aim for any share of passes.

Work from /Users/harilakshmanan/Cursor/cosci_knowledge_graph. Do not edit anything there.

## Inputs

- Your packet, named in your instructions. For each thread it gives the title, claim, stated limits,
  and every link the thread uses, with the link's type and note and both verses' Tamil, reading and
  concepts. It does not give the writer's reasoning.
- Verse detail (Tamil, Pope, Subramuniyaswami where it exists, and the start of two commentaries):
  `python3 -I scripts/link_pass.py verse 327 550 ...`
- A whole chapter with three commentaries: `python3 -I scripts/chapter_marks.py show N`

Read the Tamil of every verse the claim rests on. Translations and link notes are other models' or
translators' readings, not the text. Subramuniyaswami's translation is in copyright: never quote it.

## What to check

For each link: does the pair of verses, read in the Tamil, support the thread's claim?
- supports: yes, as the claim uses it.
- weakly: the verses are consistent with the claim but don't carry it on their own.
- irrelevant: the link is real but does not bear on this claim.
- contradicts: the verses, read fairly, cut against the claim.

For each thread:
- supported: the claim is accurate about every verse it cites, its scope matches its evidence, and
  at least three links support it.
- partly_supported: a real pattern is there, but the claim overstates it, misdescribes a verse,
  leans on a reading it doesn't name, or has fewer than three supporting links.
- unsupported: the claim fails on the verses, or the links don't bear on it.

Also say in `issue` what a careful reader should know: the overstatement, the verse misread, the
commentator the claim silently depends on, or counter-evidence in the book you know of. If the
thread's `limits` already say it, don't repeat it.

## Output

Write a JSON array to the output path you were given, one object per thread, in packet order:

    {"id": "thread:slug", "grade": "supported|partly_supported|unsupported",
     "issue": "Two or three sentences, or null if nothing needs saying.",
     "links": [{"a": 327, "b": 550, "verdict": "supports|weakly|irrelevant|contradicts",
                "reason": "one sentence citing the Tamil words that decide it"}]}

Every thread and every link in the packet must appear exactly once. Validate that the file parses
and the counts match. Then reply with only the grade per thread id.
