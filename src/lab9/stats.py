"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge labels must have the same length")
    if not human:
        raise ValueError("at least one label pair is required")
    allowed = {"PASS", "FAIL"}
    if any(label not in allowed for label in (*human, *judge)):
        raise ValueError("labels must be PASS or FAIL")
    return {
        "tp": sum(h == POS and j == POS for h, j in zip(human, judge)),
        "fp": sum(h != POS and j == POS for h, j in zip(human, judge)),
        "fn": sum(h == POS and j != POS for h, j in zip(human, judge)),
        "tn": sum(h != POS and j != POS for h, j in zip(human, judge)),
    }


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    p_denom = cm["tp"] + cm["fp"]
    r_denom = cm["tp"] + cm["fn"]
    precision = cm["tp"] / p_denom if p_denom else 0.0
    recall = cm["tp"] / r_denom if r_denom else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    cm = confusion(human, judge)
    n = len(human)
    observed = (cm["tp"] + cm["tn"]) / n
    human_fail = (cm["tp"] + cm["fn"]) / n
    judge_fail = (cm["tp"] + cm["fp"]) / n
    human_pass = (cm["fp"] + cm["tn"]) / n
    judge_pass = (cm["fn"] + cm["tn"]) / n
    expected = human_fail * judge_fail + human_pass * judge_pass
    if expected == 1.0:
        raise ValueError("Cohen's kappa is undefined when expected agreement is 1")
    return (observed - expected) / (1.0 - expected)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    rates = (observed_rate, sensitivity, specificity)
    if any(not 0.0 <= value <= 1.0 for value in rates):
        raise ValueError("observed rate, sensitivity and specificity must be in [0, 1]")
    denom = sensitivity + specificity - 1.0
    if denom <= 0.0:
        raise ValueError("Rogan-Gladen correction requires sensitivity + specificity > 1")
    corrected = (observed_rate + specificity - 1.0) / denom
    return min(1.0, max(0.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("paired samples must have the same length")
    if not a:
        raise ValueError("paired bootstrap requires at least one item")
    if n_resamples < 1:
        raise ValueError("n_resamples must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    if np.array_equal(left, right):
        return 0.0, 0.0, 0.0

    def mean_difference(x, y):
        return np.mean(x - y)

    result = bootstrap(
        (left, right),
        mean_difference,
        paired=True,
        vectorized=False,
        n_resamples=n_resamples,
        confidence_level=confidence,
        method="percentile",
        rng=np.random.default_rng(rng),
    )
    difference = float(np.mean(left - right))
    return difference, float(result.confidence_interval.low), float(result.confidence_interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    from math import comb

    _validate_pass_k(n, c, k)
    failures = n - c
    return 1.0 - (comb(failures, k) / comb(n, k) if failures >= k else 0.0)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    from math import comb

    _validate_pass_k(n, c, k)
    return comb(c, k) / comb(n, k) if c >= k else 0.0


def _validate_pass_k(n: int, c: int, k: int) -> None:
    if any(not isinstance(v, int) or isinstance(v, bool) for v in (n, c, k)):
        raise ValueError("n, c and k must be integers")
    if n < 1 or c < 0 or c > n or k < 1 or k > n:
        raise ValueError("require n >= 1, 0 <= c <= n and 1 <= k <= n")
