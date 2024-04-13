import os
import json
import pygame

import src.config.config as configuration
from src.board.game_board import GameBoard
from src.board.tower_selection_panel import TowerSelectionPanel
from src.entities.Player import Player
from src.game.game_state import GameState
from src.managers.audio_manager import AudioManager
from src.managers.collision_manager import CollisionManager
from src.managers.enemy_manager import EnemyManager
from src.managers.event_manager import EventManager
from src.managers.game_state_manager import GameStateManager
from src.managers.level_manager import LevelManager
from src.managers.projectile_manager import ProjectileManager
from src.managers.tower_manager import TowerManager
from src.managers.ui_manager import UIManager


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
        pygame.init()
        self.screen = pygame.display.set_mode([configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT],
                                              pygame.DOUBLEBUF, pygame.SRCALPHA)
        pygame.display.set_caption("Mr. Mega\'s Awesome Tower Defense Game")
        self.clock = pygame.time.Clock()
        self.event_manager = EventManager()
        theme_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'theme.json')
        self.audio_manager = AudioManager()
        self.state_manager = GameStateManager(self)
        self.player = Player(update_ui_callback=self.update_ui, on_death_callback=self.player_on_death_callback)
        self.UI_manager = UIManager((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), theme_path, self)
        self.tower_manager = TowerManager(self.player)
        self.level_manager = LevelManager(self.tower_manager, self.UI_manager)
        self.projectile_manager = ProjectileManager()
        self.collision_manager = CollisionManager()
        self.tower_selection_panel = TowerSelectionPanel(self.screen, self.tower_manager)
        self.board = GameBoard(configuration.GAME_BOARD_WIDTH, configuration.GAME_BOARD_HEIGHT)
        self.is_running = False
        self.enemy_manager = EnemyManager(self.level_manager, self.enemy_defeated_callback,
                                          self.player_take_damage_callback)
        self.current_state = None
        self.previous_state = None
        self.is_build_mode = True

    def initialize_game(self, level_num=-1):
        self.state_manager.change_state(GameState.PLAYING)
        self.level_manager.load_levels()
        self.UI_manager.player_info_panel.set_visibility(True)
        if level_num > -1:
            self.level_manager.start_level(level_num)
        self.player.start_level()
        self.enemy_manager.reset()
        self.level_manager.reset_level()

    def run(self):
        self.is_running = True
        self.state_manager.change_state(GameState.MAIN_MENU)
        while self.is_running:
            time_delta = self.clock.tick(configuration.FPS) / 1000.0
            self.event_manager.process_events(self)
            self.update(time_delta)
            self.draw()
            # pygame.display.update()
            self.clock.tick(configuration.FPS)
        pygame.quit()
    def draw(self):
        self.screen.fill(configuration.BACKGROUND_COLOR)  # Clear the screen with the background color

        # Draw game-specific elements only when in the PLAYING state
        if self.current_state == GameState.PLAYING:
            self.board.draw_board(self.screen, self.level_manager.get_current_level().path)
            self.tower_manager.draw_towers(self.screen)
            self.enemy_manager.draw(self.screen)
            self.projectile_manager.draw_projectiles(self.screen)
            self.tower_selection_panel.draw()

        # Always draw the UI elements on top of the game elements
        self.UI_manager.draw_ui(self.screen)

        pygame.display.flip()  # Update the display

    def update(self, time_delta):
        if configuration.DEBUG:
            print("Updating game state")

        self.UI_manager.update(time_delta)

        if self.current_state == GameState.MAIN_MENU:
            self.UI_manager.main_menu.update(time_delta)
        elif self.current_state == GameState.CAMPAIGN_MAP:
            self.UI_manager.campaign_map.update(time_delta)
        elif self.current_state == GameState.LEVEL_COMPLETE or self.current_state == GameState.LEVEL_DEFEAT:
            self.UI_manager.level_end_screen.update(time_delta)
        elif self.current_state == GameState.PLAYING:
            # Main game update logic for each frame
            new_enemies = self.level_manager.update_levels()
            if all(not item for item in new_enemies) and len(self.enemy_manager.entities) == 0:
                if self.level_manager.check_level_complete():
                    # self.UI_manager.level_end_screen.capturedScreen = pygame.display.get_surface().copy()
                    self.set_gameboard_ui_visibility(False)
                    self.state_manager.change_state(GameState.LEVEL_COMPLETE)

            for enemy in new_enemies:
                self.enemy_manager.add_enemy(enemy)
            self.enemy_manager.update()
            self.tower_manager.update(self.enemy_manager.get_enemies(), self.projectile_manager)
            self.projectile_manager.update_entities()
            self.collision_manager.handle_group_collisions(
                self.enemy_manager.entities, self.projectile_manager.projectiles
            )
            self.level_manager.wave_panel.update(time_delta, self.level_manager.current_level.enemy_wave_list)
            self.UI_manager.player_info_panel.update(self.enemy_manager)
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
        self.player.levelScore += enemy.score_value
        self.player.add_gold(enemy.gold_value)
        self.UI_manager.player_info_panel.gold_label.set_text(f"Gold: {self.player.gold}")
        self.UI_manager.player_info_panel.score_label.set_text(f"Score: {self.player.levelScore}")
        self.UI_manager.player_info_panel.enemy_count_label.set_text(f"Enemies: {len(self.enemy_manager.entities)}")

    def player_take_damage_callback(self, amount):
        self.player.take_damage(amount)
        self.UI_manager.player_info_panel.health_label.set_text(f'health: {self.player.health}')

    def set_gameboard_ui_visibility(self, visible):
        self.UI_manager.player_info_panel.set_visibility(visible)
        self.level_manager.wave_panel.visible = visible
        # TODO Link to all panels in playing scene

    def update_ui(self):
        """
        Used to allow the player to update the UI without direct access to the UI_manager
        :return:
        """
        self.UI_manager.update(self.clock.tick(configuration.FPS) / 1000.0)

    def save_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        filename = f"src/save_data/{save_slot_or_filename}.json" if isinstance(save_slot_or_filename,
                                                                               int) else save_slot_or_filename

        player_data = {"player": self.player.to_dict()}

        try:
            with open(filename, 'w') as f:
                json.dump(player_data, f, indent=4)
                print(f"Game saved to {filename}")
        except Exception as e:
            print(f"Failed to save game: {e}")

    def load_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        filename = f"src/save_data/{save_slot_or_filename}.json" if isinstance(save_slot_or_filename,
                                                                               int) else save_slot_or_filename
        try:
            with open(filename, 'r') as f:
                player_data = json.load(f)
                self.player.from_dict(player_data["player"])
                self.UI_manager.campaign_map.update_player_progress(player_data["player"]['unlocked_levels'])
                print(f"Game loaded from {filename}")
        except FileNotFoundError:
            print(f"Save file not found: {filename}")


    def player_on_death_callback(self):
        self.state_manager.change_state(GameState.LEVEL_DEFEAT)
        self.set_gameboard_ui_visibility(False)