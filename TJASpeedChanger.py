import argparse
import os
import locale
import sys
# 多語言支援
LANGUAGES = {
    'en': {
        'title': 'TJA Speed Changer - Modify TJA files and audio source speed',
        'description': 'Modify TJA files and audio source speed for Taiko no Tatsujin',
        'epilog': '''
Usage Examples:
  python tja_speed_changer.py song.tja 0.9
  python tja_speed_changer.py "Central Dogma Pt.1.tja" 0.8
  python tja_speed_changer.py song.tja 1.2
Notes:
  - FFmpeg is required to process audio files
  - Speed range: 0.5 ~ 2.0
  - New TJA and audio files will be automatically generated
  - Supports #DELAY command adjustment
        ''',
        'tja_file_help': 'TJA file path',
        'speed_help': 'Speed multiplier (0.5~2.0)',
        'lang_help': 'Interface language (en/zh-tw/ja)',
        'error_speed_range': '❌ Error: Speed multiplier must be between 0.5 and 2.0',
        'error_file_not_found': '❌ Error: TJA file not found: {}',
        'error_file_encoding': '❌ Error: Unable to read TJA file. Please check file encoding.',
        'start_processing': '🎵 Start processing: {} (Speed: {}x)',
        'tja_processed': '✅ TJA file processed: {}',
        'warning_no_wave': '⚠️  Warning: WAVE tag not found in TJA file, only processing score file',
        'warning_audio_not_found': '⚠️  Warning: Audio file not found: {}',
        'manual_audio_note': 'Only TJA file processed, please handle audio file manually',
        'start_audio_processing': '🎧 Start processing audio file...',
        'audio_processed': '✅ Audio file processed: {}',
        'processing_complete': '\n🎉 Processing complete!',
        'new_files': '📁 New files:',
        'tja_label': '   - TJA: {}',
        'audio_label': '   - Audio: {}',
        'audio_processing_failed': '❌ Audio processing failed',
        'error_occurred': '❌ Error occurred: {}',
        'ffmpeg_not_found': 'FFmpeg not found, please ensure FFmpeg is installed and added to system PATH',
        'ffmpeg_error': 'FFmpeg error: {}',
        'audio_processing_error': 'Error occurred while processing audio: {}'
    },
    'zh-tw': {
        'title': 'TJA速度修改器 - 修改TJA檔案與音源速度',
        'description': '修改太鼓達人TJA檔案與音源速度',
        'epilog': '''
使用範例:
  python tja_speed_changer.py song.tja 0.9
  python tja_speed_changer.py "Central Dogma Pt.1.tja" 0.8
  python tja_speed_changer.py song.tja 1.2
注意事項:
  - 需要安裝FFmpeg來處理音源檔案
  - 速度倍率範圍: 0.5 ~ 2.0
  - 會自動產生新的TJA和音源檔案
  - 支援 #DELAY 指令調整
        ''',
        'tja_file_help': 'TJA檔案路徑',
        'speed_help': '速度倍率 (0.5~2.0)',
        'lang_help': '介面語言 (en/zh-tw/ja)',
        'error_speed_range': '❌ 錯誤: 速度倍率必須介於0.5到2.0之間',
        'error_file_not_found': '❌ 錯誤: 找不到TJA檔案: {}',
        'error_file_encoding': '❌ 錯誤: 無法讀取TJA檔案，請檢查檔案編碼',
        'start_processing': '🎵 開始處理: {} (速度: {}x)',
        'tja_processed': '✅ TJA檔案已處理: {}',
        'warning_no_wave': '⚠️  警告: TJA檔案中找不到WAVE標籤，僅處理譜面檔案',
        'warning_audio_not_found': '⚠️  警告: 找不到音源檔案: {}',
        'manual_audio_note': '僅處理了TJA檔案，請手動處理音源檔案',
        'start_audio_processing': '🎧 開始處理音源檔案...',
        'audio_processed': '✅ 音源檔案已處理: {}',
        'processing_complete': '\n🎉 處理完成！',
        'new_files': '📁 新檔案:',
        'tja_label': '   - TJA: {}',
        'audio_label': '   - 音源: {}',
        'audio_processing_failed': '❌ 音源處理失敗',
        'error_occurred': '❌ 發生錯誤: {}',
        'ffmpeg_not_found': '找不到FFmpeg，請確保已安裝FFmpeg並加入系統PATH',
        'ffmpeg_error': 'FFmpeg錯誤: {}',
        'audio_processing_error': '處理音源時發生錯誤: {}'
    },
    'ja': {
        'title': 'TJA速度変更ツール - TJAファイルと音源の速度を変更',
        'description': '太鼓の達人TJAファイルと音源の速度を変更',
        'epilog': '''
使用例:
  python tja_speed_changer.py song.tja 0.9
  python tja_speed_changer.py "Central Dogma Pt.1.tja" 0.8
  python tja_speed_changer.py song.tja 1.2
注意事項:
  - 音源ファイルの処理にはFFmpegが必要です
  - 速度倍率範囲: 0.5 ~ 2.0
  - 新しいTJAと音源ファイルが自動生成されます
  - #DELAYコマンドの調整をサポート
        ''',
        'tja_file_help': 'TJAファイルのパス',
        'speed_help': '速度倍率 (0.5~2.0)',
        'lang_help': 'インターフェース言語 (en/zh-tw/ja)',
        'error_speed_range': '❌ エラー: 速度倍率は0.5から2.0の間でなければなりません',
        'error_file_not_found': '❌ エラー: TJAファイルが見つかりません: {}',
        'error_file_encoding': '❌ エラー: TJAファイルを読み取れません。ファイルのエンコーディングを確認してください。',
        'start_processing': '🎵 処理開始: {} (速度: {}x)',
        'tja_processed': '✅ TJAファイル処理完了: {}',
        'warning_no_wave': '⚠️  警告: TJAファイルにWAVEタグが見つかりません、譜面ファイルのみ処理します',
        'warning_audio_not_found': '⚠️  警告: 音源ファイルが見つかりません: {}',
        'manual_audio_note': 'TJAファイルのみ処理されました、音源ファイルは手動で処理してください',
        'start_audio_processing': '🎧 音源ファイル処理開始...',
        'audio_processed': '✅ 音源ファイル処理完了: {}',
        'processing_complete': '\n🎉 処理完了！',
        'new_files': '📁 新しいファイル:',
        'tja_label': '   - TJA: {}',
        'audio_label': '   - 音源: {}',
        'audio_processing_failed': '❌ 音源処理失敗',
        'error_occurred': '❌ エラーが発生しました: {}',
        'ffmpeg_not_found': 'FFmpegが見つかりません、FFmpegがインストールされ、システムPATHに追加されているか確認してください',
        'ffmpeg_error': 'FFmpegエラー: {}',
        'audio_processing_error': '音源処理中にエラーが発生しました: {}'
    }
}
def get_system_language():
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
def get_text(key, lang='en'):
    """獲取指定語言的文本"""
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, LANGUAGES['en'][key])
def detect_file_encoding(file_path):
    """檢測檔案編碼"""
    encodings = ['utf-8', 'utf-8-sig', 'cp950', 'gbk', 'shift_jis', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # 預設返回utf-8
def adjust_tja_speed(tja_path, speed, lang='en'):
    """調整TJA檔案的速度參數，包含 #DELAY 處理"""
    
    # 自動檢測檔案編碼
    detected_encoding = detect_file_encoding(tja_path)
    
    try:
        with open(tja_path, 'r', encoding=detected_encoding, errors='ignore') as file:
            lines = file.readlines()
    except Exception as e:
        print(get_text('error_file_encoding', lang))
        raise e
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
        # 修改WAVE檔案名稱 - 始終轉換為OGG格式
        elif line.startswith('WAVE:'):
            wave_filename = line.strip().split(':', 1)[1]
            file_root, file_ext = os.path.splitext(wave_filename)
            # 始終轉換為OGG格式
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
        # 新增：處理 #DELAY 指令
        elif line.startswith('#DELAY'):
            parts = line.strip().split(' ')
            if len(parts) >= 2:
                try:
                    # DELAY的秒數需要乘以速度倍率（因為歌曲變速了，延遲時間也要相應調整）
                    delay_seconds = float(parts[1])
                    new_delay = delay_seconds * speed
                    new_lines.append(f'#DELAY {new_delay:.3f}\n')
                except ValueError:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    # 儲存新的TJA檔案
    base, ext = os.path.splitext(tja_path)
    new_tja_path = f'{base}_{speed:.2f}x{ext}'
    
    # 使用UTF-8編碼儲存，確保相容性
    with open(new_tja_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    return wave_filename, new_wave_filename, new_tja_path
def find_audio_file(base_dir, wave_filename):
    """尋找各種副檔名的音源檔案 (mp3, wav, ogg, flac, m4a)"""
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

def adjust_audio_speed_ffmpeg(input_path, output_path, speed, lang='en'):
    """使用ffmpeg調整音源速度並轉換為OGG格式"""
    try:
        import subprocess
        
        # 確保輸出為OGG格式，無論輸入格式為何
        output_path_ogg = os.path.splitext(output_path)[0] + '.ogg'
        
        # 使用atempo濾鏡調整速度，保持音調，並轉換為OGG格式
        if speed > 2.0:
            # 如果速度超過2.0，需要串聯多個atempo
            cmd = [
                'ffmpeg', '-i', input_path,
                '-filter:a', f'atempo=2.0,atempo={speed/2.0}',
                '-c:a', 'libvorbis',  # OGG Vorbis編碼器
                '-q:a', '5',          # 品質等級5 (良好平衡)
                '-y', output_path_ogg
            ]
        elif speed < 0.5:
            # 如果速度低於0.5，需要串聯多個atempo
            cmd = [
                'ffmpeg', '-i', input_path,
                '-filter:a', f'atempo=0.5,atempo={speed/0.5}',
                '-c:a', 'libvorbis',  # OGG Vorbis編碼器
                '-q:a', '5',          # 品質等級5 (良好平衡)
                '-y', output_path_ogg
            ]
        else:
            cmd = [
                'ffmpeg', '-i', input_path,
                '-filter:a', f'atempo={speed}',
                '-c:a', 'libvorbis',  # OGG Vorbis編碼器
                '-q:a', '5',          # 品質等級5 (良好平衡)
                '-y', output_path_ogg
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(get_text('ffmpeg_error', lang).format(result.stderr))
            return False, output_path_ogg
        return True, output_path_ogg
    except FileNotFoundError:
        print(get_text('ffmpeg_not_found', lang))
        return False, None
    except Exception as e:
        print(get_text('audio_processing_error', lang).format(e))
        return False, None
def main():
    # 自動檢測系統語言
    default_lang = get_system_language()
    
    # 暫時創建parser來處理語言參數
    temp_parser = argparse.ArgumentParser(add_help=False)
    temp_parser.add_argument('--lang', '--language', 
                           choices=['en', 'zh-tw', 'ja'], 
                           default=default_lang)
    temp_args, _ = temp_parser.parse_known_args()
    lang = temp_args.lang
    
    # 創建主要的parser，使用選定的語言
    parser = argparse.ArgumentParser(
        description=get_text('description', lang),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_text('epilog', lang)
    )
    
    parser.add_argument('tja_file', type=str, help=get_text('tja_file_help', lang))
    parser.add_argument('speed', type=float, help=get_text('speed_help', lang))
    parser.add_argument('--lang', '--language', 
                        choices=['en', 'zh-tw', 'ja'], 
                        default=default_lang,
                        help=get_text('lang_help', lang))
    
    args = parser.parse_args()
    lang = args.lang  # 使用用户指定的語言
    # 檢查速度範圍
    if not (0.5 <= args.speed <= 2.0):
        print(get_text('error_speed_range', lang))
        return
    # 檢查TJA檔案是否存在
    if not os.path.exists(args.tja_file):
        print(get_text('error_file_not_found', lang).format(args.tja_file))
        return
    print(get_text('start_processing', lang).format(args.tja_file, args.speed))
    try:
        # 處理TJA檔案
        wave_filename, new_wave_filename, new_tja_path = adjust_tja_speed(args.tja_file, args.speed, lang)
        print(get_text('tja_processed', lang).format(new_tja_path))
        if wave_filename is None:
            print(get_text('warning_no_wave', lang))
            return
        # 處理音源檔案 - 尋找各種格式並轉換為OGG
        base_dir = os.path.dirname(args.tja_file)
        input_audio_path = find_audio_file(base_dir, wave_filename)
        output_audio_path = os.path.join(base_dir, new_wave_filename)
        
        if not input_audio_path:
            print(get_text('warning_audio_not_found', lang).format(wave_filename))
            print(get_text('manual_audio_note', lang))
            return
            
        print(get_text('start_audio_processing', lang))
        print(f"找到音源檔案: {os.path.basename(input_audio_path)}")
        
        success, actual_output_path = adjust_audio_speed_ffmpeg(input_audio_path, output_audio_path, args.speed, lang)
        if success:
            print(get_text('audio_processed', lang).format(actual_output_path))
            print(get_text('processing_complete', lang))
            print(get_text('new_files', lang))
            print(get_text('tja_label', lang).format(new_tja_path))
            print(get_text('audio_label', lang).format(actual_output_path))
        else:
            print(get_text('audio_processing_failed', lang))
    except Exception as e:
        print(get_text('error_occurred', lang).format(e))
if __name__ == '__main__':
    main()