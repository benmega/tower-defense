import pygame
<<<<<<< HEAD
import os
import sys

<<<<<<< HEAD
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller bundle."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
=======
def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
>>>>>>> claude/unruffled-ramanujan-1882ca
    return os.path.join(base_path, relative_path)
=======
from src.utils.resource_path import resource_path

>>>>>>> claude/laughing-ardinghelli-b72776

def load_scaled_image(path, size):
    if not path or not size:
        return None
<<<<<<< HEAD
<<<<<<< HEAD

    try:
        full_path = resource_path(path)
=======

    full_path = get_asset_path(path) if not os.path.isabs(path) else path

    try:
>>>>>>> claude/unruffled-ramanujan-1882ca
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {full_path}: {e}")
=======
    abs_path = resource_path(path)
    try:
        image = pygame.image.load(abs_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {abs_path}: {e}")
>>>>>>> claude/laughing-ardinghelli-b72776
        return None
