# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TJASpeedChangerGUI_Final.py'],
    pathex=[],
    binaries=[('ffmpeg.exe', '.')],
    datas=[('LOGO_BLACK_TRANS.png', '.')],
    hiddenimports=['tkinterdnd2', 'tkinterdnd2.tkdnd', 'PIL', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TJASpeedChangerGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
)
