"""Score the two saved predictions against an adjudicated copy of expert_form.csv."""
import argparse
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def decisions(path, allowed):
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            case, decision = row["case"], row["decision"].strip().lower()
            if case in result or decision not in allowed:
                raise ValueError(f"{path}: duplicate case or invalid decision for {case!r}")
            result[case] = decision
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adjudicated_form", type=Path)
    gold = decisions(parser.parse_args().adjudicated_form, {"accept", "hold", "unresolved"})
    for name in ("baseline", "evidence_first"):
        predictions = decisions(HERE / f"{name}.csv", {"accept", "hold"})
        if gold.keys() != predictions.keys():
            raise ValueError("Expected one adjudicated decision for every packet case")
        scored = [k for k in gold if gold[k] != "unresolved"]
        accepted = [k for k in scored if predictions[k] == "accept"]
        sound = [k for k in scored if gold[k] == "accept"]
        hits = sum(gold[k] == "accept" for k in accepted)
        print(f"{name}: agreement {sum(predictions[k] == gold[k] for k in scored)}/{len(scored)}, "
              f"accept precision {hits}/{len(accepted)}, sound recall {hits}/{len(sound)}, "
              f"expert unresolved {len(gold)-len(scored)}")


if __name__ == "__main__":
    main()
