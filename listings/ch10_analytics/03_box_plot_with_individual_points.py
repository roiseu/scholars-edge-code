import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

runs = pd.read_csv("results/tables/per_fold_results.csv")   # columns: method, fold, f1

fig, ax = plt.subplots(figsize=(3.5, 2.6))   # IEEE single-column width
sns.boxplot(data=runs, x="method", y="f1", color="white", width=0.5,
            showfliers=False, ax=ax)
sns.stripplot(data=runs, x="method", y="f1", color="#0072B2", size=4,
              jitter=0.15, ax=ax)
ax.set_xlabel("")
ax.set_ylabel("F1-score per fold")
ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
fig.savefig("results/figures/fig_f1_distribution.pdf")
