import json
import os
import sys

import pygame

from src.config.config import DEBUG

from src.board.wave_panel import WavePanel
from src.config.config import LEVELS_JSON_PATH
from src.game.level import Level
from src.utils.resource_path import resource_path


def parse_levels(levels_data):
    # Convert JSON data into Level objects
    parsed_levels = []
    for level_data in levels_data['levels']:
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
        paths_to_try = []

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            if hasattr(sys, '_MEIPASS'):
                paths_to_try.append(os.path.join(sys._MEIPASS, LEVELS_JSON_PATH))
            paths_to_try.append(os.path.join(base_path, LEVELS_JSON_PATH))
        else:
            paths_to_try.append(resource_path(LEVELS_JSON_PATH))

        paths_to_try.append(LEVELS_JSON_PATH)

        for levels_path in paths_to_try:
            try:
                if os.path.exists(levels_path):
                    with open(levels_path, 'r') as file:
                        levels_data = json.load(file)
                        self.levels = parse_levels(levels_data)
                        print(f"Successfully loaded {len(self.levels)} levels from {levels_path}")
                        return
            except Exception as e:
                print(f"Failed to load from {levels_path}: {e}")
                continue

        print(f"Error: Could not load levels from any path. Tried: {paths_to_try}")

    def next_level(self):
        if self.current_level_index < len(self.levels) - 1:
            return self.levels[self.current_level_index + 1]
        else:
            return None  # No more levels

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
            self.levels[self.current_level_index].reset()
            self.start_level(level_index=self.current_level_index)

    def start_level(self, level_index=None):
        if not self.levels:
            print("ERROR: No levels loaded! Check that the levels JSON file exists and is accessible.")
            return

        if level_index is not None:
            if level_index < 0 or level_index >= len(self.levels):
                print(f"ERROR: Invalid level index {level_index}. Available levels: 0-{len(self.levels)-1}")
                return
            if DEBUG:
                print(f"Starting level {level_index + 1}")
            self.current_level_index = level_index
        else:
            next_level_index = self.current_level_index + 1
            if next_level_index < len(self.levels):
                self.current_level_index = next_level_index
                if DEBUG:
                    print(f"Starting next level: {self.current_level_index + 1}")
            else:
                if DEBUG:
                    print("All levels completed!")
                return

        self.current_level = self.levels[self.current_level_index]
        self.current_level.start_time = pygame.time.get_ticks()
        self.current_level.initialize_wave_start_times()
        self.wave_panel.recreate_wave_buttons(current_level=self.current_level)
        self.tower_manager.towers = []
