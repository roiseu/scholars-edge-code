"""Verify that everything is installed (book Appendix A).  Usage: python scripts/check_setup.py"""
import shutil
import sys
from importlib.metadata import version, PackageNotFoundError

print(f"Python {sys.version.split()[0]}")
for pkg in ["numpy", "pandas", "scipy", "statsmodels", "scikit-learn",
            "matplotlib", "seaborn", "opacus", "google-cloud-bigquery"]:
    try:
        print(f"  [OK] {pkg} {version(pkg)}")
    except PackageNotFoundError:
        print(f"  [MISSING] {pkg}")

for tool in ["git", "gcloud", "docker", "pdflatex"]:
    print(f"  [{'OK' if shutil.which(tool) else 'NOT FOUND'}] {tool}")
