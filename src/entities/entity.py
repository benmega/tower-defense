import pygame

from src.config import TILE_SIZE
from src.utils.helpers import load_scaled_image


class Entity:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = load_scaled_image(image_path, TILE_SIZE)
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Other common methods like movement or collision detection can go here
