# One-time setup
git config --global user.name "Your Name"
git config --global user.email "you@university.edu"

# Start tracking a project
cd my-research-project
git init
git add README.md src/ notebooks/
git commit -m "Initial project structure"

# Connect to GitHub and upload
git remote add origin https://github.com/yourname/my-research-project.git
git branch -M main
git push -u origin main

# Everyday cycle: check, stage, commit, push
git status
git add src/preprocess.py
git commit -m "Fit scaler inside pipeline to prevent leakage"
git push

# Try something risky on a separate branch
git checkout -b experiment-new-features
git log --oneline --graph
