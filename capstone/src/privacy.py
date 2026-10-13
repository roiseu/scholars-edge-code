"""Noise calibration for DP-SGD and a membership-inference attack (book Ch. 21).

`noise_for_epsilon` uses Opacus's RDP accountant when Opacus is installed
(as in the book). Opacus depends on PyTorch, so for readers who do not want to
install it there is a small, dependency-free fallback that implements the same
Renyi-DP analysis of the sampled Gaussian mechanism (Mironov et al., 2019) for
integer orders. The fallback is very slightly more conservative (it gives a
marginally larger noise multiplier) because it searches integer orders only.
"""
import math

import numpy as np
from scipy.special import gammaln, logsumexp
from sklearn.metrics import roc_auc_score

try:  # the book's version
    from opacus.accountants.utils import get_noise_multiplier as _opacus_get_noise_multiplier
    HAVE_OPACUS = True
except Exception:  # ImportError, or torch missing
    HAVE_OPACUS = False

ORDERS = np.arange(2, 257)


# --------------------------------------------------------------------------
# Pure-NumPy RDP accountant (fallback)
# --------------------------------------------------------------------------
def _log_a_int(q, sigma, alpha):
    """log A_alpha for the sampled Gaussian mechanism, integer alpha."""
    i = np.arange(alpha + 1)
    log_binom = gammaln(alpha + 1) - gammaln(i + 1) - gammaln(alpha - i + 1)
    with np.errstate(divide="ignore"):
        log_terms = (log_binom + i * math.log(q) + (alpha - i) * math.log1p(-q)
                     + (i * i - i) / (2 * sigma ** 2))
    return logsumexp(log_terms)


def compute_rdp(q, sigma, steps, orders=ORDERS):
    """RDP of `steps` compositions of the sampled Gaussian mechanism."""
    if sigma == 0:
        return np.full(len(orders), np.inf)
    if q >= 1.0:
        return steps * np.asarray(orders, float) / (2 * sigma ** 2)
    rdp = np.array([_log_a_int(q, sigma, int(a)) / (a - 1) for a in orders])
    return steps * rdp


def rdp_to_epsilon(rdp, delta, orders=ORDERS):
    """Convert RDP to (epsilon, delta)-DP (Balle et al., 2020 conversion, as in Opacus)."""
    orders = np.asarray(orders, float)
    eps = (rdp - (np.log(delta) + np.log(orders)) / (orders - 1)
           + np.log((orders - 1) / orders))
    eps = np.where(np.isnan(eps), np.inf, eps)
    return float(np.min(eps))


def epsilon_spent(sigma, sample_rate, steps, delta):
    return rdp_to_epsilon(compute_rdp(sample_rate, sigma, steps), delta)


def get_noise_multiplier_numpy(target_epsilon, target_delta, sample_rate, steps,
                               epsilon_tolerance=0.01):
    """Smallest noise multiplier sigma whose epsilon is <= target (bisection)."""
    lo, hi = 0.0, 10.0
    while epsilon_spent(hi, sample_rate, steps, target_delta) > target_epsilon:
        hi *= 2
        if hi > 1e6:
            raise ValueError("Target epsilon is unreachable with these settings.")
    eps = math.inf
    while target_epsilon - eps > epsilon_tolerance or eps > target_epsilon:
        mid = (lo + hi) / 2
        eps = epsilon_spent(mid, sample_rate, steps, target_delta)
        if eps < target_epsilon:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-6:
            break
    return hi


# --------------------------------------------------------------------------
# The book's functions
# --------------------------------------------------------------------------
def noise_for_epsilon(target_eps, n_local, batch, epochs, rounds, delta=None):
    delta = delta or min(1e-5, 1.0 / (10 * n_local))
    steps = int(np.ceil(n_local / batch)) * epochs * rounds
    sample_rate = min(1.0, batch / n_local)
    if HAVE_OPACUS:
        sigma = _opacus_get_noise_multiplier(target_epsilon=target_eps, target_delta=delta,
                                             sample_rate=sample_rate, steps=steps,
                                             accountant="rdp")
    else:
        sigma = get_noise_multiplier_numpy(target_eps, delta, sample_rate, steps)
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
