# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file for Tower Defense Game
#
# Build with:  pyinstaller build.spec
# Output:      dist/TowerDefense/TowerDefense.exe
#
# NOTE: Run this from the project root directory

import os

block_cipher = None

datas = [
    ('assets', 'assets'),
    ('src/config/theme.json', 'src/config'),
    ('src/config/levels', 'src/config/levels'),
]

hiddenimports = [
    'pygame',
    'pygame_gui',
    'pygame.mixer',
    'pygame.font',
    'pygame.image',
]

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'pydoc',
        'doctest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TowerDefense',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icons.ico' if os.path.exists('assets/images/icons.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TowerDefense',
)
