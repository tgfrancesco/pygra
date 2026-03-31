"""
dialogs.py — compatibility shim

All dialog classes and helpers live in the submodules:
  dialogs_style.py    — color palette helpers, StyleDialog, AppearanceDialog,
                        HistAppearanceDialog, Hist2DAppearanceDialog
  dialogs_analysis.py — FitDialog, TransformDialog, StatsDialog, DataEditorDialog
  dialogs_misc.py     — TextAnnotationDialog, PaletteDialog
"""

from .dialogs_style import *       # noqa: F401,F403
from .dialogs_analysis import *    # noqa: F401,F403
from .dialogs_misc import *        # noqa: F401,F403
