from google.cloud import bigquery

client = bigquery.Client(project="your-project-id")

sql = """
SELECT EXTRACT(YEAR FROM creation_date) AS year, COUNT(*) AS questions
FROM `bigquery-public-data.stackoverflow.posts_questions`
GROUP BY year ORDER BY year
"""

# 1. Dry run: how much data would this query scan?
dry = client.query(sql, job_config=bigquery.QueryJobConfig(dry_run=True,
                                                           use_query_cache=False))
print(f"This query will process {dry.total_bytes_processed / 1e9:.2f} GB")

# 2. Run with a hard limit: the query fails if it would scan more than 20 GB
capped = bigquery.QueryJobConfig(maximum_bytes_billed=20 * 10**9)
df = client.query(sql, job_config=capped).to_dataframe()
print(df.tail())
