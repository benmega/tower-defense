import pygame
from src.config.config import TOWER_IMAGE_PATH, ENEMY_IMAGE_PATH


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, key, path):
        """ Loads an image and stores it with the specified key. """
        image = pygame.image.load(path)
        self.images[key] = image
        return image

    def get_image(self, key):
        """ Retrieves an image by its key. """
        return self.images.get(key)

    def load_sound(self, key, path):
        """ Loads a sound and stores it with the specified key. """
        sound = pygame.mixer.Sound(path)
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        """ Retrieves a sound by its key. """
        return self.sounds.get(key)

    def load_font(self, key, path, size):
        """ Loads a font and stores it with the specified key. """
        font = pygame.font.Font(path, size)
        self.fonts[key] = font
        return font

    def get_font(self, key):
        """ Retrieves a font by its key. """
        return self.fonts.get(key)

    def preload_assets(self):
        """ Preloads necessary assets for the game. """
        # Example assets (You'll replace these with your actual asset paths)
        self.load_image('enemy', ENEMY_IMAGE_PATH)
        self.load_image('tower', TOWER_IMAGE_PATH)
        self.load_sound('explosion', 'assets/sounds/explosion.wav')
        self.load_font('main_font', 'assets/fonts/main_font.ttf', 24)

    # Additional methods for managing assets, such as clearing assets or handling animations, etc.
