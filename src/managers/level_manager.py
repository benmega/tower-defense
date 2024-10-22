import json

import pygame

from src.board.wave_panel import WavePanel
from src.config.config import LEVELS_JSON_PATH
from src.game.level import Level


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
        try:
            with open(LEVELS_JSON_PATH, 'r') as file:
                levels_data = json.load(file)
                # Parse and create Level objects
                self.levels = parse_levels(levels_data)
        except Exception as e:
            print(f"Error loading levels: {e}")

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
            new_enemies.append(current_level.update_level(current_time))
            if current_level.is_completed():
                self.start_next_level() # TODO check if this is this ever hit

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
        if level_index is not None:
            # Start the specified level
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
