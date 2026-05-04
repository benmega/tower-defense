# -*- mode: python ; coding: utf-8 -*-
<<<<<<< HEAD

block_cipher = None

import os

# Get the directory where this spec file is located
spec_dir = os.getcwd()

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(spec_dir, 'assets'), 'assets'),
        (os.path.join(spec_dir, 'src/config/theme.json'), 'src/config'),
        (os.path.join(spec_dir, 'src/config/levels'), 'src/config/levels'),
        ('C:\\Users\\Ben\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\pygame_gui\\data', 'pygame_gui\\data'),
    ],
    hiddenimports=['pygame_gui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
=======
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
>>>>>>> claude/laughing-ardinghelli-b72776
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

<<<<<<< HEAD
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

=======
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

>>>>>>> claude/laughing-ardinghelli-b72776
exe = EXE(
    pyz,
    a.scripts,
    [],
<<<<<<< HEAD
=======
    exclude_binaries=True,   # one-folder build (not onefile)
>>>>>>> claude/laughing-ardinghelli-b72776
    name='TowerDefense',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
<<<<<<< HEAD
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

=======
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
>>>>>>> claude/laughing-ardinghelli-b72776
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
<<<<<<< HEAD
    name='TowerDefense',
=======
    name='TowerDefense',     # dist/TowerDefense/
>>>>>>> claude/laughing-ardinghelli-b72776
)
