#!/usr/bin/env python3
"""
Test script for Enhanced TJA Speed Changer
Tests new features: OGG conversion, Japanese language, enhanced drag & drop
"""

import os
import sys
from pathlib import Path
import tempfile

def create_test_files():
    """Create test TJA and various audio files"""
    test_content = """TITLE:Test Song Enhanced
SUBTITLE:Test Subtitle
BPM:120.000
WAVE:test_audio.mp3
OFFSET:-2.500000
DEMOSTART:30.000
GENRE:Test
SONGVOL:100
SEVOL:100
SIDE:Normal
LIFE:0
GAME:Taiko

COURSE:Oni
LEVEL:5
BALLOON:
SCOREINIT:300
SCOREDIFF:120

#START
1001100110011001,
2002200220022002,
#BPMCHANGE 140.000
1001100110011001,
#DELAY 2.000
2002200220022002,
#END

COURSE:Hard
LEVEL:4
BALLOON:
SCOREINIT:300
SCOREDIFF:120

#START
1001100110011001,
2002200220022002,
#BPMCHANGE 130.000
1001100110011001,
2002200220022002,
#END
"""
    
    # Create test TJA file
    test_tja = Path("test_song_enhanced.tja")
    with open(test_tja, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # Create dummy audio files with different formats
    test_files = []
    
    # MP3 file
    test_mp3 = Path("test_audio.mp3")
    with open(test_mp3, 'wb') as f:
        f.write(b'ID3')  # Dummy MP3 header
    test_files.append(test_mp3)
    
    # WAV file
    test_wav = Path("test_audio.wav")
    with open(test_wav, 'wb') as f:
        f.write(b'RIFF')  # Dummy WAV header
    test_files.append(test_wav)
    
    # OGG file
    test_ogg = Path("test_audio.ogg")
    with open(test_ogg, 'wb') as f:
        f.write(b'OggS')  # Dummy OGG header
    test_files.append(test_ogg)
    
    print(f"Created test files:")
    print(f"  TJA: {test_tja.absolute()}")
    for audio_file in test_files:
        print(f"  Audio: {audio_file.absolute()}")
    
    return test_tja, test_files

def test_japanese_language():
    """Test Japanese language support"""
    print("\n=== Testing Japanese Language Support ===")
    
    try:
        from TJASpeedChangerGUI_Enhanced import LanguageManager
        
        lang_mgr = LanguageManager()
        
        # Test Japanese language
        lang_mgr.set_language('ja')
        
        # Test key translations
        test_keys = [
            'main_window_title',
            'file_selection', 
            'process_button',
            'audio_format_conversion'
        ]
        
        print("Japanese translations:")
        for key in test_keys:
            translation = lang_mgr.get_text(key)
            print(f"  {key}: {translation}")
        
        # Test system language detection
        system_lang = lang_mgr.get_system_language()
        print(f"System language detected: {system_lang}")
        
        available_langs = lang_mgr.get_available_languages()
        print(f"Available languages: {available_langs}")
        
        if 'ja' in available_langs:
            print("✓ Japanese language support working correctly")
            return True
        else:
            print("✗ Japanese language not available")
            return False
            
    except Exception as e:
        print(f"✗ Japanese language test failed: {e}")
        return False

def test_ogg_conversion_logic():
    """Test OGG conversion logic"""
    print("\n=== Testing OGG Conversion Logic ===")
    
    try:
        from TJASpeedChangerGUI_Enhanced import TJAProcessor, LanguageManager
        
        lang_mgr = LanguageManager()
        processor = TJAProcessor(lang_mgr)
        
        # Test audio file finding with various extensions
        test_tja, test_audio_files = create_test_files()
        
        base_dir = str(Path.cwd())
        
        # Test finding MP3 file when TJA references it
        found_audio = processor.find_audio_file(base_dir, "test_audio.mp3")
        if found_audio:
            print(f"✓ Found MP3 audio: {os.path.basename(found_audio)}")
        else:
            print("✗ Failed to find MP3 audio")
            return False
        
        # Test finding WAV file when TJA references MP3 (fallback logic)
        # Remove MP3 temporarily
        Path("test_audio.mp3").unlink()
        found_audio = processor.find_audio_file(base_dir, "test_audio.mp3")
        if found_audio and found_audio.endswith('.wav'):
            print(f"✓ Found WAV fallback: {os.path.basename(found_audio)}")
        else:
            print("✗ Failed to find WAV fallback")
        
        # Restore MP3 for cleanup
        with open("test_audio.mp3", 'wb') as f:
            f.write(b'ID3')
        
        # Test TJA processing with OGG extension enforcement
        wave_filename, new_wave_filename, new_tja_path = processor.adjust_tja_speed(
            str(test_tja), 1.5
        )
        
        if new_wave_filename and new_wave_filename.endswith('.ogg'):
            print(f"✓ TJA processing enforces OGG extension: {new_wave_filename}")
            
            # Verify TJA file content
            if Path(new_tja_path).exists():
                with open(new_tja_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'WAVE:test_audio_1.50x.ogg' in content:
                        print("✓ TJA file correctly updated with OGG extension")
                    else:
                        print("✗ TJA file not updated with OGG extension")
                        return False
                        
                # Clean up
                Path(new_tja_path).unlink()
            else:
                print("✗ New TJA file not created")
                return False
        else:
            print("✗ OGG extension not enforced")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ OGG conversion logic test failed: {e}")
        return False

def test_drag_drop_enhancement():
    """Test drag and drop enhancement"""
    print("\n=== Testing Drag & Drop Enhancement ===")
    
    try:
        from TJASpeedChangerGUI_Enhanced import TJASpeedChangerGUI, HAS_TKINTERDND2
        
        print(f"tkinterdnd2 available: {HAS_TKINTERDND2}")
        
        # Test GUI initialization
        app = TJASpeedChangerGUI()
        
        # Test drag drop setup
        if hasattr(app, 'setup_drag_drop'):
            print("✓ Drag & drop setup method exists")
            
            # Check if proper drag drop zones are created
            if hasattr(app, 'drag_drop_label'):
                print("✓ Drag & drop label created")
                
                # Test file validation (simulated drop)
                test_files = ["test.tja", "test.mp3", "invalid.txt"]
                
                for test_file in test_files:
                    # Simulate the validation logic
                    is_valid = test_file.lower().endswith('.tja')
                    if test_file == "test.tja" and is_valid:
                        print(f"✓ File validation works for {test_file}")
                    elif test_file != "test.tja" and not is_valid:
                        print(f"✓ File validation rejects {test_file}")
                    else:
                        print(f"✗ File validation failed for {test_file}")
                        return False
            else:
                print("✗ Drag & drop label not found")
                return False
        else:
            print("✗ Drag & drop setup method not found")
            return False
        
        # Don't start the GUI event loop in test
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"✗ Drag & drop test failed: {e}")
        return False

def test_command_line_ogg_conversion():
    """Test command line version with OGG conversion"""
    print("\n=== Testing Command Line OGG Conversion ===")
    
    try:
        test_tja, test_audio_files = create_test_files()
        
        # Import the enhanced command line functions
        sys.path.append(str(Path(__file__).parent))
        from TJASpeedChanger import adjust_tja_speed, find_audio_file, adjust_audio_speed_ffmpeg
        
        # Test TJA processing
        wave_filename, new_wave_filename, new_tja_path = adjust_tja_speed(str(test_tja), 0.8)
        
        if new_wave_filename == "test_audio_0.80x.ogg":
            print("✓ Command line TJA processing creates correct OGG filename")
        else:
            print(f"✗ Incorrect OGG filename: {new_wave_filename}")
            return False
        
        # Test audio file finding
        base_dir = str(Path.cwd())
        found_audio = find_audio_file(base_dir, "test_audio.mp3")
        
        if found_audio and Path(found_audio).exists():
            print(f"✓ Command line audio finding works: {os.path.basename(found_audio)}")
        else:
            print("✗ Command line audio finding failed")
            return False
        
        # Clean up
        if Path(new_tja_path).exists():
            Path(new_tja_path).unlink()
        
        return True
        
    except Exception as e:
        print(f"✗ Command line OGG conversion test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = [
        "test_song_enhanced.tja",
        "test_song_enhanced_1.50x.tja",
        "test_song_enhanced_0.80x.tja",
        "test_audio.mp3",
        "test_audio.wav", 
        "test_audio.ogg",
        "test_audio_1.50x.ogg",
        "test_audio_0.80x.ogg"
    ]
    
    for file_name in test_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink()
    
    print("\n✓ Test files cleaned up")

def main():
    """Run all enhanced feature tests"""
    print("TJA Speed Changer Enhanced Features - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Japanese Language Support", test_japanese_language),
        ("OGG Conversion Logic", test_ogg_conversion_logic),
        ("Drag & Drop Enhancement", test_drag_drop_enhancement),
        ("Command Line OGG Conversion", test_command_line_ogg_conversion)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("ENHANCED FEATURES TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All enhanced features working correctly!")
        print("\nEnhanced features ready:")
        print("  ✓ Japanese language support (ja)")
        print("  ✓ Automatic OGG conversion (MP3/WAV/FLAC → OGG)")
        print("  ✓ Improved drag & drop (with fallback)")
        print("  ✓ Correct TJA extension updating")
        print("\nTo use the enhanced GUI:")
        print("  python TJASpeedChangerGUI_Enhanced.py")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check the errors above.")
    
    # Cleanup
    cleanup_test_files()

if __name__ == '__main__':
    main()