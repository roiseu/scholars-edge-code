"""Logistic regression, DP-SGD, and federated averaging in NumPy (book Ch. 21, Phase 3)."""
import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def predict_proba(w, X):
    return sigmoid(X @ w[:-1] + w[-1])

def per_example_grads(w, X, y):
    err = predict_proba(w, X) - y                       # shape (batch,)
    return np.hstack([err[:, None] * X, err[:, None]])  # weights + bias

def local_train(w, X, y, rng, epochs=1, batch=256, lr=0.1,
                clip=None, noise_mult=0.0, l2=1e-4):
    """Mini-batch SGD; DP-SGD when clip is set (per-example clipping + noise)."""
    w = w.copy()
    n = len(y)
    for _ in range(epochs):
        order = rng.permutation(n)
        for start in range(0, n, batch):
            b = order[start:start + batch]
            g = per_example_grads(w, X[b], y[b])
            if clip is not None:
                norms = np.linalg.norm(g, axis=1, keepdims=True)
                g = g / np.maximum(1.0, norms / clip)
                noisy_sum = g.sum(axis=0) + rng.normal(0.0, noise_mult * clip, g.shape[1])
                grad = noisy_sum / batch
            else:
                grad = g.mean(axis=0)
            grad[:-1] += l2 * w[:-1]
            w -= lr * grad
    return w

def fedavg(clients, n_features, rounds=30, seed=0, noise_mults=None, **local_kw):
    """Federated averaging; optional per-client noise multipliers for DP-SGD."""
    rng = np.random.default_rng(seed)
    w = np.zeros(n_features + 1)
    sizes = np.array([len(y) for _, y in clients], dtype=float)
    weights = sizes / sizes.sum()
    for _ in range(rounds):
        updates = []
        for k, (Xk, yk) in enumerate(clients):
            nm = 0.0 if noise_mults is None else noise_mults[k]
            updates.append(local_train(w, Xk, yk, rng, noise_mult=nm, **local_kw))
        w = np.sum([a * u for a, u in zip(weights, updates)], axis=0)
    return w
