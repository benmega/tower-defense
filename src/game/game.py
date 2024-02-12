import pygame_gui

from src.board.game_board import GameBoard
from src.board.wave_panel import WavePanel
from src.entities.Player import Player
import pygame

from src.game.game_state import GameState
from src.managers.collision_manager import CollisionManager
from src.managers.enemy_manager import EnemyManager
from src.managers.event_manager import EventManager
from src.managers.level_manager import LevelManager
from src.managers.projectile_manager import ProjectileManager
from src.managers.tower_manager import TowerManager
import src.config.config as configuration
from src.screens.campain_map import CampaignMap
from src.screens.level_completion import LevelCompletionScreen
from src.screens.main_menu import MainMenu
from src.screens.options_screen import OptionsScreen
from src.board.tower_selection_panel import TowerSelectionPanel
import os



class Game:
    '''
    Core game class responsible for initializing the game, running the main loop, handling game state transitions (like starting, game over), and managing high-level game events.
    Potential TODOs: Implementing efficient game state management, optimizing the main game loop for performance, and handling transitions between different parts of the game smoothly.
    '''
    def __init__(self):
        self.score_label = None
        self.is_build_mode = False
        pygame.init()
        self.screen = pygame.display.set_mode([configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT], pygame.DOUBLEBUF)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.board = GameBoard(configuration.GAME_BOARD_WIDTH, configuration.GAME_BOARD_HEIGHT)
        self.level_manager = LevelManager()
        self.tower_manager = TowerManager()
        self.projectile_manager = ProjectileManager()
        self.collision_manager = CollisionManager()
        theme_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'theme.json')
        self.UI_manager = pygame_gui.UIManager((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), theme_path)
        self.event_manager = EventManager()
        self.is_running = False
        self.checkCounter = 0
        self.player = Player()
        self.enemy_manager = EnemyManager(self.level_manager, self.enemy_defeated_callback, self.player_take_damage_callback)
        self.current_state = GameState.MAIN_MENU
        self.main_menu = MainMenu(self.screen, self.UI_manager)
        self.options_screen = OptionsScreen(self.screen, self.UI_manager)
        self.campaign_map = CampaignMap(self.screen, self.UI_manager)
        self.level_completion_screen = LevelCompletionScreen(self)
        self.is_build_mode = True
        self.tower_selection_panel = TowerSelectionPanel(self.screen, self.tower_manager)
        self.wave_panel = WavePanel(self.UI_manager, self.level_manager, self.screen)

    def initialize_game(self):
        grid_width = configuration.DEFAULT_GRID_SIZE[0]
        grid_height = configuration.DEFAULT_GRID_SIZE[1]

        # self.tower_manager.add_tower(grid_width*3, grid_height*7)  # Example of creating and adding a tower
        # self.tower_manager.add_tower(grid_width*8, grid_height*7)  # Example of creating and adding a tower
        # self.tower_manager.add_tower(grid_width * 3, grid_height * 4)  # Example of creating and adding a tower
        # self.tower_manager.add_tower(grid_width * 8, grid_height * 4)  # Example of creating and adding a tower

        # Initialize UI elements
        self.gold_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_RESOURCES_POSITION, [configuration.UI_LABEL_WIDTH, configuration.UI_LABEL_HEIGHT]),
                                                      text=f"Gold: {self.player.gold}",
                                                      manager=self.UI_manager)
        self.health_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_HEALTH_POSITION, [configuration.UI_LABEL_WIDTH, configuration.UI_LABEL_HEIGHT]),
                                                        text=f"Health: {self.player.health}",
                                                        manager=self.UI_manager)
        self.score_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_SCORE_POSITION, [configuration.UI_LABEL_WIDTH, configuration.UI_LABEL_HEIGHT]),
                                                       text=f"Score: {self.player.score}",
                                                       manager=self.UI_manager)
        self.enemy_count_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_ENEMY_COUNT_POSITION, [configuration.UI_LABEL_WIDTH, configuration.UI_LABEL_HEIGHT]),
                                                             text=f"Enemies: {len(self.enemy_manager.entities)}",
                                                             manager=self.UI_manager)
    def draw(self):
        self.screen.fill(configuration.BACKGROUND_COLOR)  # Clear the screen with the background color
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.draw()
        elif self.current_state == GameState.OPTIONS:
            self.options_screen.draw()
        elif self.current_state == GameState.CAMPAIGN_MAP:
            self.campaign_map.draw()
        elif self.current_state == GameState.LEVEL_COMPLETE:
            self.level_completion_screen.draw()
        elif self.current_state == GameState.PLAYING:
            self.board.draw_board(self.screen, self.level_manager.get_current_level().path) # Draw the game board
            self.tower_manager.draw_towers(self.screen)
            self.enemy_manager.draw(self.screen)
            self.projectile_manager.draw_projectiles(self.screen)
            self.tower_selection_panel.draw()
            #self.wave_panel.draw()
        self.UI_manager.draw_ui(self.screen)  # Draw the game UI
        pygame.display.flip()  # Update the display


    def run(self):
        self.is_running = True

        while self.is_running:
            time_delta = self.clock.tick(configuration.FPS) / 1000.0
            self.event_manager.process_events(self)
            self.update(time_delta)
            self.draw()
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(configuration.FPS)
        pygame.quit()

    def update(self, time_delta):
        if configuration.DEBUG:
            print("Updating game state")

        self.UI_manager.update(time_delta)

        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.update(time_delta)
        elif self.current_state == GameState.LEVEL_COMPLETE:
            self.level_completion_screen.update(time_delta)
        elif self.current_state == GameState.PLAYING:
            # Main game update logic for each frame
            new_enemies = self.level_manager.update_levels()
            if not new_enemies and len(self.enemy_manager.entities) == 0:
                if self.level_manager.check_level_complete():
                    self.level_completion_screen.background = self.capture_screen()
                    self.current_state = GameState.LEVEL_COMPLETE
                    self.level_completion_screen.open_screen()
            for enemy in new_enemies:
                self.enemy_manager.add_enemy(enemy)
            self.enemy_manager.update()
            self.tower_manager.update(self.enemy_manager.get_enemies(), self.projectile_manager)
            self.projectile_manager.update_entities()
            self.collision_manager.handle_group_collisions(
                self.enemy_manager.entities, self.projectile_manager.projectiles
            )
            self.wave_panel.update(time_delta)
            self.check_game_over()

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
        self.player.score += enemy.score_value
        self.player.gold += enemy.gold_value
        self.gold_label.set_text(f"Gold: {self.player.gold}")
        self.score_label.set_text(f"Score: {self.player.score}")
        self.enemy_count_label.set_text(f"Enemies: {len(self.enemy_manager.entities)}")

    def player_take_damage_callback(self, amount):
        self.player.health -= amount
        self.health_label.set_text(f'health: {self.player.health}')
        if self.player.health <= 0:
            self.player.health = 0
            self.game_over()

    def game_over(self):
        self.is_running = False
        self.display_game_over_screen()

    def display_game_over_screen(self):
        # Code to display your game over screen...
        print("GAME OVER!!!!")

    def go_to_next_level(self):
        if self.level_manager.next_level():
            self.tower_manager.towers = []
            self.level_manager.start_next_level()
        else:  # no new enemies, no enemies to manage, and no next level
            print("Congrats! You win!")
            self.is_running = False

    def capture_screen(self):
        # Capture the current display surface
        return pygame.display.get_surface().copy()

    def set_gameboard_UI_visibility(self, visible):
        self.score_label.visible = visible
        self.enemy_count_label.visible = visible
        self.gold_label.visible = visible
        self.health_label.visible = visible