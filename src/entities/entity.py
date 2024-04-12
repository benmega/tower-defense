from typing import Optional

import pygame
from pygame import Surface

from src.utils.helpers import load_scaled_image
from src.config.config import TILE_SIZE

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size=TILE_SIZE):
        super().__init__()
        self.size = size
        self.image = load_scaled_image(image_path, self.size).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        # self.grid_x = grid_x
        # self.grid_y = grid_y
        self.active = True
        self.width, self.height = self.image.get_size()


    def update(self):
        # Update logic for the entity, to be overridden by subclasses
        pass


    def draw(self, screen):
        if self.active and self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pass

    def on_collision(self, other_entity):
        # Collision handling logic, to be overridden by subclasses
        pass

    def deactivate(self):
        # Deactivate the entity (e.g., when it is destroyed)
        self.active = False

# Additional methods as needed
