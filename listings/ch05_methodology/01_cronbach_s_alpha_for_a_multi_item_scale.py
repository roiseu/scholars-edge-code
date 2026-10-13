import pandas as pd

def cronbach_alpha(items: pd.DataFrame) -> float:
    """Items: one column per question, one row per respondent."""
    items = items.dropna()
    k = items.shape[1]
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)

survey = pd.read_csv("survey_responses.csv")
trust_items = survey[["trust1", "trust2", "trust3", "trust4", "trust5"]]
alpha = cronbach_alpha(trust_items)
print(f"Cronbach's alpha (trust scale): {alpha:.3f}")

# Item-level check: does alpha improve if an item is dropped?
for col in trust_items.columns:
    a = cronbach_alpha(trust_items.drop(columns=col))
    print(f"  alpha without {col}: {a:.3f}")
