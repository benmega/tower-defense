import pygame_gui

from src.board.game_board import GameBoard
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
from src.utils.helpers import load_scaled_image
# import json


class Game:

    def __init__(self):
        self.is_build_mode = False
        pygame.init()
        self.screen = pygame.display.set_mode((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.board = GameBoard(configuration.GAME_BOARD_WIDTH, configuration.GAME_BOARD_HEIGHT)
        self.level_manager = LevelManager()
        self.tower_manager = TowerManager()
        self.enemy_manager = EnemyManager()
        self.projectile_manager = ProjectileManager()
        self.collision_manager = CollisionManager()
        self.UI_manager = pygame_gui.UIManager(configuration.DEFAULT_GRID_SIZE)
        self.event_manager = EventManager()
        self.is_running = False
        self.initialize_game()
        self.checkCounter = 0
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

    def load_resources(self):
        # Load and store images for enemies, towers, and projectiles
        self.enemy_image = load_scaled_image(configuration.ENEMY_IMAGE_PATH, configuration.TILE_SIZE)
        self.tower_image = load_scaled_image(configuration.TOWER_IMAGE_PATH, configuration.TILE_SIZE)
        self.projectile_image = load_scaled_image(configuration.PROJECTILE_IMAGE_PATH, configuration.TILE_SIZE)


    def draw(self):
        # Clear the screen with the background color
        self.screen.fill(configuration.BACKGROUND_COLOR)

        # Draw the game board
        self.board.draw_board(self.screen, self.level_manager.get_current_level().path)
        # Draw towers, enemies, and projectiles
        self.tower_manager.draw_towers(self.screen)
        self.enemy_manager.draw(self.screen)
        self.projectile_manager.draw_projectiles(self.screen)

        # Draw the game UI
        self.draw_ui()

        # Update the display
        pygame.display.flip()

    def draw_ui(self):
        #  TODO    Draw UI elements here (e.g., score, health bar, etc.)
        pass



    def check_game_over(self):
        # Check if the game should end (e.g., player health reaches 0)
        pass

    def run(self):
        print("Game is running")
        #time_delta = clock.tick(60) / 1000.0
        self.is_running = True
        self.load_resources()  # Load images and other resources
        self.level_manager.start_next_level()
        self.enemy_manager.reset()

        while self.is_running:
            self.event_manager.process_events(self)
            # self.handle_events() #TODO move to event manager
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(configuration.FPS)

        pygame.quit()

    # def handle_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.is_running = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             # Check if the click is for building a tower
    #             self.UI_manager.process_events(event)
    #             if self.is_build_mode and self.is_build_mode:
    #                 pos = pygame.mouse.get_pos()
    #                 self.handle_build(pos)

    def handle_build(self, pos):
        x, y = pos
        if self.is_valid_build_position(x, y):
            new_tower = Tower(x, y, ...)
            self.tower_manager.add_tower(new_tower)
            # Deduct resources, etc.

    def is_valid_build_position(self, x, y):
        # Logic to check if the position is valid for building
        # Example: Not on a path, not overlapping with other towers
        pass
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
        # self.level_manager.update_levels()
        self.UI_manager.update(configuration.FPS/1000)
        self.check_game_over()
        self.check_completions()
        #yall_entities = self.enemy_manager.enemies + self.projectile_manager.projectiles
        self.collision_manager.handle_group_collisions(
            self.enemy_manager.entities, self.projectile_manager.projectiles
        )

    def check_completions(self):
        # Check if any enemies have reached their goal or if any towers have been destroyed
        # This can also include checking if the player has won or lost the level
        if self.level_manager.get_current_level() == len(self.level_manager.levels):
            print("Finished")
        pass
