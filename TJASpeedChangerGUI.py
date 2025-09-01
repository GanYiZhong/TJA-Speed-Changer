#!/usr/bin/env python3
"""
TJA Speed Changer GUI
A graphical interface for modifying TJA files and audio source speed for Taiko no Tatsufin
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinterdnd2 as tkdnd
import os
import sys
import json
import locale
import threading
import subprocess
from pathlib import Path
import tempfile
import shutil


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
                'drag_drop_hint': 'Drag and drop TJA file here or click Browse',
                'speed_setting': 'Speed Setting',
                'speed_range': 'Speed: {:.2f}x (Range: 0.5 - 2.0)',
                'language_setting': 'Language',
                'process_button': 'Process Files',
                'status_ready': 'Ready',
                'result_title': 'Processing Results',
                'clear_log': 'Clear Log',
                'file_not_selected': 'Please select a TJA file first',
                'invalid_file_type': 'Invalid file type. Please select a .tja file',
                'error_occurred': 'Error occurred: {}'
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
                new_wave_filename = f'{file_root}_{speed:.2f}x{file_ext}'
                new_lines.append(f'WAVE:{new_wave_filename}\n')
            # Process BPMCHANGE commands in charts
            elif line.startswith('#BPMCHANGE'):
                parts = line.strip().split(' ')
                if len(parts) >= 2:
                    try:
                        new_bpm = float(parts[1]) * speed
                        new_lines.append(f'#BPMCHANGE {new_bpm:.3f}\n')
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
        """Adjust audio speed using FFmpeg"""
        if not self.ffmpeg_path:
            raise Exception(self.lang_mgr.get_text('ffmpeg_not_found'))
        
        if progress_callback:
            progress_callback(f"Processing audio file: {os.path.basename(input_path)}")
        
        try:
            # Use atempo filter to adjust speed while preserving pitch
            if speed > 2.0:
                # If speed exceeds 2.0, chain multiple atempo filters
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo=2.0,atempo={speed/2.0}',
                    '-y', output_path
                ]
            elif speed < 0.5:
                # If speed is below 0.5, chain multiple atempo filters
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo=0.5,atempo={speed/0.5}',
                    '-y', output_path
                ]
            else:
                cmd = [
                    self.ffmpeg_path, '-i', input_path,
                    '-filter:a', f'atempo={speed}',
                    '-y', output_path
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            return True
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('audio_processing_error', str(e)))
    
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
            
            # Process audio file
            base_dir = os.path.dirname(tja_path)
            input_audio_path = os.path.join(base_dir, wave_filename)
            output_audio_path = os.path.join(base_dir, new_wave_filename)
            
            if not os.path.exists(input_audio_path):
                if log_callback:
                    log_callback(self.lang_mgr.get_text('warning_audio_not_found', input_audio_path))
                    log_callback(self.lang_mgr.get_text('manual_audio_note'))
                return new_tja_path, None
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('start_audio_processing'))
            
            self.adjust_audio_speed(input_audio_path, output_audio_path, speed, progress_callback)
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('audio_processed', output_audio_path))
            
            return new_tja_path, output_audio_path
            
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('error_occurred', str(e)))


class TJASpeedChangerGUI:
    """Main GUI application"""
    
    def __init__(self):
        # Initialize managers
        self.lang_mgr = LanguageManager()
        self.lang_mgr.current_language = self.lang_mgr.get_system_language()
        self.processor = TJAProcessor(self.lang_mgr)
        
        # Initialize GUI
        self.root = tkdnd.Tk()
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
        
        # Configure drag and drop
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
        
        # Drag and drop label
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
        
        # Speed scale
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            speed_frame, 
            from_=0.5, 
            to=2.0, 
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            command=self.update_speed_label
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
        language_texts = [language_options[lang] for lang in language_values]
        
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
            command=self.process_files,
            style='Accent.TButton'
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
        """Set up drag and drop functionality"""
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<DropEnter>>', self.on_drop_enter)
        self.root.dnd_bind('<<DropLeave>>', self.on_drop_leave)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        
    def on_drop_enter(self, event):
        """Handle drag enter event"""
        self.root.configure(cursor="hand2")
        
    def on_drop_leave(self, event):
        """Handle drag leave event"""
        self.root.configure(cursor="")
        
    def on_drop(self, event):
        """Handle file drop event"""
        self.root.configure(cursor="")
        files = event.data.split()
        if files:
            file_path = files[0].strip('{}')  # Remove braces if present
            if file_path.lower().endswith('.tja'):
                self.file_var.set(file_path)
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
            
    def update_speed_label(self, value=None):
        """Update speed label"""
        speed = self.speed_var.get()
        text = self.lang_mgr.get_text('speed_range', speed)
        self.speed_label.config(text=text)
        
    def on_language_change(self, event=None):
        """Handle language change"""
        new_language = self.language_var.get()
        self.lang_mgr.set_language(new_language)
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
        self.update_status(self.lang_mgr.get_text('processing', 'Processing...'))
        
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