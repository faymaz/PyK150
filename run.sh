#!/bin/bash
# Launcher script for PyK150 with picpro dependency check

echo "Starting PyK150 PIC Programmer GUI..."

# Check if picpro is installed
if ! command -v picpro &> /dev/null; then
    echo "WARNING: 'picpro' command not found in PATH!"
    echo ""
    echo "PyK150 requires the 'picpro' tool to function properly."
    echo "Please install picpro or configure the correct path in the application settings."
    echo ""
    echo "You can:"
    echo "1. Install picpro system-wide and add it to your PATH"
    echo "2. Or configure the full path to picpro executable in PyK150 settings"
    echo ""
    echo "Continuing to start PyK150 GUI..."
    echo "----------------------------------------"
fi

python3 pyk150_gui.py
