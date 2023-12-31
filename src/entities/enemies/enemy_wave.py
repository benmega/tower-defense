from src.entities.enemies.basic_enemy import BasicEnemy


class EnemyWave:
    def __init__(self, enemy_type, count, spawn_interval, path):
        """
        Initialize an enemy wave.

        :param enemy_type: The type of enemy in this wave.
        :param count: The number of enemies in this wave.
        :param spawn_interval: Time interval between enemy spawns.
        :param path: Walking path. TODO Make this part of level or path_manager class
        """
        self.enemy_type = enemy_type
        self.count = count
        self.spawn_interval = spawn_interval
        self.spawned_count = 0
        self.last_spawn_time = 0
        self.path = path

    def update(self, current_time):
        """
        Update the wave, spawning enemies at the defined interval.

        :param current_time: Current time in the game.
        :return: An enemy instance if it's time to spawn, else None.
        """
        if self.spawned_count < self.count and current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawned_count += 1
            self.last_spawn_time = current_time
            print(f"Spawning enemy {self.spawned_count}/{self.count}")
            return self.enemy_type(self.path)  # Assumes enemy_type creates an enemy instance
        return None

    @classmethod
    def from_json(cls, wave_data, path):
        """
        Factory method to create an EnemyWave instance from JSON data.

        :param wave_data: A dictionary containing wave information.
        """
        # Assuming wave_data is a dictionary with keys like 'enemy_type', 'count', etc.
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
            # Add other mappings here...
        }
        return enemy_class_map.get(enemy_type_str, BasicEnemy)  # Default to BasicEnemy if not found