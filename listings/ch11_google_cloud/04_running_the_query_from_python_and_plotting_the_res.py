import matplotlib.pyplot as plt
from google.cloud import bigquery

client = bigquery.Client(project="your-project-id")
sql = open("queries/framework_trends.sql").read()   # the query above
df = client.query(sql, job_config=bigquery.QueryJobConfig(
        maximum_bytes_billed=50 * 10**9)).to_dataframe()

fig, ax = plt.subplots(figsize=(7, 3.5))
for col, color in [("tensorflow", "#E69F00"), ("pytorch", "#D55E00"),
                   ("scikit_learn", "#0072B2")]:
    ax.plot(df["year"], df[col] / df["all_questions"] * 100,
            marker="o", color=color, label=col.replace("_", "-"))
ax.set_xlabel("Year")
ax.set_ylabel("Share of all questions (%)")
ax.set_title("Machine learning framework questions on Stack Overflow")
ax.legend(frameon=False)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("results/figures/framework_trends.pdf")
