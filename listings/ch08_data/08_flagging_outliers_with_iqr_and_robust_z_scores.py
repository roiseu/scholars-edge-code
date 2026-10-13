import pandas as pd

def flag_iqr(s, k=1.5):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (s < q1 - k * iqr) | (s > q3 + k * iqr)

def flag_robust_z(s, threshold=3.5):
    """Robust z-score based on the median absolute deviation (MAD)."""
    med = s.median()
    mad = (s - med).abs().median()
    if mad == 0:
        return pd.Series(False, index=s.index)
    return (0.6745 * (s - med) / mad).abs() > threshold

summary = []
for col in X_train.select_dtypes(include="number").columns:
    s = X_train[col].dropna()
    summary.append({"feature": col,
                    "iqr_flags": int(flag_iqr(s).sum()),
                    "robust_z_flags": int(flag_robust_z(s).sum())})
print(pd.DataFrame(summary).sort_values("robust_z_flags", ascending=False).head(10))

# Option: cap (winsorize) extreme values, with limits learned from training data
lo, hi = X_train["flow_bytes_s"].quantile([0.01, 0.99])
X_train["flow_bytes_s"] = X_train["flow_bytes_s"].clip(lo, hi)
X_test["flow_bytes_s"] = X_test["flow_bytes_s"].clip(lo, hi)
