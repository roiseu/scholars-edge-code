import pandas as pd
from statsmodels.stats.weightstats import ttost_paired
from statsmodels.stats.multitest import multipletests

runs = pd.read_csv("results/tables/capstone_runs.csv")

summary = (runs.groupby("method")[["accuracy", "precision", "recall", "f1", "auc", "mia_auc"]]
               .agg(["mean", "std"]).round(4))
print(summary)
summary.to_csv("results/tables/summary.csv")

MARGIN = 0.01   # preregistered equivalence margin for F1
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
eq.to_csv("results/tables/equivalence_tests.csv", index=False)
