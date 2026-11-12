#!/usr/bin/env bash
set -euo pipefail
python -m unittest discover -s tests -v
python -m tutor_policy_bench.cli --seeds 10
