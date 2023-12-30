import pygame

from src.entities.enemies.enemy import Enemy
from src.entities.entity import Entity
from src.config import PROJECTILE_IMAGE_PATH

class Projectile(Entity):
    def __init__(self, x, y, target, speed=0, damage=0, image_path=PROJECTILE_IMAGE_PATH):
        super().__init__(x, y, image_path)
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'  # Only one state for active projectiles
        self.image_path = image_path

    def move(self):
        dir_x, dir_y = self.target.x - self.x, self.target.y - self.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance > 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        if self.reached_target() or self.out_of_bounds():
            self.hit_target()  # Apply damage if needed
            self.state = 'expired'  # Set state to expired regardless of hit

    def reached_target(self):
        return ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2) ** 0.5 <= self.speed

    def out_of_bounds(self):
        return not (0 <= self.x <= 800 and 0 <= self.y <= 600)

    def hit_target(self):
        # Apply damage and return True if a hit is detected
        if self.reached_target():
            self.target.take_damage(self.damage)
            return True
        return False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Optional: Draw a placeholder if the image failed to load
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)


    def on_collision(self, other_entity):
        if isinstance(other_entity, Enemy):
            other_entity.take_damage(self.damage)
            self.state = 'expired'  # Mark projectile for removal