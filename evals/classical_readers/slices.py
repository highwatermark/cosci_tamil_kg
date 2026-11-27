"""Find readings by existing concept tags across the five books, or extract the grammar lenses."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh", "siddhar")
LENSES = {
    "inward-divinity": "sivam iraivan meyyunarvu",
    "ego-and-stillness": "agandhai pattru mounam samaadhi",
    "care-for-life": "anbu thondu eegai kollaamai oppuravu",
    "social-and-ritual-authority": "theettu theerththam vazhipaadu vesham aagamam",
    "knowing-and-experience": "arivu therithal aaraaydhal gnaanam",
    "body-and-liberation": "yaakkai uyir veedu padhamukthi",
    "breath-and-senses": "vaasi praanan naadi kundalini adakkam",
    "medicine-and-longevity": "marundhu noy karpam aayul",
    "alchemy-and-cipher": "vaadham paripaashai sootcham",
    "devotional-address": "paththi arul thiruvarul thiruvadi adaikkalam",
}
GRAMMAR = {
    "porul:8:1": "Record utterance, hearer, scene and time before inferring doctrine.",
    "porul:7:1": "Specify which property transfers in a comparison: action, effect, bodily quality or form.",
    "porul:6:3": "Distinguish a represented affect from the poet's own state.",
    "porul:1:49": "Compare an implicit image with an overt simile; record the clues and a rival reading.",
    "porul:2:23": "Test a love-poetry reading of divine address and record the limits of its extension.",
    "porul:1:3": "Distinguish setting, associated things and the human situation they frame.",
}


def records(path):
    with path.open() as f:
        yield from map(json.loads, f)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lens", choices=["grammar", *LENSES])
    parser.add_argument("--book", choices=BOOKS)
    parser.add_argument("--all-tags", action="store_true", help="Require every selected concept")
    args = parser.parse_args()
    if args.lens == "grammar":
        for row in records(ROOT / "kg/core/tholkappiyam.jsonl"):
            key = row["id"].removeprefix("tholkappiyam:")
            if key in GRAMMAR:
                print(json.dumps(dict(id=row["id"], tamil=row["tamil"], source=row["source"],
                                      review_question=GRAMMAR[key]), ensure_ascii=False))
        return
    tags = set(LENSES[args.lens].split())
    for book in ([args.book] if args.book else BOOKS):
        folder = ROOT / "kg" / book
        matches = {}
        for e in records(folder / "edges.jsonl"):
            if e["p"] == "EXPRESSES" and e["o"].removeprefix("concept:") in tags:
                matches.setdefault(e["s"], set()).add(e["o"].removeprefix("concept:"))
        for row in records(folder / "nodes.jsonl"):
            found = matches.get(row["id"])
            if found and (not args.all_tags or found == tags):
                print(json.dumps(dict(id=row["id"], unit_id=row.get("unit_id", row["id"]),
                                      matched=sorted(found), tamil=row["tamil"], reading=row["reading"]),
                                 ensure_ascii=False))


if __name__ == "__main__":
    main()
