import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/processed/papers.csv")
CURRENT_YEAR = datetime.date.today().year

# Temporal features
df["published"] = pd.to_datetime(df["published"], errors="coerce")
df["pub_year"] = df["published"].dt.year
df["years_since_pub"] = (CURRENT_YEAR - df["pub_year"]).clip(lower=1)

# Text length features
df["title_words"] = df["title"].str.split().str.len()
df["abstract_words"] = df["abstract"].str.split().str.len()

# Binary indicators (regular expressions use the | character for OR)
df["has_code"] = df["abstract"].str.contains(
    r"github|source code|open[- ]source", case=False, na=False).astype(int)
df["has_dataset"] = df["abstract"].str.contains(
    r"dataset|benchmark|corpus", case=False, na=False).astype(int)
df["is_survey"] = df["title"].str.contains(
    r"survey|review|overview", case=False, na=False).astype(int)

# Rate feature ("citations" must come from another source, such as Semantic
# Scholar or OpenAlex; arXiv metadata does not include citation counts)
df["citation_velocity"] = df["citations"] / df["years_since_pub"]

# Text features: TF-IDF must be fitted on training text only
train, test = train_test_split(df, test_size=0.2, random_state=42)
tfidf = TfidfVectorizer(max_features=100, stop_words="english", ngram_range=(1, 2))
X_text_train = tfidf.fit_transform(train["abstract"].fillna(""))
X_text_test = tfidf.transform(test["abstract"].fillna(""))
print(f"Engineered features: {df.shape[1]} columns; TF-IDF terms: {X_text_train.shape[1]}")
