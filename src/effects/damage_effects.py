import pygame

import src.utils.constants as C


class AoeDamageEffect(pygame.sprite.Sprite):
    def __init__(self, center, radius):
        super().__init__()
        self.image = self.create_effect_image(radius)
        self.rect = self.image.get_rect(center=center)
        self.lifetime = C.AOE_EFFECT_LIFETIME_FRAMES

    def create_effect_image(self, radius):
        # Create a surface with a transparent background
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        # Draw the AOE effect (e.g., a simple circle or more complex animation)
        pygame.draw.circle(surface, C.RGB_AOE_EFFECT, (radius, radius), radius)
        return surface

    def update(self):
        # Reduce the lifetime each frame, and kill the effect when it reaches 0
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
