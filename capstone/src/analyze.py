"""Summaries and equivalence tests (book Ch. 21, Phase 5).

    python capstone/src/analyze.py
"""
from pathlib import Path

import pandas as pd
from statsmodels.stats.weightstats import ttost_paired
from statsmodels.stats.multitest import multipletests

TABLES = Path(__file__).resolve().parents[2] / "results" / "tables"
MARGIN = 0.01   # preregistered equivalence margin for F1


def main():
    runs = pd.read_csv(TABLES / "capstone_runs.csv")

    summary = (runs.groupby("method", sort=False)[["accuracy", "precision", "recall", "f1", "auc", "mia_auc"]]
                   .agg(["mean", "std"]).round(4))
    print(summary)
    summary.to_csv(TABLES / "summary.csv")

    f1 = runs.pivot_table(index="seed", columns="method", values="f1")
    base = f1["Centralized LR"]

    tests = []
    for method in [m for m in f1.columns if m.startswith("FedAvg")]:
        diff = f1[method] - base
        p, _, _ = ttost_paired(f1[method].to_numpy(), base.to_numpy(), -MARGIN, MARGIN)
        tests.append({"method": method, "mean_diff": diff.mean(),
                      "sd_diff": diff.std(ddof=1), "p_tost": p})

    eq = pd.DataFrame(tests)
    eq["p_tost_holm"] = multipletests(eq["p_tost"], method="holm")[1]
    eq["equivalent_at_0.05"] = eq["p_tost_holm"] < 0.05
    print(eq.round(4))
    eq.to_csv(TABLES / "equivalence_tests.csv", index=False)


if __name__ == "__main__":
    main()
