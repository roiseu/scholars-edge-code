"""The full experimental loop (book Ch. 21, Phase 4).

    python capstone/src/run_experiments.py                       # NSL-KDD sample, 5 seeds
    python capstone/src/run_experiments.py --quick               # 2 seeds, 3 budgets (~1 min)
    python capstone/src/run_experiments.py --dataset cicids2017  # full data in data/raw/cicids2017
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from data import load_dataset, prepare_split
from models import local_train, fedavg, predict_proba
from privacy import HAVE_OPACUS, noise_for_epsilon, membership_inference_auc

REPO = Path(__file__).resolve().parents[2]
ROUNDS, LOCAL_EPOCHS, BATCH, LR, CLIP = 30, 1, 256, 0.1, 1.0


def metrics(y, p):
    yhat = (p >= 0.5).astype(int)
    return {"accuracy": accuracy_score(y, yhat), "precision": precision_score(y, yhat, zero_division=0),
            "recall": recall_score(y, yhat), "f1": f1_score(y, yhat), "auc": roc_auc_score(y, p)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="nsl_kdd", choices=["nsl_kdd", "cicids2017"])
    ap.add_argument("--sample-frac", type=float, default=None)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--epsilons", type=float, nargs="+", default=[0.5, 1.0, 2.0, 4.0, 8.0])
    ap.add_argument("--partition", default="by_file", choices=["by_file", "iid"])
    ap.add_argument("--quick", action="store_true", help="2 seeds, 3 budgets")
    ap.add_argument("--out", default=str(REPO / "results" / "tables" / "capstone_runs.csv"))
    args = ap.parse_args()
    if args.quick:
        args.seeds, args.epsilons = [0, 1], [0.5, 2.0, 8.0]

    print(f"Privacy accountant: {'Opacus (RDP)' if HAVE_OPACUS else 'NumPy RDP fallback'}")
    df = load_dataset(args.dataset, sample_frac=args.sample_frac)
    rows = []

    for seed in args.seeds:
        X_tr, y_tr, X_te, y_te, clients, cols = prepare_split(df, seed, partition=args.partition)
        d = len(cols)
        rng = np.random.default_rng(seed)
        if seed == args.seeds[0]:
            print(f"{d} features after selection; {len(clients)} clients with sizes "
                  f"{[len(yk) for _, yk in clients]}")

        def record(method, proba_fn, eps=None):
            r = {"seed": seed, "method": method, "epsilon": eps, **metrics(y_te, proba_fn(X_te))}
            r["mia_auc"] = membership_inference_auc(proba_fn, X_tr, y_tr, X_te, y_te, seed=seed)
            rows.append(r)
            print(f"seed={seed} {method:28s} F1={r['f1']:.4f} MIA-AUC={r['mia_auc']:.3f}")

        # 1. Centralized logistic regression (same optimizer and total passes as federated)
        w = local_train(np.zeros(d + 1), X_tr, y_tr, rng, epochs=ROUNDS * LOCAL_EPOCHS,
                        batch=BATCH, lr=LR)
        record("Centralized LR", lambda X, w=w: predict_proba(w, X))

        # 2. Random Forest reference (high-capacity, centralized)
        rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=seed).fit(X_tr, y_tr)
        record("Centralized RF", lambda X, rf=rf: rf.predict_proba(X)[:, 1])

        # 3. Federated averaging without DP
        w = fedavg(clients, d, rounds=ROUNDS, seed=seed, epochs=LOCAL_EPOCHS, batch=BATCH, lr=LR)
        record("FedAvg (no DP)", lambda X, w=w: predict_proba(w, X))

        # 4. Federated averaging with DP-SGD at each privacy budget
        for eps in args.epsilons:
            sigmas = [noise_for_epsilon(eps, len(yk), BATCH, LOCAL_EPOCHS, ROUNDS)[0]
                      for _, yk in clients]
            w = fedavg(clients, d, rounds=ROUNDS, seed=seed, noise_mults=sigmas,
                       epochs=LOCAL_EPOCHS, batch=BATCH, lr=LR, clip=CLIP)
            record(f"FedAvg DP (eps={eps})", lambda X, w=w: predict_proba(w, X), eps)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"All runs saved to {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")


if __name__ == "__main__":
    main()
