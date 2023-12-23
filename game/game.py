import pygame

from board import game_board
from board.game_board import GameBoard
from entities.enemies.basic_enemy import BasicEnemy
from entities.towers.tower import Tower
from entities.enemies.enemy import Enemy
import pygame
from game.level import Level
from entities.enemies.enemy_wave import EnemyWave


from game.tower_manager import TowerManager
from utils.helpers import load_scaled_image


# Assume load_scaled_image and other necessary functions are defined elsewhere


class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (0, 0, 0)
    FPS = 60
    TILE_SIZE = (32, 32)
    ENEMY_IMAGE_PATH = 'assets/images/enemies/enemy.png'
    TOWER_IMAGE_PATH = 'assets/images/tower.png'
    PROJECTILE_IMAGE_PATH = 'assets/images/projectile.png'

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.board = GameBoard(10, 10, grass_image_path='assets/images/grass.png')  # Update the parameters as necessary
        self.enemies = []  # List of enemies
        self.towers = []   # List of towers
        self.active_projectiles = []  # List of active projectiles
        self.levels = self.load_levels()
        self.current_level_index = 0
        self.tower_manager = TowerManager()
        self.is_running = False
        self.initialize_game()  # Setup for game start

    def initialize_game(self):
        # Initialize game elements here, like placing towers and spawning enemies
        # Load images, set up the initial game state, etc.
        # Example of creating and adding a tower
        tower = Tower(x=5, y=5, attack_range=100, damage=10, attack_speed=1)
        try:
            self.board.add_tower(tower)
        except ValueError as e:
            print(f"Error adding tower: {e}")

    def start(self):
        self.is_running = True
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        # Main game update logic for each frame
        self.update_enemies()
        self.update_towers()
        # Update projectiles
        for projectile in self.active_projectiles:
            projectile.move()
            if projectile.hit_target():
                self.active_projectiles.remove(projectile)
        self.check_game_over()

    def draw(self):
        # Clear the screen with the background color
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw the game board with all its components (background, enemies, towers)
        self.board.draw_board(self.screen)

        # Here, you can add additional drawing logic specific to the Game class
        # For example, drawing the game UI, scores, health bars, etc.
        self.draw_ui()

        # Update the display
        pygame.display.flip()

    def draw_ui(self):
    #  TODO    Draw UI elements here (e.g., score, health bar, etc.)
         pass

    def update_enemies(self):
        # Update each enemy's position, check for reaching the end, etc.
        for enemy in self.enemies:
            enemy.move()
            if enemy.health <= 0:
                self.enemies.remove(enemy)

    def update_towers(self):
        # Update towers, let them attack enemies
        for tower in self.towers:
            tower.update(self.enemies, self.active_projectiles)

    def check_game_over(self):
        # Check if the game should end (e.g., player health reaches 0)
        pass

    def add_enemy(self, enemy):
        print(f"Adding enemy at position: {enemy.x}, {enemy.y}")
        self.board.add_enemy(enemy)
        self.enemies.append(enemy)

    def add_tower(self, tower):
        self.towers.append(tower)
        self.board.add_tower(tower)

    def load_levels(self):
        # Define or load levels here
        levels = []

        # Example paths and enemy wave lists for each level
        # Replace these with your actual path and enemy configurations
        paths = [
            [(0, 0), (100, 0), (100, 100)],
            [(0, 0), (200, 0), (200, 200)],
            # ... more paths for other levels ...
        ]
        enemy_wave_lists = [
            [EnemyWave(BasicEnemy, 10,1,paths[0]), EnemyWave(BasicEnemy, 5,2,paths[0])],  # Level 1
            [EnemyWave(BasicEnemy, 15,5,paths[1]), EnemyWave(BasicEnemy, 10,10,paths[1])],  # Level 2
            # ... more enemy waves for other levels ...
        ]

        # Create Level objects for each level
        for i in range(10):
            path = paths[i % len(paths)]  # Example to reuse paths
            enemy_wave_list = enemy_wave_lists[i % len(enemy_wave_lists)]  # Example to reuse enemy wave lists
            #print(f"Creating level {i + 1} with enemy waves: {enemy_wave_list}")
            levels.append(Level(enemy_wave_list=enemy_wave_list, path=path, level_number=i + 1))

        return levels
    def start_level(self, level_index):
        self.current_level = self.levels[level_index]
        self.current_wave = self.current_level.get_next_wave()  # Store the current wave object
        self.enemies = []  # Reset the enemies list
        print(f"Starting level {level_index + 1}")

    def update(self):
        print("Updating game state")
        current_time = pygame.time.get_ticks()  # Get the current time

        # Spawn new enemies from the current wave
        if self.current_wave:
            new_enemy = self.current_wave.update(current_time)
            if new_enemy:
                self.enemies.append(new_enemy)  # Add the new enemy to the list
                self.board.add_enemy(new_enemy)
                print(f"Added new enemy. Total enemies: {len(self.enemies)}")

        # Update existing enemies
        for enemy in self.enemies:
            enemy.move()  # Or whatever your logic is for moving enemies


    def run(self):
        print("Game is running")
        self.is_running = True
        self.load_resources()  # Load images and other resources
        self.start_level(self.current_level_index)

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.update_game_state()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            print(f"Handling event: {event}")
            if event.type == pygame.QUIT:
                self.is_running = False

    def update_game_state(self):
        # Move this logic to a separate method for clarity
        self.board.update_board()  # This method should update enemies, towers, and handle projectiles

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.board.draw_board(self.screen)  # This method should draw enemies, towers, and projectiles

    def load_resources(self):
        # Load and store images for enemies, towers, and projectiles
        self.enemy_image = load_scaled_image(self.ENEMY_IMAGE_PATH, self.TILE_SIZE)
        self.tower_image = load_scaled_image(self.TOWER_IMAGE_PATH, self.TILE_SIZE)
        self.projectile_image = load_scaled_image(self.PROJECTILE_IMAGE_PATH, self.TILE_SIZE)



