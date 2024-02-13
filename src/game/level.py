import json

import pygame

from src.config.config import LEVELS_JSON_PATH
from src.entities.enemies.enemy_wave import EnemyWave


class Level:
    def __init__(self, enemy_wave_list, path, level_number):
        self.start_time = pygame.time.get_ticks()
        self.enemy_wave_list = enemy_wave_list
        self.path = path
        self.level_number = level_number
        self.active_waves = []
        self.current_wave_index = -1
        #self.level_start_time = level_start_time  # Time when the level started
        self.initialize_wave_start_times()

    def initialize_wave_start_times(self):
        initial_delay = 5000  # 5 seconds in milliseconds for the first wave
        subsequent_delay = 10000  # 10 seconds in milliseconds for subsequent waves

        for i, wave in enumerate(self.enemy_wave_list):
            if i == 0:
                wave.start_time = self.start_time + initial_delay
            else:
                wave.start_time = self.enemy_wave_list[i - 1].start_time + subsequent_delay
    @classmethod
    def from_json(cls, level_data):
        """
        Factory method to create a Level instance from JSON data.
        """
        path = cls.convert_path(level_data['path'])
        enemy_wave_list = [
            EnemyWave.from_json(wave, path) for wave in level_data['enemy_waves']
        ]

        level_number = level_data['level_number']
        return cls(enemy_wave_list, path, level_number)

    @staticmethod
    def convert_path(path_data):
        """
        Converts path data from a list of dictionaries to a list of tuples.

        :param path_data: The path data as a list of dictionaries.
        :return: Path as a list of tuples.
        """
        return [(point['x'], point['y']) for point in path_data]

    def get_next_wave(self):
        """
        Returns the next wave in the level, or None if all waves are completed.
        """
        if self.current_wave_index < len(self.enemy_wave_list)-1:
            self.current_wave_index += 1
            self.active_waves = self.enemy_wave_list[self.current_wave_index]
            return self.active_waves
        return None

    @staticmethod
    def load_levels():
        """
        Load levels from a JSON file.
        """
        with open(LEVELS_JSON_PATH, 'r') as file:
            level_data = json.load(file)
            return [Level.from_json(level) for level in level_data['levels']]

    def is_completed(self):
        # Example condition: all waves are completed
        if self.current_wave_index >= len(self.enemy_wave_list):
            return True
        if not self.enemy_wave_list:
            return True
        return False

    def reset(self):
        """
        Resets the level to its initial state, ready to be started over.
        """
        self.current_wave_index = -1  # Reset the wave index
        self.active_waves = None  # Clear the current wave
        self.start_time = pygame.time.get_ticks()  # Reset the start time

        # Reinitialize the enemy waves
        for wave in self.enemy_wave_list:
            wave.reset()


    def update_level(self, current_time):
        # Check if any upcoming waves can be started (either automatically or by player action)
        for wave in self.enemy_wave_list:
            if not wave.is_active and (wave.start_time <= current_time or wave.manually_started):
                wave.start()
                self.active_waves.append(wave)

        # Update active waves and handle spawning
        new_enemies = []
        for wave in self.active_waves:
            enemies = wave.update(current_time)
            if enemies:
                new_enemies.extend(enemies)
            if wave.is_finished():
                self.active_waves.remove(wave)

        return new_enemies