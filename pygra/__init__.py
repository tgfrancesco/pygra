"""PyGRA — interactive scientific data plotter"""

from .dataset import DataSet, apply_transform
from .widgets import DatasetWidget
from .dialogs import StyleDialog, TransformDialog, StatsDialog
from .mainwindow import MainWindow
from .state import save_state, load_state
from .main import main

__version__ = "0.4.0"
__author__  = "Francesco Tosti Guerra"
