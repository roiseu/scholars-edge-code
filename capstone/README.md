# Capstone: the privacy–utility trade-off in federated intrusion detection (Chapter 21)

A complete, small research project: train an intrusion detector centrally, then
with federated averaging (FedAvg), then with FedAvg plus differentially private
SGD at several privacy budgets ε. Measure detection quality *and* how much a
membership-inference attacker can learn, and test equivalence statistically.

```
capstone/
├── run_all.sh              one command: experiments -> analysis -> figures
└── src/
    ├── data.py             load + clean + split + feature selection + client partition
    ├── models.py           NumPy logistic regression, DP-SGD, FedAvg   (book code, unchanged)
    ├── privacy.py          noise calibration (Opacus or NumPy RDP) + membership inference
    ├── run_experiments.py  seeds x methods x privacy budgets -> results/tables/capstone_runs.csv
    ├── analyze.py          mean/SD tables + paired TOST equivalence tests (Holm-corrected)
    └── make_figures.py     results/figures/capstone_privacy_tradeoff.{pdf,png}
```

## Run it

```bash
bash capstone/run_all.sh                    # NSL-KDD sample, 5 seeds, under a minute
bash capstone/run_all.sh --quick            # 2 seeds, 3 budgets
bash capstone/run_all.sh --sample-frac 0.03 # small data: DP noise now visibly hurts
bash capstone/run_all.sh --dataset cicids2017   # after downloading CICIDS2017 (data/README.md)
```

## Differences from the book's listing

| Book | Here | Why |
|---|---|---|
| CICIDS2017 only | `--dataset nsl_kdd` (default) or `cicids2017` | CICIDS2017 is 2.8M rows and needs a manual download; NSL-KDD ships with the repo |
| Clients = CICIDS capture-day files | Clients = `protocol_type` (tcp / udp / icmp) for NSL-KDD | NSL-KDD has no per-day files; protocol groups are just as non-IID |
| `opacus` required | Opacus if installed, otherwise a NumPy RDP accountant | Opacus pulls in PyTorch (~2 GB). The fallback matches Opacus's ε to within about 1% and is always slightly conservative |
| Hard-coded paths and settings | Command-line flags | So one script covers the quick, full and CICIDS runs |

## What to expect on the NSL-KDD sample

The numbers below come from `bash capstone/run_all.sh` with 5 seeds:

| Method | F1 (mean) | MIA AUC |
|---|---|---|
| Centralized RF | 0.989 | 0.526 |
| Centralized LR | 0.884 | 0.501 |
| FedAvg (no DP) | 0.861 | 0.501 |
| FedAvg + DP, ε = 0.5 … 8 | 0.846–0.847 | 0.501 |

How to read it:

- The random forest is the only model that leaks noticeably (AUC above 0.5).
- The linear models are already close to the 0.5 chance line.
- Federation costs about 2.5 F1 points because of the non-IID clients.
- DP-SGD costs about 1.5 more, and that cost is almost flat across ε. With tens
  of thousands of records per client, the per-step noise (σ·C/batch) is tiny,
  so gradient clipping, not noise, dominates the cost.
- Re-run with `--sample-frac 0.03` and the ε dependence appears. This is a good
  discussion point for the Chapter 21 write-up.
