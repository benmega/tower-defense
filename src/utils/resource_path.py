"""
resource_path.py

Resolves file paths correctly whether the game is running from source or
from a PyInstaller-frozen executable.

PyInstaller bundles data files into a temp folder referenced by sys._MEIPASS
when running as a one-file build, or places them alongside the exe for a
one-folder build.  For a one-folder build (which this project uses) the
bundled data files live right next to TowerDefense.exe, so we just need to
anchor paths to the directory containing the executable rather than to the
current working directory.

Usage
-----
    from src.utils.resource_path import resource_path
    image = pygame.image.load(resource_path('assets/images/towers/basic_tower.png'))
"""

import os
import sys


def get_base_path() -> str:
    """
    Return the root directory that contains the bundled game data.

    - Frozen (PyInstaller): looks for assets in exe_dir, then exe_dir/_internal
    - Running from source:   project root (two levels above this file)
    """
    if getattr(sys, 'frozen', False):
        # For PyInstaller builds, sys._MEIPASS is set by the bootloader
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS

        # For one-folder builds with _internal subdirectory
        exe_dir = os.path.dirname(sys.executable)
        if os.path.exists(os.path.join(exe_dir, '_internal', 'assets')):
            return os.path.join(exe_dir, '_internal')

        # Check if assets exist directly in exe directory
        if os.path.exists(os.path.join(exe_dir, 'assets')):
            return exe_dir

        # Fall back to exe directory
        return exe_dir
    else:
        # Running from source: this file is at src/utils/resource_path.py,
        # so the project root is two directories up.
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


BASE_PATH: str = get_base_path()


def get_save_dir() -> str:
    """
    Return a writable directory for save files.

    Frozen builds may install to a read-only location (e.g. Program Files),
    so saves go to %APPDATA%/TowerDefense/save_data on Windows and
    ~/.local/share/TowerDefense/save_data elsewhere.
    When running from source, uses <project_root>/save_data.
    """
    if getattr(sys, 'frozen', False):
        if os.name == 'nt':
            base = os.environ.get('APPDATA', os.path.expanduser('~'))
        else:
            base = os.path.join(os.path.expanduser('~'), '.local', 'share')
        save_dir = os.path.join(base, 'TowerDefense', 'save_data')
    else:
        save_dir = os.path.join(BASE_PATH, 'save_data')
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def resource_path(relative_path: str) -> str:
    """
    Return the absolute path to a resource, anchored to BASE_PATH.

    Parameters
    ----------
    relative_path : str
        A path relative to the project root, e.g. 'assets/images/towers/basic_tower.png'
        or 'src/config/levels/LevelsAll.json'.

    Returns
    -------
    str
        Absolute path suitable for open() or pygame image/sound loading.
    """
    return os.path.join(BASE_PATH, relative_path)
