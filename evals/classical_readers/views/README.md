# Comparing verse links by tradition

These five GraphML exports use the five built book graphs at `72fdf53`. Each retains every readable verse in its chosen books, including isolated verses. Directed edges retain their original relation, AI grade and source JSONL line. The Siddhar nodes carry the attributed poet, work and original unit ID. A graph program can decompress and open these files as GraphML. Filter on edge attribute `audit = sound` to inspect the supported neighbourhood.

| View | Readable verses | Graded links | Sound links | Verses with an internal sound neighbour |
|---|---:|---:|---:|---:|
| [Siddhar anthology](siddhar.graphml.gz) | 2,701 | 437 | 231 | 377 |
| [Devotional songs, Thiruppugazh](devotional.graphml.gz) | 1,325 | 296 | 177 | 264 |
| [Siddhar with Tirumanthiram](siddhar_with_tirumanthiram.graphml.gz) | 5,484 | 2,548 | 1,489 | 1,989 |
| [Devotional with Tirumanthiram](devotional_with_tirumanthiram.graphml.gz) | 4,108 | 2,470 | 1,490 | 1,909 |
| [All five books](five_books.graphml.gz) | 8,539 | 8,011 | 5,322 | 4,747 |

The core devotional selection consists of the marked songs of Arunagirinathar. The core Siddhar selection uses the anthology’s existing work boundary. Tirumanthiram participates in both enlarged views because its yoga and Shaiva devotional arguments are relevant to both inquiries. Kural and Naladiyar supply the remaining books in the five-book reference graph. These are analytical choices. Individual Siddhar verses can be prayers, individual devotional songs can critique empty practice, and a poem may belong to more than one reading tradition. The two enlarged views overlap and their totals cannot be added.

## Do links improve within these views?

| Existing proposals | Sound / all | Sound rate |
|---|---:|---:|
| Both endpoints in Siddhar | 231 / 437 | 52.9% |
| Exactly one endpoint in Siddhar | 453 / 914 | 49.6% |
| Same attributed Siddhar poet | 102 / 154 | 66.2% |
| Different attributed Siddhar poets | 129 / 283 | 45.6% |
| Both endpoints in Thiruppugazh | 177 / 296 | 59.8% |
| Exactly one endpoint in Thiruppugazh | 762 / 1,435 | 53.1% |
| Both endpoints in the devotional view including Tirumanthiram | 1,490 / 2,470 | 60.3% |
| Exactly one endpoint in that enlarged devotional view | 1,095 / 1,991 | 55.0% |
| One Thiruppugazh and one Tirumanthiram endpoint | 338 / 677 | 49.9% |

Repetition, adjacent stanzas, differences among original proposal passes and the number of candidates each reader considered could all influence these figures. Tirumanthiram’s 975 sound internal records contribute heavily to the enlarged devotional view. The most conspicuous distinction inside the anthology is between same-poet and different-poet proposals. Only 377 of 2,701 anthology units currently have a sound anthology neighbour. Another reader should test close-poet and cross-poet discovery separately. Match new proposals by relation type, passage length and whether a refrain repeats. Hide poet identity and previous grades for the first judgment, then reveal attribution and variants for a second judgment. Count accepted discoveries per ten candidates and the number of previously isolated verses reached.

[coverage.csv](coverage.csv) contains the 15 book-pair combinations and each view’s internal and external rates. Sound rates weight each original graded record once. The CSV also reports distinct unordered endpoint pairs, those with at least one sound grade, and those with conflicting grades. On all five books, 8,011 records correspond to 7,963 endpoint pairs and 5,287 distinct pairs carry at least one sound grade. In boundary coverage, only verses inside the named view count in the numerator and denominator. A verse can have both internal and external sound neighbours.

## Rebuild and extend

Run from the repository root.

```sh
python3 -I evals/classical_readers/views/build.py
```

Once a new book has matching verse node and graded edge files, include it explicitly. For example, after Tiruvasagam reaches that stage, build an expanded view in a separate output directory.

```sh
python3 -I evals/classical_readers/views/build.py --view devotional_expanded=thiruppugazh,tirumanthiram,tiruvasagam --out /tmp/tamil-expanded
```

The boundary for a run is the union of books explicitly included and the five reference books. Ingested texts awaiting link grading stay outside the measured denominator. Record the exact revision when comparing snapshots. All five exports were regenerated in a temporary directory and compared byte for byte. Their XML node counts, edge counts and endpoints were checked against the coverage table.
