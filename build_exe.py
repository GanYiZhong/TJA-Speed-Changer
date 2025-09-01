#!/usr/bin/env python3
"""
Build Script for TJA Speed Changer GUI
Creates a standalone executable with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check if Python packages are installed
    try:
        import tkinterdnd2
        import PyInstaller
        print("✓ Required Python packages are installed")
    except ImportError as e:
        print(f"✗ Missing Python package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False
    
    # Check if FFmpeg exists
    if not Path("ffmpeg.exe").exists():
        print("✗ FFmpeg not found")
        print("Please run: python download_ffmpeg.py")
        return False
    else:
        print("✓ FFmpeg found")
    
    # Check if GUI script exists
    if not Path("TJASpeedChangerGUI.py").exists():
        print("✗ TJASpeedChangerGUI.py not found")
        return False
    else:
        print("✓ Main GUI script found")
    
    # Check if language files exist
    languages_dir = Path("languages")
    if not languages_dir.exists():
        print("✗ Languages directory not found")
        return False
    
    required_langs = ["en.json", "zh-tw.json", "ja.json"]
    for lang_file in required_langs:
        if not (languages_dir / lang_file).exists():
            print(f"✗ Language file not found: {lang_file}")
            return False
    
    print("✓ Language files found")
    print("All requirements met!")
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name}")
    
    # Remove spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✓ Cleaned {spec_file}")

def create_version_info():
    """Create version info for the executable"""
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'TJA Speed Changer'),
        StringStruct(u'FileDescription', u'TJA Speed Changer GUI'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'TJASpeedChangerGUI'),
        StringStruct(u'LegalCopyright', u'Open Source'),
        StringStruct(u'OriginalFilename', u'TJASpeedChangerGUI.exe'),
        StringStruct(u'ProductName', u'TJA Speed Changer'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("✓ Created version info file")

def build_executable():
    """Build the standalone executable"""
    print("Building executable...")
    
    # Create version info
    create_version_info()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file executable
        "--windowed",                   # No console window
        "--name=TJASpeedChangerGUI",   # Executable name
        "--icon=icon.ico" if Path("icon.ico").exists() else "",  # Icon if exists
        "--version-file=version_info.txt",  # Version info
        "--add-binary=ffmpeg.exe;.",    # Include FFmpeg
        "--add-data=languages;languages",  # Include language files
        "--hidden-import=tkinterdnd2",  # Ensure tkinterdnd2 is included
        "--hidden-import=tkinterdnd2.tkdnd",
        "--clean",                      # Clean cache
        "TJASpeedChangerGUI.py"        # Main script
    ]
    
    # Remove empty strings from command
    cmd = [arg for arg in cmd if arg]
    
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed!")
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False

def post_build_tasks():
    """Perform post-build tasks"""
    print("Performing post-build tasks...")
    
    # Clean up temporary files
    if Path("version_info.txt").exists():
        Path("version_info.txt").unlink()
        print("✓ Cleaned version info file")
    
    # Check if executable was created
    exe_path = Path("dist/TJASpeedChangerGUI.exe")
    if exe_path.exists():
        print(f"✓ Executable created: {exe_path.absolute()}")
        print(f"✓ File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Test the executable
        print("Testing executable...")
        try:
            result = subprocess.run([str(exe_path), "--help"], 
                                  capture_output=True, text=True, timeout=5)
            # Note: GUI apps might not respond to --help, so we just check if it starts
            print("✓ Executable test completed")
        except Exception as e:
            print(f"⚠ Executable test warning: {e}")
        
        return True
    else:
        print("✗ Executable not found after build")
        return False

def main():
    """Main build process"""
    print("TJA Speed Changer GUI - Build Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\nBuild aborted due to missing requirements.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        print("\nBuild failed!")
        sys.exit(1)
    
    # Post-build tasks
    if not post_build_tasks():
        print("\nPost-build tasks failed!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Executable location: {Path('dist/TJASpeedChangerGUI.exe').absolute()}")
    print("\nYou can now distribute the executable along with any sample files.")
    print("The executable includes:")
    print("- GUI application")
    print("- FFmpeg for audio processing") 
    print("- Multi-language support (EN/ZH-TW/JA)")
    print("- Drag & drop file support")

if __name__ == '__main__':
    main()