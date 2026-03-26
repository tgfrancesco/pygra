# Changelog

## [0.4.0] - 2026-03-26

### Changed — UI redesign
- "Plot" button moved back to the main panel (bottom of left panel), always visible
- "Load files" button moved to top of left panel, always visible
- Toolbar replaced with minimal custom toolbar: Zoom, Pan, Reset only (no duplicate actions)
- "Transform data" and "Statistics" moved to Analysis menu
- "Fit & Interpolation" unified in Analysis menu (interpolation and distribution fits in one dialog)
- "Appearance" dialog (ex "Series style") separated from interpolation; triggers auto-replot on OK
- Fit layers listed in a dedicated panel with per-layer visibility toggle and remove button
- Fit results appear automatically on the plot without additional steps

### Added
- FitDialog: shows formula read-only for predefined methods; Custom fields enabled only when "Custom..." selected
- Fit line color picker in FitDialog
- FitLayer panel: each fit/interpolation curve can be toggled visible/invisible or removed
- Cross-platform: macOS (menu in system bar), Linux, Windows

### Removed
- Undo/Redo
- Duplicate matplotlib toolbar buttons

## [0.3.0] - 2025-03-26

### Added
- Menu bar (File, Analysis, View)
- Distribution fits: Gaussian, Exponential, Maxwell-Boltzmann, Poisson, Custom
- Statistics dialog
- Export data
- Plot themes and DPI control
- AppearanceDialog / HistAppearanceDialog

## [0.2.0] - 2025-03-20

### Added
- Multiple plots from the same file
- Histogram mode
- Data transforms
- Session save/load
- CLI interface
- Interpolation overlays

## [0.1.0] - 2025-03-15

### Added
- Initial release
