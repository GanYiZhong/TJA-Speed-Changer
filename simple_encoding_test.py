#!/usr/bin/env python3
"""
簡單編碼測試
"""

def test_encoding_detection():
    """測試編碼檢測邏輯"""
    try:
        # 測試Big5內容
        big5_content = "測試中文內容"
        
        # 建立Big5測試檔案
        with open("test_big5.tja", "w", encoding="big5") as f:
            f.write("TITLE:" + big5_content + "\n")
            f.write("BPM:120\n")
            f.write("WAVE:test.ogg\n")
        
        print("Big5測試檔案已建立")
        
        # 讀取並檢測
        encodings_to_try = ['big5', 'cp950', 'utf-8', 'shift_jis']
        
        for encoding in encodings_to_try:
            try:
                with open("test_big5.tja", "r", encoding=encoding) as f:
                    content = f.read()
                    print(f"使用 {encoding} 編碼讀取成功:")
                    print(f"內容預覽: {content[:50]}...")
                    break
            except UnicodeDecodeError:
                print(f"使用 {encoding} 編碼讀取失敗")
                continue
        
        print("測試完成")
        
        # 清理
        import os
        if os.path.exists("test_big5.tja"):
            os.unlink("test_big5.tja")
            
    except Exception as e:
        print(f"測試出錯: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_encoding_detection()