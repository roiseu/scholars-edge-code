import pandas as pd

results = pd.DataFrame({
    "Method": ["Random Forest", "XGBoost", "FedIDS ($\\varepsilon$=1.0)"],
    "Accuracy": [0.975, 0.971, 0.968],
    "F1": [0.974, 0.970, 0.967],
    "AUC": [0.991, 0.988, 0.989],
})

def to_booktabs(df, caption, label, digits=3, lower_is_better=()):
    num = df.columns[1:]
    best = {c: df[c].min() if c in lower_is_better else df[c].max() for c in num}
    lines = [r"\begin{table}[t]", r"\centering",
             rf"\caption{{{caption}}}\label{{{label}}}",
             r"\begin{tabular}{l" + "c" * len(num) + "}", r"\toprule",
             " & ".join(df.columns) + r" \\", r"\midrule"]
    for _, row in df.iterrows():
        cells = [str(row.iloc[0])]
        for c in num:
            v = f"{row[c]:.{digits}f}"
            cells.append(rf"\textbf{{{v}}}" if row[c] == best[c] else v)
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)

latex = to_booktabs(results, "Detection performance (5-fold CV means).", "tab:results")
with open("paper/tables/results.tex", "w") as f:
    f.write(latex)
print(latex)
