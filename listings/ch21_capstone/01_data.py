import glob
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_cicids2017(data_dir, sample_frac=None, seed=0):
    frames = []
    for path in sorted(glob.glob(f"{data_dir}/*.csv")):
        part = pd.read_csv(path, low_memory=False, encoding="latin-1")
        part["source_file"] = path.replace("\\", "/").rsplit("/", 1)[-1]
        frames.append(part)
    df = pd.concat(frames, ignore_index=True)
    df.columns = (df.columns.str.strip().str.lower()
                    .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
    n0 = len(df)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    n1 = len(df)
    df = df.drop_duplicates()
    n2 = len(df)
    df["y"] = (df["label"].astype(str).str.strip().str.upper() != "BENIGN").astype(int)
    if sample_frac:   # optional stratified subsample for faster experiments
        df = df.groupby("y", group_keys=False).sample(frac=sample_frac, random_state=seed)
    print(f"Rows loaded: {n0:,}; removed inf/NaN: {n0 - n1:,}; "
          f"removed duplicates: {n1 - n2:,}; final: {len(df):,}")
    print("Attack share:", round(df["y"].mean(), 4))
    return df

def select_features(X_train, corr_threshold=0.95):
    """Variance and correlation filtering, fitted on training data only."""
    vt = VarianceThreshold(threshold=1e-8).fit(X_train)
    cols = X_train.columns[vt.get_support()]
    corr = X_train[cols].corr().abs()
    upper = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1))
    drop = {c for c in upper.columns if (upper[c] > corr_threshold).any()}
    return [c for c in cols if c not in drop]

def prepare_split(df, seed, partition="by_file", n_clients=8):
    """Stratified train/test split, feature selection, scaling, client partition."""
    feats = df.drop(columns=["label", "y", "source_file"]).select_dtypes("number").columns
    train, test = train_test_split(df, test_size=0.2, stratify=df["y"], random_state=seed)
    cols = select_features(train[feats])
    scaler = StandardScaler().fit(train[cols])
    X_tr, X_te = scaler.transform(train[cols]), scaler.transform(test[cols])
    y_tr, y_te = train["y"].to_numpy(), test["y"].to_numpy()

    if partition == "by_file":      # non-IID: each capture file acts as one client
        groups = train["source_file"].to_numpy()
        clients = [(X_tr[groups == g], y_tr[groups == g]) for g in np.unique(groups)]
    else:                           # IID: random assignment
        assign = np.random.default_rng(seed).integers(0, n_clients, size=len(y_tr))
        clients = [(X_tr[assign == k], y_tr[assign == k]) for k in range(n_clients)]
    return X_tr, y_tr, X_te, y_te, clients, cols
