# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file for Tower Defense Game
#
# Build with:  pyinstaller build.spec
# Output:      dist/TowerDefense/TowerDefense.exe
#
# NOTE: Run this from the project root directory (the folder containing
#       assets/, src/, and this spec file).

import os
import site

block_cipher = None

# ---------------------------------------------------------------------------
# Collect data files
# ---------------------------------------------------------------------------
# Each entry is a tuple: (source_path_or_glob, destination_folder_in_bundle)

pygame_gui_data = None
for site_dir in site.getsitepackages():
    pygame_gui_path = os.path.join(site_dir, 'pygame_gui', 'data')
    if os.path.exists(pygame_gui_path):
        pygame_gui_data = pygame_gui_path
        break

datas = [
    ('assets', 'assets'),
    ('src/config/theme.json', 'src/config'),
    ('src/config/levels', 'src/config/levels'),
]

if pygame_gui_data:
    datas.append((pygame_gui_data, 'pygame_gui/data'))

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

# ---------------------------------------------------------------------------
# PYZ (zipped Python modules)
# ---------------------------------------------------------------------------
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ---------------------------------------------------------------------------
# EXE
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# COLLECT (one-folder distribution - everything in same directory)
# ---------------------------------------------------------------------------
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
