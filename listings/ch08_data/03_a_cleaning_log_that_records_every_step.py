import pandas as pd

class CleaningLog:
    """Record row and column counts after each cleaning step."""
    def __init__(self, df):
        self.steps = [("Loaded raw data", len(df), df.shape[1])]

    def record(self, step, df):
        self.steps.append((step, len(df), df.shape[1]))
        return df

    def report(self):
        out = pd.DataFrame(self.steps, columns=["step", "rows", "columns"])
        out["rows_removed"] = (-out["rows"].diff()).fillna(0).astype(int)
        return out

df = pd.read_csv("data/raw/network_flows.csv", low_memory=False)
log = CleaningLog(df)
df = log.record("Removed exact duplicates", df.drop_duplicates())
df = log.record("Dropped rows without a label", df.dropna(subset=["label"]))
print(log.report().to_string(index=False))
