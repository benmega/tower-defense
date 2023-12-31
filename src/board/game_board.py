# game_board.py

import pygame

from src.config.config import TILE_SIZE, GRASS_IMAGE_PATH, ENTRANCE_IMAGE_PATH, PATH_IMAGE_PATH, EXIT_IMAGE_PATH
from src.utils.helpers import load_scaled_image

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grass_image = load_scaled_image(GRASS_IMAGE_PATH, TILE_SIZE)
        self.path_image = load_scaled_image(PATH_IMAGE_PATH, TILE_SIZE)
        self.entrance_image = load_scaled_image(ENTRANCE_IMAGE_PATH, TILE_SIZE)
        self.exit_image = load_scaled_image(EXIT_IMAGE_PATH, TILE_SIZE)
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        #self.path_layout = self.create_path_layout(path)

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tower_at(self, x, y):
        return self.grid[y][x] if self.is_valid_position(x, y) else None

    def get_tile_image(self, x, y, path):
        path_layout = self.create_path_layout(path)
        tile_type = path_layout[y][x]
        if tile_type == 'G':
            return self.grass_image
        elif tile_type == 'P':
            return self.path_image
        elif tile_type == 'E':
            return self.entrance_image
        elif tile_type == 'X':
            return self.exit_image
        else:
            return self.grass_image  # Default to grass if unknown type

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

    def draw_board(self, screen: object, path: object) -> object:
        # Draw the background
        self.draw_background(screen, path)
        # Draw towers
        #tower_manager.draw_towers(screen,path)
        # Draw enemies
        #enemy_manager.draw_enemies(screen)
        # Draw projectiles
        #projectile_manager.draw_projectiles(screen)
        # Additional drawing logic as needed

    def draw_background(self, screen, path):
        for y in range(self.height):
            for x in range(self.width):
                image = self.get_tile_image(x, y, path)
                screen.blit(image, (x * 32, y * 32))

    def draw_towers(self, screen):
        for tower in self.towers:
            tower_image = load_scaled_image(tower.image_path, TILE_SIZE)
            if tower_image:
                screen.blit(tower_image, (tower.x, tower.y))



    def draw_projectiles(self, screen):
        for projectile in self.active_projectiles:
            projectile_image = load_scaled_image(projectile.image_path, (32, 32))
            if projectile_image:
                screen.blit(projectile_image, (projectile.x, projectile.y))

    # Additional methods for collision detection, score tracking, etc. can be added here
    def create_path_layout(self, path):

        # Convert path points to grid coordinates TODO set path to be gride based
        path = [(x // 32, y // 32) for x, y in path]

        # Initialize layout with grass
        layout = [['G' for _ in range(self.width)] for _ in range(self.height)]


        def fill_path(x1, y1, x2, y2):
            if x1 == x2:  # Vertical path
                startY, endY = sorted([y1, y2])
                for y in range(startY, endY + 1):
                    if 0 <= y < self.height:
                        layout[y][x1] = 'P'
            elif y1 == y2:  # Horizontal path
                startX, endX = sorted([x1, x2])
                for x in range(startX, endX + 1):
                    if 0 <= x < self.width:
                        layout[y1][x] = 'P'

        # Iterate through path points
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            fill_path(x1, y1, x2, y2)

        # Mark entrance and exit
        layout[path[0][1]][path[0][0]] = 'E'  # Entrance
        layout[path[-1][1]][path[-1][0]] = 'X'  # Exit

        return layout