import pygame
<<<<<<< HEAD
import os
import sys
from src.config.config import TOWER_IMAGE_PATH, ENEMY_IMAGE_PATH
=======
from src.config.config import ENEMY_IMAGE_PATH
>>>>>>> claude/laughing-ardinghelli-b72776

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, key, path):
        """ Loads an image and stores it with the specified key. """
        full_path = get_asset_path(path) if not os.path.isabs(path) else path
        image = pygame.image.load(full_path)
        self.images[key] = image
        return image

    def get_image(self, key):
        """ Retrieves an image by its key. """
        return self.images.get(key)

    def load_sound(self, key, path):
        """ Loads a sound and stores it with the specified key. """
        full_path = get_asset_path(path) if not os.path.isabs(path) else path
        sound = pygame.mixer.Sound(full_path)
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        """ Retrieves a sound by its key. """
        return self.sounds.get(key)

    def load_font(self, key, path, size):
        """ Loads a font and stores it with the specified key. """
        full_path = get_asset_path(path) if not os.path.isabs(path) else path
        font = pygame.font.Font(full_path, size)
        self.fonts[key] = font
        return font

    def get_font(self, key):
        """ Retrieves a font by its key. """
        return self.fonts.get(key)

    def preload_assets(self):
        """ Preloads necessary assets for the game. """
        # Example assets (You'll replace these with your actual asset paths)
        self.load_image('enemy', ENEMY_IMAGE_PATH)
        self.load_image('tower', 'assets/images/towers/basic_tower.png')
        self.load_sound('explosion', 'assets/sounds/explosion.wav')
        self.load_font('main_font', 'assets/fonts/main_font.ttf', 24)

    # Additional methods for managing assets, such as clearing assets or handling animations, etc.
