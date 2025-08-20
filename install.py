#!/usr/bin/env python3
"""
Installation script for PyK150 PIC Programmer GUI
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def install_picpro():
    """Install picpro package"""
    print("Installing picpro package...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "picpro"])
        print("✓ picpro installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install picpro: {e}")
        print("Note: You may need to install picpro manually or use the original picpro source")
        return False

def create_desktop_entry():
    """Create desktop entry for Linux systems"""
    if sys.platform.startswith('linux'):
        desktop_entry = f"""[Desktop Entry]
Name=PyK150 PIC Programmer
Comment=GUI for PIC microcontroller programming
Exec=python3 {os.path.abspath('pyk150_gui.py')}
Icon=applications-electronics
Terminal=false
Type=Application
Categories=Development;Electronics;
"""
        
        desktop_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(desktop_dir, exist_ok=True)
        
        desktop_file = os.path.join(desktop_dir, "pyk150.desktop")
        try:
            with open(desktop_file, 'w') as f:
                f.write(desktop_entry)
            os.chmod(desktop_file, 0o755)
            print(f"✓ Desktop entry created: {desktop_file}")
        except Exception as e:
            print(f"✗ Failed to create desktop entry: {e}")

def main():
    print("PyK150 Installation Script")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        print("Installation failed. Please install requirements manually.")
        return
    
    # Try to install picpro
    install_picpro()
    
    # Create desktop entry
    create_desktop_entry()
    
    print("\nInstallation completed!")
    print("You can now run the application with:")
    print("  python3 pyk150_gui.py")
    
    # Test if GUI can be imported
    try:
        import tkinter
        print("✓ tkinter is available")
    except ImportError:
        print("✗ tkinter not available. Please install python3-tk package.")
    
    try:
        import serial
        print("✓ pyserial is available")
    except ImportError:
        print("✗ pyserial not available")

if __name__ == "__main__":
    main()
