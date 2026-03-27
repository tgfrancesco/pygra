"""
preferences.py — persistent user preferences
Stored in ~/.config/pygra/preferences.json
"""

import json
import os
import sys
from pathlib import Path

from .constants import DEFAULT_STYLE_SETTINGS

PREFS_PATH = Path.home() / ".config" / "pygra" / "preferences.json"

DEFAULT_PREFS = {
    # window geometry
    "window_x":      100,
    "window_y":      100,
    "window_w":      1200,
    "window_h":      760,
    "splitter_pos":  330,   # left panel width in pixels

    # style settings (mirrors DEFAULT_STYLE_SETTINGS)
    **DEFAULT_STYLE_SETTINGS,

    # saved custom colors (list of hex strings)
    "custom_colors": [],
    # last selected basic colors palette
    "last_basic_palette": "",
}


def load_prefs() -> dict:
    """
    Load user preferences from disk.

    Reads ``~/.config/pygra/preferences.json`` and merges the saved
    values over :data:`DEFAULT_PREFS`.  If the file does not exist the
    defaults are returned silently.  If the file exists but cannot be
    parsed, a warning is printed to stderr and the defaults are returned.

    Returns
    -------
    dict
        Preference dictionary containing all keys from
        :data:`DEFAULT_PREFS`, with any saved overrides applied.
    """
    prefs = dict(DEFAULT_PREFS)
    if PREFS_PATH.exists():
        try:
            with open(PREFS_PATH) as f:
                saved = json.load(f)
            prefs.update(saved)
        except Exception as e:
            print(f"Warning: could not load preferences from {PREFS_PATH}: {e}", file=sys.stderr)
    return prefs


def save_prefs(prefs: dict):
    """
    Persist *prefs* to ``~/.config/pygra/preferences.json``.

    The parent directory is created automatically if it does not exist.

    Parameters
    ----------
    prefs : dict
        Preference dictionary to serialise as JSON.

    Raises
    ------
    OSError
        If the file cannot be written (e.g. permission denied).
    """
    PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFS_PATH, "w") as f:
        json.dump(prefs, f, indent=2)
