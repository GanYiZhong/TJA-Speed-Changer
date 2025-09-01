#!/usr/bin/env python3
"""
測試編碼處理修正
"""

import os
import tempfile
from TJASpeedChangerGUI_Final import TJAProcessor, LanguageManager

def test_big5_encoding():
    """測試Big5編碼處理"""
    print("測試Big5編碼處理...")
    
    # 建立語言管理器和處理器
    lang_mgr = LanguageManager()
    processor = TJAProcessor(lang_mgr)
    
    # 建立測試用的Big5編碼TJA檔案
    test_content = """TITLE:測試歌曲
ARTIST:測試藝術家
BPM:120
WAVE:test.ogg

#START
1010,
#END
"""
    
    # 建立臨時檔案
    with tempfile.NamedTemporaryFile(mode='w', encoding='big5', suffix='.tja', delete=False) as f:
        f.write(test_content)
        temp_tja_path = f.name
    
    try:
        print(f"建立測試檔案: {temp_tja_path}")
        
        # 檢測編碼
        detected_encoding = processor.detect_file_encoding(temp_tja_path)
        print(f"檢測到編碼: {detected_encoding}")
        
        # 處理檔案
        wave_filename, new_wave_filename, new_tja_path = processor.adjust_tja_speed(
            temp_tja_path, 1.5, progress_callback=print
        )
        
        print(f"新TJA檔案: {new_tja_path}")
        
        # 檢查輸出檔案的編碼
        if os.path.exists(new_tja_path):
            output_encoding = processor.detect_file_encoding(new_tja_path)
            print(f"輸出檔案編碼: {output_encoding}")
            
            # 讀取並顯示內容
            with open(new_tja_path, 'r', encoding=output_encoding) as f:
                content = f.read()
                print("輸出檔案內容:")
                print(content[:200] + "..." if len(content) > 200 else content)
            
            if output_encoding == detected_encoding:
                print("✓ 編碼保持一致!")
            else:
                print(f"✗ 編碼不一致! 輸入: {detected_encoding}, 輸出: {output_encoding}")
            
            # 清理
            os.unlink(new_tja_path)
        else:
            print("✗ 輸出檔案未建立")
        
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理臨時檔案
        if os.path.exists(temp_tja_path):
            os.unlink(temp_tja_path)

def test_shift_jis_encoding():
    """測試Shift-JIS編碼處理"""
    print("\n測試Shift-JIS編碼處理...")
    
    # 建立語言管理器和處理器
    lang_mgr = LanguageManager()
    processor = TJAProcessor(lang_mgr)
    
    # 建立測試用的Shift-JIS編碼TJA檔案
    test_content = """TITLE:テスト楽曲
ARTIST:テストアーティスト
BPM:120
WAVE:test.ogg

#START
1010,
#END
"""
    
    # 建立臨時檔案
    with tempfile.NamedTemporaryFile(mode='w', encoding='shift_jis', suffix='.tja', delete=False) as f:
        f.write(test_content)
        temp_tja_path = f.name
    
    try:
        print(f"建立測試檔案: {temp_tja_path}")
        
        # 檢測編碼
        detected_encoding = processor.detect_file_encoding(temp_tja_path)
        print(f"檢測到編碼: {detected_encoding}")
        
        # 處理檔案
        wave_filename, new_wave_filename, new_tja_path = processor.adjust_tja_speed(
            temp_tja_path, 1.5, progress_callback=print
        )
        
        print(f"新TJA檔案: {new_tja_path}")
        
        # 檢查輸出檔案的編碼
        if os.path.exists(new_tja_path):
            output_encoding = processor.detect_file_encoding(new_tja_path)
            print(f"輸出檔案編碼: {output_encoding}")
            
            # 讀取並顯示內容
            with open(new_tja_path, 'r', encoding=output_encoding) as f:
                content = f.read()
                print("輸出檔案內容:")
                print(content[:200] + "..." if len(content) > 200 else content)
            
            if output_encoding == detected_encoding:
                print("✓ 編碼保持一致!")
            else:
                print(f"✗ 編碼不一致! 輸入: {detected_encoding}, 輸出: {output_encoding}")
            
            # 清理
            os.unlink(new_tja_path)
        else:
            print("✗ 輸出檔案未建立")
        
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理臨時檔案
        if os.path.exists(temp_tja_path):
            os.unlink(temp_tja_path)

if __name__ == '__main__':
    test_big5_encoding()
    test_shift_jis_encoding()
    print("\n測試完成!")