import numpy as np
from opacus.accountants.utils import get_noise_multiplier
from sklearn.metrics import roc_auc_score

def noise_for_epsilon(target_eps, n_local, batch, epochs, rounds, delta=None):
    delta = delta or min(1e-5, 1.0 / (10 * n_local))
    steps = int(np.ceil(n_local / batch)) * epochs * rounds
    sigma = get_noise_multiplier(target_epsilon=target_eps, target_delta=delta,
                                 sample_rate=min(1.0, batch / n_local), steps=steps,
                                 accountant="rdp")
    return sigma, delta

def membership_inference_auc(proba_fn, X_mem, y_mem, X_non, y_non, n=20000, seed=0):
    """Loss-threshold attack: lower loss suggests a training member.
    AUC = 0.5 means the attacker cannot distinguish members from non-members."""
    rng = np.random.default_rng(seed)
    i = rng.choice(len(y_mem), size=min(n, len(y_mem)), replace=False)
    j = rng.choice(len(y_non), size=min(n, len(y_non)), replace=False)

    def loss(X, y):
        p = np.clip(proba_fn(X), 1e-7, 1 - 1e-7)
        return -(y * np.log(p) + (1 - y) * np.log(1 - p))

    scores = np.concatenate([-loss(X_mem[i], y_mem[i]), -loss(X_non[j], y_non[j])])
    labels = np.concatenate([np.ones(len(i)), np.zeros(len(j))])
    return roc_auc_score(labels, scores)
