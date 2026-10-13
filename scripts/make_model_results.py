"""Produce real model-comparison results on NSL-KDD for the Chapter 7 and 10 notebooks.

Outputs (in data/sample/):
  model_results.csv      method (baseline|proposed), seed, accuracy, f1
                         10 repeated 80/20 splits: baseline = logistic regression,
                         proposed = random forest.
  per_fold_results.csv   method, fold, f1 for four classifiers, 5-fold stratified CV.
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scholarsedge.datasets import SAMPLE, load_nsl_kdd_xy  # noqa: E402


def models(seed):
    return {
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=seed),
        "Random Forest": RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=seed),
        "Gradient Boosting": HistGradientBoostingClassifier(random_state=seed),
    }


def main():
    X, y = load_nsl_kdd_xy()

    rows = []
    for seed in range(10):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y,
                                                  random_state=seed)
        m = models(seed)
        for method, name in [("baseline", "Logistic Regression"), ("proposed", "Random Forest")]:
            pred = m[name].fit(X_tr, y_tr).predict(X_te)
            rows.append({"method": method, "model": name, "seed": seed,
                         "accuracy": accuracy_score(y_te, pred), "f1": f1_score(y_te, pred)})
    pd.DataFrame(rows).round(6).to_csv(SAMPLE / "model_results.csv", index=False)
    print("  -> data/sample/model_results.csv")

    rows = []
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for fold, (tr, te) in enumerate(cv.split(X, y), start=1):
        for name, model in models(42).items():
            pred = model.fit(X.iloc[tr], y[tr]).predict(X.iloc[te])
            rows.append({"method": name, "fold": fold, "f1": f1_score(y[te], pred)})
    pd.DataFrame(rows).round(6).to_csv(SAMPLE / "per_fold_results.csv", index=False)
    print("  -> data/sample/per_fold_results.csv")


if __name__ == "__main__":
    main()
