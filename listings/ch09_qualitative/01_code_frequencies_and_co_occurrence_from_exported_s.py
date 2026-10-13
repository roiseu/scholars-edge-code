import pandas as pd

# Export with one row per coded segment: participant, segment_id, code
seg = pd.read_csv("coded_segments.csv")

# How many segments and how many participants for each code?
spread = (seg.groupby("code")["participant"]
             .agg(segments="count", participants="nunique")
             .sort_values("participants", ascending=False))
print(spread)

# Which codes are applied to the same segments?
onehot = pd.crosstab(seg["segment_id"], seg["code"]).clip(upper=1)
cooccurrence = onehot.T.dot(onehot)
print(cooccurrence)
