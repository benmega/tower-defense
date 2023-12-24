from src.board.game_board import GameBoard
from src.entities.enemies.basic_enemy import BasicEnemy
from src.entities.towers.tower import Tower
import pygame
from src.game.level import Level
from src.entities.enemies.enemy_wave import EnemyWave
from src.managers.collision_manager import CollisionManager

from src.managers.tower_manager import TowerManager
from src.utils.helpers import load_scaled_image


# Assume load_scaled_image and other necessary functions are defined elsewhere


def load_levels():
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
        [EnemyWave(BasicEnemy, 5, 1, paths[0]), EnemyWave(BasicEnemy, 2, 2, paths[0])],  # Level 1
        [EnemyWave(BasicEnemy, 1, 5, paths[1]), EnemyWave(BasicEnemy, 1, 10, paths[1])],  # Level 2
        # ... more enemy waves for other levels ...
    ]

    # Create Level objects for each level
    for i in range(10):
        path = paths[i % len(paths)]  # Example to reuse paths
        enemy_wave_list = enemy_wave_lists[i % len(enemy_wave_lists)]  # Example to reuse enemy wave lists
        # print(f"Creating level {i + 1} with enemy waves: {enemy_wave_list}")
        levels.append(Level(enemy_wave_list=enemy_wave_list, path=path, level_number=i + 1))

    return levels


class Game:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (0, 0, 0)
    FPS = 60
    TILE_SIZE = (32, 32)
    ENEMY_IMAGE_PATH = 'assets/images/enemies/enemy.png'
    TOWER_IMAGE_PATH = 'assets/images/tower.png'
    PROJECTILE_IMAGE_PATH = 'assets/images/projectile.png'

    def __init__(self):
        self.is_build_mode = False
        self.tower_image = None
        self.projectile_image = None
        self.enemy_image = None
        self.current_wave = None
        self.current_level = None
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.board = GameBoard(10, 10, grass_image_path='assets/images/grass.png')  # Update the parameters as necessary
        #self.enemies = []  # List of enemies
        #self.towers = []  # List of towers
        self.active_projectiles = []  # List of active projectiles
        self.levels = load_levels()
        self.current_level_index = 0
        self.tower_manager = TowerManager()
        self.is_running = False
        self.initialize_game()  # Setup for game start
        self.collision_manager = CollisionManager()

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

    def draw(self):
        # Clear the screen with the background color
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw the game board with all its components (background, enemies, towers)
        self.board.draw_board(self.screen, self.active_projectiles)

        # Here, you can add additional drawing logic specific to the Game class
        # For example, drawing the game UI, scores, health bars, etc.
        self.draw_ui()

        # Update the display
        pygame.display.flip()

    def draw_ui(self):
        #  TODO    Draw UI elements here (e.g., score, health bar, etc.)
        pass


    def remove_enemy(self, enemy):
        # Encapsulate any additional logic needed when an enemy is removed
        self.board.enemies.remove(enemy)
        # Additional logic like updating score or triggering effects can be added here

    def spawn_new_enemies(self): #TODO move to gameboard
        current_time = pygame.time.get_ticks()  # Get the current time
        if self.current_wave:
            new_enemy = self.current_wave.update(current_time)
            if new_enemy:
                self.board.enemies.append(new_enemy)  # Add the new enemy to the list
                print(f"Added new enemy. Total enemies: {len(self.board.enemies)}")

    def check_game_over(self):
        # Check if the game should end (e.g., player health reaches 0)
        pass

    def add_enemy(self, enemy):
        print(f"Adding enemy at position: {enemy.x}, {enemy.y}")
        self.board.add_enemy(enemy)
        self.board.enemies.append(enemy)

    def add_tower(self, tower):
        self.towers.append(tower)
        self.board.add_tower(tower)

    def start_level(self, level_index):
        self.current_level = self.levels[level_index]
        self.current_wave = self.current_level.get_next_wave()  # Store the current wave object
        self.board.enemies = []  # Reset the enemies list
        print(f"Starting level {level_index + 1}")



    def run(self):
        print("Game is running")
        self.is_running = True
        self.load_resources()  # Load images and other resources
        self.start_level(self.current_level_index)

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click is for building a tower
                if self.is_build_mode:
                    pos = pygame.mouse.get_pos()
                    self.handle_build(pos)

    def handle_build(self, pos):
        x, y = pos
        if self.is_valid_build_position(x, y):
            new_tower = Tower(x, y, ...)
            self.add_tower(new_tower)
            # Deduct resources, etc.

    def is_valid_build_position(self, x, y):
        # Logic to check if the position is valid for building
        # Example: Not on a path, not overlapping with other towers
        pass
    def update(self):
        print("Updating game state")
        # Main game update logic for each frame
        self.board.update_enemies()
        self.spawn_new_enemies() # TODO move to gameboard
        self.board.update_towers(self.active_projectiles)
        self.board.update_projectiles(self.active_projectiles)
        self.check_game_over()
        self.update_projectiles()
        self.check_completions()
        all_entities = self.board.enemies + self.active_projectiles  # Adjust as needed
        self.collision_manager.handle_collisions(all_entities)

    def update_projectiles(self):
        # Iterate through active projectiles and move them
        for projectile in self.active_projectiles[:]:
            projectile.move()
            if projectile.hit_target():
                projectile.target.take_damage(projectile.damage)
                if projectile.target.health <= 0:
                    projectile.target.die()
                    if projectile.target in self.board.enemies:
                        self.board.enemies.remove(projectile.target)
                self.active_projectiles.remove(projectile)
            elif projectile.out_of_bounds():
                # Remove projectiles that have left the game area
                self.active_projectiles.remove(projectile)

    def check_completions(self):
        # Check if any enemies have reached their goal or if any towers have been destroyed
        # This can also include checking if the player has won or lost the level
        pass

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.board.draw_board(self.screen,
                              self.active_projectiles)  # This method should draw enemies, towers, and projectiles

    def load_resources(self):
        # Load and store images for enemies, towers, and projectiles
        self.enemy_image = load_scaled_image(self.ENEMY_IMAGE_PATH, self.TILE_SIZE)
        self.tower_image = load_scaled_image(self.TOWER_IMAGE_PATH, self.TILE_SIZE)
        self.projectile_image = load_scaled_image(self.PROJECTILE_IMAGE_PATH, self.TILE_SIZE)
