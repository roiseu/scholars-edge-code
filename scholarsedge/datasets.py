"""Paths and loaders for the sample datasets in data/sample/.

Every notebook starts with:

    from scholarsedge.datasets import ROOT, SAMPLE, RESULTS, load_nsl_kdd, ...

so that the same code works no matter which folder Jupyter was started from.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SAMPLE = DATA / "sample"
RAW = DATA / "raw"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"
TABLES = RESULTS / "tables"
for _p in (FIGURES, TABLES):
    _p.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# NSL-KDD: the open network-intrusion dataset used in place of CICIDS2017
# --------------------------------------------------------------------------
NSL_KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate", "label", "difficulty",
]

# Standard grouping of NSL-KDD attack names into the four classic families
ATTACK_FAMILY = {
    **dict.fromkeys(["back", "land", "neptune", "pod", "smurf", "teardrop", "apache2",
                     "mailbomb", "processtable", "udpstorm"], "DoS"),
    **dict.fromkeys(["ipsweep", "nmap", "portsweep", "satan", "mscan", "saint"], "Probe"),
    **dict.fromkeys(["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy",
                     "warezclient", "warezmaster", "named", "sendmail", "snmpgetattack",
                     "snmpguess", "worm", "xlock", "xsnoop", "httptunnel"], "R2L"),
    **dict.fromkeys(["buffer_overflow", "loadmodule", "perl", "rootkit", "ps",
                     "sqlattack", "xterm"], "U2R"),
}


def load_nsl_kdd(benign_label="BENIGN"):
    """Load the NSL-KDD sample (KDDTrain+_20Percent + KDDTest+, 47,736 records).

    The book's code is written for CICIDS2017, where benign traffic is labelled
    "BENIGN". To let that code run unchanged, NSL-KDD's "normal" label is
    renamed to `benign_label` (pass benign_label="normal" to keep the original).

    Added columns:
      source_file   which of the two original files the record came from
      attack_family BENIGN / DoS / Probe / R2L / U2R
    """
    folder = SAMPLE / "nsl_kdd"
    frames = []
    for name in ["KDDTrain+_20Percent.txt", "KDDTest+.txt"]:
        part = pd.read_csv(folder / name, header=None, names=NSL_KDD_COLUMNS)
        part["source_file"] = name
        frames.append(part)
    df = pd.concat(frames, ignore_index=True)
    df["label"] = df["label"].replace({"normal": benign_label})
    df["attack_family"] = df["label"].map(ATTACK_FAMILY).fillna(benign_label)
    return df


def load_nsl_kdd_xy():
    """Numeric feature matrix X and binary target y (1 = attack) for quick examples."""
    df = load_nsl_kdd()
    y = (df["label"] != "BENIGN").astype(int).to_numpy()
    X = df.drop(columns=["label", "difficulty", "attack_family", "source_file"])
    X = X.select_dtypes("number")
    return X, y


# --------------------------------------------------------------------------
# Other samples
# --------------------------------------------------------------------------
def load_arxiv_sample():
    """~2,500 real arXiv papers: paper_id, title, abstract, categories."""
    return pd.read_csv(SAMPLE / "arxiv_abstracts_sample.csv")


def load_bfi():
    """Big Five Inventory items (2,800 respondents; psych::bfi via Rdatasets)."""
    return pd.read_csv(SAMPLE / "bfi_personality.csv")


def load_prestige():
    """Prestige of 102 Canadian occupations, 1971 (carData::Prestige)."""
    return pd.read_csv(SAMPLE / "prestige_occupations.csv")


def load_sleepstudy():
    """Reaction times (ms) under sleep deprivation (lme4::sleepstudy)."""
    return pd.read_csv(SAMPLE / "sleepstudy_reaction_times.csv")
