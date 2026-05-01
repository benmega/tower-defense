# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file for Mr. Mega's Awesome Tower Defense Game
#
# Build with:  pyinstaller build.spec
# Output:      dist/TowerDefense/TowerDefense.exe
#
# NOTE: Run this from the project root directory (the folder containing
#       assets/, src/, and this spec file).

import os

block_cipher = None

# ---------------------------------------------------------------------------
# Collect data files
# ---------------------------------------------------------------------------
# Each entry is a tuple: (source_path_or_glob, destination_folder_in_bundle)
# The destination '.' means "root of the bundle folder".

datas = [
    # Entire assets directory (images, sounds, ~150 MB)
    ('assets', 'assets'),

    # pygame-gui theme file
    ('src/config/theme.json', 'src/config'),

    # Level JSON files
    ('src/config/levels', 'src/config/levels'),
]

# ---------------------------------------------------------------------------
# Hidden imports that PyInstaller may miss
# ---------------------------------------------------------------------------
hiddenimports = [
    'pygame',
    'pygame_gui',
    'pygame.mixer',
    'pygame.font',
    'pygame.image',
]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
a = Analysis(
    ['src/main.py'],
    pathex=['.'],           # project root on the search path
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

# ---------------------------------------------------------------------------
# PYZ (zipped Python modules)
# ---------------------------------------------------------------------------
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ---------------------------------------------------------------------------
# EXE
# ---------------------------------------------------------------------------
# icon: assets/images/icons.png exists but Windows requires .ico format.
# Convert icons.png to icons.ico with Pillow before building, then set:
#   icon='assets/images/icons.ico'
# For now we leave icon unset; PyInstaller will use its default.

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # one-folder build (not onefile)
    name='TowerDefense',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # hide the console window (windowed mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icons.ico',
)

# ---------------------------------------------------------------------------
# COLLECT (one-folder distribution)
# ---------------------------------------------------------------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TowerDefense',     # dist/TowerDefense/
)
