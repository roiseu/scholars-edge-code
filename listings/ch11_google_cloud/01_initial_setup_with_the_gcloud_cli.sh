# Sign in and select your project
gcloud auth login
gcloud config set project your-project-id

# Enable the services this book uses
gcloud services enable bigquery.googleapis.com storage.googleapis.com aiplatform.googleapis.com

# Let client libraries (Python, etc.) use your credentials -- no key file needed
gcloud auth application-default login

# Install the Python client libraries
pip install "google-cloud-bigquery[pandas]" google-cloud-storage google-cloud-aiplatform
