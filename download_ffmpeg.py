#!/usr/bin/env python3
"""
FFmpeg Download Utility
Downloads and extracts FFmpeg static build for packaging
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path
import ssl

def download_ffmpeg():
    """Download FFmpeg static build for Windows"""
    
    print("Downloading FFmpeg static build...")
    
    # FFmpeg static build URL (Windows 64-bit)
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    # Create downloads directory
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    
    zip_path = downloads_dir / "ffmpeg.zip"
    
    try:
        # Create SSL context that doesn't verify certificates (for compatibility)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        print(f"Downloading from: {ffmpeg_url}")
        print(f"Saving to: {zip_path}")
        
        # Download with progress
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded * 100) // total_size)
                print(f"\rProgress: {percent}% ({downloaded // 1024 // 1024} MB)", end="")
            else:
                print(f"\rDownloaded: {downloaded // 1024 // 1024} MB", end="")
        
        urllib.request.urlretrieve(ffmpeg_url, zip_path, progress_hook)
        print("\nDownload completed!")
        
        # Extract FFmpeg
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find ffmpeg.exe in the zip
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('ffmpeg.exe'):
                    # Extract just the ffmpeg.exe file
                    print(f"Extracting: {file_info.filename}")
                    file_info.filename = 'ffmpeg.exe'  # Rename to simple name
                    zip_ref.extract(file_info, '.')
                    break
            else:
                print("Error: ffmpeg.exe not found in the archive!")
                return False
        
        # Clean up
        zip_path.unlink()
        downloads_dir.rmdir()
        
        print("FFmpeg extraction completed!")
        print(f"FFmpeg executable: {Path('ffmpeg.exe').absolute()}")
        return True
        
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        return False

def verify_ffmpeg():
    """Verify FFmpeg installation"""
    ffmpeg_path = Path("ffmpeg.exe")
    if not ffmpeg_path.exists():
        return False
    
    try:
        import subprocess
        result = subprocess.run([str(ffmpeg_path), '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("FFmpeg verification successful!")
            print(f"Version info: {result.stdout.split()[2]}")
            return True
        else:
            print("FFmpeg verification failed!")
            return False
    except Exception as e:
        print(f"Error verifying FFmpeg: {e}")
        return False

if __name__ == '__main__':
    print("FFmpeg Download Utility for TJA Speed Changer")
    print("=" * 50)
    
    # Check if FFmpeg already exists
    if Path("ffmpeg.exe").exists():
        print("FFmpeg already exists. Verifying...")
        if verify_ffmpeg():
            print("FFmpeg is ready to use!")
            sys.exit(0)
        else:
            print("Existing FFmpeg is not working. Re-downloading...")
            Path("ffmpeg.exe").unlink()
    
    # Download FFmpeg
    if download_ffmpeg():
        if verify_ffmpeg():
            print("\nFFmpeg is ready for packaging!")
        else:
            print("\nWarning: FFmpeg download completed but verification failed.")
            sys.exit(1)
    else:
        print("\nFFmpeg download failed!")
        sys.exit(1)