"""
state.py — save and load application state as JSON
"""

import json
import numpy as np


def save_state(path: str, dataset_widgets: list, axis_settings: dict, style_settings: dict):
    """Serialise the full application state to a JSON file."""
    series = []
    for dw in dataset_widgets:
        cfg = dw.get_config()
        series.append({
            "path":   dw.dataset.path,
            "name":   dw.dataset.name,
            "data":   dw.dataset.arr.tolist(),
            "config": cfg,
        })
    state = {
        "version":        "0.3.0",
        "series":         series,
        "axis_settings":  axis_settings,
        "style_settings": style_settings,
    }
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def load_state(path: str) -> dict:
    """Load application state from a JSON file."""
    with open(path) as f:
        state = json.load(f)
    for s in state["series"]:
        s["data"] = np.array(s["data"])
    return state
