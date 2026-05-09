import pygame

from src.config.config import ENEMY_IMAGE_PATH
from src.utils.resource_path import resource_path


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, key, path):
        """ Loads an image and stores it with the specified key. """
        image = pygame.image.load(resource_path(path))
        self.images[key] = image
        return image

    def get_image(self, key):
        """ Retrieves an image by its key. """
        return self.images.get(key)

    def load_sound(self, key, path):
        """ Loads a sound and stores it with the specified key. """
        sound = pygame.mixer.Sound(resource_path(path))
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        """ Retrieves a sound by its key. """
        return self.sounds.get(key)

    def load_font(self, key, path, size):
        """ Loads a font and stores it with the specified key. """
        font = pygame.font.Font(resource_path(path), size)
        self.fonts[key] = font
        return font

    def get_font(self, key):
        """ Retrieves a font by its key. """
        return self.fonts.get(key)

    def preload_assets(self):
        """ Preloads necessary assets for the game. """
        self.load_image('enemy', ENEMY_IMAGE_PATH)
        self.load_image('tower', 'assets/images/towers/basic_tower.png')
        self.load_sound('explosion', 'assets/sounds/explosion.wav')
        self.load_font('main_font', 'assets/fonts/main_font.ttf', 24)
