# Option 1: venv (built into Python)
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# Option 2: conda
conda create -n scholars-edge python=3.11 -y
conda activate scholars-edge

# Install the packages used in this book
pip install numpy pandas scipy statsmodels scikit-learn xgboost \
            matplotlib seaborn jupyterlab requests opacus \
            "google-cloud-bigquery[pandas]" google-cloud-storage \
            google-cloud-aiplatform google-genai

pip freeze > requirements.txt        # record exact versions
