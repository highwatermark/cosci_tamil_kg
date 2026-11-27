"""Emit Tamil-only review cases from built graph IDs or canonical core IDs."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PILOT = """siddhar:127 siddhar:295 siddhar:2414 siddhar:2635 siddhar:2
kural:355 naladiyar:47 tirumanthiram:725 thiruppugazh:1087 thiruppugazh:344""".split()


def packet(ids):
    wanted = set(ids)
    found = {}
    for book in sorted({i.split(":")[0] for i in ids}):
        if not book.isidentifier():
            raise ValueError(book)
        node_path = ROOT / "kg" / book / "nodes.jsonl"
        if node_path.exists():
            with node_path.open() as f:
                for node in map(json.loads, f):
                    if node["id"] in wanted and node["type"] == "Verse" and node["tamil"]:
                        found[node["id"]] = node["tamil"]
        if all(i in found for i in wanted if i.split(":")[0] == book):
            continue
        sources = [ROOT / "kg/core" / f"{book}.jsonl"]
        if book == "pattupattu":
            sources.append(ROOT / "kg/core/pattupattu_units.jsonl")
        for source in sources:
            if source.exists():
                with source.open() as f:
                    for row in map(json.loads, f):
                        if row.get("id") in wanted and row.get("tamil"):
                            found.setdefault(row["id"], row["tamil"])
    if wanted - found.keys():
        raise ValueError(f"Unknown or empty Tamil units: {sorted(wanted-found.keys())}")
    return [{"case": i, "tamil": found[i]} for i in ids]


if __name__ == "__main__":
    print(json.dumps(packet(sys.argv[1:] or PILOT), ensure_ascii=False, indent=2))
