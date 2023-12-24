# game_board.py
import pygame
from src.utils.helpers import load_scaled_image

class GameBoard:
    def __init__(self, width, height,grass_image_path):
        self.enemies = []
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.towers = []
        self.grass_image = pygame.transform.scale(pygame.image.load(grass_image_path), (32, 32))
    def add_tower(self, tower):
        """
        Add a tower to the game board.
        """
        if self.is_valid_position(tower.x, tower.y):
            self.grid[tower.y][tower.x] = tower
            self.towers.append(tower)
        else:
            raise ValueError("Invalid position for tower")

    def is_valid_position(self, x, y):
        """
        Check if a position is within the bounds of the game board.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tower_at(self, x, y):
        """
        Return the tower at the given position, if any.
        """
        return self.grid[y][x] if self.is_valid_position(x, y) else None

    def add_enemy(self, enemy):
        """
        Add an enemy to the game board.
        """
        self.enemies.append(enemy)

    def update(self, active_projectiles):
        self.update_enemies()
        self.update_towers(active_projectiles)
        self.update_projectiles(active_projectiles)

    def update_enemies(self):
        for enemy in self.enemies[:]:  # Iterate over a copy of the list
            enemy.move()
            if enemy.reached_goal or enemy.health <= 0:
                self.enemies.remove(enemy)
            if enemy.state == 'dead' and enemy in self.enemies:
                self.enemies.remove(enemy)
    def update_towers(self, active_projectiles):
        for tower in self.towers:
            tower.update(self.enemies, active_projectiles)

    def update_projectiles(self, active_projectiles):
        for projectile in active_projectiles[:]:  # Iterate over a copy of the list
            projectile.move()
            if projectile.state == 'expired':
                active_projectiles.remove(projectile)

    def draw_background(self, screen):
        grass_width, grass_height = self.grass_image.get_size()
        for x in range(0, screen.get_width(), grass_width):
            for y in range(0, screen.get_height(), grass_height):
                screen.blit(self.grass_image, (x, y))

    def update_board(self,active):
        # Update enemies
        for enemy in self.enemies:
            enemy.move()
            # Check for other conditions like enemy reaching the end or dying

        # Update towers
        for tower in self.towers:
            tower.update(self.enemies,[]) # TODO Fix this

        # Additional update logic (e.g., handling projectiles) goes here


    def draw_board(self, screen, active_projectiles):
        self.draw_background(screen)
        self.draw_towers(screen)
        self.draw_enemies(screen)
        self.draw_projectiles(screen, active_projectiles)

    def draw_towers(self, screen):
        for tower in self.towers:
            tower_image = load_scaled_image(tower.image_path, (32, 32))
            if tower_image:
                screen.blit(tower_image, (tower.x, tower.y))

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy_image = load_scaled_image(enemy.image_path, (32, 32))
            if enemy_image:
                screen.blit(enemy_image, (enemy.x, enemy.y))


    def draw_projectiles(self, screen, active_projectiles):
        for projectile in active_projectiles:
            projectile_image = load_scaled_image(projectile.image_path, (32, 32))
            if projectile_image:
                screen.blit(projectile_image, (projectile.x, projectile.y))

    # TODO: Implement additional methods like collision detection, score tracking, etc.