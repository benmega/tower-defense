# game_board.py
import pygame
from utils.helpers import load_scaled_image

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

    def update(self):
        """
        Update the game board state, including moving enemies and tower attacks.
        """
        # Update enemies
        for enemy in self.enemies:
            enemy.move()

        for tower in self.towers:
            tower.update(self.enemies)

        # Implement logic to let towers attack enemies
        pass

    # Additional methods can be added for board functionality

    def draw_background(self, screen):
        grass_width, grass_height = self.grass_image.get_size()
        for x in range(0, screen.get_width(), grass_width):
            for y in range(0, screen.get_height(), grass_height):
                screen.blit(self.grass_image, (x, y))

    def update_board(self):
        # Update enemies
        for enemy in self.enemies:
            enemy.move()
            # Check for other conditions like enemy reaching the end or dying

        # Update towers
        for tower in self.towers:
            tower.update(self.enemies,[]) # TODO Fix this

        # Additional update logic (e.g., handling projectiles) goes here

    def draw_board(self, screen):
        # Draw the background
        self.draw_background(screen)

        # Draw towers
        for tower in self.towers:
            tower_image = load_scaled_image(tower.image_path, (32, 32))  # Assuming each tower has an image_path attribute
            if tower_image:
                screen.blit(tower_image, (tower.x, tower.y))

        # Draw enemies
        for enemy in self.enemies:
            enemy_image = load_scaled_image(enemy.image_path, (32, 32))
            if enemy_image:
                print(f"Drawing enemy at {enemy.x}, {enemy.y}")
                screen.blit(enemy_image, (enemy.x, enemy.y))
            else:
                print(f"Failed to load image at {enemy.image_path}")

