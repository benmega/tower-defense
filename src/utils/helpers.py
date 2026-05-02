import pygame
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller bundle."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

def load_scaled_image(path, size):
    if not path or not size:
        return None

    try:
        full_path = resource_path(path)
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None


