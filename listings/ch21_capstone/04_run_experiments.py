import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from data import load_cicids2017, prepare_split
from models import local_train, fedavg, predict_proba
from privacy import noise_for_epsilon, membership_inference_auc

SEEDS = [0, 1, 2, 3, 4]
EPSILONS = [0.5, 1.0, 2.0, 4.0, 8.0]
ROUNDS, LOCAL_EPOCHS, BATCH, LR, CLIP = 30, 1, 256, 0.1, 1.0

def metrics(y, p):
    yhat = (p >= 0.5).astype(int)
    return {"accuracy": accuracy_score(y, yhat), "precision": precision_score(y, yhat, zero_division=0),
            "recall": recall_score(y, yhat), "f1": f1_score(y, yhat), "auc": roc_auc_score(y, p)}

df = load_cicids2017("data/raw", sample_frac=None)
rows = []

for seed in SEEDS:
    X_tr, y_tr, X_te, y_te, clients, cols = prepare_split(df, seed, partition="by_file")
    d = len(cols)
    rng = np.random.default_rng(seed)

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
    for eps in EPSILONS:
        sigmas = [noise_for_epsilon(eps, len(yk), BATCH, LOCAL_EPOCHS, ROUNDS)[0]
                  for _, yk in clients]
        w = fedavg(clients, d, rounds=ROUNDS, seed=seed, noise_mults=sigmas,
                   epochs=LOCAL_EPOCHS, batch=BATCH, lr=LR, clip=CLIP)
        record(f"FedAvg DP (eps={eps})", lambda X, w=w: predict_proba(w, X), eps)

pd.DataFrame(rows).to_csv("results/tables/capstone_runs.csv", index=False)
print("All runs saved to results/tables/capstone_runs.csv")
