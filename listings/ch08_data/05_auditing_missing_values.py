import pandas as pd

missing = pd.DataFrame({
    "count": df.isna().sum(),
    "pct": (df.isna().mean() * 100).round(2),
})
missing = missing[missing["count"] > 0].sort_values("pct", ascending=False)
print(missing)

# Columns missing in most rows are often better dropped -- but justify and report it
high_missing = missing.index[missing["pct"] > 40].tolist()
print(f"Candidates for removal (>40% missing): {high_missing}")
