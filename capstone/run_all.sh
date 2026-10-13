#!/usr/bin/env bash
# One command regenerates every capstone result (book Ch. 12 and 21).
#   bash capstone/run_all.sh            # NSL-KDD sample (a few minutes)
#   bash capstone/run_all.sh --quick    # smoke test (about a minute)
#   bash capstone/run_all.sh --dataset cicids2017
set -euo pipefail    # stop at the first error
cd "$(dirname "$0")/.."

python capstone/src/run_experiments.py "$@"
python capstone/src/analyze.py
python capstone/src/make_figures.py

echo "All results regenerated in results/"
