import os
import json
import pygame
import pygame_gui

import src.config.config as configuration
from src.board.game_board import GameBoard
from src.board.tower_selection_panel import TowerSelectionPanel
from src.entities.Player import Player
from src.game.game_state import GameState
from src.game.player_info_panel import PlayerInfoPanel
from src.managers.collision_manager import CollisionManager
from src.managers.enemy_manager import EnemyManager
from src.managers.event_manager import EventManager
from src.managers.level_manager import LevelManager
from src.managers.projectile_manager import ProjectileManager
from src.managers.tower_manager import TowerManager
from src.screens.campain_map import CampaignMap
from src.screens.level_completion import LevelCompletionScreen
from src.screens.game_data_screen import GameDataScreen
from src.screens.main_menu import MainMenu
from src.screens.options_screen import OptionsScreen


def capture_screen():
    # Capture the current display surface
    return pygame.display.get_surface().copy()


class Game:
    """
    Core game class responsible for initializing the game, running the main loop, handling game state transitions (
    like starting, game over), and managing high-level game events. Potential TODOs: Implementing efficient game
    state management, optimizing the main game loop for performance, and handling transitions between different parts
    of the game smoothly.
    """

    def __init__(self):
        self.score_label = None
        self.is_build_mode = False
        pygame.init()
        self.screen = pygame.display.set_mode([configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT],
                                              pygame.DOUBLEBUF)
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.event_manager = EventManager()
        theme_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'theme.json')
        self.UI_manager = pygame_gui.UIManager((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), theme_path)
        self.tower_manager = TowerManager()
        self.level_manager = LevelManager(self.tower_manager, self.UI_manager)
        self.projectile_manager = ProjectileManager()
        self.collision_manager = CollisionManager()

        self.tower_selection_panel = TowerSelectionPanel(self.screen, self.tower_manager)
        self.board = GameBoard(configuration.GAME_BOARD_WIDTH, configuration.GAME_BOARD_HEIGHT)
        self.is_running = False
        self.checkCounter = 0
        self.player = Player(update_ui_callback=self.update_ui)
        self.enemy_manager = EnemyManager(self.level_manager, self.enemy_defeated_callback,
                                          self.player_take_damage_callback)
        self.current_state = GameState.MAIN_MENU
        self.previous_state = None  # Initialize previous state
        self.main_menu = MainMenu(self.screen, self.UI_manager)
        self.options_screen = OptionsScreen(self.UI_manager)
        self.load_game_screen = GameDataScreen(self.UI_manager)
        #player_progress = {'unlocked_levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]} # sample progress
        self.campaign_map = CampaignMap(self.UI_manager, self.player.player_progress)
        self.level_completion_screen = LevelCompletionScreen(self)
        self.is_build_mode = True
        self.player_info_panel = PlayerInfoPanel(self.UI_manager, self.player, self.screen)

    def initialize_game(self):
        self.current_state = GameState.PLAYING
        self.level_manager.load_levels()
        self.player_info_panel.set_visibility(True)

        # Initialize UI elements
        # self.gold_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_RESOURCES_POSITION,
        #                                                                         [configuration.UI_LABEL_WIDTH,
        #                                                                          configuration.UI_LABEL_HEIGHT]),
        #                                               text=f"Gold: {self.player.gold}",
        #                                               manager=self.UI_manager)
        # self.health_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_HEALTH_POSITION,
        #                                                                           [configuration.UI_LABEL_WIDTH,
        #                                                                            configuration.UI_LABEL_HEIGHT]),
        #                                                 text=f"Health: {self.player.health}",
        #                                                 manager=self.UI_manager)
        # self.score_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(configuration.UI_SCORE_POSITION,
        #                                                                          [configuration.UI_LABEL_WIDTH,
        #                                                                           configuration.UI_LABEL_HEIGHT]),
        #                                                text=f"Score: {self.player.score}",
        #                                                manager=self.UI_manager)
        # self.enemy_count_label = pygame_gui.elements.UILabel(
        #     relative_rect=pygame.Rect(configuration.UI_ENEMY_COUNT_POSITION,
        #                               [configuration.UI_LABEL_WIDTH, configuration.UI_LABEL_HEIGHT]),
        #     text=f"Enemies: {len(self.enemy_manager.entities)}",
        #     manager=self.UI_manager)

    def draw(self):
        self.screen.fill(configuration.BACKGROUND_COLOR)  # Clear the screen with the background color
        if self.current_state == GameState.MAIN_MENU:
            self.main_menu.draw()
        elif self.current_state == GameState.OPTIONS:
            self.options_screen.draw(self.screen)
        elif self.current_state == GameState.LOAD_GAME:
            self.load_game_screen.draw(self.screen)
        elif self.current_state == GameState.CAMPAIGN_MAP:
            self.campaign_map.draw(screen=self.screen)
        elif self.current_state == GameState.LEVEL_COMPLETE:
            self.level_completion_screen.draw()
        elif self.current_state == GameState.PLAYING:
            self.board.draw_board(self.screen, self.level_manager.get_current_level().path)  # Draw the game board
            self.tower_manager.draw_towers(self.screen)
            self.enemy_manager.draw(self.screen)
            self.projectile_manager.draw_projectiles(self.screen)
            self.tower_selection_panel.draw()
            # self.wave_panel.draw()
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
            if all(not item for item in new_enemies) and len(self.enemy_manager.entities) == 0:
                if self.level_manager.check_level_complete():
                    self.level_completion_screen.background = capture_screen()
                    self.current_state = GameState.LEVEL_COMPLETE
                    self.player.complete_level(self.level_manager.current_level_index)
                    self.campaign_map.update_player_progress(self.player.player_progress)
                    self.level_completion_screen.open_screen()
            for enemy in new_enemies:
                self.enemy_manager.add_enemy(enemy)
            self.enemy_manager.update()
            self.tower_manager.update(self.enemy_manager.get_enemies(), self.projectile_manager)
            self.projectile_manager.update_entities()
            self.collision_manager.handle_group_collisions(
                self.enemy_manager.entities, self.projectile_manager.projectiles
            )
            self.level_manager.wave_panel.update(time_delta, self.level_manager.current_level.enemy_wave_list)
            self.player_info_panel.update(self.enemy_manager)
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
        self.player_info_panel.gold_label.set_text(f"Gold: {self.player.gold}")
        self.player_info_panel.score_label.set_text(f"Score: {self.player.score}")
        self.player_info_panel.enemy_count_label.set_text(f"Enemies: {len(self.enemy_manager.entities)}")

    def player_take_damage_callback(self, amount):
        self.player.health -= amount
        self.player_info_panel.health_label.set_text(f'health: {self.player.health}')
        if self.player.health <= 0:
            self.player.health = 0
            self.game_over()

    def game_over(self):
        self.is_running = False
        self.display_game_over_screen()

    def display_game_over_screen(self):
        # Code to display your game over screen...
        print("GAME OVER!!!!")

    # def start_level(self, index=None):
    #     self.level_manager.start_level(index)
    # if self.level_manager.next_level():
    #     self.tower_manager.towers = []
    #     if index:
    #         self.level_manager.start_level(index)
    #     else:
    #         self.level_manager.start_level()
    #     self.wave_panel.recreate_wave_buttons()

    def set_gameboard_ui_visibility(self, visible):
        self.player_info_panel.set_visibility(visible)

    def update_ui(self):
        # Update UI elements here
        # For example, updating gold, health, and score labels
        self.player_info_panel.gold_label.set_text(f"Gold: {self.player.gold}")
        self.player_info_panel.health_label.set_text(f"Health: {self.player.health}")
        self.player_info_panel.score_label.set_text(f"Score: {self.player.score}")
        self.UI_manager.update(self.clock.tick(configuration.FPS) / 1000.0)

    def change_state(self, new_state):
        self.previous_state = self.current_state  # Store current state as previous
        self.current_state = new_state  # Update current state to the new state
        if new_state == GameState.MAIN_MENU:
            self.main_menu.open_menu()

    def save_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        filename = f"src/save_data/{save_slot_or_filename}.json" if isinstance(save_slot_or_filename, int) else save_slot_or_filename

        # Prepare the player data to save
        player_data = {
            "player": self.player.to_dict()  # Assuming you have a method in Player class to convert player data to a dictionary
        }

        try:
            with open(filename, 'w') as f:
                json.dump(player_data, f, indent=4)
                print(f"Game saved to {filename}")
        except Exception as e:
            print(f"Failed to save game: {e}")

    def load_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        # This is just an example; adjust based on your save system
        filename = f"src/save_data/{save_slot_or_filename}.json" if isinstance(save_slot_or_filename,
                                                                               int) else save_slot_or_filename

        try:
            with open(filename, 'r') as f:
                player_data = json.load(f)
                self.player.from_dict(player_data["player"])
                # Assuming you have a method in campaign_map to update based on player data
                self.campaign_map.update_player_progress(player_data["player"])
                print(f"Game loaded from {filename}")
        except FileNotFoundError:
            print(f"Save file not found: {filename}")