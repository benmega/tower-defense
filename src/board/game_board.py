# game_board.py

import pygame

from src.config import TILE_SIZE
from src.utils.helpers import load_scaled_image

class GameBoard:
    def __init__(self, width, height, grass_image_path):
        #self.enemies = []
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        #self.towers = []
        self.grass_image = pygame.transform.scale(pygame.image.load(grass_image_path), (32, 32))
        self.active_projectiles = []  # Moved from Game to GameBoard for encapsulation

    # def add_tower(self, tower):
    #     if self.is_valid_position(tower.x, tower.y):
    #         self.grid[tower.y][tower.x] = tower
    #         self.towers.append(tower)
    #     else:
    #         raise ValueError("Invalid position for tower")

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tower_at(self, x, y):
        return self.grid[y][x] if self.is_valid_position(x, y) else None

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def update_board(self):
        self.update_enemies()
        self.update_towers()
        self.update_projectiles()

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.reached_goal or enemy.health <= 0 or enemy.state == 'dead':
                self.enemies.remove(enemy)

    def update_towers(self):
        for tower in self.towers:
            tower.update(self.enemies, self.active_projectiles)

    def update_projectiles(self):
        for projectile in self.active_projectiles[:]:
            projectile.move()
            if projectile.state == 'expired':
                self.active_projectiles.remove(projectile)

    def draw_board(self, screen: object, enemy_manager: object, tower_manager: object, projectile_manager: object) -> object:
        # Draw the background
        self.draw_background(screen)
        # Draw towers
        tower_manager.draw_towers(screen)
        # Draw enemies
        enemy_manager.draw_enemies(screen)
        # Draw projectiles
        projectile_manager.draw_projectiles(screen)
        # Additional drawing logic as needed

    def draw_background(self, screen):
        grass_width, grass_height = self.grass_image.get_size()
        for x in range(0, screen.get_width(), grass_width):
            for y in range(0, screen.get_height(), grass_height):
                screen.blit(self.grass_image, (x, y))

    def draw_towers(self, screen):
        for tower in self.towers:
            tower_image = load_scaled_image(tower.image_path, TILE_SIZE)
            if tower_image:
                screen.blit(tower_image, (tower.x, tower.y))

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy_image = load_scaled_image(enemy.image_path, TILE_SIZE)
            if enemy_image:
                screen.blit(enemy_image, (enemy.x, enemy.y))

    def draw_projectiles(self, screen):
        for projectile in self.active_projectiles:
            projectile_image = load_scaled_image(projectile.image_path, (32, 32))
            if projectile_image:
                screen.blit(projectile_image, (projectile.x, projectile.y))

    # Additional methods for collision detection, score tracking, etc. can be added here
