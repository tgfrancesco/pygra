"""
fitting.py — fit functions for histogram and xy data
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm, expon, maxwell, poisson


def fit_gaussian(data: np.ndarray):
    mu, sigma = norm.fit(data)
    x = np.linspace(data.min(), data.max(), 300)
    y = norm.pdf(x, mu, sigma)
    label = f"Gaussian  μ={mu:.4g}  σ={sigma:.4g}"
    return x, y, label, {"μ": mu, "σ": sigma}


def fit_exponential(data: np.ndarray):
    loc, scale = expon.fit(data, floc=0)
    x = np.linspace(data.min(), data.max(), 300)
    y = expon.pdf(x, loc=loc, scale=scale)
    lam = 1.0 / scale
    label = f"Exponential  λ={lam:.4g}"
    return x, y, label, {"λ": lam}


def fit_maxwell_boltzmann(data: np.ndarray):
    loc, scale = maxwell.fit(data, floc=0)
    x = np.linspace(max(data.min(), 0), data.max(), 300)
    y = maxwell.pdf(x, loc=loc, scale=scale)
    label = f"Maxwell-Boltzmann  a={scale:.4g}"
    return x, y, label, {"a": scale}


def fit_poisson(data: np.ndarray):
    mu = data.mean()
    x_int = np.arange(int(data.min()), int(data.max()) + 1)
    y = poisson.pmf(x_int, mu)
    label = f"Poisson  μ={mu:.4g}"
    return x_int.astype(float), y, label, {"μ": mu}


def fit_custom(data: np.ndarray, formula: str, param_names: list):
    """Fit a custom formula (using x and param names) to data density."""
    import math
    safe_ns = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    safe_ns.update({k: getattr(np, k) for k in dir(np) if not k.startswith("_")})

    def model(x, *params):
        ns = dict(safe_ns)
        ns["x"] = x
        for name, val in zip(param_names, params):
            ns[name] = val
        return eval(formula, {"__builtins__": {}}, ns)

    counts, edges = np.histogram(data, bins="auto", density=True)
    x_centers = 0.5 * (edges[:-1] + edges[1:])
    p0 = [1.0] * len(param_names)
    popt, _ = curve_fit(model, x_centers, counts, p0=p0, maxfev=10000)
    x_fine = np.linspace(data.min(), data.max(), 300)
    y_fine = model(x_fine, *popt)
    params_dict = {n: v for n, v in zip(param_names, popt)}
    label = "Custom  " + "  ".join(f"{n}={v:.4g}" for n, v in params_dict.items())
    return x_fine, y_fine, label, params_dict


FIT_FUNCTIONS = {
    "Gaussian":          fit_gaussian,
    "Exponential":       fit_exponential,
    "Maxwell-Boltzmann": fit_maxwell_boltzmann,
    "Poisson":           fit_poisson,
}
