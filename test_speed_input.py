#!/usr/bin/env python3
"""
測試速度輸入框功能
"""

import tkinter as tk
from tkinter import ttk

def validate_speed_input(value_if_allowed, char):
    """驗證速度輸入框只允許數字和小數點"""
    print(f"測試輸入: '{value_if_allowed}', 字符: '{char}'")
    
    if value_if_allowed == "":
        print("✓ 允許空字符串")
        return True
    
    # 允許的字符：數字和一個小數點
    if not char.isdigit() and char != '.':
        print("✗ 不允許的字符")
        return False
    
    # 檢查小數點數量
    if char == '.':
        if value_if_allowed.count('.') > 1:
            print("✗ 太多小數點")
            return False
    
    # 檢查是否為有效的數字格式
    try:
        if value_if_allowed != '.':
            float(value_if_allowed)
            print("✓ 有效數字")
    except ValueError:
        if value_if_allowed != '.':
            print("✗ 無效數字格式")
            return False
        else:
            print("✓ 允許單獨的小數點")
    
    return True

def test_gui():
    """測試GUI"""
    root = tk.Tk()
    root.title("Speed Input Test")
    root.geometry("300x150")
    
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # 測試輸入框
    label = ttk.Label(frame, text="測試速度輸入 (只允許數字和小數點):")
    label.pack(pady=(0, 10))
    
    speed_var = tk.StringVar(value="1.00")
    vcmd = (root.register(validate_speed_input), '%P', '%S')
    
    entry = ttk.Entry(
        frame, 
        textvariable=speed_var,
        width=15,
        justify='center',
        validate='key',
        validatecommand=vcmd
    )
    entry.pack(pady=(0, 10))
    
    # 顯示當前值
    def show_value():
        print(f"當前值: '{speed_var.get()}'")
        try:
            float_val = float(speed_var.get())
            result_label.config(text=f"數值: {float_val}")
        except ValueError:
            result_label.config(text="無效數值")
    
    button = ttk.Button(frame, text="檢查值", command=show_value)
    button.pack(pady=(0, 10))
    
    result_label = ttk.Label(frame, text="")
    result_label.pack()
    
    # 測試案例說明
    instructions = ttk.Label(
        frame, 
        text="測試案例:\n- 輸入數字 (1, 2, 10)\n- 輸入小數 (1.5, 0.01)\n- 輸入小數點 (.5)\n- 嘗試輸入字母 (應該被阻止)",
        justify=tk.LEFT
    )
    instructions.pack(pady=(10, 0))
    
    root.mainloop()

if __name__ == "__main__":
    print("開始測試速度輸入驗證...")
    
    # 測試驗證函數
    test_cases = [
        ("1", "1"),
        ("1.", "."),
        ("1.5", "5"),
        ("1.5.", "."),
        ("a", "a"),
        ("1a", "a"),
        (".", "."),
        ("", "1"),
    ]
    
    print("\n驗證函數測試:")
    for value, char in test_cases:
        print(f"\n測試: value='{value}', char='{char}'")
        result = validate_speed_input(value, char)
        print(f"結果: {'通過' if result else '拒絕'}")
    
    print("\n啟動GUI測試...")
    test_gui()