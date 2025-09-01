#!/usr/bin/env python3
"""
測試ANSI編碼處理
"""

def test_ansi_big5():
    """測試ANSI Big5 (CP950) 編碼"""
    print("測試ANSI Big5編碼...")
    
    # 繁體中文測試內容
    test_content = """TITLE:人魚姬
ARTIST:測試藝術家
BPM:120.000
WAVE:mermaid.ogg

#START
1010,
#END
"""
    
    # 建立CP950 (ANSI Big5)測試檔案
    try:
        with open("test_ansi_big5.tja", "w", encoding="cp950") as f:
            f.write(test_content)
        print("✓ ANSI Big5測試檔案建立成功")
        
        # 嘗試用不同編碼讀取
        encodings = ['cp950', 'big5', 'utf-8', 'gbk']
        
        for encoding in encodings:
            try:
                with open("test_ansi_big5.tja", "r", encoding=encoding) as f:
                    content = f.read()
                    title_line = [line for line in content.split('\n') if line.startswith('TITLE:')][0]
                    print(f"使用 {encoding} 讀取: {title_line}")
            except (UnicodeDecodeError, IndexError) as e:
                print(f"使用 {encoding} 讀取失敗: {type(e).__name__}")
        
        # 清理檔案
        import os
        if os.path.exists("test_ansi_big5.tja"):
            os.unlink("test_ansi_big5.tja")
            
    except Exception as e:
        print(f"測試失敗: {e}")

def test_ansi_shift_jis():
    """測試ANSI Shift-JIS (CP932) 編碼"""
    print("\n測試ANSI Shift-JIS編碼...")
    
    # 日文測試內容
    test_content = """TITLE:人魚姫
ARTIST:テストアーティスト
BPM:120.000
WAVE:mermaid.ogg

#START
1010,
#END
"""
    
    # 建立CP932 (ANSI Shift-JIS)測試檔案
    try:
        with open("test_ansi_sjis.tja", "w", encoding="cp932") as f:
            f.write(test_content)
        print("✓ ANSI Shift-JIS測試檔案建立成功")
        
        # 嘗試用不同編碼讀取
        encodings = ['cp932', 'shift_jis', 'utf-8', 'euc-jp']
        
        for encoding in encodings:
            try:
                with open("test_ansi_sjis.tja", "r", encoding=encoding) as f:
                    content = f.read()
                    title_line = [line for line in content.split('\n') if line.startswith('TITLE:')][0]
                    print(f"使用 {encoding} 讀取: {title_line}")
            except (UnicodeDecodeError, IndexError) as e:
                print(f"使用 {encoding} 讀取失敗: {type(e).__name__}")
        
        # 清理檔案
        import os
        if os.path.exists("test_ansi_sjis.tja"):
            os.unlink("test_ansi_sjis.tja")
            
    except Exception as e:
        print(f"測試失敗: {e}")

if __name__ == "__main__":
    test_ansi_big5()
    test_ansi_shift_jis()
    print("\n測試完成!")