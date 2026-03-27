"""
dataset.py — data loading and transform operations
"""

import numpy as np
from scipy.signal import savgol_filter


class DataSet:
    """Loads a whitespace-delimited data file, ignoring comment lines starting with '#'."""

    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]
        self.raw: list = []
        self._load()

    def _load(self):
        self.skipped_rows: list[tuple[int, str]] = []  # (line_number, content)
        with open(self.path) as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    self.raw.append([float(v) for v in line.split()])
                except ValueError:
                    self.skipped_rows.append((lineno, line))
        self.arr = np.array(self.raw) if self.raw else np.empty((0, 0))

    @property
    def ncols(self) -> int:
        return self.arr.shape[1] if self.arr.ndim == 2 and self.arr.size > 0 else 0

    @property
    def nrows(self) -> int:
        return self.arr.shape[0]

    def col(self, idx: int):
        """Return a copy of column idx, or None if out of range."""
        if idx < 0 or idx >= self.ncols:
            return None
        return self.arr[:, idx].copy()


def apply_transform(dataset: DataSet, cfg: dict) -> np.ndarray:
    """Apply a transform operation to a column of a DataSet."""
    col = dataset.col(cfg["col"])
    if col is None:
        raise ValueError(f"Column {cfg['col']} does not exist.")

    op  = cfg["op"]
    val = cfg["val"]

    if op == "multiply by constant":
        result = col * val
    elif op == "divide by constant":
        if val == 0:
            raise ValueError("Cannot divide by zero.")
        result = col / val
    elif op == "add constant":
        result = col + val
    elif op == "subtract constant":
        result = col - val
    elif op == "normalize by max":
        m = np.max(np.abs(col))
        if m == 0:
            raise ValueError("Max is zero, cannot normalize.")
        result = col / m
    elif op == "normalize by value":
        if val == 0:
            raise ValueError("Cannot normalize by zero.")
        result = col / val
    elif op == "numerical derivative (dy/dx)":
        xcol = dataset.col(cfg["xcol"])
        if xcol is None:
            raise ValueError(f"x column {cfg['xcol']} does not exist.")
        result = np.gradient(col, xcol)
    elif op == "moving average":
        w = max(3, int(val))
        if w % 2 == 0:
            w += 1
        wl = min(w, len(col) - (0 if len(col) % 2 != 0 else 1))
        result = savgol_filter(col, window_length=wl, polyorder=1)
    else:
        raise ValueError(f"Unknown operation: {op}")

    if cfg.get("new_col", True):
        dataset.arr = np.column_stack([dataset.arr, result])
    else:
        dataset.arr[:, cfg["col"]] = result

    return result
