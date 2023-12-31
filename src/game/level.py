import json
from src.entities.enemies.enemy_wave import EnemyWave
from src.config.config import LEVELS_JSON_PATH

class Level:
    def __init__(self, enemy_wave_list, path, level_number):
        self.enemy_wave_list = enemy_wave_list
        self.path = path
        self.level_number = level_number
        self.current_wave_index = 0


    @classmethod
    def from_json(cls, level_data):
        """
        Factory method to create a Level instance from JSON data.
        """
        path = cls.convert_path(level_data['path'])
        enemy_wave_list = [
            EnemyWave.from_json(wave,path) for wave in level_data['enemy_waves']
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
        if self.current_wave_index < len(self.enemy_wave_list):
            wave = self.enemy_wave_list[self.current_wave_index]
            self.current_wave_index += 1
            return wave
        return None

    @staticmethod
    def load_levels():
        """
        Load levels from a JSON file.
        """
        with open(LEVELS_JSON_PATH, 'r') as file:
            level_data = json.load(file)
            return [Level.from_json(level) for level in level_data['levels']]

# Example usage
# levels = Level.load_levels()
