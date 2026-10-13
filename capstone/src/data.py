"""Loading, cleaning, and splitting (book Ch. 21, Phase 2).

`load_cicids2017` and `prepare_split` are the book's code. `load_nsl_kdd`
returns the open NSL-KDD sample in exactly the same shape, so the rest of the
pipeline does not care which dataset it gets.
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

# Columns that are never model features
META_COLUMNS = ["label", "y", "source_file", "client_group", "attack_family", "difficulty"]


def _clean(df):
    df.columns = (df.columns.str.strip().str.lower()
                    .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
    n0 = len(df)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    n1 = len(df)
    df = df.drop_duplicates()
    n2 = len(df)
    df["y"] = (df["label"].astype(str).str.strip().str.upper() != "BENIGN").astype(int)
    print(f"Rows loaded: {n0:,}; removed inf/NaN: {n0 - n1:,}; "
          f"removed duplicates: {n1 - n2:,}; final: {len(df):,}")
    return df


def _subsample(df, sample_frac, seed):
    if sample_frac:   # optional stratified subsample for faster experiments
        df = df.groupby("y", group_keys=False).sample(frac=sample_frac, random_state=seed)
    print("Attack share:", round(df["y"].mean(), 4))
    return df


def load_cicids2017(data_dir, sample_frac=None, seed=0):
    """The book's loader: the eight CICIDS2017 MachineLearningCSV files."""
    frames = []
    for path in sorted(glob.glob(f"{data_dir}/*.csv")):
        part = pd.read_csv(path, low_memory=False, encoding="latin-1")
        part["source_file"] = path.replace("\\", "/").rsplit("/", 1)[-1]
        frames.append(part)
    if not frames:
        raise FileNotFoundError(f"No CSV files in {data_dir}. See data/README.md.")
    df = _clean(pd.concat(frames, ignore_index=True))
    df["client_group"] = df["source_file"]     # each capture day = one client
    return _subsample(df, sample_frac, seed)


def load_nsl_kdd(sample_frac=None, seed=0):
    """Open NSL-KDD sample, shaped like the CICIDS2017 output above.

    Federated clients: NSL-KDD has no capture-day files, so records are grouped
    by `protocol_type` (tcp / udp / icmp). The three clients differ strongly in
    size and attack mix, which gives the same kind of non-IID split the book
    studies with CICIDS2017's per-day files.
    """
    from scholarsedge.datasets import load_nsl_kdd as _load
    raw = _load().drop(columns=["difficulty"])   # difficulty is derived from the label
    df = _clean(raw)
    df["client_group"] = df["protocol_type"]
    return _subsample(df, sample_frac, seed)


def load_dataset(name, sample_frac=None, seed=0):
    if name == "nsl_kdd":
        return load_nsl_kdd(sample_frac, seed)
    if name == "cicids2017":
        return load_cicids2017(REPO / "data" / "raw" / "cicids2017", sample_frac, seed)
    raise ValueError(f"Unknown dataset {name!r}")


def select_features(X_train, corr_threshold=0.95):
    """Variance and correlation filtering, fitted on training data only."""
    vt = VarianceThreshold(threshold=1e-8).fit(X_train)
    cols = X_train.columns[vt.get_support()]
    corr = X_train[cols].corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1))
    drop = {c for c in upper.columns if (upper[c] > corr_threshold).any()}
    return [c for c in cols if c not in drop]


def prepare_split(df, seed, partition="by_file", n_clients=8):
    """Stratified train/test split, feature selection, scaling, client partition.

    partition="by_file": non-IID, one client per value of `client_group`
    partition="iid":     random assignment to `n_clients` clients
    """
    feats = (df.drop(columns=[c for c in META_COLUMNS if c in df.columns])
               .select_dtypes("number").columns)
    train, test = train_test_split(df, test_size=0.2, stratify=df["y"], random_state=seed)
    cols = select_features(train[feats])
    scaler = StandardScaler().fit(train[cols])
    X_tr, X_te = scaler.transform(train[cols]), scaler.transform(test[cols])
    y_tr, y_te = train["y"].to_numpy(), test["y"].to_numpy()

    if partition == "by_file":      # non-IID: each group acts as one client
        groups = train["client_group"].to_numpy()
        clients = [(X_tr[groups == g], y_tr[groups == g]) for g in np.unique(groups)]
    else:                           # IID: random assignment
        assign = np.random.default_rng(seed).integers(0, n_clients, size=len(y_tr))
        clients = [(X_tr[assign == k], y_tr[assign == k]) for k in range(n_clients)]
    return X_tr, y_tr, X_te, y_te, clients, cols
