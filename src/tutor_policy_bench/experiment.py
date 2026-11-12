import csv
import json
import math
import platform
import statistics
import sys
from pathlib import Path
from .simulator import PROFILES, run_episode

DEFAULT_POLICIES = ("direct_answer", "fixed_hint", "bkt_threshold", "multi_agent")
METRICS = ("immediate_accuracy", "delayed_transfer_accuracy", "mastery_gain", "hint_count",
           "answer_reveal_count", "interaction_cost", "budget_rejections")

def summary_stats(values):
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if len(values) > 1 else 0.0
    half = 1.96 * sd / math.sqrt(len(values)) if len(values) > 1 else 0.0
    return mean, sd, mean - half, mean + half

def run_experiment(seeds=10, output_dir="outputs", policies=None,
                   noise_levels=(0.0, 0.10, 0.25), mismatch_levels=(0.0, 0.15, 0.30),
                   ollama_policy=None):
    policies = tuple(policies or DEFAULT_POLICIES)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in range(seeds):
        for profile in PROFILES:
            for noise in noise_levels:
                for mismatch in mismatch_levels:
                    for policy in policies:
                        rows.append(run_episode(seed, profile, policy, noise, mismatch,
                                                ollama_policy=ollama_policy))
    with (out / "episode_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    groups = {}
    for row in rows:
        key = (row["profile"], row["policy"], row["observation_noise"], row["model_mismatch"])
        groups.setdefault(key, []).append(row)
    summaries = []
    for key, group in sorted(groups.items()):
        item = {"profile": key[0], "policy": key[1], "observation_noise": key[2],
                "model_mismatch": key[3], "n_seeds": len(group)}
        for metric in METRICS:
            mean, sd, low, high = summary_stats([float(row[metric]) for row in group])
            item[metric + "_mean"] = mean
            item[metric + "_sd"] = sd
            item[metric + "_ci95_low"] = low
            item[metric + "_ci95_high"] = high
        summaries.append(item)
    with (out / "policy_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)
    metadata = {
        "benchmark": "TutorPolicyBench", "version": "0.1.0", "seeds": seeds,
        "episodes": len(rows), "profiles": list(PROFILES), "policies": list(policies),
        "noise_levels": list(noise_levels), "mismatch_levels": list(mismatch_levels),
        "python": sys.version, "platform": platform.platform(),
        "data_status": "synthetic_only_unless_separate_ASSISTments_calibration_is_run",
        "interval_note": "descriptive normal approximation; use paired seed-level analysis for research"
    }
    (out / "summary.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata
