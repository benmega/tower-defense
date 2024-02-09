import pygame


from src.utils.helpers import load_scaled_image
from src.config.config import ENEMY_IMAGE_PATH, TILE_SIZE, DEBUG, ENEMY_GOLD_VALUE, ENEMY_SCORE_VALUE, \
    ENEMY_DAMAGE_TO_PLAYER


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, speed, path, image_path=ENEMY_IMAGE_PATH):
        super().__init__()
        if not path or len(path) == 0:
            raise ValueError("Invalid path provided to Enemy")
        self.image = load_scaled_image(image_path, TILE_SIZE).convert_alpha()
        #self.image = load_scaled_image(image_path, TILE_SIZE)
        self.rect = self.image.get_rect(topleft=path[0])
        self.health = health
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.active = True
        self.state = 'moving'  # Possible states: 'moving', 'attacking', 'idle', 'finished'
        self.reached_goal = False
        self.score_value = ENEMY_SCORE_VALUE
        self.gold_value = ENEMY_GOLD_VALUE
        self.damage_to_player = ENEMY_DAMAGE_TO_PLAYER

    def move(self):

        if self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            self.move_towards(next_x, next_y)
        else: #path complete
            # print('idle')
            self.state = 'finished'
            self.reached_goal = True

    def move_towards(self, next_x, next_y):
        if DEBUG:
            print(f'enemy moving towards {next_x}, {next_y}')
        dir_x, dir_y = next_x - self.rect.x, next_y - self.rect.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance != 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed

        if abs(self.rect.x - next_x) <= self.speed and abs(self.rect.y - next_y) <= self.speed:
            self.rect.x, self.rect.y = next_x, next_y
            if self.path_index < len(self.path):
                self.path_index += 1

    def is_invisible(self):
        if self.state == 'dead':
            return  True
        if self.state == 'idle':
            return  True
    def take_damage(self, amount):
        if not self.is_invisible():
            self.health -= amount
            if self.health <= 0:
                self.die()

    def die(self):
        self.state = 'dead'
        self.active = False

    def update(self):
        if self.state == 'dead' or not self.active:
            return  # Skip updating if the enemy is dead or inactive
        self.move()

    def on_collision(self, other_entity):
        from src.entities.projectiles.projectile import Projectile
        if isinstance(other_entity, Projectile):
            self.health -= other_entity.damage
            if self.health <= 0:
                self.die()
