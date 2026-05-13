import os
import sys
import json
import pygame

import src.config.config as configuration
from src.utils.resource_path import resource_path
from src.utils.screen_utils import capture_screen
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
from src.effects.particle_system import ParticleSystem
from src.effects.screen_shake import ScreenShake
from src.utils import constants as C


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
        pygame.display.set_caption("Tower Defense")
        # Set window icon
        try:
            icon = pygame.image.load('assets/images/towers/basic_tower.png').convert_alpha()
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Failed to load icon: {e}")

        self.clock = pygame.time.Clock()
        self.event_manager = EventManager()
        theme_path = resource_path('src/config/theme.json')
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
        self.is_build_mode = False  # Start in selection mode, not build mode
        self.frame_time_delta = 0.0
        # Initialize tower info panel after UI_manager
        from src.game.tower_info_panel import TowerInfoPanel
        self.tower_info_panel = TowerInfoPanel(self.UI_manager)

        # Initialize particle system and screen shake
        self.particles = ParticleSystem()
        self.shake = ScreenShake()
        self._shake_offset = (0, 0)
        self._last_dt = 0.0
        self._game_surface = pygame.Surface((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT))
        self._campaign_win_played = False

    def initialize_game(self, level_num=-1):
        self.level_manager.load_levels()
        if not self.level_manager.levels:
            print("ERROR: Failed to load any levels. Cannot start game.")
            self.state_manager.change_state(GameState.MAIN_MENU)
            return

        self.state_manager.change_state(GameState.PLAYING)
        self.UI_manager.player_info_panel.set_visibility(True)
        if level_num > -1:
            self.level_manager.start_level(level_num)

        if not self.level_manager.current_level:
            print("ERROR: Failed to initialize level. Cannot start game.")
            self.state_manager.change_state(GameState.MAIN_MENU)
            return

        self.player.start_level()
        self.enemy_manager.reset()
        if level_num > -1:
            self.level_manager.start_level(level_num)
        else:
            self.level_manager.reset_level()

    def run(self):
        self.is_running = True
        self.state_manager.change_state(GameState.MAIN_MENU)
        while self.is_running:
            self.frame_time_delta = self.clock.tick(configuration.FPS) / 1000.0
            self.event_manager.process_events(self)
            self.update(self.frame_time_delta)
            self.draw()
        pygame.quit()

    def draw(self):
        self.screen.fill(configuration.BACKGROUND_COLOR)  # Clear the screen with the background color

        # Draw game-specific elements only when in the PLAYING state
        if self.current_state == GameState.PLAYING:
            current_level = self.level_manager.get_current_level()
            if current_level:
                # Render game world to intermediate surface for shake effect
                self._game_surface.fill(configuration.BACKGROUND_COLOR)
                self.board.draw_board(self._game_surface, current_level.path, self._last_dt)
                self.tower_manager.draw_towers(self._game_surface)
                # Draw tower range circles if enabled
                if self.tower_manager.show_ranges:
                    self._draw_tower_ranges_to(self._game_surface)
                self.enemy_manager.draw(self._game_surface)
                self.projectile_manager.draw_projectiles(self._game_surface)
                self.particles.draw(self._game_surface)
                # Apply shake offset when blitting to screen
                ox, oy = self._shake_offset
                self.screen.blit(self._game_surface, (ox, oy))

            # Draw UI overlays directly (not affected by shake)
            self.tower_selection_panel.draw()
            self._draw_wave_countdown(current_level)
            # Draw placement preview
            self._draw_placement_preview()
            # Update and draw tower info panel
            if self.tower_manager.selected_tower:
                self.tower_info_panel.show(self.tower_manager.selected_tower, self.player.gold)
            else:
                self.tower_info_panel.hide()
            self.tower_info_panel.draw(self.screen)

        # Always draw the UI elements on top of the game elements
        self.UI_manager.draw_ui(self.screen)

        pygame.display.flip()  # Update the display

    def update(self, time_delta):
        if configuration.DEBUG:
            print("Updating game state")

        self._last_dt = time_delta  # Store time delta for drawing
        self.UI_manager.update(time_delta)

        if self.current_state == GameState.MAIN_MENU:
            self.UI_manager.main_menu.update(time_delta)
        elif self.current_state == GameState.CAMPAIGN_MAP:
            self.UI_manager.campaign_map.update(time_delta)
        elif self.current_state == GameState.LEVEL_COMPLETE or self.current_state == GameState.LEVEL_DEFEAT:
            self.UI_manager.level_end_screen.update(time_delta)
        elif self.current_state == GameState.PLAYING:
            # Ensure a level is loaded before proceeding
            if not self.level_manager.current_level:
                print("ERROR: No level is loaded. Returning to main menu.")
                self.state_manager.change_state(GameState.MAIN_MENU)
                return

            # Update particle system and screen shake
            self.particles.update(time_delta)
            self._shake_offset = self.shake.update(time_delta)

            # Main game update logic for each frame
            new_enemies = self.level_manager.update_levels()
            if all(not item for item in new_enemies) and len(self.enemy_manager.entities) == 0:
                if self.level_manager.check_level_complete():
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
            if self.level_manager.current_level:
                self.level_manager.wave_panel.update(time_delta, self.level_manager.current_level.enemy_wave_list)
            self.UI_manager.player_info_panel.update(
                self.enemy_manager,
                current_level=self.level_manager.current_level,
                level_index=self.level_manager.current_level_index,
                is_build_mode=self.is_build_mode,
            )
            self.check_game_over()

    def check_game_over(self):
        if self.player.health <= 0:
            return True
        if self.level_manager.current_level_index >= len(self.level_manager.levels) - 1:
            if self.level_manager.check_level_complete():
                # Play campaign win sound once
                if not self._campaign_win_played:
                    self.audio_manager.play_sfx('campaign_win')
                    self._campaign_win_played = True
                print("Campaign finished")
                return True
        return False

    def enemy_defeated_callback(self, enemy):
        self.player.levelScore += enemy.score_value
        self.player.add_gold(enemy.gold_value)
        self.UI_manager.player_info_panel.gold_label.set_text(f"Gold: {self.player.gold}")
        self.UI_manager.player_info_panel.score_label.set_text(f"Score: {self.player.levelScore}")
        self.UI_manager.player_info_panel.enemy_count_label.set_text(f"Enemies: {len(self.enemy_manager.entities)}")

        # Emit death particle burst (red)
        self.particles.emit(enemy.rect.centerx, enemy.rect.centery,
                          count=10, color=C.RGB_HEALTH_RED, speed=2.0, life=0.5)
        # Emit gold pickup particle sparkle
        self.particles.emit(enemy.rect.centerx, enemy.rect.centery - 20,
                          count=6, color=C.RGB_GOLD_BRIGHT, speed=1.5, life=0.8)
        # Play death sound
        self.audio_manager.play_sfx('enemy_death')

    def player_take_damage_callback(self, amount):
        self.player.take_damage(amount)
        self.UI_manager.player_info_panel.health_label.set_text(f'health: {self.player.health}')
        # Trigger screen shake on damage
        self.shake.trigger(magnitude=8, duration=0.25)

    def set_gameboard_ui_visibility(self, visible):
        self.UI_manager.player_info_panel.set_visibility(visible)
        self.level_manager.wave_panel.visible = visible

    def update_ui(self):
        self.UI_manager.update(self.clock.get_time() / 1000.0)

    @staticmethod
    def _save_dir() -> str:
        """
        Return a writable directory for save files.

        When running from a frozen PyInstaller bundle the install folder may
        be read-only (e.g. Program Files), so we store saves in
        %APPDATA%/TowerDefense/save_data on Windows and
        ~/.local/share/TowerDefense/save_data on other platforms.
        When running from source we keep the original src/save_data location.
        """
        if getattr(sys, 'frozen', False):
            if os.name == 'nt':
                base = os.environ.get('APPDATA', os.path.expanduser('~'))
            else:
                base = os.path.join(os.path.expanduser('~'), '.local', 'share')
            save_dir = os.path.join(base, 'TowerDefense', 'save_data')
        else:
            save_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'save_data'
            )
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

    def save_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        if isinstance(save_slot_or_filename, int):
            filename = os.path.join(self._save_dir(), f"savegame_slot{save_slot_or_filename}.json")
        else:
            filename = save_slot_or_filename

        player_data = {"player": self.player.to_dict()}

        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(player_data, f, indent=4)
                print(f"Game saved to {filename}")
        except Exception as e:
            print(f"Failed to save game: {e}")

    def load_game(self, save_slot_or_filename):
        # Determine the filename based on the input parameter
        if isinstance(save_slot_or_filename, int):
            filename = os.path.join(self._save_dir(), f"savegame_slot{save_slot_or_filename}.json")
        else:
            filename = save_slot_or_filename
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

    def _draw_wave_countdown(self, current_level):
        """Show next-wave countdown just above the selection panel."""
        if not current_level:
            return
        now = pygame.time.get_ticks()
        panel_y = self.tower_selection_panel.panel_y
        for wave in current_level.enemy_wave_list:
            secs = (wave.start_time - now) / 1000.0
            if secs > 0:
                label = f"Next wave in: {secs:.1f}s  [SPACE to skip]"
                font = pygame.font.Font(None, 22)
                surf = font.render(label, True, (60, 60, 60))
                self.screen.blit(surf, (self.screen.get_width() - surf.get_width() - 10, panel_y - surf.get_height() - 4))
                break

    def _draw_placement_preview(self):
        """Draw a preview of the tower being placed, showing range and validity."""
        if self.tower_manager.selected_tower_type is None:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Snap to nearest grid cell
        grid_x = (mouse_x // configuration.TILE_SIZE[0]) * configuration.TILE_SIZE[0]
        grid_y = (mouse_y // configuration.TILE_SIZE[1]) * configuration.TILE_SIZE[1]

        # Check if position is valid
        if self.board.can_build_at((grid_x, grid_y)):
            tint_color = (0, 200, 0, 100)  # Green for valid
        else:
            tint_color = (200, 0, 0, 100)  # Red for invalid

        # Get preview surface and blit with transparency
        from src.entities.towers.tower import Tower
        preview_surface = Tower.get_preview_surface(self.tower_manager.selected_tower_type)
        self.screen.blit(preview_surface, (grid_x, grid_y))

        # Draw tint overlay
        tint_surface = pygame.Surface(configuration.TILE_SIZE, pygame.SRCALPHA)
        tint_surface.fill(tint_color)
        self.screen.blit(tint_surface, (grid_x, grid_y))

        # Draw range circle
        tower_center_x = grid_x + configuration.TILE_SIZE[0] // 2
        tower_center_y = grid_y + configuration.TILE_SIZE[1] // 2
        tower_class = self.tower_manager.tower_types.get(self.tower_manager.selected_tower_type)
        if tower_class:
            default_range = 100  # Default range
            pygame.draw.circle(
                self.screen, C.RGB_GOLD_BRIGHT,
                (int(tower_center_x), int(tower_center_y)),
                int(default_range), 1
            )

    def _draw_tower_ranges_to(self, surface):
        """Draw range circles for all towers onto the given surface."""
        for tower in self.tower_manager.towers:
            center_x = tower.x + configuration.TILE_SIZE[0] // 2
            center_y = tower.y + configuration.TILE_SIZE[1] // 2
            pygame.draw.circle(
                surface, C.RGB_GOLD_BRIGHT,
                (int(center_x), int(center_y)),
                int(tower.attack_range), 1
            )
