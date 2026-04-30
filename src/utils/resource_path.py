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

    - Frozen (PyInstaller one-folder): directory of TowerDefense.exe
    - Frozen (PyInstaller onefile):    sys._MEIPASS temp directory
    - Running from source:             project root (two levels above this file)
    """
    if getattr(sys, 'frozen', False):
        # sys._MEIPASS is set for onefile builds; for one-folder builds the
        # data sits next to the exe, so sys.executable's directory is correct
        # in both cases.
        return os.path.dirname(sys.executable)
    else:
        # Running from source: this file is at src/utils/resource_path.py,
        # so the project root is two directories up.
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


BASE_PATH: str = get_base_path()


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
