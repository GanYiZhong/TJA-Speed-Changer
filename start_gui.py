#!/usr/bin/env python3
"""
TJA Speed Changer - GUI Launcher
Automatically detects best GUI version to use
"""

import sys
import subprocess
from pathlib import Path

def check_tkinterdnd2():
    """Check if tkinterdnd2 is available"""
    try:
        import tkinterdnd2
        return True
    except ImportError:
        return False

def main():
    print("TJA Speed Changer GUI - Launcher")
    print("=" * 40)
    
    # Check available versions (prefer final version)
    final_version = Path("TJASpeedChangerGUI_Final.py")
    enhanced_version = Path("TJASpeedChangerGUI_Enhanced.py")
    basic_version = Path("TJASpeedChangerGUI_Basic.py")
    simple_version = Path("TJASpeedChangerGUI_Simple.py")
    
    # Choose best version
    if final_version.exists():
        print("✓ Using final version (recommended - all features included)")
        gui_script = "TJASpeedChangerGUI_Final.py"
    elif enhanced_version.exists() and check_tkinterdnd2():
        print("✓ Enhanced version available with full drag & drop support")
        gui_script = "TJASpeedChangerGUI_Enhanced.py"
    elif basic_version.exists():
        print("✓ Using basic version (guaranteed compatibility)")
        gui_script = "TJASpeedChangerGUI_Basic.py"
    elif simple_version.exists():
        print("✓ Using simple version")
        gui_script = "TJASpeedChangerGUI_Simple.py"
    else:
        print("✗ No GUI version found!")
        sys.exit(1)
    
    print(f"Starting: {gui_script}")
    print("-" * 40)
    
    try:
        # Start the GUI
        subprocess.run([sys.executable, gui_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGUI closed by user")
        sys.exit(0)

if __name__ == '__main__':
    main()