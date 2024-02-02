import pygame_gui

from src.board.game_board import GameBoard
from src.entities.Player import Player
# from src.entities.enemies.basic_enemy import BasicEnemy
from src.entities.towers.tower import Tower
import pygame
# from src.game.level import Level
# from src.entities.enemies.enemy_wave import EnemyWave
from src.managers.collision_manager import CollisionManager
from src.managers.enemy_manager import EnemyManager
from src.managers.event_manager import EventManager
from src.managers.level_manager import LevelManager
from src.managers.projectile_manager import ProjectileManager
from src.managers.tower_manager import TowerManager
import src.config.config as configuration
from src.managers.ui_manager import UIManager
from src.utils.helpers import load_scaled_image
# import json


class Game:

    def __init__(self):
        self.score_label = None
        self.is_build_mode = False
        pygame.init()
        self.screen = pygame.display.set_mode((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.board = GameBoard(configuration.GAME_BOARD_WIDTH, configuration.GAME_BOARD_HEIGHT)
        self.level_manager = LevelManager()
        self.tower_manager = TowerManager()
        self.enemy_manager = EnemyManager(self.enemy_defeated_callback)
        self.projectile_manager = ProjectileManager()
        self.collision_manager = CollisionManager()
        self.UI_manager = UIManager(configuration.DEFAULT_GRID_SIZE)
        self.event_manager = EventManager()
        self.is_running = False
        self.checkCounter = 0
        self.player = Player()
        self.initialize_game()
    def initialize_game(self):
        self.load_resources()
        gridWidth = configuration.DEFAULT_GRID_SIZE[0]
        gridHeight = configuration.DEFAULT_GRID_SIZE[1]
        self.tower_manager.add_tower(Tower(gridWidth*2,gridHeight*7)) # Example of creating and adding a tower
        self.tower_manager.add_tower(Tower(gridWidth*5,gridHeight*7))  # Example of creating and adding a tower
        self.tower_manager.add_tower(Tower(gridWidth * 2, gridHeight * 4))  # Example of creating and adding a tower
        self.tower_manager.add_tower(Tower(gridWidth * 5, gridHeight * 4))  # Example of creating and adding a tower
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                              text='Say Hello',
                                              manager=self.UI_manager)
        # Initialize UI elements
        self.gold_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 10), (100, 50)),
                                                      text=f"Gold: {self.player.gold}",
                                                      manager=self.UI_manager)
        self.health_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 60), (100, 50)),
                                                        text=f"Health: {self.player.health}",
                                                        manager=self.UI_manager)
        self.score_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 110), (100, 50)),
                                                       text=f"Score: {self.player.score}",
                                                       manager=self.UI_manager)
        self.enemy_count_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 160), (150, 50)),
                                                             text="Enemies: 0",
                                                             manager=self.UI_manager)
        # Add other UI elements as needed

    def load_resources(self):
        # Load and store images for enemies, towers, and projectiles
        self.enemy_image = load_scaled_image(configuration.ENEMY_IMAGE_PATH, configuration.TILE_SIZE)
        self.tower_image = load_scaled_image(configuration.TOWER_IMAGE_PATH, configuration.TILE_SIZE)
        self.projectile_image = load_scaled_image(configuration.PROJECTILE_IMAGE_PATH, configuration.TILE_SIZE)


    def draw(self):
        self.screen.fill(configuration.BACKGROUND_COLOR) # Clear the screen with the background color
        self.board.draw_board(self.screen, self.level_manager.get_current_level().path) # Draw the game board
        self.tower_manager.draw_towers(self.screen)
        self.enemy_manager.draw(self.screen)
        self.projectile_manager.draw_projectiles(self.screen)
        self.UI_manager.draw_ui(self.screen)  # Draw the game UI
        pygame.display.flip() # Update the display


    def run(self):
        if configuration.DEBUG:
            print("Game is running")
        self.is_running = True
        self.load_resources()  # Load images and other resources
        self.level_manager.start_next_level()
        self.enemy_manager.reset()

        while self.is_running:
            self.event_manager.process_events(self)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(configuration.FPS)

        pygame.quit()


    # def handle_build(self, pos):
    #     x, y = pos
    #     new_tower = Tower(x, y, ...)
    #     if self.is_valid_build_position(x, y) and self.player.gold >= new_tower.build_cost:
    #         self.tower_manager.add_tower(new_tower)
    #         self.player.gold -= new_tower.build_cost
    #
    # def is_valid_build_position(self, x, y):
    #     # Logic to check if the position is valid for building
    #     # Example: Not on a path, not overlapping with other towers
    #     pass
    def update(self):
        if configuration.DEBUG:
            print("Updating game state")
        # Main game update logic for each frame
        new_enemies = self.level_manager.update_levels()
        if not new_enemies and len(self.enemy_manager.entities) == 0:
            if self.level_manager.check_level_complete():
                if self.level_manager.next_level():
                    self.level_manager.start_next_level()
                else: # no new enemies, no enemies to manage, and no next level
                    print("Congrats! You win!")
                    self.is_running = False
        for enemy in new_enemies:
            self.enemy_manager.add_enemy(enemy)
        self.enemy_manager.update()
        self.tower_manager.update(self.enemy_manager.get_enemies(), self.projectile_manager)
        self.projectile_manager.update_entities()
        self.score_label.set_text(f"Score: {self.player.score}")
        self.UI_manager.update(configuration.FPS/1000)
        self.check_game_over()
        self.collision_manager.handle_group_collisions(
            self.enemy_manager.entities, self.projectile_manager.projectiles
        )

    def check_game_over(self):
        # Check if the game should end (e.g., player health reaches 0)
        if self.player.health <= 0:
            return True
        if self.level_manager.get_current_level() == len(self.level_manager.levels):
            if self.level_manager.check_level_complete():
                print("Finished")
                return True
        return False

    def enemy_defeated_callback(self, enemy):
        self.player.score += enemy.gold_value  # Assuming `score_value` attribute exists
        self.player.gold += enemy.gold_value  # Assuming `gold_value` attribute exists
        self.UI_manager.update_score(self.player.score)
        self.UI_manager.update_resources(self.player.gold)