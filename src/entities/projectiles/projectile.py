import pygame

from src.entities.enemies.enemy import Enemy
from src.entities.entity import Entity
from src.config.config import PROJECTILE_IMAGE_PATH, DEBUG, SCREEN_HEIGHT, SCREEN_WIDTH


class Projectile(Entity):
    def __init__(self, x, y, target, speed=0, damage=0, image_path=PROJECTILE_IMAGE_PATH):
        super().__init__(x, y, image_path)
        # self.x = x
        # self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'  # Only one state for active projectiles
        self.image_path = image_path

    def update(self):
        self.move()

    def move(self):
        if DEBUG:
            print('projectile moving')
        dir_x, dir_y = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance > 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed

        if self.reached_target():
            self.hit_target()  # Apply damage if needed
            self.state = 'expired'  # Set state to expired regardless of hit
        elif self.out_of_bounds():
            self.state = 'expired'  # Set state to expired regardless of hit
    def reached_target(self):
        return ((self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2) ** 0.5 <= self.speed

    def out_of_bounds(self):
        return not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT)

    def hit_target(self):
        # Apply damage and return True if a hit is detected
        if self.reached_target():
            self.target.take_damage(self.damage)
            return True
        return False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            # Optional: Draw a placeholder if the image failed to load
            pygame.draw.circle(screen, (255, 0, 0), (int(self.rect.x), int(self.rect.y)), 5)


    def on_collision(self, other_entity):
        if isinstance(other_entity, Enemy):
            other_entity.take_damage(self.damage)
            self.state = 'expired'  # Mark projectile for removal