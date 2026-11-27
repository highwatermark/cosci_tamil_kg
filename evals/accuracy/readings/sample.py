"""Print Tamil-only packets for a repeatable, order-stratified reading audit."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOOKS = ("tirumanthiram", "thiruppugazh")


def packet(seed):
    for book in BOOKS:
        with (ROOT / "kg" / "core" / f"{book}.jsonl").open(encoding="utf-8") as source:
            rows = sorted((r for r in map(json.loads, source) if r["tamil"]), key=lambda r: r["number"])
        for third in range(3):
            group = rows[len(rows)*third//3:len(rows)*(third+1)//3]
            ranked = sorted(group, key=lambda r: hashlib.sha256(f"{seed}|{r['id']}".encode()).digest())
            for row in ranked[:2]:
                yield {"id": row["id"], "stratum": third+1, "source": row["source"], "tamil": row["tamil"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="reading-audit-v1")
    for item in packet(parser.parse_args().seed):
        print(json.dumps(item, ensure_ascii=False))
