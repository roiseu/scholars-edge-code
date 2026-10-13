import re
import pandas as pd

# Exports from each database, after renaming columns to: title, abstract, doi, year
files = ["scopus.csv", "ieee.csv", "wos.csv"]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print(f"Records identified: {len(df)}")

def norm_title(t):
    return re.sub(r"[^a-z0-9 ]", "", str(t).lower()).strip()

df["doi_norm"] = df["doi"].fillna("").str.lower().str.strip()
df["title_norm"] = df["title"].apply(norm_title)

with_doi = df[df["doi_norm"] != ""].drop_duplicates("doi_norm")
without_doi = df[df["doi_norm"] == ""]
dedup = pd.concat([with_doi, without_doi]).drop_duplicates("title_norm")
print(f"Duplicates removed: {len(df) - len(dedup)}")
print(f"Records to screen: {len(dedup)}")

# Flags to help human screeners -- NOT automatic exclusion
topic_terms = ["federated", "intrusion", "anomaly detection"]
review_terms = ["survey", "systematic review", "tutorial"]
text = (dedup["title"].fillna("") + " " + dedup["abstract"].fillna("")).str.lower()
dedup["matches_topic"] = text.apply(lambda s: any(t in s for t in topic_terms))
dedup["possible_review"] = text.apply(lambda s: any(t in s for t in review_terms))

dedup["screener_1"] = ""   # include / exclude
dedup["screener_2"] = ""
dedup["reason"] = ""
cols = ["title", "year", "doi", "abstract", "matches_topic",
        "possible_review", "screener_1", "screener_2", "reason"]
dedup[cols].to_csv("screening_sheet.csv", index=False)
print("Screening sheet saved.")
