import os
import random
import numpy as np

def set_seed(seed: int = 42) -> None:
    """Make Python, NumPy, and (if installed) PyTorch runs repeatable."""
    random.seed(seed)
    np.random.seed(seed)
    # Note: PYTHONHASHSEED only affects hashing if set before Python starts
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

# Report variability across several seeds, not a single lucky run
scores = []
for seed in [0, 1, 2, 3, 4]:
    set_seed(seed)
    scores.append(train_and_evaluate(seed=seed))   # your experiment function
print(f"F1 = {np.mean(scores):.4f} +/- {np.std(scores, ddof=1):.4f} over 5 seeds")
