import pygame

from src.entities.entity import Entity
from src.utils.helpers import load_scaled_image


class Enemy(Entity):
    def __init__(self, health, speed, path, image_path='assets/images/enemies/enemy.png'):
        super().__init__(path[0][0], path[0][1], image_path)
        self.health = health
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.image_path = image_path
        self.state = 'moving'  # Possible states: 'moving', 'attacking', 'idle'
        self.reached_goal = False
        self.image = load_scaled_image(image_path, (32, 32)) #TODO make game board size adjustable
        self.width, self.height = self.image.get_size()
    def move(self):
        if self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            self.move_towards(next_x, next_y)
        else:
            self.state = 'idle'
            # Additional logic when path is complete

    def move_towards(self, next_x, next_y):
        dir_x, dir_y = next_x - self.x, next_y - self.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance != 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        if abs(self.x - next_x) <= self.speed and abs(self.y - next_y) <= self.speed:
            self.x, self.y = next_x, next_y
            if self.path_index < len(self.path) - 1:
                self.path_index += 1

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)
        if self.health <= 0:
            self.die()

    def die(self):
        self.state = 'dead'
        # Logic for enemy death, like updating score or game state

    # Additional methods for collision detection and other behaviors can be added here
    def on_collision(self, other_entity):
        # Implement collision logic specific to Enemy
        pass