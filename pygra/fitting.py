"""
fitting.py — fit functions for histogram and xy data
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm, expon, maxwell, poisson


def fit_gaussian(data: np.ndarray):
    """
    Fit a Gaussian (normal) distribution to *data* using MLE.

    Parameters
    ----------
    data : numpy.ndarray
        1-D array of sample values.

    Returns
    -------
    x : numpy.ndarray
        300 evenly-spaced points spanning ``[data.min(), data.max()]``.
    y : numpy.ndarray
        Gaussian PDF evaluated at each point in *x*.
    label : str
        Human-readable label including the fitted μ and σ.
    params : dict
        ``{"μ": float, "σ": float}`` — fitted mean and standard deviation.
    """
    mu, sigma = norm.fit(data)
    x = np.linspace(data.min(), data.max(), 300)
    y = norm.pdf(x, mu, sigma)
    label = f"Gaussian  μ={mu:.4g}  σ={sigma:.4g}"
    return x, y, label, {"μ": mu, "σ": sigma}


def fit_exponential(data: np.ndarray):
    """
    Fit an exponential distribution to *data* with fixed location (loc=0).

    Parameters
    ----------
    data : numpy.ndarray
        1-D array of non-negative sample values.

    Returns
    -------
    x : numpy.ndarray
        300 evenly-spaced points spanning ``[data.min(), data.max()]``.
    y : numpy.ndarray
        Exponential PDF evaluated at each point in *x*.
    label : str
        Human-readable label including the fitted rate λ.
    params : dict
        ``{"λ": float}`` — fitted rate parameter (1 / scale).
    """
    loc, scale = expon.fit(data, floc=0)
    x = np.linspace(data.min(), data.max(), 300)
    y = expon.pdf(x, loc=loc, scale=scale)
    lam = 1.0 / scale
    label = f"Exponential  λ={lam:.4g}"
    return x, y, label, {"λ": lam}


def fit_maxwell_boltzmann(data: np.ndarray):
    """
    Fit a Maxwell-Boltzmann distribution to *data* with fixed location (loc=0).

    Parameters
    ----------
    data : numpy.ndarray
        1-D array of positive sample values.

    Returns
    -------
    x : numpy.ndarray
        300 evenly-spaced points spanning
        ``[max(data.min(), 0), data.max()]``.
    y : numpy.ndarray
        Maxwell-Boltzmann PDF evaluated at each point in *x*.
    label : str
        Human-readable label including the fitted scale parameter *a*.
    params : dict
        ``{"a": float}`` — fitted scale parameter.
    """
    loc, scale = maxwell.fit(data, floc=0)
    x = np.linspace(max(data.min(), 0), data.max(), 300)
    y = maxwell.pdf(x, loc=loc, scale=scale)
    label = f"Maxwell-Boltzmann  a={scale:.4g}"
    return x, y, label, {"a": scale}


def fit_poisson(data: np.ndarray):
    """
    Estimate the Poisson parameter μ from *data* and compute the PMF.

    The estimator is the sample mean, which is the MLE for the Poisson
    distribution.

    Parameters
    ----------
    data : numpy.ndarray
        1-D array of non-negative integer-valued samples (stored as float).

    Returns
    -------
    x : numpy.ndarray
        Integer x-values from ``int(data.min())`` to ``int(data.max())``
        inclusive, cast to float.
    y : numpy.ndarray
        Poisson PMF values at each integer in *x*.
    label : str
        Human-readable label including the estimated μ.
    params : dict
        ``{"μ": float}`` — estimated mean (sample mean of *data*).
    """
    mu = data.mean()
    x_int = np.arange(int(data.min()), int(data.max()) + 1)
    y = poisson.pmf(x_int, mu)
    label = f"Poisson  μ={mu:.4g}"
    return x_int.astype(float), y, label, {"μ": mu}


def fit_custom(data: np.ndarray, formula: str, param_names: list):
    """
    Fit a user-defined formula to the density histogram of *data*.

    The formula is evaluated in a sandboxed namespace that exposes NumPy
    ufuncs (e.g. ``exp``, ``sin``, ``sqrt``) and math constants.  NumPy
    ufuncs take priority over their scalar ``math`` counterparts so that
    array formulas work correctly.

    Parameters
    ----------
    data : numpy.ndarray
        1-D array of sample values used to build the histogram.
    formula : str
        Python expression in terms of ``x`` and the names listed in
        *param_names*.  Example: ``"a * exp(-b * x)"``.
    param_names : list of str
        Names of the free parameters appearing in *formula*.
        All initial guesses are set to 1.0.

    Returns
    -------
    x : numpy.ndarray
        300 evenly-spaced points spanning ``[data.min(), data.max()]``.
    y : numpy.ndarray
        Formula evaluated at *x* with the optimised parameters.
    label : str
        Human-readable label listing each fitted parameter value.
    params : dict
        Mapping of parameter name → fitted float value.

    Raises
    ------
    scipy.optimize.OptimizeWarning
        If the covariance of the parameters could not be estimated.
    RuntimeError
        If the least-squares minimisation fails entirely.

    Notes
    -----
    All initial parameter guesses are 1.0.  Formulas that require very
    different starting points may not converge from these defaults.
    """
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


# Registry mapping fit-method names (as they appear in FitDialog) to the
# corresponding fit function.  Each function accepts a 1-D NumPy array and
# returns ``(x, y, label, params_dict)``.  Only distribution fits are
# included here; spline, polynomial, linear, and custom fits are handled
# separately in mainwindow because they operate on xy data, not histograms.
FIT_FUNCTIONS = {
    "Gaussian":          fit_gaussian,
    "Exponential":       fit_exponential,
    "Maxwell-Boltzmann": fit_maxwell_boltzmann,
    "Poisson":           fit_poisson,
}
