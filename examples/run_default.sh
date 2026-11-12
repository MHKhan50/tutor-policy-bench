#!/usr/bin/env bash
set -euo pipefail
python -m unittest discover -s tests -v
python -m tutor_policy_bench.cli --seeds 30 --policies direct_answer fixed_hint bkt_threshold multi_agent random
python scripts/paired_analysis.py
