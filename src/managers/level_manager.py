import json

import pygame

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
    def __init__(self):
        # self.current_wave = None
        # self.enemy_manager = enemy_manager
        self.levels = []
        self.current_level = None
        self.current_level_index = -1
        self.load_levels()

    def load_levels(self):
        # Load levels from the JSON file
        # try:
        with open(LEVELS_JSON_PATH, 'r') as file:
            levels_data = json.load(file)
            # Parse and create Level objects
            self.levels = parse_levels(levels_data)
        # except Exception as e:
        # print(f"Error loading levels: {e}")
        # Handle exceptions (file not found, JSON parse error, etc.)

    def next_level(self):
        if self.current_level_index < len(self.levels) - 1:
            return self.levels[self.current_level_index + 1]
        else:
            return None  # No more levels

    def reset_level(self):
        if self.current_level_index != -1:
            # Reset the current level to its initial state
            self.levels[self.current_level_index].reset()

    def get_current_level(self):
        if self.current_level_index != -1 and self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None

    # Additional methods as necessary for level management
    def start_level(self, level_index):

        self.current_level_index = level_index
        self.current_level = self.levels[level_index]
        self.current_level.start_time = pygame.time.get_ticks()
        # self.current_level.get_next_wave()
        print(f"Starting level {level_index + 1}")

    def update_levels(self):
        current_time = pygame.time.get_ticks()
        new_enemies = []

        current_level = self.get_current_level()
        if current_level:
            # for wave in current_level.enemy_wave_list:
            wave = current_level.current_wave
            if wave:
                enemy = wave.update(current_time)
                if enemy:
                    new_enemies.append(enemy)
                elif wave.is_Finished():
                    current_level.get_next_wave()
            else:
                current_level.get_next_wave()
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

    def start_next_level(self):
        next_level = self.next_level()
        if next_level:
            self.current_level_index += 1
            self.current_level = next_level
            print(f"Starting next level: {self.current_level_index + 1}")
        else:
            print("All levels completed!")
            # Handle the game completion scenario here (e.g., go to a victory screen)
