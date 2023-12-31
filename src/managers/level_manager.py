import json

import pygame

from src.config.config import LEVELS_JSON_PATH
from src.game.level import Level


class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level_index = -1
        self.load_levels()

    def load_levels(self):
        # Load levels from the JSON file
        #try:
        with open(LEVELS_JSON_PATH, 'r') as file:
            levels_data = json.load(file)
            # Parse and create Level objects
            self.levels = self.parse_levels(levels_data)
        #except Exception as e:
            #print(f"Error loading levels: {e}")
            # Handle exceptions (file not found, JSON parse error, etc.)

    def parse_levels(self, levels_data):
        # Convert JSON data into Level objects
        parsed_levels = []
        for level_data in levels_data['levels']:
            # Assuming Level class has an appropriate constructor or factory method
            level = Level.from_json(level_data)
            parsed_levels.append(level)
        return parsed_levels

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        else:
            return None  # No more levels

    def reset_level(self):
        if self.current_level_index != -1:
            # Reset the current level to its initial state
            self.levels[self.current_level_index].reset()

    def get_current_level(self):
        if self.current_level_index != -1:
            return self.levels[self.current_level_index]
        return None

    # Additional methods as necessary for level management
    def start_level(self, level_index):
        self.current_level = self.levels[level_index]
        self.current_wave = self.current_level.get_next_wave()  # Store the current wave object
        print(f"Starting level {level_index + 1}")


    def update_levels(self):
        # Get the current time from Pygame
        current_time = pygame.time.get_ticks()

        # Logic to update the current level and enemy waves
        new_enemies = []
        for wave in self.get_current_level().enemy_wave_list:
            enemy = wave.update(current_time)
            if enemy:
                new_enemies.append(enemy)
        return new_enemies