from sklearn.metrics import cohen_kappa_score

# Code assigned by each coder to the same 12 segments
coder_1 = ["fatigue", "ritual", "trust", "trust", "ritual", "fatigue",
           "trust", "ritual", "fatigue", "trust", "ritual", "trust"]
coder_2 = ["fatigue", "ritual", "trust", "ritual", "ritual", "fatigue",
           "trust", "ritual", "fatigue", "trust", "trust", "trust"]

kappa = cohen_kappa_score(coder_1, coder_2)
print(f"Cohen's kappa = {kappa:.2f}")
# A common rough guide (Landis and Koch, 1977): 0.61-0.80 substantial; above 0.80 almost perfect
