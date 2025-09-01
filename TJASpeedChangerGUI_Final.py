#!/usr/bin/env python3
"""
TJA Speed Changer GUI - Final Version
完整功能版本：精確滑桿、語言切換清除記錄、編碼修復、OGG轉換
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import sys
import json
import locale
import threading
import subprocess
import webbrowser
from pathlib import Path
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def resource_path(relative_path):
    """獲取資源檔案的絕對路徑，支援開發環境和打包後環境"""
    try:
        # PyInstaller打包後的路徑
        base_path = sys._MEIPASS
    except AttributeError:
        # 開發環境路徑
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class LanguageManager:
    """多語言管理器"""
    
    def __init__(self):
        self.current_language = 'en'
        self.languages = self._get_builtin_languages()
        self.load_languages()
        
    def load_languages(self):
        """從語言目錄載入語言檔案"""
        lang_dir = Path(__file__).parent / 'languages'
        if not lang_dir.exists():
            return  # 使用內建語言
            
        for lang_file in lang_dir.glob('*.json'):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    loaded_lang = json.load(f)
                    # 與內建語言合併（內建作為後備）
                    if lang_code in self.languages:
                        self.languages[lang_code].update(loaded_lang)
                    else:
                        self.languages[lang_code] = loaded_lang
            except Exception as e:
                print(f"載入語言檔案錯誤 {lang_file}: {e}")
    
    def _get_builtin_languages(self):
        """內建語言"""
        return {
            'en': {
                'main_window_title': 'TJA Speed Changer',
                'file_selection': 'TJA File Selection',
                'browse_button': 'Browse...',
                'click_to_browse': 'Click to browse for TJA file or drag & drop here',
                'speed_setting': 'Speed Setting',
                'speed_range': 'Speed: {:.2f}x (Range: 0.01 - 10.0)',
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
                'error_speed_range': 'Error: Speed multiplier must be between 0.01 and 10.0',
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
                'audio_processing_error': 'Error occurred while processing audio: {}',
                'audio_format_conversion': 'Converting audio format to OGG...',
                'language_changed_message': 'Language changed to: {}',
                'encoding_detected': 'Detected file encoding: {}',
                'encoding_preserved': 'Saved with original encoding: {}',
                'encoding_fallback': 'Using UTF-8 encoding as fallback',
                'file_dropped': 'File dropped: {}',
                'drag_drop_invalid': 'Invalid file type. Please drag a .tja file.'
            },
            'zh-tw': {
                'main_window_title': 'TJA速度修改器',
                'file_selection': 'TJA檔案選擇',
                'browse_button': '瀏覽...',
                'click_to_browse': '點擊瀏覽TJA檔案或拖拉到此處',
                'speed_setting': '速度設定',
                'speed_range': '速度: {:.2f}x (範圍: 0.01 - 10.0)',
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
                'error_speed_range': '錯誤: 速度倍率必須介於0.01到10.0之間',
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
                'audio_format_conversion': '轉換音源格式為OGG...',
                'language_changed_message': '語言已切換至: {}',
                'encoding_detected': '檢測到檔案編碼: {}',
                'encoding_preserved': '使用原始編碼儲存: {}',
                'encoding_fallback': '使用UTF-8編碼作為後備',
                'file_dropped': '拖拉檔案: {}',
                'drag_drop_invalid': '無效的檔案類型，請拖拉.tja檔案'
            },
            'ja': {
                'main_window_title': 'TJA速度変更ツール',
                'file_selection': 'TJAファイル選択',
                'browse_button': '参照...',
                'click_to_browse': 'クリックしてTJAファイルを参照またはドラッグ＆ドロップ',
                'speed_setting': '速度設定',
                'speed_range': '速度: {:.2f}x (範囲: 0.01 - 10.0)',
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
                'error_speed_range': 'エラー: 速度倍率は0.01から10.0の間でなければなりません',
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
                'audio_format_conversion': '音源形式をOGGに変換中...',
                'language_changed_message': '言語が変更されました: {}',
                'encoding_detected': 'ファイルエンコーディングを検出: {}',
                'encoding_preserved': '元のエンコーディングで保存: {}',
                'encoding_fallback': 'UTF-8エンコーディングをフォールバックとして使用',
                'file_dropped': 'ファイルドロップ: {}',
                'drag_drop_invalid': '無効なファイル形式です。.tjaファイルをドラッグしてください'
            }
        }
    
    def get_system_language(self):
        """自動檢測系統語言"""
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
        """獲取本地化文本"""
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
        """設定當前語言"""
        if language in self.languages:
            self.current_language = language
    
    def get_available_languages(self):
        """獲取可用語言列表"""
        return list(self.languages.keys())


class TJAProcessor:
    """TJA檔案處理器 - 支援OGG轉換和改進的編碼處理"""
    
    def __init__(self, language_manager):
        self.lang_mgr = language_manager
        self.ffmpeg_path = self._find_ffmpeg()
    
    def _find_ffmpeg(self):
        """尋找FFmpeg執行檔"""
        # 首先嘗試捆綁的FFmpeg
        if getattr(sys, 'frozen', False):
            # 以exe執行
            ffmpeg_path = Path(sys._MEIPASS) / 'ffmpeg.exe'
            if ffmpeg_path.exists():
                return str(ffmpeg_path)
        
        # 嘗試當前目錄
        local_ffmpeg = Path('ffmpeg.exe')
        if local_ffmpeg.exists():
            return str(local_ffmpeg)
        
        # 嘗試系統PATH
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'ffmpeg'
        except:
            pass
        
        return None
    
    def detect_file_encoding(self, file_path):
        """檢測檔案編碼 - 改進版本，更精確的檢測，優先檢測ANSI編碼"""
        # 按優先順序嘗試常見編碼，ANSI(CP950)和CP932優先
        encodings_to_try = [
            'utf-8-sig',    # UTF-8 with BOM
            'utf-8',        # UTF-8 without BOM
            'cp950',        # Traditional Chinese ANSI (Big5 Windows) - 最優先
            'big5',         # Traditional Chinese (Big5 標準)
            'cp932',        # Japanese ANSI (Shift-JIS Windows)
            'shift_jis',    # Japanese Shift-JIS 標準
            'gbk',          # Simplified Chinese
            'euc-jp',       # Japanese (alternative)
            'iso-2022-jp',  # Japanese (JIS)
            'iso-8859-1',   # Western European
            'latin1'        # Latin-1 (fallback)
        ]
        
        # 如果有chardet可用，首先嘗試使用自動檢測
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(8192)  # 只讀取前8KB進行檢測，節省時間
                detected = chardet.detect(raw_data)
                if detected and detected['encoding']:
                    confidence = detected['confidence']
                    detected_encoding = detected['encoding'].lower()
                    
                    # 高信心度的檢測結果直接使用
                    if confidence > 0.8:
                        # 標準化編碼名稱，優先使用Big5和Shift-JIS
                        if 'utf-8' in detected_encoding:
                            return 'utf-8-sig' if 'sig' in detected_encoding or confidence > 0.95 else 'utf-8'
                        elif 'big5' in detected_encoding or 'cp950' in detected_encoding:
                            return 'cp950'  # 統一使用cp950 (ANSI Big5)
                        elif 'gb' in detected_encoding or ('chinese' in detected_encoding and 'big5' not in detected_encoding):
                            return 'gbk'
                        elif 'shift' in detected_encoding or 'cp932' in detected_encoding or 'japanese' in detected_encoding:
                            return 'cp932'  # 統一使用cp932 (ANSI Shift-JIS)
                        else:
                            return detected['encoding']
                    
                    # 中等信心度的檢測結果也嘗試驗證
                    elif confidence > 0.6:
                        try:
                            with open(file_path, 'r', encoding=detected['encoding'], errors='strict') as f:
                                test_content = f.read(1024)  # 驗證前1KB
                                if len(test_content) > 0:
                                    return detected['encoding']
                        except (UnicodeDecodeError, UnicodeError):
                            pass  # 檢測結果不準確，繼續手動檢測
        except ImportError:
            pass  # chardet不可用，繼續手動檢測
        
        # 手動編碼檢測 - 嘗試讀取整個文件來驗證
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                    content = f.read()
                    if len(content) > 0:
                        # 額外驗證：檢查是否包含常見的TJA關鍵字
                        content_lower = content.lower()
                        tja_keywords = ['title:', 'bpm:', 'wave:', '#start', '#end']
                        if any(keyword in content_lower for keyword in tja_keywords):
                            # 對於CP950和CP932，進行額外驗證
                            if encoding in ['cp950', 'cp932']:
                                # 檢查是否包含CJK字符，確認這確實是正確的編碼
                                has_cjk = any(ord(char) > 127 for char in content)
                                if has_cjk:
                                    # 嘗試重新編碼驗證一致性
                                    try:
                                        content.encode(encoding)
                                        return encoding
                                    except UnicodeEncodeError:
                                        continue
                                else:
                                    return encoding
                            else:
                                return encoding
            except (UnicodeDecodeError, UnicodeError, Exception):
                continue
        
        # 最後手段：使用utf-8
        return 'utf-8'
    
    def adjust_tja_speed(self, tja_path, speed, progress_callback=None):
        """調整TJA檔案速度參數，強制OGG格式，保持原始編碼"""
        if progress_callback:
            progress_callback(f"Processing TJA file: {os.path.basename(tja_path)}")
        
        # 自動檢測檔案編碼並保存供後續使用
        detected_encoding = self.detect_file_encoding(tja_path)
        original_encoding = detected_encoding  # 保存原始編碼
        
        if progress_callback:
            progress_callback(self.lang_mgr.get_text('encoding_detected', detected_encoding))
        
        try:
            with open(tja_path, 'r', encoding=detected_encoding, errors='replace') as file:
                lines = file.readlines()
        except Exception as e:
            # 如果檢測到的編碼失敗，嘗試UTF-8與錯誤處理
            try:
                with open(tja_path, 'r', encoding='utf-8', errors='replace') as file:
                    lines = file.readlines()
                original_encoding = 'utf-8'  # 更新為實際使用的編碼
                if progress_callback:
                    progress_callback(self.lang_mgr.get_text('encoding_fallback'))
            except Exception:
                raise Exception("無法讀取TJA檔案，請檢查檔案編碼。")
        
        new_lines = []
        wave_filename = None
        original_title = None
        
        for line in lines:
            # 修改標題加上速度標記
            if line.startswith('TITLE:'):
                original_title = line.strip().split(':', 1)[1]
                new_lines.append(f'TITLE:{original_title} ({speed:.2f}x)\n')
            # 解析並修改BPM
            elif line.startswith('BPM:'):
                bpm = float(line.strip().split(':')[1])
                new_bpm = bpm * speed
                new_lines.append(f'BPM:{new_bpm:.3f}\n')
            # 解析並修改OFFSET
            elif line.startswith('OFFSET:'):
                offset = float(line.strip().split(':')[1])
                new_offset = offset / speed
                new_lines.append(f'OFFSET:{new_offset:.6f}\n')
            # 解析並修改DEMOSTART
            elif line.startswith('DEMOSTART:'):
                demostart = float(line.strip().split(':')[1])
                new_demostart = demostart / speed
                new_lines.append(f'DEMOSTART:{new_demostart:.3f}\n')
            # 修改WAVE檔案名稱 - 總是轉換為OGG
            elif line.startswith('WAVE:'):
                wave_filename = line.strip().split(':', 1)[1]
                file_root, file_ext = os.path.splitext(wave_filename)
                # 總是轉換為OGG格式
                new_wave_filename = f'{file_root}_{speed:.2f}x.ogg'
                new_lines.append(f'WAVE:{new_wave_filename}\n')
            # 處理譜面中的BPMCHANGE指令
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
            # 處理#DELAY指令
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
        
        # 儲存新的TJA檔案 - 使用原始編碼
        base, ext = os.path.splitext(tja_path)
        new_tja_path = f'{base}_{speed:.2f}x{ext}'
        
        # 使用原始檔案的編碼儲存，確保編碼一致性
        # 第一優先：嚴格使用原始編碼，不允許任何字符丟失
        save_success = False
        try:
            with open(new_tja_path, 'w', encoding=original_encoding, errors='strict') as f:
                f.writelines(new_lines)
            save_success = True
            if progress_callback:
                progress_callback(self.lang_mgr.get_text('encoding_preserved', original_encoding))
        except (UnicodeEncodeError, UnicodeError):
            # 嚴格模式失敗，嘗試安全模式但保持原編碼
            pass
        
        # 如果嚴格模式失敗，嘗試安全模式但仍使用原始編碼
        if not save_success:
            try:
                # 對於CJK編碼，首先嘗試xmlcharrefreplace來保留無法編碼的字符
                error_strategy = 'xmlcharrefreplace' if original_encoding in ['shift_jis', 'cp932', 'big5', 'cp950', 'gbk'] else 'replace'
                with open(new_tja_path, 'w', encoding=original_encoding, errors=error_strategy) as f:
                    f.writelines(new_lines)
                save_success = True
                if progress_callback:
                    progress_callback(self.lang_mgr.get_text('encoding_preserved', original_encoding))
            except Exception:
                pass
        
        # 如果還是失敗，最後嘗試ignore策略但保持原編碼
        if not save_success:
            try:
                with open(new_tja_path, 'w', encoding=original_encoding, errors='ignore') as f:
                    f.writelines(new_lines)
                save_success = True
                if progress_callback:
                    progress_callback(self.lang_mgr.get_text('encoding_preserved', original_encoding))
            except Exception:
                pass
        
        # 最後手段：UTF-8（應該很少用到）
        if not save_success:
            try:
                with open(new_tja_path, 'w', encoding='utf-8', errors='replace') as f:
                    f.writelines(new_lines)
                if progress_callback:
                    progress_callback(self.lang_mgr.get_text('encoding_fallback'))
            except Exception:
                raise Exception("無法儲存TJA檔案，請檢查檔案權限。")
        
        # 返回新的wave檔案名（現在總是OGG）
        if wave_filename:
            file_root, _ = os.path.splitext(wave_filename)
            new_wave_filename = f'{file_root}_{speed:.2f}x.ogg'
        else:
            new_wave_filename = None
        
        return wave_filename, new_wave_filename, new_tja_path
    
    def find_audio_file(self, base_dir, wave_filename):
        """尋找各種副檔名的音源檔案"""
        if not wave_filename:
            return None
            
        # 首先嘗試精確的檔案名
        exact_path = os.path.join(base_dir, wave_filename)
        if os.path.exists(exact_path):
            return exact_path
        
        # 嘗試不同的副檔名
        file_root = os.path.splitext(wave_filename)[0]
        audio_extensions = ['.ogg', '.mp3', '.wav', '.flac', '.m4a', '.aac']
        
        for ext in audio_extensions:
            audio_path = os.path.join(base_dir, file_root + ext)
            if os.path.exists(audio_path):
                return audio_path
        
        return None
    
    def adjust_audio_speed(self, input_path, output_path, speed, progress_callback=None):
        """使用FFmpeg調整音源速度並轉換為OGG格式"""
        if not self.ffmpeg_path:
            raise Exception(self.lang_mgr.get_text('ffmpeg_not_found'))
        
        if progress_callback:
            progress_callback(self.lang_mgr.get_text('audio_format_conversion'))
        
        try:
            # 確保輸出為OGG格式，無論輸入格式為何
            output_path_ogg = os.path.splitext(output_path)[0] + '.ogg'
            
            # 使用atempo濾鏡調整速度同時保持音調
            # 同時轉換為OGG格式與良好品質
            # atempo範圍限制在0.5-2.0，超出範圍需要串聯多個濾鏡
            def build_atempo_chain(target_speed):
                """構建atempo濾鏡鏈"""
                if 0.5 <= target_speed <= 2.0:
                    return f'atempo={target_speed}'
                
                chain = []
                current_speed = target_speed
                
                # 處理大於2.0的速度
                while current_speed > 2.0:
                    chain.append('atempo=2.0')
                    current_speed /= 2.0
                
                # 處理小於0.5的速度
                while current_speed < 0.5:
                    chain.append('atempo=0.5')
                    current_speed /= 0.5
                
                # 加入最後的調整
                if current_speed != 1.0:
                    chain.append(f'atempo={current_speed}')
                
                return ','.join(chain)
            
            atempo_filter = build_atempo_chain(speed)
            
            cmd = [
                self.ffmpeg_path, '-i', input_path,
                '-filter:a', atempo_filter,
                '-c:a', 'libvorbis',  # OGG Vorbis編碼器
                '-q:a', '5',          # 品質等級5（良好平衡）
                '-y', output_path_ogg
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            return output_path_ogg  # 返回實際的輸出路徑
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('audio_processing_error', str(e)))
    
    def process_files(self, tja_path, speed, progress_callback=None, log_callback=None):
        """主要處理功能，支援OGG轉換"""
        try:
            if log_callback:
                log_callback(self.lang_mgr.get_text('start_processing', os.path.basename(tja_path), speed))
            
            # 處理TJA檔案
            wave_filename, new_wave_filename, new_tja_path = self.adjust_tja_speed(
                tja_path, speed, progress_callback
            )
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('tja_processed', new_tja_path))
            
            if wave_filename is None:
                if log_callback:
                    log_callback(self.lang_mgr.get_text('warning_no_wave'))
                return new_tja_path, None
            
            # 尋找各種副檔名的音源檔案
            base_dir = os.path.dirname(tja_path)
            input_audio_path = self.find_audio_file(base_dir, wave_filename)
            
            if not input_audio_path:
                if log_callback:
                    log_callback(self.lang_mgr.get_text('warning_audio_not_found', wave_filename))
                    log_callback(self.lang_mgr.get_text('manual_audio_note'))
                return new_tja_path, None
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('start_audio_processing'))
                log_callback(f"找到音源: {os.path.basename(input_audio_path)}")
            
            # 處理音源（總是輸出為OGG）
            output_audio_path = os.path.join(base_dir, new_wave_filename)
            actual_output_path = self.adjust_audio_speed(input_audio_path, output_audio_path, speed, progress_callback)
            
            if log_callback:
                log_callback(self.lang_mgr.get_text('audio_processed', actual_output_path))
            
            return new_tja_path, actual_output_path
            
        except Exception as e:
            raise Exception(self.lang_mgr.get_text('error_occurred', str(e)))


class TJASpeedChangerGUI:
    """最終版GUI應用程式 - 無拖放依賴，精確滑桿，語言切換清除記錄"""
    
    def __init__(self):
        # 初始化管理器
        self.lang_mgr = LanguageManager()
        self.lang_mgr.current_language = self.lang_mgr.get_system_language()
        self.processor = TJAProcessor(self.lang_mgr)
        
        # 初始化GUI with drag and drop support
        self.root = TkinterDnD.Tk()
        self.setup_gui()
        self.update_language()
        
    def setup_gui(self):
        """設定主要GUI"""
        self.root.title("TJA Speed Changer")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)
        
        # 配置樣式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置grid權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)  # 結果區域
        
        # 檔案選擇區段
        self.setup_file_selection(main_frame, 0)
        
        # 速度設定區段
        self.setup_speed_setting(main_frame, 1)
        
        # 語言設定區段
        self.setup_language_setting(main_frame, 2)
        
        # 處理按鈕
        self.setup_process_button(main_frame, 3)
        
        # 結果區段
        self.setup_results_section(main_frame, 4)
        
        # 狀態列
        self.setup_status_bar(main_frame, 5)
        
        # Logo區域
        self.setup_logo_section(main_frame, 6)
        
    def setup_file_selection(self, parent, row):
        """設定檔案選擇區段"""
        # 檔案選擇框架
        file_frame = ttk.LabelFrame(parent, padding="5")
        file_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # 檔案路徑輸入框 with drag and drop support
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state='readonly')
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # 設置拖拉功能
        self.file_entry.drop_target_register(DND_FILES)
        self.file_entry.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # 瀏覽按鈕
        self.browse_button = ttk.Button(file_frame, command=self.browse_file)
        self.browse_button.grid(row=0, column=1)
        
        # 點擊提示標籤
        self.click_label = ttk.Label(file_frame, foreground='gray')
        self.click_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # 儲存參照
        self.file_frame = file_frame
        
    def setup_speed_setting(self, parent, row):
        """設定速度調整區段"""
        # 速度框架
        speed_frame = ttk.LabelFrame(parent, padding="5")
        speed_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        speed_frame.columnconfigure(0, weight=1)
        
        # 速度變數
        self.speed_var = tk.DoubleVar(value=1.0)
        
        # 滑桿和數字輸入框架
        control_frame = ttk.Frame(speed_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        control_frame.columnconfigure(0, weight=1)
        
        # 精確控制的速度滑桿 (擴大範圍)
        self.speed_scale = ttk.Scale(
            control_frame, 
            from_=0.01, 
            to=10.0, 
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            command=self.on_speed_change
        )
        self.speed_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # 數字輸入框 (with decimal point validation)
        self.speed_entry_var = tk.StringVar(value="1.00")
        
        # 註冊驗證函數
        vcmd = (self.root.register(self.validate_speed_input), '%P', '%S')
        
        self.speed_entry = ttk.Entry(
            control_frame, 
            textvariable=self.speed_entry_var, 
            width=8,
            justify='center',
            validate='key',
            validatecommand=vcmd
        )
        self.speed_entry.grid(row=0, column=1, padx=(5, 0))
        self.speed_entry.bind('<Return>', self.on_speed_entry_change)
        self.speed_entry.bind('<FocusOut>', self.on_speed_entry_change)
        
        # 速度標籤
        self.speed_label = ttk.Label(speed_frame)
        self.speed_label.grid(row=1, column=0, pady=(5, 0))
        
        # 儲存參照
        self.speed_frame = speed_frame
        
    def setup_language_setting(self, parent, row):
        """設定語言選擇區段"""
        # 語言框架
        lang_frame = ttk.LabelFrame(parent, padding="5")
        lang_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 語言下拉選單
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
        
        # 儲存參照
        self.lang_frame = lang_frame
        
    def setup_process_button(self, parent, row):
        """設定處理按鈕"""
        # 處理按鈕
        self.process_button = ttk.Button(
            parent,
            command=self.process_files
        )
        self.process_button.grid(row=row, column=0, pady=(0, 10))
        
    def setup_results_section(self, parent, row):
        """設定結果區段"""
        # 結果框架
        results_frame = ttk.LabelFrame(parent, padding="5")
        results_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # 結果文字區域
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            state='disabled'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        
        # 清除按鈕
        self.clear_button = ttk.Button(results_frame, command=self.clear_results)
        self.clear_button.grid(row=1, column=0)
        
        # 儲存參照
        self.results_frame = results_frame
        
    def setup_status_bar(self, parent, row):
        """設定狀態列"""
        # 狀態列
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=row, column=0, sticky=(tk.W, tk.E))
    
    def setup_logo_section(self, parent, row):
        """設定Logo區域"""
        # Logo框架
        logo_frame = ttk.Frame(parent, padding="5")
        logo_frame.grid(row=row, column=0, pady=(10, 0))
        
        # 嘗試載入Logo圖片
        logo_path = resource_path("LOGO_BLACK_TRANS.png")
        if os.path.exists(logo_path) and HAS_PIL:
            try:
                # 載入並調整Logo大小
                image = Image.open(logo_path)
                # 調整大小保持比例，最大寬度150px
                width, height = image.size
                max_width = 150
                if width > max_width:
                    ratio = max_width / width
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(image)
                
                # 可點擊的Logo標籤
                logo_label = ttk.Label(logo_frame, image=photo, cursor="hand2")
                logo_label.image = photo  # 保持參照防止垃圾回收
                logo_label.grid(row=0, column=0, padx=5)
                logo_label.bind("<Button-1>", self.on_logo_click)
                
            except Exception as e:
                print(f"無法載入Logo: {e}")
                self.setup_text_logo(logo_frame)
        else:
            # 後備文字Logo
            self.setup_text_logo(logo_frame)
        
        # 作者資訊
        author_label = ttk.Label(
            logo_frame, 
            text="by ZhongTaiko Studios", 
            font=('Arial', 8),
            foreground='gray',
            cursor="hand2"
        )
        author_label.grid(row=1, column=0, pady=(2, 0))
        author_label.bind("<Button-1>", self.on_logo_click)
    
    def setup_text_logo(self, parent):
        """設定文字Logo（後備）"""
        logo_text = ttk.Label(
            parent,
            text="ZhongTaiko\nTHE CONTROLLER.",
            font=('Arial', 10, 'bold'),
            justify=tk.CENTER,
            cursor="hand2"
        )
        logo_text.grid(row=0, column=0, padx=5)
        logo_text.bind("<Button-1>", self.on_logo_click)
    
    def on_logo_click(self, event):
        """處理Logo點擊事件"""
        try:
            webbrowser.open("https://taiko.ac")
        except Exception as e:
            print(f"無法打開網頁瀏覽器: {e}")
            
    def on_file_drop(self, event):
        """處理拖拉檔案事件"""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]  # 只取第一個檔案
            if file_path.lower().endswith('.tja'):
                self.file_var.set(file_path)
                self.log_message(self.lang_mgr.get_text('file_dropped', os.path.basename(file_path)))
            else:
                messagebox.showwarning("Warning", self.lang_mgr.get_text('drag_drop_invalid'))
    
    def browse_file(self):
        """瀏覽TJA檔案"""
        file_path = filedialog.askopenfilename(
            title=self.lang_mgr.get_text('file_selection'),
            filetypes=[('TJA files', '*.tja'), ('All files', '*.*')]
        )
        if file_path:
            self.file_var.set(file_path)
    
    def validate_speed_input(self, value_if_allowed, char):
        """驗證速度輸入框只允許數字和小數點"""
        if value_if_allowed == "":
            return True  # 允許空字符串
        
        # 允許的字符：數字和一個小數點
        if not char.isdigit() and char != '.':
            return False
        
        # 檢查小數點數量
        if char == '.':
            if value_if_allowed.count('.') > 1:
                return False
        
        # 檢查是否為有效的數字格式
        try:
            if value_if_allowed != '.':  # 允許只輸入小數點
                float(value_if_allowed)
        except ValueError:
            if value_if_allowed != '.':  # 除了單純的小數點
                return False
        
        return True
    
    def on_speed_change(self, value=None):
        """處理速度滑桿變化，精確捨入"""
        raw_speed = self.speed_var.get()
        # 捨入至兩位小數以獲得清潔顯示
        rounded_speed = round(raw_speed, 2)
        # 將變數更新為捨入值
        self.speed_var.set(rounded_speed)
        # 同步更新數字輸入框
        self.speed_entry_var.set(f"{rounded_speed:.2f}")
        # 更新標籤
        self.update_speed_label()
    
    def on_speed_entry_change(self, event=None):
        """處理數字輸入框變化"""
        speed_text = self.speed_entry_var.get().strip()
        
        # 如果是空字符串或只是小數點，不處理
        if speed_text == "" or speed_text == ".":
            return
        
        try:
            speed = float(speed_text)
            
            # 限制範圍
            if speed < 0.01:
                speed = 0.01
                self.speed_entry_var.set(f"{speed:.2f}")
            elif speed > 10.0:
                speed = 10.0
                self.speed_entry_var.set(f"{speed:.2f}")
            
            # 更新滑桿
            self.speed_var.set(speed)
            self.update_speed_label()
            
        except ValueError:
            # 如果輸入無效，恢復到當前滑桿值
            current_speed = self.speed_var.get()
            self.speed_entry_var.set(f"{current_speed:.2f}")
    
    def update_speed_label(self, value=None):
        """更新速度標籤"""
        speed = self.speed_var.get()
        text = self.lang_mgr.get_text('speed_range', speed)
        self.speed_label.config(text=text)
        
    def on_language_change(self, event=None):
        """處理語言變更並刷新記錄"""
        new_language = self.language_var.get()
        old_language = self.lang_mgr.current_language
        
        # 如果是相同語言則不處理
        if new_language == old_language:
            return
            
        self.lang_mgr.set_language(new_language)
        
        # 清除並刷新記錄顯示
        self.clear_results()
        
        # 以新語言顯示語言變更訊息
        language_names = {'en': 'English', 'zh-tw': '繁體中文', 'ja': '日本語'}
        language_name = language_names.get(new_language, new_language)
        self.log_message(self.lang_mgr.get_text('language_changed_message', language_name))
        
        self.update_language()
        
    def update_language(self):
        """以當前語言更新所有文字元素"""
        # 視窗標題
        self.root.title(self.lang_mgr.get_text('main_window_title'))
        
        # 標籤和框架
        self.file_frame.config(text=self.lang_mgr.get_text('file_selection'))
        self.browse_button.config(text=self.lang_mgr.get_text('browse_button'))
        self.click_label.config(text=self.lang_mgr.get_text('click_to_browse'))
        
        self.speed_frame.config(text=self.lang_mgr.get_text('speed_setting'))
        self.update_speed_label()
        
        self.lang_frame.config(text=self.lang_mgr.get_text('language_setting'))
        
        self.process_button.config(text=self.lang_mgr.get_text('process_button'))
        
        self.results_frame.config(text=self.lang_mgr.get_text('result_title'))
        self.clear_button.config(text=self.lang_mgr.get_text('clear_log'))
        
        # 狀態
        self.status_var.set(self.lang_mgr.get_text('status_ready'))
        
    def log_message(self, message):
        """將訊息添加到結果區域"""
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, message + '\n')
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')
        self.root.update()
        
    def clear_results(self):
        """清除結果區域"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        
    def update_status(self, status):
        """更新狀態列"""
        self.status_var.set(status)
        self.root.update()
        
    def process_files(self):
        """處理TJA檔案與OGG轉換"""
        # 驗證輸入
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
        if not (0.01 <= speed <= 10.0):
            messagebox.showerror("Error", self.lang_mgr.get_text('error_speed_range'))
            return
        
        # 處理期間停用UI
        self.process_button.config(state='disabled')
        self.update_status(self.lang_mgr.get_text('processing'))
        
        # 在獨立執行緒中執行處理
        thread = threading.Thread(
            target=self._process_files_thread,
            args=(tja_path, speed)
        )
        thread.daemon = True
        thread.start()
        
    def _process_files_thread(self, tja_path, speed):
        """在獨立執行緒中處理檔案"""
        try:
            def progress_callback(message):
                self.root.after(0, self.update_status, message)
                
            def log_callback(message):
                self.root.after(0, self.log_message, message)
            
            # 處理檔案
            new_tja_path, new_audio_path = self.processor.process_files(
                tja_path, speed, progress_callback, log_callback
            )
            
            # 顯示結果
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
        """啟動GUI應用程式"""
        self.root.mainloop()


def main():
    """主要進入點"""
    try:
        app = TJASpeedChangerGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"啟動應用程式失敗: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()