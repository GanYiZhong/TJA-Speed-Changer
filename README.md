# TJA Speed Changer GUI

A graphical user interface tool for modifying TJA files and audio source speed for Taiko no Tatsufin.

[中文說明]([https://pages.github.com/](https://github.com/GanYiZhong/TJA-Speed-Changer/blob/main/README_CH.md))

## Features

- **GUI Interface**: Easy-to-use graphical interface with enhanced drag & drop support
- **Multi-language Support**: English, Traditional Chinese, and Japanese (日本語)
- **Smart Audio Processing**: Automatic conversion of MP3/WAV/FLAC to OGG format with speed adjustment
- **TJA File Processing**: Modify BPM, OFFSET, DEMOSTART, and other parameters with automatic OGG extension updating
- **Flexible Audio Input**: Automatically finds audio files with different extensions (mp3, wav, ogg, flac, m4a, aac)
- **Standalone Executable**: Self-contained executable with embedded FFmpeg

## Requirements

### For Running the Executable
- Windows 10/11 (64-bit)
- No additional software required (FFmpeg is embedded)

### For Development
- Python 3.8+
- Required packages (see `requirements.txt`)
- FFmpeg (automatically downloaded by build script)

## Installation

### Option 1: Download Pre-built Executable
1. Download `TJASpeedChangerGUI.exe` from the releases
2. Run the executable directly
3. No installation required

### Option 2: Build from Source

1. **Clone or download the source code**
   ```bash
   # If using git
   git clone https://github.com/GanYiZhong/TJA-Speed-Changer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download FFmpeg**
   ```bash
   python download_ffmpeg.py
   ```

4. **Run the GUI application**
   ```bash
   # Enhanced version (recommended - includes all new features)
   python TJASpeedChangerGUI_Enhanced.py
   
   # Or simplified version (works without tkinterdnd2)
   python TJASpeedChangerGUI_Simple.py
   ```

5. **Build standalone executable (optional)**
   ```bash
   python build_exe.py
   ```

## Usage

### GUI Application

1. **Select TJA File**
   - Click "Browse..." to select a TJA file
   - Or drag and drop a TJA file into the application window

2. **Adjust Speed**
   - Use the slider to set speed multiplier (0.5x to 2.0x)
   - Real-time display of selected speed

3. **Choose Language**
   - Select your preferred language from the dropdown
   - Interface will update immediately

4. **Process Files**
   - Click "Process Files" to start
   - Monitor progress in the results area
   - New files will be created with speed suffix

### Command Line (Original)

```bash
python TJASpeedChanger.py song.tja 1.2 --lang en
```

## File Processing

The tool processes:

### TJA Files
- **BPM**: Adjusted proportionally to speed
- **OFFSET**: Adjusted inversely to speed
- **DEMOSTART**: Adjusted inversely to speed
- **BPMCHANGE**: All tempo changes adjusted
- **DELAY**: Delay commands adjusted
- **WAVE**: Audio filename updated with speed suffix
- **TITLE**: Title updated with speed indicator

### Audio Files
- **Smart Format Detection**: Automatically finds audio files with various extensions (mp3, wav, ogg, flac, m4a, aac)
- **Universal OGG Conversion**: All audio formats are converted to OGG Vorbis for consistency
- Speed adjustment using FFmpeg's `atempo` filter while preserving original pitch
- High-quality OGG encoding with optimal quality settings
- Handles complex speed ratios with filter chaining for extreme speeds

## Output Files

The tool creates new files with speed suffix:
- `song_1.20x.tja` (modified TJA file with updated WAVE path)
- `audio_1.20x.ogg` (speed-adjusted and format-converted audio file)

**Note**: All audio files are converted to OGG format regardless of input format (MP3, WAV, FLAC, etc.)

Original files are never modified.

## Language Support

### Supported Languages
- **English** (`en`)
- **Traditional Chinese** (`zh-tw`) 
- **Japanese** (`ja`)

### Language Files
Language resources are stored in `languages/` directory:
- `en.json` - English translations
- `zh-tw.json` - Traditional Chinese translations
- `ja.json` - Japanese translations

## Technical Details

### Architecture
- **GUI Framework**: tkinter with tkinterdnd2 for drag & drop
- **Audio Processing**: FFmpeg with atempo filter
- **Encoding Detection**: Automatic detection of TJA file encoding
- **Threading**: Non-blocking UI with background processing

### FFmpeg Integration
- Static FFmpeg binary embedded in executable
- Automatic fallback to system FFmpeg if available
- Support for complex speed ratios via filter chaining

### Build System
- **PyInstaller**: Creates standalone executable
- **Dependency Management**: Automatic FFmpeg download
- **Version Info**: Embedded version information
- **Size Optimization**: Single-file executable

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- For development: Run `python download_ffmpeg.py`
- For executable: Should not occur (FFmpeg is embedded)

**"Unable to read TJA file"**
- File may be corrupted or use unsupported encoding
- Try opening file in text editor to verify

**"Invalid file type"**
- Only `.tja` files are supported
- Check file extension

**Audio processing fails**
- Verify audio file exists in same directory as TJA
- Check if audio file is not corrupted
- Ensure sufficient disk space

### Performance Notes
- Large audio files may take longer to process
- Complex speed ratios (very high/low) may take more time
- Processing runs in background thread (UI remains responsive)

## Development

### Project Structure
```
taikojiro292/
├── TJASpeedChangerGUI_Enhanced.py     # Enhanced GUI with all new features
├── TJASpeedChangerGUI_Simple.py       # Simplified GUI (no external deps)
├── TJASpeedChangerGUI.py               # Original GUI (for reference)
├── TJASpeedChanger.py                  # Enhanced command-line tool
├── download_ffmpeg.py                  # FFmpeg download utility
├── build_exe.py                        # Build script for executable
├── test_enhanced_features.py           # Test script for new features
├── requirements.txt                    # Python dependencies
├── languages/                          # Language resource files
│   ├── en.json
│   ├── zh-tw.json
│   └── ja.json
└── README.md                          # This file
```

### Adding New Languages
1. Create new JSON file in `languages/` directory
2. Use existing files as template
3. Add language code to GUI language selector
4. Test all UI elements

### Modifying Build Process
- Edit `build_exe.py` for PyInstaller options
- Modify `requirements.txt` for dependencies  
- Update version info in build script

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions welcome! Please:
1. Test changes thoroughly
2. Update documentation
3. Follow existing code style
4. Add language translations if applicable

## Credits

- Original TJA Speed Changer logic
- FFmpeg project for audio processing
- tkinterdnd2 for drag & drop functionality
- PyInstaller for executable packaging
