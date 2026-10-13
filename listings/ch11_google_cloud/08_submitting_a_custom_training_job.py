from google.cloud import aiplatform

aiplatform.init(project="your-project-id", location="us-central1",
                staging_bucket="gs://my-research-data-2026/staging")

# Choose from "Prebuilt containers for custom training" in the Vertex AI docs.
# The container must match your framework (e.g., scikit-learn, PyTorch) and
# your hardware (a GPU container only if you request a GPU).
CONTAINER_URI = "REPLACE_WITH_PREBUILT_CONTAINER_URI"

job = aiplatform.CustomTrainingJob(
    display_name="fedids-baselines-v1",
    script_path="src/train.py",
    container_uri=CONTAINER_URI,
    requirements=["xgboost", "pandas", "pyarrow", "gcsfs"],
)

job.run(
    args=["--data-uri=gs://my-research-data-2026/processed/",
          "--output-dir=gs://my-research-data-2026/results/",
          "--seed=42"],
    replica_count=1,
    machine_type="n1-standard-8",
)
print("Training job finished; results written to Cloud Storage.")
