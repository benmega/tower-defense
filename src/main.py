# Constants
'''
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (32, 32)
ENEMY_IMAGE_PATH = '../assets/images/enemies/enemy.png'
TOWER_IMAGE_PATH = '../assets/images/towers/tower.png'
PROJECTILE_IMAGE_PATH = '../assets/images/projectiles/projectile.png'
'''

import os
import sys


def _set_working_directory():
    """
    When running as a PyInstaller frozen executable the process CWD is
    wherever the user launched the exe from, which is rarely the bundle
    folder.  All asset paths in config.py are relative to the project root,
    so we must set CWD to the directory that contains the exe (one-folder
    build) or to sys._MEIPASS (onefile build) before any game code runs.
    """
    if getattr(sys, 'frozen', False):
        # One-folder build: data lives next to the exe.
        # Onefile build: data is extracted to sys._MEIPASS.
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        os.chdir(base)


_set_working_directory()

from src.game.game import Game

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()