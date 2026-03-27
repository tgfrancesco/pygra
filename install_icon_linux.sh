#!/usr/bin/env bash
# Install PyGRA icon and .desktop file on Linux
# Run once after installing PyGRA:  bash install_icon_linux.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_SRC="$SCRIPT_DIR/logo/pygra_icon.png"

# fallback to old logo if new icon not present
if [ ! -f "$ICON_SRC" ]; then
    ICON_SRC="$SCRIPT_DIR/logo/pygra_logo.png"
fi
if [ ! -f "$ICON_SRC" ]; then
    ICON_SRC="$SCRIPT_DIR/pygra_logo.png"
fi

if [ ! -f "$ICON_SRC" ]; then
    echo "Error: could not find PyGRA icon file."
    exit 1
fi

# Install icon
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$ICON_DIR"
cp "$ICON_SRC" "$ICON_DIR/pygra.png"
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

# Install .desktop file
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

# Find pygra executable
PYGRA_BIN="$(which pygra 2>/dev/null || echo "pygra")"

cat > "$DESKTOP_DIR/pygra.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=PyGRA
Comment=Interactive scientific data plotter
Exec=$PYGRA_BIN %F
Icon=pygra
Terminal=false
Categories=Science;Education;DataVisualization;
MimeType=text/plain;
StartupWMClass=pygra
DESKTOP

chmod +x "$DESKTOP_DIR/pygra.desktop"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "PyGRA icon and launcher installed."
echo "You may need to log out and back in for the dock icon to appear."
