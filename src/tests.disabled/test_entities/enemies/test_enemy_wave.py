# test_enemy_wave.py

import unittest
from src.entities.enemies.enemy_wave import EnemyWave
from src.entities.enemies.basic_enemy import BasicEnemy

class TestEnemyWave(unittest.TestCase):
    def setUp(self):
        # Setup an enemy wave for each test
        self.enemy_wave = EnemyWave(BasicEnemy, 5, 2)  # 5 enemies with a spawn interval of 2

    def test_initial_state(self):
        # Test initial state of the wave
        self.assertEqual(self.enemy_wave.spawned_count, 0)
        self.assertEqual(self.enemy_wave.last_spawn_time, 0)

    def test_spawn_enemies(self):
        # Test spawning of enemies
        first_enemy = self.enemy_wave.update(2)  # Simulate 2 units of time passing
        self.assertIsNotNone(first_enemy)
        self.assertIsInstance(first_enemy, BasicEnemy)
        self.assertEqual(self.enemy_wave.spawned_count, 1)

        # Simulate more time passing and check for additional spawns
        second_enemy = self.enemy_wave.update(4)
        self.assertIsNotNone(second_enemy)
        self.assertEqual(self.enemy_wave.spawned_count, 2)

    def test_complete_wave(self):
        # Test if the wave correctly completes after all enemies have spawned
        for _ in range(5):
            self.enemy_wave.update(2 * _)
        self.assertEqual(self.enemy_wave.spawned_count, 5)
        self.assertIsNone(self.enemy_wave.update(12))  # No more enemies should spawn

    def test_no_premature_spawn(self):
        # Test that enemies do not spawn before the spawn interval
        self.assertIsNone(self.enemy_wave.update(1))  # Should not spawn at 1 unit of time
        self.assertEqual(self.enemy_wave.spawned_count, 0)

    def tearDown(self):
        # Teardown if necessary
        pass

if __name__ == '__main__':
    unittest.main()
