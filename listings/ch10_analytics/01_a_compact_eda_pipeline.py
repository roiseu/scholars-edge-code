import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/processed/research_dataset.csv")

print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(df.dtypes.value_counts())
print(df.describe(include="all").T.round(3))
print("Outcome balance:\n", df["label"].value_counts(normalize=True).round(3))

num_cols = df.select_dtypes(include="number").columns.tolist()

# Univariate: histograms of numeric features
n = len(num_cols)
rows = int(np.ceil(n / 3))
fig, axes = plt.subplots(rows, 3, figsize=(12, 3 * rows))
axes = np.atleast_1d(axes).ravel()
for ax, col in zip(axes, num_cols):
    ax.hist(df[col].dropna(), bins=40, color="#0072B2", alpha=0.8)
    ax.set_title(f"{col} (skew = {df[col].skew():.2f})", fontsize=9)
for ax in axes[n:]:
    ax.set_visible(False)
fig.tight_layout()
fig.savefig("results/figures/eda_univariate.png", dpi=200)

# Bivariate: correlation heatmap (lower triangle only)
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, mask=mask, cmap="vlag", center=0, vmin=-1, vmax=1,
            annot=len(num_cols) <= 12, fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Feature correlation matrix")
fig.tight_layout()
fig.savefig("results/figures/eda_correlation.png", dpi=200)
