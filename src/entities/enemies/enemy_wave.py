import pygame

from src.config.config import FPS, DEBUG
from src.entities.enemies.basic_enemy import BasicEnemy
from src.entities.enemies.fast_enemy import FastEnemy
from src.entities.enemies.flying_enemy import FlyingEnemy
from src.entities.enemies.healer_enemy import HealerEnemy
from src.entities.enemies.siege_enemy import SiegeEnemy
from src.entities.enemies.stealth_enemy import StealthEnemy
from src.entities.enemies.swarm_enemy import SwarmEnemy
from src.entities.enemies.tank_enemy import TankEnemy


class EnemyWave:
    def __init__(self, enemy_type, count, spawn_interval, path):
        """
        Initialize an enemy wave.

        :param enemy_type: The type of enemy in this wave.
        :param count: The number of enemies in this wave.
        :param spawn_interval: Time interval between enemy spawns. (milliseconds)
        :param path: Walking path.
        """
        self.enemy_type = enemy_type
        self.count = count
        self.spawn_interval = spawn_interval
        self.spawned_count = 0
        self.last_spawn_time = 0
        self.path = path
        self.manually_started = False
        self.is_active = False
        self.start_time = pygame.time.get_ticks() + 10

    def update(self, current_time):
        """
        Update the wave, spawning enemies at the defined interval.

        :param current_time: Current time in the game.
        :return: A list containing an enemy instance if it's time to spawn, else an empty list.
        """

        if self.spawned_count < self.count and current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawned_count += 1
            self.last_spawn_time = current_time
            if DEBUG:
                print(f"Spawning enemy {self.spawned_count}/{self.count}")
            # Wrap the enemy instance in a list before returning
            return [self.enemy_type(self.path)]  # Assumes enemy_type creates an enemy instance
        return []  # Return an empty list if no enemy is spawned

    @classmethod
    def from_json(cls, wave_data, path):
        """
        Factory method to create an EnemyWave instance from JSON data.

        :param wave_data: A dictionary containing wave information.
        :param path: The path for the wave to follow
        """
        enemy_type_str = wave_data['enemy_type']
        count = wave_data['count']
        spawn_interval = wave_data['spawn_interval']

        # Convert enemy_type string to actual class. This requires a mapping from strings to enemy classes.
        enemy_type = cls.get_enemy_class_from_string(enemy_type_str)

        return cls(enemy_type, count, spawn_interval, path)

    @staticmethod
    def get_enemy_class_from_string(enemy_type_str):
        """
        Maps a string to an enemy class.

        :param enemy_type_str: The string representing the enemy type.
        :return: Corresponding enemy class.
        """
        enemy_class_map = {
            'BasicEnemy': BasicEnemy,
            'FastEnemy': FastEnemy,
            'FlyingEnemy': FlyingEnemy,
            'HealerEnemy': HealerEnemy,
            'SiegeEnemy': SiegeEnemy,
            'StealthEnemy': StealthEnemy,
            'SwarmEnemy': SwarmEnemy,
            'TankEnemy': TankEnemy
        }
        return enemy_class_map.get(enemy_type_str, BasicEnemy)  # Default to BasicEnemy if not found'

    def is_finished(self):
        return self.spawned_count == self.count

    def reset(self):
        """
        Resets the enemy wave to its initial state.
        """
        self.spawned_count = 0  # Reset the number of spawned enemies
        self.start_time = pygame.time.get_ticks()  # Reset the start time for the wave
        self.is_active = False  # Set the wave to inactive until it's triggered again

    def start(self):
        self.manually_started = True
        # Set up the wave to start spawning enemies
