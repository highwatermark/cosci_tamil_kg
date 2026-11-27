"""Reveal saved readings and source references after the reviewer freezes their own gloss."""
import argparse
import json
from pathlib import Path
import runpy

sampling = runpy.run_path(str(Path(__file__).with_name("sample.py")))
ROOT = sampling["ROOT"]


def reveal(items):
    marks = {}
    for book in sampling["BOOKS"]:
        for path in sorted((ROOT / "kg" / "themes" / book).glob("ch*.json")):
            chapter = json.loads(path.read_text(encoding="utf-8"))
            for number, mark in chapter["verses"].items():
                marks[f"{book}:{number}"] = (path.relative_to(ROOT), mark)
    for item in items:
        path, mark = marks[item["id"]]
        edition = Path("data/text") / (item["source"] + ".txt")
        lines = (ROOT / edition).read_text(encoding="utf-8").splitlines()
        matches = [n for n, line in enumerate(lines, 1) if item["tamil"][0] in line]
        yield {
            "id": item["id"],
            "edition": str(edition),
            "first_line_matches": matches,
            "marks": str(path),
            "reading": mark["reading"],
            "nuance": mark.get("nuance"),
            "flagged_uncertain": mark.get("uncertain", False),
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="reading-audit-v1")
    for row in reveal(sampling["packet"](parser.parse_args().seed)):
        print(json.dumps(row, ensure_ascii=False))
