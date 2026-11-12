#!/usr/bin/env python3
import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

def calibrate(input_path, output_path):
    aggregates = defaultdict(lambda: {"n": 0, "correct": 0, "hints": [], "attempts": [], "times": []})
    with open(input_path, "r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"skill_id", "correct"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
        for row in reader:
            if row.get("original") and row.get("original").strip() not in ("1", "1.0"):
                continue
            if row.get("tutor_mode") and row.get("tutor_mode").strip().lower() != "tutor":
                continue
            skill = (row.get("skill_id") or "").strip()
            correct = (row.get("correct") or "").strip()
            if not skill or correct not in ("0", "1"):
                continue
            record = aggregates[skill]
            record["n"] += 1
            record["correct"] += int(correct)
            for source, target in (("hint_count", "hints"), ("attempt_count", "attempts"),
                                   ("ms_first_response", "times")):
                try:
                    value = float((row.get(source) or "").strip())
                except (TypeError, ValueError):
                    continue
                if value >= 0:
                    record[target].append(value)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["skill_id", "n_interactions", "correct_rate", "mean_hint_count",
              "mean_attempt_count", "median_response_ms"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for skill, record in sorted(aggregates.items()):
            writer.writerow({
                "skill_id": skill, "n_interactions": record["n"],
                "correct_rate": record["correct"] / float(record["n"]),
                "mean_hint_count": statistics.mean(record["hints"]) if record["hints"] else "",
                "mean_attempt_count": statistics.mean(record["attempts"]) if record["attempts"] else "",
                "median_response_ms": statistics.median(record["times"]) if record["times"] else "",
            })
    return len(aggregates)

def main():
    parser = argparse.ArgumentParser(description="Aggregate ASSISTments skill-level descriptive priors")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/derived/assistments_skill_priors.csv")
    args = parser.parse_args()
    print("Skills aggregated:", calibrate(args.input, args.output))
    print("Output:", args.output)

if __name__ == "__main__":
    main()
