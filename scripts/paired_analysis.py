"""Paired comparisons and the retention ablation behind the numbers in the README.

Run from the repository root after the main experiment:
    python scripts/paired_analysis.py --episodes outputs/episode_results.csv
"""
import argparse
import csv
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tutor_policy_bench.simulator import PROFILES, run_episode  # noqa: E402

BASELINES = ("direct_answer", "fixed_hint", "bkt_threshold", "random")
METRICS = ("delayed_transfer_accuracy", "immediate_accuracy", "mastery_gain")


def paired(rows, a, b, metric):
    """Mean difference a - b over matching (seed, profile, noise, mismatch) cells."""
    cell = lambda r: (r["seed"], r["profile"], r["observation_noise"], r["model_mismatch"])
    left = {cell(r): float(r[metric]) for r in rows if r["policy"] == a}
    right = {cell(r): float(r[metric]) for r in rows if r["policy"] == b}
    diffs = [left[k] - right[k] for k in left if k in right]
    half = 1.96 * statistics.stdev(diffs) / math.sqrt(len(diffs))
    return statistics.mean(diffs), half, len(diffs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", default="outputs/episode_results.csv")
    parser.add_argument("--out", default="outputs/paired_differences.csv")
    args = parser.parse_args()

    rows = list(csv.DictReader(open(args.episodes, encoding="utf-8")))
    out = []
    for b in BASELINES:
        for metric in METRICS:
            mean, half, n = paired(rows, "multi_agent", b, metric)
            out.append({"comparison": "multi_agent - " + b, "metric": metric, "mean_difference": round(mean, 4),
                        "ci95_low": round(mean - half, 4), "ci95_high": round(mean + half, 4), "n_pairs": n})
            print("%-30s %-27s %+.3f  [%+.3f, %+.3f]" % (out[-1]["comparison"], metric, mean, mean - half, mean + half))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out)

    # Ablation: switch retention decay off and see whether the ranking holds.
    seeds = sorted({int(r["seed"]) for r in rows})
    noises = sorted({float(r["observation_noise"]) for r in rows})
    mismatches = sorted({float(r["model_mismatch"]) for r in rows})
    print("\nDelayed transfer with and without retention decay")
    for policy in ("direct_answer", "fixed_hint", "bkt_threshold", "multi_agent"):
        values = []
        for scale in (1.0, 0.0):
            values.append(statistics.mean(
                run_episode(s, p, policy, n, m, decay_scale=scale)["delayed_transfer_accuracy"]
                for s in seeds for p in PROFILES for n in noises for m in mismatches))
        print("%-15s decay on %.3f   decay off %.3f" % (policy, values[0], values[1]))


if __name__ == "__main__":
    main()
