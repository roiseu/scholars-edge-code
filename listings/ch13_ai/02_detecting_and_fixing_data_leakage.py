from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline

# PROBLEM (common in generated code): the scaler is fitted on ALL rows,
# so statistics from the test set leak into training.
X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

# FIX: put preprocessing inside a pipeline so it is re-fitted on each
# training fold only, and fix random seeds for reproducibility.
pipe = make_pipeline(StandardScaler(),
                     RandomForestClassifier(n_estimators=200, random_state=42))
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_validate(pipe, X, y, cv=cv, scoring=["accuracy", "f1"])

for metric in ["test_accuracy", "test_f1"]:
    print(f"{metric}: {scores[metric].mean():.4f} +/- {scores[metric].std():.4f}")
