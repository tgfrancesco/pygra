"""
dialogs_misc.py — miscellaneous dialogs: text annotations and palette browser
"""

from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QHBoxLayout,
    QDoubleSpinBox, QCheckBox,
    QLabel, QListWidget, QGridLayout,
    QPushButton, QScrollArea, QWidget, QTextEdit,
)
from PyQt5.QtCore import Qt

from .dialogs_style import pick_color


# ---------------------------------------------------------------------------
# TextAnnotationDialog
# ---------------------------------------------------------------------------

class TextAnnotationDialog(QDialog):
    """
    Dialog for adding or editing a text annotation on the plot.

    Parameters
    ----------
    cfg : dict, optional
        Pre-fill values with keys ``"text"``, ``"fontsize"``, ``"color"``,
        ``"bold"``, ``"rotation"``.  Defaults to empty text, size 12, black,
        not bold, 0° rotation.
    parent : QWidget, optional
        Parent widget.
    """

    def __init__(self, cfg: dict | None = None, parent=None):
        super().__init__(parent)
        cfg = cfg or {}
        self.setWindowTitle("Text annotation")
        self._color = cfg.get("color", "#000000")
        self._build(cfg)

    def _build(self, cfg: dict):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Build button box first so the text widget can reference the OK button
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        ok_btn = btns.button(QDialogButtonBox.Ok)

        # Multiline QTextEdit — Enter confirms, Shift+Enter inserts newline
        class _TextEdit(QTextEdit):
            def keyPressEvent(self_, event):
                if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                    if event.modifiers() & Qt.ShiftModifier:
                        self_.insertPlainText("\n")
                    else:
                        ok_btn.click()
                else:
                    super().keyPressEvent(event)

        self.text_edit = _TextEdit()
        self.text_edit.setPlainText(cfg.get("text", ""))
        self.text_edit.setFixedHeight(72)
        form.addRow("Text\n(Shift+Enter = newline):", self.text_edit)

        self.fontsize = QDoubleSpinBox()
        self.fontsize.setRange(6.0, 48.0); self.fontsize.setSingleStep(0.5)
        self.fontsize.setValue(cfg.get("fontsize", 12.0))
        form.addRow("Font size:", self.fontsize)

        self.rotation = QDoubleSpinBox()
        self.rotation.setRange(-180.0, 180.0); self.rotation.setSingleStep(5.0)
        self.rotation.setValue(cfg.get("rotation", 0.0))
        form.addRow("Rotation (°):", self.rotation)

        self.bold_cb = QCheckBox()
        self.bold_cb.setChecked(cfg.get("bold", False))
        form.addRow("Bold:", self.bold_cb)

        self.color_btn = QPushButton()
        self._refresh_btn()
        self.color_btn.clicked.connect(self._pick_color)
        form.addRow("Color:", self.color_btn)

        layout.addLayout(form)
        layout.addWidget(btns)

    def _refresh_btn(self):
        self.color_btn.setStyleSheet(
            f"background-color: {self._color}; border: 1px solid #888; "
            f"border-radius: 4px; min-width: 80px; padding: 4px;"
        )
        self.color_btn.setText(self._color)

    def _pick_color(self):
        new_color = pick_color(self._color, self)
        if new_color != self._color:
            self._color = new_color
            self._refresh_btn()

    def get_config(self) -> dict:
        """
        Return the annotation configuration chosen by the user.

        Returns
        -------
        dict
            Keys: ``"text"`` (str), ``"fontsize"`` (float), ``"rotation"``
            (float), ``"color"`` (str), ``"bold"`` (bool).
        """
        return {
            "text":     self.text_edit.toPlainText(),
            "fontsize": self.fontsize.value(),
            "rotation": self.rotation.value(),
            "color":    self._color,
            "bold":     self.bold_cb.isChecked(),
        }


# ---------------------------------------------------------------------------
# PaletteDialog
# ---------------------------------------------------------------------------

class PaletteDialog(QDialog):
    """
    Scientific color palette browser.

    Groups palettes by category (colorblind-friendly, matplotlib
    categorical, sequential/diverging, CSS colors).  Clicking a color
    swatch sets :attr:`selected_color`; accepting the dialog returns it
    to the caller.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget.

    Attributes
    ----------
    selected_color : str or None
        The hex color string last clicked by the user, or ``None`` if no
        color has been selected yet.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scientific color palettes")
        self.selected_color = None
        self._build()
        self.resize(500, 400)

    def _build(self):
        from .palettes import PALETTES, PALETTE_GROUPS
        layout = QHBoxLayout(self)

        left = QVBoxLayout()
        self.group_list = QListWidget(); self.group_list.setMaximumWidth(170)
        for group in PALETTE_GROUPS:
            self.group_list.addItem(group)
        self.group_list.currentTextChanged.connect(self._on_group)
        left.addWidget(QLabel("Group:")); left.addWidget(self.group_list)

        self.palette_list = QListWidget(); self.palette_list.setMaximumWidth(170)
        self.palette_list.currentTextChanged.connect(self._on_palette)
        left.addWidget(QLabel("Palette:")); left.addWidget(self.palette_list)
        layout.addLayout(left)

        right = QVBoxLayout()
        right.addWidget(QLabel("Click a color to select it:"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        self._swatch_container = QWidget()
        self._swatch_layout = QGridLayout(self._swatch_container)
        self._swatch_layout.setSpacing(3)
        scroll.setWidget(self._swatch_container)
        right.addWidget(scroll)

        self._selected_lbl = QLabel("Selected: —"); self._selected_lbl.setFixedHeight(28)
        right.addWidget(self._selected_lbl)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        right.addWidget(btns)
        layout.addLayout(right)

        if self.group_list.count():
            self.group_list.setCurrentRow(0)

    def _on_group(self, group):
        from .palettes import PALETTE_GROUPS
        self.palette_list.clear()
        for name in PALETTE_GROUPS.get(group, []):
            self.palette_list.addItem(name)
        if self.palette_list.count():
            self.palette_list.setCurrentRow(0)

    def _on_palette(self, name):
        from .palettes import PALETTES
        while self._swatch_layout.count():
            item = self._swatch_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for i, hex_c in enumerate(PALETTES.get(name, [])):
            btn = QPushButton(); btn.setFixedSize(40, 40)
            btn.setToolTip(hex_c)
            btn.setStyleSheet(f"background-color: {hex_c}; border: 2px solid #888; border-radius: 4px;")
            btn.clicked.connect(lambda checked, c=hex_c: self._select(c))
            self._swatch_layout.addWidget(btn, i // 8, i % 8)

    def _select(self, color: str):
        self.selected_color = color
        light = sum(int(color.lstrip("#")[i:i+2], 16) for i in (0,2,4)) / 3 > 128
        self._selected_lbl.setText(f"Selected: {color}")
        self._selected_lbl.setStyleSheet(
            f"background-color: {color}; color: {'#000' if light else '#fff'};"
            f"padding: 4px; border-radius: 4px;"
        )
