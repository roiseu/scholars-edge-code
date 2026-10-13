"""Download the open datasets used in the notebooks and build data/sample/.

Run from the repository root:

    python scripts/build_sample_data.py            # download + build everything
    python scripts/build_sample_data.py --offline  # rebuild derived files only

Everything in data/sample/ is either (a) a copy of an openly licensed public
dataset, (b) a small subset of one, or (c) results computed from them by the
scripts in this folder. See data/README.md for sources, licences and citations.
The two qualitative files (coded_segments.csv, transcripts/) are hand-written
illustrations and are NOT produced by this script.
"""
import argparse
import hashlib
import sys
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample"
CACHE = ROOT / "data" / "raw" / "_downloads"  # git-ignored

SOURCES = {
    # NSL-KDD (Canadian Institute for Cybersecurity, UNB) via a public GitHub mirror
    "KDDTrain+_20Percent.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B_20Percent.txt",
    "KDDTest+.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt",
    # arXiv titles/abstracts/categories (Keras multi-label text classification example)
    "arxiv_data.csv": "https://github.com/soumik12345/multi-label-text-classification/releases/download/v0.2/arxiv_data.csv",
    # Rdatasets mirror of R package datasets
    "bfi.csv": "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/psych/bfi.csv",
    "Prestige.csv": "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/carData/Prestige.csv",
    "sleepstudy.csv": "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/lme4/sleepstudy.csv",
}

TOPIC_PATTERN = (r"federated|intrusion|anomaly detection|privacy|adversarial attack|"
                 r"malware|cyber|security|network traffic|attack detection")


def download(name, url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / name
    if not path.exists():
        print(f"Downloading {name} ...")
        with urlopen(url, timeout=120) as r:
            path.write_bytes(r.read())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    print(f"  {name:28s} {path.stat().st_size / 1e6:7.2f} MB  sha256:{digest}")
    return path


def build_nsl_kdd():
    out = SAMPLE / "nsl_kdd"
    out.mkdir(parents=True, exist_ok=True)
    for name in ["KDDTrain+_20Percent.txt", "KDDTest+.txt"]:
        (out / name).write_bytes((CACHE / name).read_bytes())
    print(f"  -> {out.relative_to(ROOT)}/ (2 files)")


def build_arxiv_sample(n_topic=1300, n_other=1200, seed=42):
    """A ~2,500-paper subset: every security/privacy/federated paper we can find
    (up to n_topic) plus a random background sample of other ML papers."""
    df = pd.read_csv(CACHE / "arxiv_data.csv")
    df = df.rename(columns={"titles": "title", "summaries": "abstract", "terms": "categories"})
    df["title"] = df["title"].str.split().str.join(" ")
    df["abstract"] = df["abstract"].str.split().str.join(" ")
    df["categories"] = (df["categories"].str.strip("[]").str.replace("'", "")
                        .str.replace(" ", ""))
    df = df.drop_duplicates("title")
    text = (df["title"] + " " + df["abstract"]).str.lower()
    topic = df[text.str.contains(TOPIC_PATTERN, regex=True)]
    topic = topic.sample(n=min(n_topic, len(topic)), random_state=seed)
    other = df.drop(topic.index).sample(n=n_other, random_state=seed)
    sample = pd.concat([topic, other]).sample(frac=1, random_state=seed).reset_index(drop=True)
    sample.insert(0, "paper_id", [f"ax{i:05d}" for i in range(len(sample))])
    path = SAMPLE / "arxiv_abstracts_sample.csv"
    sample.to_csv(path, index=False)
    print(f"  -> {path.relative_to(ROOT)} ({len(sample):,} papers, {len(topic):,} on-topic)")
    return sample


def build_database_exports(papers, seed=7):
    """Simulate three bibliographic-database exports (Scopus / IEEE / WoS style)
    from the real arXiv records, with overlapping records and the formatting
    noise that real exports have (case, punctuation, trailing spaces). Used to
    exercise the Chapter 4 de-duplication code."""
    out = SAMPLE / "lit_search_exports"
    out.mkdir(parents=True, exist_ok=True)
    pool = papers[(papers["title"] + " " + papers["abstract"]).str.lower()
                  .str.contains(r"federated|intrusion|anomaly detection|privacy")].copy()
    pool["year"] = ""          # not available in this corpus
    pool["doi"] = ""           # arXiv preprints in this corpus carry no DOI
    for i, name in enumerate(["scopus", "ieee", "wos"]):
        part = pool.sample(frac=0.55, random_state=seed + i).copy()
        if name == "ieee":     # different capitalisation in one export
            part["title"] = part["title"].str.upper()
        if name == "wos":      # trailing punctuation and spaces in another
            part["title"] = part["title"] + ". "
        part[["title", "abstract", "doi", "year"]].to_csv(out / f"{name}.csv", index=False)
        print(f"  -> {(out / (name + '.csv')).relative_to(ROOT)} ({len(part)} records)")


def build_rdatasets():
    bfi = pd.read_csv(CACHE / "bfi.csv").rename(columns={"rownames": "respondent_id"})
    bfi.to_csv(SAMPLE / "bfi_personality.csv", index=False)
    prestige = pd.read_csv(CACHE / "Prestige.csv").rename(columns={"rownames": "occupation"})
    prestige.to_csv(SAMPLE / "prestige_occupations.csv", index=False)
    sleep = pd.read_csv(CACHE / "sleepstudy.csv").drop(columns=["rownames"])
    sleep = sleep.rename(columns={"Reaction": "reaction_ms", "Days": "days", "Subject": "subject"})
    sleep.to_csv(SAMPLE / "sleepstudy_reaction_times.csv", index=False)
    print("  -> data/sample/bfi_personality.csv, prestige_occupations.csv, "
          "sleepstudy_reaction_times.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="use previously downloaded files in data/raw/_downloads")
    args = ap.parse_args()
    SAMPLE.mkdir(parents=True, exist_ok=True)
    print("1. Fetching sources")
    for name, url in SOURCES.items():
        if args.offline and not (CACHE / name).exists():
            sys.exit(f"Missing {CACHE / name}; run without --offline first.")
        download(name, url)
    print("2. Building data/sample/")
    build_nsl_kdd()
    papers = build_arxiv_sample()
    build_database_exports(papers)
    build_rdatasets()
    print("3. Computing model results (scripts/make_model_results.py)")
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_model_results
    make_model_results.main()
    print("Done.")


if __name__ == "__main__":
    main()
