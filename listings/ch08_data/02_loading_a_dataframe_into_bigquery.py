import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

client = bigquery.Client(project="your-project-id")
DATASET = "research_data"

def ensure_dataset(dataset_id, location="US"):
    full_id = f"{client.project}.{dataset_id}"
    try:
        client.get_dataset(full_id)
    except NotFound:
        ds = bigquery.Dataset(full_id)
        ds.location = location
        client.create_dataset(ds)
        print(f"Created dataset {full_id}")

def load_dataframe(df, table_id):
    full_table = f"{client.project}.{DATASET}.{table_id}"
    config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    client.load_table_from_dataframe(df, full_table, job_config=config).result()
    print(f"Loaded {len(df):,} rows into {full_table}")

ensure_dataset(DATASET)
load_dataframe(pd.read_csv("data/raw/arxiv_papers.csv"), "arxiv_papers")
