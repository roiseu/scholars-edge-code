import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

# Identifiers such as IP addresses would create thousands of one-hot columns
# (and can leak the label), so they are dropped before modelling.
X = df.drop(columns=["label", "timestamp", "src_ip", "dst_ip"], errors="ignore")
y = (df["label"] != "BENIGN").astype(int)

num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()

# scikit-learn imputers expect np.nan, not pandas' <NA>, in text columns
X[cat_cols] = X[cat_cols].astype(object).where(X[cat_cols].notna(), np.nan)

# Scale first so that KNN distances are not dominated by large-valued features.
# (StandardScaler ignores NaN when fitting and keeps NaN when transforming.)
numeric = Pipeline([
    ("scale", StandardScaler()),
    ("impute", KNNImputer(n_neighbors=5, add_indicator=True)),
])
categorical = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])
preprocess = ColumnTransformer([("num", numeric, num_cols),
                                ("cat", categorical, cat_cols)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

X_train_p = preprocess.fit_transform(X_train)   # learn from training data only
X_test_p = preprocess.transform(X_test)          # apply to test data
print(f"Processed training matrix: {X_train_p.shape}")
