#!/usr/bin/env python3
"""
Test script for encoding detection functionality
"""

import os
import sys
from pathlib import Path

# Add current directory to path to import our GUI module
sys.path.insert(0, str(Path(__file__).parent))

def test_encoding_detection():
    """Test the encoding detection functionality"""
    print("Testing Encoding Detection")
    print("=" * 40)
    
    # Import the GUI class
    try:
        from TJASpeedChangerGUI_Final import TJASpeedChangerGUI
        gui = TJASpeedChangerGUI()
        print("✓ GUI class imported successfully")
    except Exception as e:
        print(f"✗ Failed to import GUI class: {e}")
        return False
    
    # Test with any existing TJA files in the directory
    tja_files = list(Path(".").glob("*.tja"))
    
    if not tja_files:
        # Create a test TJA file with UTF-8 encoding
        test_content = """TITLE:Test Song
SUBTITLE:Encoding Test
BPM:120
WAVE:test.ogg

#START

1010,
1010,

#END
"""
        test_file = Path("test_utf8.tja")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        tja_files = [test_file]
        print("Created test TJA file with UTF-8 encoding")
    
    # Test encoding detection on each file
    for tja_file in tja_files:
        print(f"\nTesting file: {tja_file}")
        try:
            encoding = gui.detect_file_encoding(str(tja_file))
            print(f"  Detected encoding: {encoding}")
            
            # Try to read the file with detected encoding
            with open(tja_file, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"  File size: {len(content)} characters")
                print("  ✓ Successfully read with detected encoding")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 40)
    print("Encoding detection test completed!")
    return True

if __name__ == "__main__":
    test_encoding_detection()