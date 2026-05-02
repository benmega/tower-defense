# test_level.py
import unittest
from src.game.level import Level
from src.entities.enemies.enemy_wave import EnemyWave

class MockEnemy:
    def __init__(self, path):
        self.path = path

class TestLevel(unittest.TestCase):
    def setUp(self):
        self.path = [(0, 0), (100, 0), (100, 100)]
        self.enemy_wave_list = [
            EnemyWave(MockEnemy, 10, 1000, self.path, 0),
            EnemyWave(MockEnemy, 5, 2000, self.path, 1)
        ]
        self.level = Level(self.enemy_wave_list, self.path, 1)

    def test_initialization(self):
        """Level should keep waves and path"""
        self.assertEqual(len(self.level.enemy_wave_list), len(self.enemy_wave_list))
        self.assertEqual(self.level.path, self.path)

    def test_enemy_wave_handling(self):
        """get_next_wave should pop waves in order"""
        initial_wave_count = len(self.level.enemy_wave_list)
        next_wave = self.level.get_next_wave()
        self.assertIsInstance(next_wave, EnemyWave)
        self.assertEqual(len(self.level.enemy_wave_list), initial_wave_count - 1)

    def test_level_progression(self):
        """Level should eventually have no waves left"""
        while self.level.enemy_wave_list:
            self.level.get_next_wave()
        self.assertEqual(len(self.level.enemy_wave_list), 0)

if __name__ == '__main__':
    unittest.main()
