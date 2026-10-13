import numpy as np
import pandas as pd

df = pd.read_csv("data/raw/network_flows.csv", low_memory=False)

# Consistent, code-friendly column names
df.columns = (df.columns.str.strip().str.lower()
                .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))

# Normalize categorical text
df["protocol"] = df["protocol"].astype("string").str.strip().str.upper()
df["label"] = df["label"].astype("string").str.strip()

# Parse timestamps; invalid values become NaT rather than crashing
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
print(f"Unparseable timestamps: {df['timestamp'].isna().sum()}")

# Infinite values (common in flow statistics) are treated as missing
df = df.replace([np.inf, -np.inf], np.nan)

# Validity check: values that cannot be correct
invalid = (df["flow_duration"] < 0).sum()
print(f"Negative flow durations: {invalid}")
df.loc[df["flow_duration"] < 0, "flow_duration"] = np.nan
