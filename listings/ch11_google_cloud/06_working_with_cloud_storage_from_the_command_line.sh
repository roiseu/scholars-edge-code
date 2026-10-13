# Create a bucket in the Mumbai region
gcloud storage buckets create gs://my-research-data-2026 --location=asia-south1

# Upload a file and a whole folder
gcloud storage cp data/processed/cleaned.csv gs://my-research-data-2026/processed/
gcloud storage cp -r results gs://my-research-data-2026/

# List contents and download
gcloud storage ls gs://my-research-data-2026/processed/
gcloud storage cp gs://my-research-data-2026/processed/cleaned.csv ./
