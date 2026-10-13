import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

papers = pd.read_csv("included_abstracts.csv")
abstracts = papers["abstract"].dropna().tolist()
print(f"Analyzing {len(abstracts)} abstracts")

vectorizer = CountVectorizer(
    max_df=0.90,           # ignore terms in more than 90% of documents
    min_df=3,              # ignore terms in fewer than 3 documents
    stop_words="english",
    max_features=2000,
    ngram_range=(1, 2),    # include bigrams such as "machine learning"
)
dtm = vectorizer.fit_transform(abstracts)

lda = LatentDirichletAllocation(n_components=8, random_state=42,
                                learning_method="online", max_iter=25)
lda.fit(dtm)

terms = vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_, start=1):
    top = [terms[j] for j in topic.argsort()[:-11:-1]]
    print(f"Topic {i}: {', '.join(top)}")

doc_topics = lda.transform(dtm)
papers = papers.loc[papers["abstract"].notna()].copy()
papers["dominant_topic"] = doc_topics.argmax(axis=1) + 1
papers["topic_weight"] = doc_topics.max(axis=1)
print(papers["dominant_topic"].value_counts().sort_index())
