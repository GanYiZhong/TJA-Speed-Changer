#!/usr/bin/env python3
"""
TJA Speed Changer GUI - Simplified Version
A graphical interface without external dependencies for testing
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.dnd as tkdnd
import os
import sys
import json
import locale
import threading
import subprocess
from pathlib import Path


class LanguageManager:
    """Manages multi-language support"""
    
    def __init__(self):
        self.current_language = 'en'
        self.languages = {}
        self.load_languages()
        
    def load_languages(self):
        """Load language files from languages directory"""
        lang_dir = Path(__file__).parent / 'languages'
        if not lang_dir.exists():
            # Fallback to built-in languages if directory doesn't exist
            self.languages = self._get_builtin_languages()
            return
            
        for lang_file in lang_dir.glob('*.json'):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.languages[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading language file {lang_file}: {e}")
                
        # If no languages loaded, use built-in fallback
        if not self.languages:
            self.languages = self._get_builtin_languages()
    
    def _get_builtin_languages(self):
        """Fallback built-in languages"""
        return {
            'en': {
                'main_window_title': 'TJA Speed Changer',
                'file_selection': 'TJA File Selection',
                'browse_button': 'Browse...',
                'drag_drop_hint': 'Click Browse to select TJA file',
                'speed_setting': 'Speed Setting',
                'speed_range': 'Speed: {:.2f}x (Range: 0.5 - 2.0)',
                'language_setting': 'Language',
                'process_button': 'Process Files',
                'processing': 'Processing...',
                'status_ready': 'Ready',
                'status_processing': 'Processing TJA file...',
                'status_audio_processing': 'Processing audio file...',
                'status_completed': 'Processing completed!',
                'result_title': 'Processing Results',
                'clear_log': 'Clear Log',
                'file_not_selected': 'Please select a TJA file first',
                'invalid_file_type': 'Invalid file type. Please select a .tja file',
                'error_occurred': 'Error occurred: {}',
                'error_file_not_found': 'Error: TJA file not found: {}',
                'error_speed_range': 'Error: Speed multiplier must be between 0.5 and 2.0',
                'start_processing': 'Start processing: {} (Speed: {}x)',
                'tja_processed': 'TJA file processed: {}',
                'processing_complete': 'Processing complete!',
                'new_files': 'New files:',
                'tja_label': '   - TJA: {}',
                'audio_label': '   - Audio: {}',
                'warning_no_wave': 'Warning: WAVE tag not found in TJA file, only processing score file',
                'warning_audio_not_found': 'Warning: Audio file not found: {}',
                'manual_audio_note': 'Only TJA file processed, please handle audio file manually',
                'start_audio_processing': 'Start processing audio file...',
                'audio_processed': 'Audio file processed: {}',
                'audio_processing_failed': 'Audio processing failed',
                'ffmpeg_not_found': 'FFmpeg not found, please ensure FFmpeg is installed and added to system PATH',
                'ffmpeg_error': 'FFmpeg error: {}',
                'audio_processing_error': 'Error occurred while processing audio: {}'
            },
            'zh-tw': {
                'main_window_title': 'TJA速度修改器',
                'file_selection': 'TJA檔案選擇',
                'browse_button': '瀏覽...',
                'drag_drop_hint': '拖放TJA檔案至此處或點擊瀏覽',
                'speed_setting': '速度設定',
                'speed_range': '速度: {:.2f}x (範圍: 0.5 - 2.0)',
                'language_setting': '語言',
                'process_button': '處理檔案',
                'processing': '處理中...',
                'status_ready': '準備就緒',
                'status_processing': '處理TJA檔案中...',
                'status_audio_processing': '處理音源檔案中...',
                'status_completed': '處理完成！',
                'result_title': '處理結果',
                'clear_log': '清除記錄',
                'file_not_selected': '請先選擇TJA檔案',
                'invalid_file_type': '無效的檔案類型，請選擇.tja檔案',
                'error_occurred': '發生錯誤: {}',
                'error_file_not_found': '錯誤: 找不到TJA檔案: {}',
                'error_speed_range': '錯誤: 速度倍率必須介於0.5到2.0之間',
                'start_processing': '開始處理: {} (速度: {}x)',
                'tja_processed': 'TJA檔案已處理: {}',
                'processing_complete': '處理完成！',
                'new_files': '新檔案:',
                'tja_label': '   - TJA: {}',
                'audio_label': '   - 音源: {}',
                'warning_no_wave': '警告: TJA檔案中找不到WAVE標籤，僅處理譜面檔案',
                'warning_audio_not_found': '警告: 找不到音源檔案: {}',
                'manual_audio_note': '僅處理了TJA檔案，請手動處理音源檔案',
                'start_audio_processing': '開始處理音源檔案...',
                'audio_processed': '音源檔案已處理: {}',
                'audio_processing_failed': '音源處理失敗',
                'ffmpeg_not_found': '找不到FFmpeg，請確保已安裝FFmpeg並加入系統PATH',
                'ffmpeg_error': 'FFmpeg錯誤: {}',
                'audio_processing_error': '處理音源時發生錯誤: {}',
                'audio_format_conversion': '轉換音源格式為OGG...'
            },
            'ja': {
                'main_window_title': 'TJA速度変更ツール',
                'file_selection': 'TJAファイル選択',
                'browse_button': '参照...',
                'drag_drop_hint': 'TJAファイルをここにドラッグ＆ドロップまたは参照をクリック',
                'speed_setting': '速度設定',
                'speed_range': '速度: {:.2f}x (範囲: 0.5 - 2.0)',
                'language_setting': '言語',
                'process_button': 'ファイル処理',
                'processing': '処理中...',
                'status_ready': '準備完了',
                'status_processing': 'TJAファイル処理中...',
                'status_audio_processing': '音源ファイル処理中...',
                'status_completed': '処理完了！',
                'result_title': '処理結果',
                'clear_log': 'ログクリア',
                'file_not_selected': 'TJAファイルを選択してください',
                'invalid_file_type': '無効なファイルタイプです。.tjaファイルを選択してください',
                'error_occurred': 'エラーが発生しました: {}',
                'error_file_not_found': 'エラー: TJAファイルが見つかりません: {}',
                'error_speed_range': 'エラー: 速度倍率は0.5から2.0の間でなければなりません',
                'start_processing': '処理開始: {} (速度: {}x)',
                'tja_processed': 'TJAファイル処理完了: {}',
                'processing_complete': '処理完了！',
                'new_files': '新しいファイル:',
                'tja_label': '   - TJA: {}',
                'audio_label': '   - 音源: {}',
                'warning_no_wave': '警告: TJAファイルにWAVEタグが見つかりません、譜面ファイルのみ処理します',
                'warning_audio_not_found': '警告: 音源ファイルが見つかりません: {}',
                'manual_audio_note': 'TJAファイルのみ処理されました、音源ファイルは手動で処理してください',
                'start_audio_processing': '音源ファイル処理開始...',
                'audio_processed': '音源ファイル処理完了: {}',
                'audio_processing_failed': '音源処理失敗',
                'ffmpeg_not_found': 'FFmpegが見つかりません、FFmpegがインストールされ、システムPATHに追加されているか確認してください',
                'ffmpeg_error': 'FFmpegエラー: {}',
                'audio_processing_error': '音源処理中にエラーが発生しました: {}',
                'audio_format_conversion': '音源形式をOGGに変換中...'
            }
        }
    
    def get_system_language(self):
        """Auto-detect system language"""
        try:
            lang_code = locale.getdefaultlocale()[0]
            if lang_code:
                if lang_code.startswith('zh'):
                    if 'TW' in lang_code or 'HK' in lang_code:
                        return 'zh-tw'
                elif lang_code.startswith('ja'):
                    return 'ja'
            return 'en'
        except:
            return 'en'
    
    def get_text(self, key, *args):
        """Get localized text"""
        text = self.languages.get(self.current_language, {}).get(key)
        if text is None:
            text = self.languages.get('en', {}).get(key, key)
        
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    
    def set_language(self, language):
        """Set current language"""
        if language in self.languages:
            self.current_language = language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.languages.keys())


class TJAProcessor:
    """Handles TJA file processing logic"""
    
    def __init__(self, language_manager):
        self.lang_mgr = language_manager
        self.ffmpeg_path = self._find_ffmpeg()
    
    def _find_ffmpeg(self):
        """Find FFmpeg executable"""
        # First try bundled FFmpeg
        if getattr(sys, 'frozen', False):
            # Running as exe
            ffmpeg_path = Path(sys._MEIPASS) / 'ffmpeg.exe'
            if ffmpeg_path.exists():
                return str(ffmpeg_path)
        
        # Try current directory
        local_ffmpeg = Path('ffmpeg.exe')
        if local_ffmpeg.exists():
            return str(local_ffmpeg)
        
        # Try system PATH
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'ffmpeg'
        except:
            pass
        
        return None
    
    def detect_file_encoding(self, file_path):
        """Detect file encoding"""
        encodings = ['utf-8', 'utf-8-sig', 'cp950', 'gbk', 'shift_jis', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        return 'utf-8'
    
    def adjust_tja_speed(self, tja_path, speed, progress_callback=None):
        """Adjust TJA file speed parameters"""
        if progress_callback:
            progress_callback(f"Processing TJA file: {os.path.basename(tja_path)}")
        
        # Auto-detect file encoding
        detected_encoding = self.detect_file_encoding(tja_path)
        
        try:
            with open(tja_path, 'r', encoding=detected_encoding, errors='ignore') as file:
                lines = file.readlines()
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('error_file_encoding'))
        
        new_lines = []
        wave_filename = None
        original_title = None
        
        for line in lines:
            # Modify title with speed marker
            if line.startswith('TITLE:'):
                original_title = line.strip().split(':', 1)[1]
                new_lines.append(f'TITLE:{original_title} ({speed:.2f}x)\n')
            # Parse and modify BPM
            elif line.startswith('BPM:'):
                bpm = float(line.strip().split(':')[1])
                new_bpm = bpm * speed
                new_lines.append(f'BPM:{new_bpm:.3f}\n')
            # Parse and modify OFFSET
            elif line.startswith('OFFSET:'):
                offset = float(line.strip().split(':')[1])
                new_offset = offset / speed
                new_lines.append(f'OFFSET:{new_offset:.6f}\n')
            # Parse and modify DEMOSTART
            elif line.startswith('DEMOSTART:'):
                demostart = float(line.strip().split(':')[1])
                new_demostart = demostart / speed
                new_lines.append(f'DEMOSTART:{new_demostart:.3f}\n')
            # Modify WAVE filename
            elif line.startswith('WAVE:'):
                wave_filename = line.strip().split(':', 1)[1]
                file_root, file_ext = os.path.splitext(wave_filename)
                # Always convert to OGG format
                new_wave_filename = f'{file_root}_{speed:.2f}x.ogg'
                new_lines.append(f'WAVE:{new_wave_filename}\n')
            # Process BPMCHANGE commands in charts
            elif line.startswith('#BPMCHANGE'):
                parts = line.strip().split(' ')
                if len(parts) >= 2:
                    try:
                        new_bmp = float(parts[1]) * speed  # Fixed typo: new_bpm -> new_bmp
                        new_lines.append(f'#BPMCHANGE {new_bmp:.3f}\n')
                    except ValueError:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            # Process #DELAY commands
            elif line.startswith('#DELAY'):
                parts = line.strip().split(' ')
                if len(parts) >= 2:
                    try:
                        delay_seconds = float(parts[1])
                        new_delay = delay_seconds * speed
                        new_lines.append(f'#DELAY {new_delay:.3f}\n')
                    except ValueError:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Save new TJA file
        base, ext = os.path.splitext(tja_path)
        new_tja_path = f'{base}_{speed:.2f}x{ext}'
        
        # Use UTF-8 encoding to ensure compatibility
        with open(new_tja_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return wave_filename, new_wave_filename, new_tja_path
    
    def adjust_audio_speed(self, input_path, output_path, speed, progress_callback=None):
        """Adjust audio speed using FFmpeg and convert to OGG format"""
        if not self.ffmpeg_path:
            raise Exception(self.lang_mgr.get_text('ffmpeg_not_found'))
        
        if progress_callback:
            progress_callback(self.lang_mgr.get_text('audio_format_conversion'))
        
        try:
            # Ensure output is OGG format regardless of input format
            output_path_ogg = os.path.splitext(output_path)[0] + '.ogg'
            
            # Use atempo filter to adjust speed while preserving pitch
            # Also convert to OGG format with good quality
            if speed > 2.0:
                # If speed exceeds 2.0, chain multiple atempo filters
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo=2.0,atempo={speed/2.0}',
                    '-c:a', 'libvorbis',  # OGG Vorbis codec
                    '-q:a', '5',          # Quality level 5 (good balance)
                    '-y', output_path_ogg
                ]
            elif speed < 0.5:
                # If speed is below 0.5, chain multiple atempo filters
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo=0.5,atempo={speed/0.5}',
                    '-c:a', 'libvorbis',  # OGG Vorbis codec
                    '-q:a', '5',          # Quality level 5 (good balance)
                    '-y', output_path_ogg
                ]
            else:
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo={speed}',
                    '-c:a', 'libvorbis',  # OGG Vorbis codec
                    '-q:a', '5',          # Quality level 5 (good balance)
                    '-y', output_path_ogg
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            return output_path_ogg  # Return the actual output path
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('audio_processing_error', str(e)))
    
    def find_audio_file(self, base_dir, wave_filename):
        """Find audio file with various extensions (mp3, wav, ogg)"""
        if not wave_filename:
            return None
            
        # First try exact filename
        exact_path = os.path.join(base_dir, wave_filename)
        if os.path.exists(exact_path):
            return exact_path
        
        # Try different extensions
        file_root = os.path.splitext(wave_filename)[0]
        audio_extensions = ['.ogg', '.mp3', '.wav', '.flac', '.m4a']
        
        for ext in audio_extensions:
            audio_path = os.path.join(base_dir, file_root + ext)
            if os.path.exists(audio_path):
                return audio_path
        
        return None
    
    def process_files(self, tja_path, speed, progress_callback=None, log_callback=None):
        """Main processing function"""
        try:
            if log_callback:
                log_callback(self.lang_mgr.get_text('start_processing', os.path.basename(tja_path), speed))
            
            # Process TJA file
            wave_filename, new_wave_filename, new_tja_path = self.adjust_tja_speed(
                tja_path, speed, progress_callback
            )
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('tja_processed', new_tja_path))
            
            if wave_filename is None:
                if log_callback:
                    log_callback(self.lang_mgr.get_text('warning_no_wave'))
                return new_tja_path, None
            
            # Find audio file with various extensions
            base_dir = os.path.dirname(tja_path)
            input_audio_path = self.find_audio_file(base_dir, wave_filename)
            
            if not input_audio_path:
                if log_callback:
                    log_callback(self.lang_mgr.get_text('warning_audio_not_found', wave_filename))
                    log_callback(self.lang_mgr.get_text('manual_audio_note'))
                return new_tja_path, None
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('start_audio_processing'))
                log_callback(f"Found audio: {os.path.basename(input_audio_path)}")
            
            # Process audio (always outputs to OGG)
            output_audio_path = os.path.join(base_dir, new_wave_filename)
            actual_output_path = self.adjust_audio_speed(input_audio_path, output_audio_path, speed, progress_callback)
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('audio_processed', actual_output_path))
            
            return new_tja_path, actual_output_path
            
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('error_occurred', str(e)))


class TJASpeedChangerGUI:
    """Main GUI application - Simplified Version"""
    
    def __init__(self):
        # Initialize managers
        self.lang_mgr = LanguageManager()
        self.lang_mgr.current_language = self.lang_mgr.get_system_language()
        self.processor = TJAProcessor(self.lang_mgr)
        
        # Initialize GUI
        self.root = tk.Tk()
        self.setup_gui()
        self.update_language()
        
    def setup_gui(self):
        """Set up the main GUI"""
        self.root.title("TJA Speed Changer")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)  # Results area
        
        # File selection section
        self.setup_file_selection(main_frame, 0)
        
        # Speed setting section
        self.setup_speed_setting(main_frame, 1)
        
        # Language setting section
        self.setup_language_setting(main_frame, 2)
        
        # Process button
        self.setup_process_button(main_frame, 3)
        
        # Results section
        self.setup_results_section(main_frame, 4)
        
        # Status bar
        self.setup_status_bar(main_frame, 5)
        
        # Set up drag and drop
        self.setup_drag_drop()
        
    def setup_file_selection(self, parent, row):
        """Set up file selection section"""
        # File selection frame
        file_frame = ttk.LabelFrame(parent, padding="5")
        file_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # File path entry
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state='readonly')
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Browse button
        self.browse_button = ttk.Button(file_frame, command=self.browse_file)
        self.browse_button.grid(row=0, column=1)
        
        # Hint label
        self.drag_drop_label = ttk.Label(file_frame, foreground='gray')
        self.drag_drop_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Store references
        self.file_frame = file_frame
        
    def setup_speed_setting(self, parent, row):
        """Set up speed setting section"""
        # Speed frame
        speed_frame = ttk.LabelFrame(parent, padding="5")
        speed_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        speed_frame.columnconfigure(0, weight=1)
        
        # Speed scale with precision control
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            speed_frame, 
            from_=0.5, 
            to=2.0, 
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            command=self.on_speed_change
        )
        self.speed_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Speed label
        self.speed_label = ttk.Label(speed_frame)
        self.speed_label.grid(row=1, column=0)
        
        # Store references
        self.speed_frame = speed_frame
        
    def setup_language_setting(self, parent, row):
        """Set up language setting section"""
        # Language frame
        lang_frame = ttk.LabelFrame(parent, padding="5")
        lang_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Language combobox
        self.language_var = tk.StringVar(value=self.lang_mgr.current_language)
        language_options = {
            'en': 'English',
            'zh-tw': '繁體中文',
            'ja': '日本語'
        }
        
        available_languages = self.lang_mgr.get_available_languages()
        language_values = [lang for lang in available_languages if lang in language_options]
        
        self.language_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=language_values,
            state='readonly',
            width=15
        )
        self.language_combo.grid(row=0, column=0, padx=5)
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Store references
        self.lang_frame = lang_frame
        
    def setup_process_button(self, parent, row):
        """Set up process button"""
        # Process button
        self.process_button = ttk.Button(
            parent,
            command=self.process_files
        )
        self.process_button.grid(row=row, column=0, pady=(0, 10))
        
    def setup_results_section(self, parent, row):
        """Set up results section"""
        # Results frame
        results_frame = ttk.LabelFrame(parent, padding="5")
        results_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            state='disabled'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # Clear button
        self.clear_button = ttk.Button(results_frame, command=self.clear_results)
        self.clear_button.grid(row=1, column=0)
        
        # Store references
        self.results_frame = results_frame
        
    def setup_status_bar(self, parent, row):
        """Set up status bar"""
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=row, column=0, sticky=(tk.W, tk.E))
    
    def setup_drag_drop(self):
        """Set up drag and drop functionality - simplified version"""
        # Bind click events to file entry and drag drop label for better UX
        self.file_entry.bind('<Button-1>', self.on_entry_click)
        self.drag_drop_label.bind('<Button-1>', self.browse_file)
        
        # Try to set up Windows drag and drop if available
        try:
            if sys.platform.startswith('win'):
                self.setup_windows_drag_drop()
        except:
            pass  # Fallback to browse button only
        
        # Style the drag drop area to look more interactive
        self.setup_interactive_drop_zone()
    
    def setup_windows_drag_drop(self):
        """Set up Windows-specific drag and drop"""
        try:
            # This is a simplified drag-drop implementation for Windows
            # We'll monitor for file drops on the main window
            self.root.bind('<Enter>', self.on_drag_enter)
            self.root.bind('<Leave>', self.on_drag_leave)
            
            # Alternative: Use Windows OLE drag-drop via windnd if available
            try:
                import windnd
                windnd.hook_dropfiles(self.root, func=self.on_drop_files)
            except ImportError:
                # windnd not available, use alternative method
                self.setup_alternative_drag_drop()
        except:
            pass
    
    def setup_interactive_drop_zone(self):
        """Set up interactive drop zone styling"""
        # Create a label that acts as a drop zone
        self.drag_drop_label.config(
            relief='groove',
            borderwidth=2,
            background='#f0f0f0',
            cursor='hand2'
        )
        
        # Bind mouse events for visual feedback
        self.drag_drop_label.bind('<Enter>', lambda e: self.drag_drop_label.config(background='#e0e0e0'))
        self.drag_drop_label.bind('<Leave>', lambda e: self.drag_drop_label.config(background='#f0f0f0'))
        
    def setup_alternative_drag_drop(self):
        """Alternative drag and drop setup (not used in simplified version)"""
        pass
        
    def on_entry_click(self, event):
        """Handle entry click - open file dialog"""
        self.browse_file()
    
    def on_drag_enter(self, event):
        """Handle drag enter event"""
        self.root.config(cursor='hand2')
    
    def on_drag_leave(self, event):
        """Handle drag leave event"""
        self.root.config(cursor='')
    
    def on_drop_files(self, files):
        """Handle dropped files (windnd callback)"""
        if files:
            file_path = files[0]  # Take the first file
            if file_path.lower().endswith('.tja'):
                self.file_var.set(file_path)
                self.log_message(f"Dropped file: {os.path.basename(file_path)}")
            else:
                self.log_message(self.lang_mgr.get_text('invalid_file_type'))
            
    def browse_file(self):
        """Browse for TJA file"""
        file_path = filedialog.askopenfilename(
            title=self.lang_mgr.get_text('file_selection'),
            filetypes=[('TJA files', '*.tja'), ('All files', '*.*')]
        )
        if file_path:
            self.file_var.set(file_path)
            
    def on_speed_change(self, value=None):
        """Handle speed scale change with precision rounding"""
        raw_speed = self.speed_var.get()
        # Round to 2 decimal places for clean display
        rounded_speed = round(raw_speed, 2)
        # Update the variable to the rounded value
        self.speed_var.set(rounded_speed)
        # Update the label
        self.update_speed_label()
    
    def update_speed_label(self, value=None):
        """Update speed label"""
        speed = self.speed_var.get()
        text = self.lang_mgr.get_text('speed_range', speed)
        self.speed_label.config(text=text)
        
    def on_language_change(self, event=None):
        """Handle language change with log refresh"""
        new_language = self.language_var.get()
        old_language = self.lang_mgr.current_language
        
        # Don't process if same language
        if new_language == old_language:
            return
            
        self.lang_mgr.set_language(new_language)
        
        # Clear and refresh log display
        self.clear_results()
        
        # Show language change message in the new language
        language_names = {'en': 'English', 'zh-tw': '繁體中文', 'ja': '日本語'}
        language_name = language_names.get(new_language, new_language)
        self.log_message(f"Language changed to: {language_name}")
        
        self.update_language()
        
    def update_language(self):
        """Update all text elements with current language"""
        # Window title
        self.root.title(self.lang_mgr.get_text('main_window_title'))
        
        # Labels and frames
        self.file_frame.config(text=self.lang_mgr.get_text('file_selection'))
        self.browse_button.config(text=self.lang_mgr.get_text('browse_button'))
        self.drag_drop_label.config(text=self.lang_mgr.get_text('drag_drop_hint'))
        
        self.speed_frame.config(text=self.lang_mgr.get_text('speed_setting'))
        self.update_speed_label()
        
        self.lang_frame.config(text=self.lang_mgr.get_text('language_setting'))
        
        self.process_button.config(text=self.lang_mgr.get_text('process_button'))
        
        self.results_frame.config(text=self.lang_mgr.get_text('result_title'))
        self.clear_button.config(text=self.lang_mgr.get_text('clear_log'))
        
        # Status
        self.status_var.set(self.lang_mgr.get_text('status_ready'))
        
    def log_message(self, message):
        """Add message to results area"""
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, message + '\n')
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')
        self.root.update()
        
    def clear_results(self):
        """Clear results area"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        
    def update_status(self, status):
        """Update status bar"""
        self.status_var.set(status)
        self.root.update()
        
    def process_files(self):
        """Process TJA files"""
        # Validate input
        tja_path = self.file_var.get()
        if not tja_path:
            messagebox.showerror("Error", self.lang_mgr.get_text('file_not_selected'))
            return
            
        if not tja_path.lower().endswith('.tja'):
            messagebox.showerror("Error", self.lang_mgr.get_text('invalid_file_type'))
            return
            
        if not os.path.exists(tja_path):
            messagebox.showerror("Error", self.lang_mgr.get_text('error_file_not_found', tja_path))
            return
            
        speed = self.speed_var.get()
        if not (0.5 <= speed <= 2.0):
            messagebox.showerror("Error", self.lang_mgr.get_text('error_speed_range'))
            return
        
        # Disable UI during processing
        self.process_button.config(state='disabled')
        self.update_status(self.lang_mgr.get_text('processing'))
        
        # Run processing in separate thread
        thread = threading.Thread(
            target=self._process_files_thread,
            args=(tja_path, speed)
        )
        thread.daemon = True
        thread.start()
        
    def _process_files_thread(self, tja_path, speed):
        """Process files in separate thread"""
        try:
            def progress_callback(message):
                self.root.after(0, self.update_status, message)
                
            def log_callback(message):
                self.root.after(0, self.log_message, message)
            
            # Process files
            new_tja_path, new_audio_path = self.processor.process_files(
                tja_path, speed, progress_callback, log_callback
            )
            
            # Show results
            def show_completion():
                self.log_message(self.lang_mgr.get_text('processing_complete'))
                self.log_message(self.lang_mgr.get_text('new_files'))
                self.log_message(self.lang_mgr.get_text('tja_label', new_tja_path))
                if new_audio_path:
                    self.log_message(self.lang_mgr.get_text('audio_label', new_audio_path))
                
                self.update_status(self.lang_mgr.get_text('status_completed'))
                self.process_button.config(state='normal')
                
                messagebox.showinfo(
                    "Completed",
                    self.lang_mgr.get_text('processing_complete')
                )
            
            self.root.after(0, show_completion)
            
        except Exception as e:
            def show_error():
                error_msg = str(e)
                self.log_message(error_msg)
                self.update_status(self.lang_mgr.get_text('status_ready'))
                self.process_button.config(state='normal')
                messagebox.showerror("Error", error_msg)
            
            self.root.after(0, show_error)
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = TJASpeedChangerGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()