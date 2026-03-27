"""
widgets.py — DatasetWidget: compact per-series panel
"""

import numpy as np

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
    QSpinBox, QCheckBox, QScrollArea, QFrame,
    QMessageBox, QFileDialog, QHBoxLayout,
)

from .constants import MARKERS, MARKER_LABELS, LINESTYLES, LINESTYLE_LABELS
from .dialogs import AppearanceDialog, HistAppearanceDialog


class DatasetWidget(QWidget):
    """
    Compact per-series control panel embedded in the left tab widget.

    Shows dataset name and dimensions, a histogram-mode toggle, column
    selectors for x, y, dx, dy (line mode) or a single column (histogram
    mode), an Appearance button, a duplicate-series button, and a
    visibility checkbox.  Style details are edited through
    :class:`~dialogs.AppearanceDialog` or
    :class:`~dialogs.HistAppearanceDialog`.

    Parameters
    ----------
    dataset : DataSet
        The dataset this widget controls.
    color : str
        Initial hex color string for the series (e.g. ``"#1f77b4"``).
    on_duplicate : callable, optional
        Called with *dataset* when the "Add another plot" button is
        clicked.
    on_replot : callable, optional
        Called with no arguments whenever a style change requires a
        full replot.
    parent : QWidget, optional
        Parent widget.
    """

    def __init__(self, dataset, color: str, on_duplicate=None,
                 on_replot=None, parent=None):
        super().__init__(parent)
        self.dataset      = dataset
        self.on_duplicate = on_duplicate
        self.on_replot    = on_replot   # callable: triggers a full replot

        # series style
        self._series_style = {
            "label":      dataset.name,
            "linestyle":  "-",
            "linewidth":  1.8,
            "marker":     "o",
            "markersize": 5.0,
            "color":      color,
            "face_color": color,
        }
        # histogram style
        self._hist_style = {
            "hist_bins":  "auto",
            "hist_nbins": 20,
            "hist_norm":  "count",
            "color":      color,
            "face_color": color,
        }

        self._build()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        inner  = QWidget()
        layout = QGridLayout(inner)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(5)

        nc = self.dataset.ncols
        nr = self.dataset.nrows

        layout.addWidget(QLabel(f"<b>{self.dataset.name}</b>"), 0, 0, 1, 4)
        layout.addWidget(QLabel(f"{nr} rows, {nc} cols"),       1, 0, 1, 4)

        # histogram mode
        self.hist_mode = QCheckBox("histogram mode")
        self.hist_mode.toggled.connect(self._toggle_mode)
        layout.addWidget(self.hist_mode, 2, 0, 1, 4)

        def col_spin(default):
            s = QSpinBox()
            s.setMinimum(-1)
            s.setMaximum(max(0, nc - 1))
            s.setValue(default if default < nc else -1)
            s.setSpecialValueText("—")
            s.setFixedWidth(55)
            return s

        # plot columns
        self._lbl_x  = QLabel("x:");  self.xcol  = col_spin(0)
        self._lbl_y  = QLabel("y:");  self.ycol  = col_spin(1)
        self._lbl_dx = QLabel("dx:"); self.dxcol = col_spin(-1)
        self._lbl_dy = QLabel("dy:"); self.dycol = col_spin(-1)
        layout.addWidget(self._lbl_x,  3, 0); layout.addWidget(self.xcol,  3, 1)
        layout.addWidget(self._lbl_y,  3, 2); layout.addWidget(self.ycol,  3, 3)
        layout.addWidget(self._lbl_dx, 4, 0); layout.addWidget(self.dxcol, 4, 1)
        layout.addWidget(self._lbl_dy, 4, 2); layout.addWidget(self.dycol, 4, 3)

        # histogram column
        self._lbl_hcol = QLabel("column:")
        self.hcol = col_spin(0)
        layout.addWidget(self._lbl_hcol, 3, 0); layout.addWidget(self.hcol, 3, 1)

        # appearance button (label editing is inside Appearance dialog)
        self.appear_btn = QPushButton("Appearance...")
        self.appear_btn.clicked.connect(self._open_appearance)
        layout.addWidget(self.appear_btn, 6, 0, 1, 4)

        # duplicate
        dup_btn = QPushButton("Add another plot from this file")
        dup_btn.clicked.connect(self._duplicate)
        layout.addWidget(dup_btn, 7, 0, 1, 4)

        # visibility
        self.visible = QCheckBox("visible"); self.visible.setChecked(True)
        layout.addWidget(self.visible, 8, 0, 1, 4)

        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        self._toggle_mode(False)

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def _toggle_mode(self, hist: bool):
        for w in [self._lbl_x,  self.xcol,  self._lbl_y,  self.ycol,
                  self._lbl_dx, self.dxcol, self._lbl_dy, self.dycol]:
            w.setVisible(not hist)
        for w in [self._lbl_hcol, self.hcol]:
            w.setVisible(hist)

    # ------------------------------------------------------------------
    # Appearance
    # ------------------------------------------------------------------

    def _open_appearance(self):
        if self.hist_mode.isChecked():
            cfg = dict(self._hist_style)
            dlg = HistAppearanceDialog(cfg, self)
            if dlg.exec_():
                self._hist_style.update(dlg.get_config())
                if self.on_replot:
                    self.on_replot()
        else:
            cfg = dict(self._series_style)
            dlg = AppearanceDialog(cfg, self)
            if dlg.exec_():
                self._series_style.update(dlg.get_config())
                if self.on_replot:
                    self.on_replot()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _duplicate(self):
        if self.on_duplicate:
            self.on_duplicate(self.dataset)

    def refresh_col_ranges(self):
        """
        Update the maximum value of all column spinboxes.

        Should be called after the underlying dataset gains or loses
        columns (e.g. after a transform operation adds a new column).
        """
        nc = max(0, self.dataset.ncols - 1)
        for w in [self.xcol, self.ycol, self.dxcol, self.dycol, self.hcol]:
            w.setMaximum(nc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_config(self) -> dict:
        """
        Return the current widget configuration as a plotting dict.

        In line mode the result includes series-style keys; in histogram
        mode it includes histogram-style keys instead.

        Returns
        -------
        dict
            Keys always present: ``"label"`` (str), ``"visible"`` (bool),
            ``"hist_mode"`` (bool), ``"xcol"``, ``"ycol"``, ``"dxcol"``,
            ``"dycol"``, ``"hcol"`` (int).  Additional keys from
            :attr:`_series_style` (line mode) or :attr:`_hist_style`
            (histogram mode) are merged in.
        """
        hist = self.hist_mode.isChecked()
        cfg = {
            "label":     self._series_style.get("label", self.dataset.name),
            "visible":   self.visible.isChecked(),
            "hist_mode": hist,
            "xcol":  self.xcol.value(),
            "ycol":  self.ycol.value(),
            "dxcol": self.dxcol.value(),
            "dycol": self.dycol.value(),
            "hcol":  self.hcol.value(),
        }
        if hist:
            cfg.update(self._hist_style)
        else:
            cfg.update(self._series_style)
        return cfg
