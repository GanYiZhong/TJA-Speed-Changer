#!/usr/bin/env python3
"""
Setup script for TJA Speed Changer GUI
Installs dependencies and creates logo
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    packages = ["Pillow"]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    # Optional packages
    optional_packages = ["tkinterdnd2"]
    
    for package in optional_packages:
        try:
            print(f"Installing optional package {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠ Optional package {package} failed to install: {e}")
            print("  This is not critical - the app will still work")
    
    return True

def create_logo_if_needed():
    """Create logo if it doesn't exist"""
    logo_path = Path("LOGO_BLACK_TRANS.png")
    
    if logo_path.exists():
        print("✓ Logo already exists")
        return True
    
    print("Creating logo...")
    try:
        import create_logo
        create_logo.create_logo()
        return True
    except Exception as e:
        print(f"✗ Failed to create logo: {e}")
        print("  The app will use text logo instead")
        return False

def main():
    """Main setup process"""
    print("TJA Speed Changer GUI - Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed due to dependency installation issues")
        sys.exit(1)
    
    # Create logo
    create_logo_if_needed()
    
    # Final status
    print("\n" + "=" * 40)
    print("SETUP COMPLETED!")
    print("=" * 40)
    
    print("You can now run the GUI with:")
    print("  python TJASpeedChangerGUI_Final.py")
    print("\nOr use the launcher:")
    print("  python start_gui.py")
    
    # Check for FFmpeg
    try:
        result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n✓ FFmpeg found in system PATH")
        else:
            print("\n⚠ FFmpeg not found in system PATH")
            print("  You can download it with: python download_ffmpeg.py")
    except:
        print("\n⚠ Cannot check for FFmpeg")
        print("  You may need to download it with: python download_ffmpeg.py")

if __name__ == '__main__':
    main()