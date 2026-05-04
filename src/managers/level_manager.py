import json
import os

import pygame

from src.board.wave_panel import WavePanel
from src.config.config import LEVELS_JSON_PATH
from src.game.level import Level
from src.utils.helpers import get_asset_path


def parse_levels(levels_data):
    # Convert JSON data into Level objects
    parsed_levels = []
    for level_data in levels_data['levels']:
        # Assuming Level class has an appropriate constructor or factory method
        level = Level.from_json(level_data)
        parsed_levels.append(level)
    return parsed_levels


class LevelManager:
    def __init__(self,tower_manager, UI_manager):
        self.tower_manager = tower_manager
        self.UI_manager = UI_manager
        self.wave_panel = WavePanel(self.UI_manager)
        self.levels = []
        self.current_level = None
        self.current_level_index = -1
        self.load_levels()


    def load_levels(self):
        # Load levels from the JSON file
<<<<<<< HEAD
        import os
        import sys

        paths_to_try = []

        # Try frozen (PyInstaller) paths first
        if hasattr(sys, 'frozen'):
            # Use sys._MEIPASS for PyInstaller temp directory (most reliable)
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
                paths_to_try.append(os.path.join(base_path, LEVELS_JSON_PATH))
                print(f"[DEBUG] PyInstaller sys._MEIPASS: {base_path}")
            else:
                # Fallback for PyInstaller if _MEIPASS not available
                base_path = os.path.dirname(sys.executable)
                paths_to_try.append(os.path.join(base_path, LEVELS_JSON_PATH))
                print(f"[DEBUG] PyInstaller exe directory: {base_path}")
        else:
            # Development path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            paths_to_try.append(os.path.join(project_root, LEVELS_JSON_PATH))
            print(f"[DEBUG] Development path: {os.path.join(project_root, LEVELS_JSON_PATH)}")

        # Relative path fallback
        paths_to_try.append(LEVELS_JSON_PATH)

        for levels_path in paths_to_try:
            try:
                print(f"[DEBUG] Trying to load levels from: {levels_path}")
                if os.path.exists(levels_path):
                    print(f"[DEBUG] Found file at: {levels_path}")
                    with open(levels_path, 'r') as file:
                        levels_data = json.load(file)
                        self.levels = parse_levels(levels_data)
                        print(f"Successfully loaded {len(self.levels)} levels from {levels_path}")
                        return
                else:
                    print(f"[DEBUG] File not found: {levels_path}")
            except Exception as e:
                print(f"Failed to load from {levels_path}: {e}")
                continue

        print(f"Error: Could not load levels from any path. Tried: {paths_to_try}")
        import traceback
        traceback.print_exc()
=======
        try:
            full_path = get_asset_path(LEVELS_JSON_PATH) if not os.path.isabs(LEVELS_JSON_PATH) else LEVELS_JSON_PATH
            with open(full_path, 'r') as file:
                levels_data = json.load(file)
                # Parse and create Level objects
                self.levels = parse_levels(levels_data)
        except Exception as e:
            print(f"Error loading levels: {e}")
>>>>>>> claude/unruffled-ramanujan-1882ca

    def next_level(self):
        if self.current_level_index < len(self.levels) - 1:
            return self.levels[self.current_level_index + 1]
        else:
            return None  # No more levels

    def start_next_level(self):
        self.start_level()

    def get_current_level(self):
        if self.current_level_index != -1 and self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None

    def update_levels(self):
        current_time = pygame.time.get_ticks()
        new_enemies = []

        current_level = self.get_current_level()
        if current_level:
            spawned_enemies = current_level.update_level(current_time)
            if spawned_enemies:
                # Defensive normalization to keep the spawn contract flat.
                if isinstance(spawned_enemies, list):
                    new_enemies.extend(spawned_enemies)
                else:
                    new_enemies.append(spawned_enemies)
            if current_level.is_completed():
                self.start_level()  # advance to next level

        return new_enemies

    def check_level_complete(self):
        current_level = self.get_current_level()
        if not current_level:
            return False
        for wave in current_level.enemy_wave_list:
            if wave.spawned_count < wave.count:
                return False
        return True

    def reset_level(self):
        if self.current_level_index != -1:
            # Reset the current level to its initial state
            self.levels[self.current_level_index].reset()
            self.start_level(level_index=self.current_level_index)

    def start_level(self, level_index=None):
        if not self.levels:
            print("ERROR: No levels loaded! Check that the levels JSON file exists and is accessible.")
            return

        if level_index is not None:
            # Start the specified level
            if level_index < 0 or level_index >= len(self.levels):
                print(f"ERROR: Invalid level index {level_index}. Available levels: 0-{len(self.levels)-1}")
                return
            print(f"Starting level {level_index + 1}")
            self.current_level_index = level_index
        else:
            # Start the next level
            next_level_index = self.current_level_index + 1
            if next_level_index < len(self.levels):
                self.current_level_index = next_level_index
                print(f"Starting next level: {self.current_level_index + 1}")
            else:
                print("All levels completed!")
                # Handle the game completion scenario here (e.g., go to a victory screen)
                return  # Exit the method if there are no more levels to start

        # Common code for starting a level
        self.current_level = self.levels[self.current_level_index]
        self.current_level.start_time = pygame.time.get_ticks()
        self.current_level.initialize_wave_start_times()
        self.wave_panel.recreate_wave_buttons(current_level=self.current_level)
        self.tower_manager.towers = []
