# Authenticate this notebook with your Google account
from google.colab import auth
auth.authenticate_user()

# Optional: mount Google Drive
from google.colab import drive
drive.mount("/content/drive")

# Query BigQuery directly from the notebook
from google.cloud import bigquery
client = bigquery.Client(project="your-project-id")
df = client.query("SELECT CURRENT_DATE() AS today").to_dataframe()
print(df)
