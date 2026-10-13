import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": 300, "savefig.bbox": "tight",
    "pdf.fonttype": 42,          # embed fonts as TrueType (required by many publishers)
})
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9"]

# Panel (a): F1-score by model, mean +/- SD over 5 folds
models = ["Random Forest", "XGBoost", "FedIDS (eps = 1.0)", "FedIDS (eps = 0.1)"]
f1_mean = np.array([0.974, 0.970, 0.967, 0.908])
f1_sd = np.array([0.002, 0.003, 0.004, 0.009])

# Panel (b): accuracy across privacy budgets
eps = np.array([0.1, 0.5, 1.0, 5.0, 10.0])
acc = np.array([91.2, 95.4, 96.8, 97.1, 97.2])
acc_sd = np.array([0.8, 0.5, 0.4, 0.3, 0.3])
acc_no_dp = 97.5

fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.6))   # IEEE double-column width

y = np.arange(len(models))
axes[0].errorbar(f1_mean, y, xerr=f1_sd, fmt="o", color=OKABE_ITO[0],
                 ecolor="gray", capsize=3)
axes[0].set_yticks(y)
axes[0].set_yticklabels(models)
axes[0].invert_yaxis()
axes[0].set_xlabel("F1-score (mean $\\pm$ SD, 5 folds)")
axes[0].set_title("(a) Detection performance", loc="left")
axes[0].grid(axis="x", alpha=0.3)

axes[1].errorbar(eps, acc, yerr=acc_sd, fmt="o-", color=OKABE_ITO[2],
                 capsize=3, label="FedIDS with DP")
axes[1].axhline(acc_no_dp, ls="--", color=OKABE_ITO[3], label="Federated, no DP")
axes[1].set_xscale("log")
axes[1].set_xlabel(r"Privacy budget $\varepsilon$ (log scale)")
axes[1].set_ylabel("Accuracy (%)")
axes[1].set_title("(b) Privacy-accuracy trade-off", loc="left")
axes[1].legend(frameon=False, fontsize=8)
axes[1].grid(alpha=0.3)

fig.tight_layout()
fig.savefig("results/figures/fig_results.pdf")
fig.savefig("results/figures/fig_results.png")
