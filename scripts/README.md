# scripts/

| Script | What it does |
|---|---|
| `build_sample_data.py` | Downloads every open dataset from its source URL into `data/raw/_downloads/`, then rebuilds `data/sample/` (subsets, simulated database exports, renamed columns) and calls `make_model_results.py`. |
| `make_model_results.py` | Trains four classifiers on NSL-KDD (10 seeds; 5-fold CV) and writes `model_results.csv` and `per_fold_results.csv`. |
| `check_setup.py` | The Appendix A environment check, as a command-line script. |
