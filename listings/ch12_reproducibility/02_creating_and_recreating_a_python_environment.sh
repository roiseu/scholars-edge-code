# Create an isolated environment for the project
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

pip install numpy pandas scikit-learn xgboost matplotlib
pip freeze > requirements.txt      # record exact versions

# Anyone can recreate the same environment later
pip install -r requirements.txt

# Conda alternative
conda env export --no-builds > environment.yml
conda env create -f environment.yml
