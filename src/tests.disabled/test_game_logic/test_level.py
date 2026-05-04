# test_level.py
import unittest
from src.game.level import Level
from src.entities.enemies.enemy_wave import EnemyWave


class MockEnemy:
    """Lightweight placeholder enemy class"""
    def __init__(self, path):
        self.path = path


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.path = [(0, 0), (100, 0), (100, 100)]
        self.enemy_wave_list = [
            EnemyWave(MockEnemy, 10, 1000, self.path, 0),
            EnemyWave(MockEnemy, 5, 2000, self.path, 1)
        ]
        self.level = Level(self.enemy_wave_list.copy(), self.path, 1)

    def test_initialization(self):
        """Level should initialize with correct waves and path"""
        self.assertEqual(len(self.level.enemy_wave_list), len(self.enemy_wave_list))
        self.assertEqual(self.level.path, self.path)
        self.assertEqual(self.level.level_number, 1)

    def test_enemy_wave_handling(self):
        """get_next_wave should pop waves in order"""
        initial_count = len(self.level.enemy_wave_list)
        wave1 = self.level.get_next_wave()
        self.assertIsInstance(wave1, EnemyWave)
        self.assertEqual(len(self.level.enemy_wave_list), initial_count - 1)

        wave2 = self.level.get_next_wave()
        self.assertIsInstance(wave2, EnemyWave)
        self.assertEqual(len(self.level.enemy_wave_list), 0)

    def test_get_next_wave_empty(self):
        """get_next_wave should return None if no waves left"""
        # Pop all waves
        self.level.get_next_wave()
        self.level.get_next_wave()
        self.assertEqual(self.level.get_next_wave(), None)

    def test_level_progression(self):
        """Level should eventually be finished after all waves consumed"""
        while self.level.get_next_wave():
            pass
        self.assertEqual(len(self.level.enemy_wave_list), 0)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
