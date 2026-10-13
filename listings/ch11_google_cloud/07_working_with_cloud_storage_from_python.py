from io import StringIO
import pandas as pd
from google.cloud import storage

client = storage.Client(project="your-project-id")
BUCKET = "my-research-data-2026"

def upload(local_path, dest):
    client.bucket(BUCKET).blob(dest).upload_from_filename(local_path)
    print(f"Uploaded {local_path} -> gs://{BUCKET}/{dest}")

def read_csv_from_gcs(path):
    text = client.bucket(BUCKET).blob(path).download_as_text()
    return pd.read_csv(StringIO(text))

def list_files(prefix=""):
    for b in client.list_blobs(BUCKET, prefix=prefix):
        print(f"{b.name:55s} {b.size / 1024:10.1f} KB  {b.updated:%Y-%m-%d}")

upload("data/processed/cleaned.csv", "processed/cleaned.csv")
df = read_csv_from_gcs("processed/cleaned.csv")
list_files("processed/")
