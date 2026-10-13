#!/usr/bin/env bash
set -euo pipefail    # stop at the first error

python src/01_download_data.py
python src/02_clean.py
python src/03_train.py --seeds 0 1 2 3 4
python src/04_evaluate.py
python src/05_make_figures.py
python src/06_make_tables.py

echo "All results regenerated in results/"
