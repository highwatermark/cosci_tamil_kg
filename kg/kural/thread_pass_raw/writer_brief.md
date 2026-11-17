# Brief: finding threads in the Kural's link graph

A thread is a claim about how the Thirukkural treats one theme across its chapters or books, which
several audited links between verses support together. Threads are the top layer of a knowledge
graph of the book's meanings; readers will use them to see where the book argues with itself,
qualifies itself, or repeats one logic in different domains.

You get one or two candidate packets. Each is a cluster of verses and the sound links among them,
found mechanically: either verses chained by tension and qualifies links, or links whose two verses
share one concept. A cluster is a place to look, not a thread. Your job is to decide whether it
holds a thread, and if so to state it exactly.

Work from /Users/harilakshmanan/Cursor/cosci_knowledge_graph. Do not edit anything there.

## Inputs

- Your packets, named in your instructions. Each lists the verses (with concepts, reading and Tamil)
  and the links (type and the proposer's note).
- The 14 existing threads: `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/threads/existing_threads.md`
  If your cluster covers one of them, write the extended thread and set `replaces` to its id.
- Verse detail (Tamil, Pope, Subramuniyaswami where it exists, and the start of two commentaries):
  `python3 -I scripts/link_pass.py verse 327 550 ...`
- A whole chapter with three commentaries: `python3 -I scripts/chapter_marks.py show N`

Subramuniyaswami's translation is in copyright. Read it as one more witness; never quote it.

## Method

1. Read the packet whole. Group its links by what they show, not by concept label. Ask: what would
   a careful reader learn about the book from these verses taken together that no single verse
   teaches?
2. A thread needs at least three links from the packet whose verses, read in the Tamil, carry the
   claim. Read the Tamil of every verse you build on. Link notes were written by another model and
   may overstate; a link you use must hold on its own verses.
3. Write at most two threads per packet. Zero is a respectable answer: say why in one line.
4. Prefer claims about structure: a term the book awards to different things, a rule stated as
   absolute and then qualified, one logic applied in ethics, statecraft and love, a dispute the
   commentators settle differently. Avoid claims that only restate a chapter's topic.
5. State the claim's scope honestly. "Several verses" is not "the Kural keeps". If the cluster
   contains counter-evidence, say so in `limits`.
6. Attribute. A reading that depends on a commentator names the commentator. Translators' readings
   count as readings, not as the text.

## Output

Write a JSON array to the output path you were given. One object per thread, plus one object per
packet that yields no thread:

    {"candidate": "07", "id": "thread:short_slug", "title": "A question or a short phrase",
     "claim": "Two to four sentences. Cite verse numbers. Say what the verses show together.",
     "limits": "One or two sentences: what this thread does not claim, and any counter-evidence.",
     "links": [[327, 550], [33, 297]],
     "replaces": null}

    {"candidate": "08", "no_thread_reason": "One line."}

Rules for `links`: each pair must appear in your packet, written in the packet's order (a-b);
at least three per thread; use only links whose verses you read. Ids are lowercase with
underscores and must not collide with the existing thread ids unless `replaces` names that id.
Validate that the file parses, every link is in the packet, and every thread has three or more
links. Then reply with only: the thread ids and titles you wrote, and which candidates gave none.
