# Data

```
data/
├── sample/   small open datasets, committed to the repo, used by every notebook
└── raw/      large/full datasets you download yourself (git-ignored)
```

Everything in `sample/` can be rebuilt with `python scripts/build_sample_data.py`,
except the hand-written qualitative illustration (see the last row).

## What is in `data/sample/` and where it came from

| File | Used in | What it is | Source and licence |
|---|---|---|---|
| `nsl_kdd/KDDTrain+_20Percent.txt`, `nsl_kdd/KDDTest+.txt` | Ch 8, 10, 13, 21 | 47,736 labelled network connection records (41 features; normal vs. DoS / Probe / R2L / U2R attacks). **Stands in for CICIDS2017**, which is too large to commit. | NSL-KDD, Canadian Institute for Cybersecurity, University of New Brunswick (<https://www.unb.ca/cic/datasets/nsl.html>), from the public mirror `github.com/defcom17/NSL_KDD`. Free for research use; cite Tavallaee et al. (2009). |
| `arxiv_abstracts_sample.csv` | Ch 4, 8 | 2,500 real arXiv papers (title, abstract, categories): 1,300 on security, privacy, federated learning and anomaly detection, plus 1,200 other ML papers as background. | arXiv metadata (CC0 1.0), taken from the dataset published with the Keras multi-label text classification example (`github.com/soumik12345/multi-label-text-classification`, release v0.2). |
| `lit_search_exports/{scopus,ieee,wos}.csv` | Ch 4 | Three *simulated* database exports built from the arXiv sample: overlapping records with case and punctuation differences, to exercise de-duplication. | Derived from the row above by `build_sample_data.py`. |
| `bfi_personality.csv` | Ch 5 | 25 Big Five personality items (6-point Likert) from 2,800 respondents, plus gender, education and age. | `psych::bfi` (Revelle, SAPA project), via Rdatasets. R package licence GPL (>= 2). |
| `prestige_occupations.csv` | Ch 7 | Prestige, education, income and type for 102 Canadian occupations (1971 census). | `carData::Prestige` (Fox & Weisberg), via Rdatasets. GPL (>= 2). |
| `sleepstudy_reaction_times.csv` | Ch 7 | Reaction times in ms for 18 subjects over 10 days of sleep restriction. | `lme4::sleepstudy` (Belenky et al., 2003), via Rdatasets. GPL (>= 2). |
| `model_results.csv`, `per_fold_results.csv` | Ch 7, 10 | Real results of running logistic regression, decision tree, random forest and gradient boosting on NSL-KDD (10 seeds; 5-fold CV). | Computed by `scripts/make_model_results.py`. |
| `qualitative/transcripts/P01–P08.txt`, `qualitative/coded_segments.csv` | Ch 9 | Eight short interview transcripts with security-operations analysts and an exported code table. | **Illustrative, written for this repository.** These are not real participants. They exist so the Chapter 9 code has something to run on. |

## How the book's file names map to these samples

The book's listings use file names from its running example (a federated
intrusion-detection study). The notebooks swap in these open datasets:

| Book listing reads… | Notebook uses… |
|---|---|
| `data/raw/network_flows.csv`, CICIDS2017 | `nsl_kdd/` (via `scholarsedge.datasets.load_nsl_kdd()`) |
| `scopus.csv`, `ieee.csv`, `wos.csv` | `lit_search_exports/*.csv` |
| `included_abstracts.csv`, `data/processed/papers.csv` | `arxiv_abstracts_sample.csv` (or a live arXiv download) |
| `survey_responses.csv` (`trust1..trust5`) | `bfi_personality.csv` (`A1..A5`, agreeableness) |
| `latency_measurements.csv` (`latency_ms`) | `sleepstudy_reaction_times.csv` (`reaction_ms`) |
| `phishing_study.csv` | `prestige_occupations.csv` |
| `model_results.csv`, `per_fold_results.csv` | same names, real NSL-KDD results |
| `coded_segments.csv`, `transcripts/` | `qualitative/` |

## Full datasets (optional, for the real experiments)

**CICIDS2017** (used by the capstone in the book, about 2.8 million flows):

1. Request and download the *MachineLearningCSV* files from
   <https://www.unb.ca/cic/datasets/ids-2017.html>.
2. Unzip the eight CSV files into `data/raw/cicids2017/`.
3. Run the capstone with `--dataset cicids2017` (see `capstone/README.md`).

**arXiv live data**: the Chapter 3 and 8 notebooks call the arXiv API directly
when you have internet access, and fall back to the sample otherwise.

**Stack Overflow on BigQuery** (Chapter 11): `bigquery-public-data.stackoverflow`
is queried in place; you need a Google Cloud project, not a download.

## Citations

- Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009). A detailed analysis of the KDD CUP 99 data set. *IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA)*.
- Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward generating a new intrusion detection dataset and intrusion traffic characterization. *ICISSP* (CICIDS2017).
- Revelle, W. *psych: Procedures for Psychological, Psychometric, and Personality Research*. R package.
- Fox, J., & Weisberg, S. *carData: Companion to Applied Regression Data Sets*. R package.
- Belenky, G., et al. (2003). Patterns of performance degradation and restoration during sleep restriction and subsequent recovery. *Journal of Sleep Research*, 12, 1–12.
- Arel-Bundock, V. *Rdatasets*. <https://github.com/vincentarelbundock/Rdatasets>

Check each licence yourself before reusing the data outside this repository.
