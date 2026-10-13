"""Privacy-utility and privacy-attack figures from the capstone runs (Ch. 10 style).

    python capstone/src/make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RESULTS = Path(__file__).resolve().parents[2] / "results"
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9"]
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 42})


def main():
    runs = pd.read_csv(RESULTS / "tables" / "capstone_runs.csv")
    dp = runs.dropna(subset=["epsilon"]).groupby("epsilon")[["f1", "mia_auc"]].agg(["mean", "std"])
    ref = runs[runs["epsilon"].isna()].groupby("method")[["f1", "mia_auc"]].mean()

    fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.6))
    for ax, metric, title in [(axes[0], "f1", "(a) Detection F1"),
                              (axes[1], "mia_auc", "(b) Membership-inference AUC")]:
        ax.errorbar(dp.index, dp[(metric, "mean")], yerr=dp[(metric, "std")], fmt="o-",
                    color=OKABE_ITO[2], capsize=3, label="FedAvg + DP-SGD")
        for (name, row), c in zip(ref.iterrows(), [OKABE_ITO[0], OKABE_ITO[1], OKABE_ITO[3]]):
            ax.axhline(row[metric], ls="--", lw=1, color=c, label=name)
        ax.set_xscale("log")
        ax.set_xticks(dp.index, [f"{e:g}" for e in dp.index])
        ax.minorticks_off()
        ax.set_xlabel(r"Privacy budget $\varepsilon$ (log scale)")
        ax.set_title(title, loc="left")
        ax.grid(alpha=0.3)
    axes[1].axhline(0.5, color="gray", lw=0.8)
    axes[1].legend(frameon=False, fontsize=7, loc="upper left")
    fig.tight_layout()
    (RESULTS / "figures").mkdir(parents=True, exist_ok=True)
    fig.savefig(RESULTS / "figures" / "capstone_privacy_tradeoff.pdf")
    fig.savefig(RESULTS / "figures" / "capstone_privacy_tradeoff.png")
    print("Saved results/figures/capstone_privacy_tradeoff.{pdf,png}")


if __name__ == "__main__":
    main()
