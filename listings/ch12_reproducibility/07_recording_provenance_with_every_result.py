import datetime
import json
import platform
import subprocess
import sys
from importlib.metadata import version

def git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip())
        return commit, dirty
    except Exception:
        return "unknown", None

def save_run(config, metrics, path="results/runs.jsonl"):
    commit, dirty = git_info()
    record = {
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "git_commit": commit,
        "uncommitted_changes": dirty,     # True means results may not be reproducible
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {p: version(p) for p in ["numpy", "pandas", "scikit-learn"]},
        "config": config,
        "metrics": metrics,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

save_run({"model": "xgboost", "max_depth": 6, "seed": 42},
         {"accuracy": 0.9712, "f1": 0.9701})
