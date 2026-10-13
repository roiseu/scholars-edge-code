import matplotlib.pyplot as plt
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay,
                             PrecisionRecallDisplay)

# y_test: true labels; y_pred: predicted labels; y_score: predicted probabilities
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, normalize="true", display_labels=["Benign", "Attack"],
    cmap="Blues", values_format=".2f", colorbar=False, ax=axes[0])
axes[0].set_title("Confusion matrix (row-normalized)")

RocCurveDisplay.from_predictions(y_test, y_score, name="FedIDS", ax=axes[1])
axes[1].plot([0, 1], [0, 1], ls="--", color="gray")
axes[1].set_title("ROC curve")

PrecisionRecallDisplay.from_predictions(y_test, y_score, name="FedIDS", ax=axes[2])
axes[2].set_title("Precision-recall curve")

fig.tight_layout()
fig.savefig("results/figures/fig_classification.pdf")
