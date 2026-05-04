import pygame
import os
import sys

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

def load_scaled_image(path, size):
    if not path or not size:
        return None

    full_path = get_asset_path(path) if not os.path.isabs(path) else path

    try:
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {full_path}: {e}")
        return None


