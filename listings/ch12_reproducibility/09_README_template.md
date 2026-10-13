# FedIDS: Federated Intrusion Detection Evaluation Framework

Code and data for "Measuring the Privacy-Utility Trade-off in Federated
Intrusion Detection" (Author et al., 2026). DOI: 10.5281/zenodo.0000000

## Requirements
Python 3.11; see requirements.txt. Tested on Ubuntu 22.04, 1x NVIDIA T4.

## Data
CICIDS 2017: download from https://www.unb.ca/cic/datasets/ids-2017.html
and place the CSV files in data/raw/. (Not redistributed due to licence terms.)

## Reproduce all results
    pip install -r requirements.txt
    bash run_all.sh          # about 3 hours on the hardware above

## Repository structure
src/       numbered pipeline scripts
results/   generated figures and tables
paper/     LaTeX source of the manuscript

## Licence and citation
Code: MIT. Please cite the paper and this repository (see CITATION.cff).
