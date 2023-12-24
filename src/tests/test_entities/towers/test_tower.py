# test_tower.py

import unittest
from unittest.mock import Mock
from src.entities.towers.tower import Tower
from src.entities.enemies.basic_enemy import BasicEnemy

class TestTower(unittest.TestCase):
    def setUp(self):
        # Setup a tower and mock enemies for each test
        self.tower = Tower(x=50, y=50, attack_range=100, damage=10, attack_speed=1)
        self.enemy_in_range = Mock(spec=BasicEnemy)
        self.enemy_in_range.x = 60
        self.enemy_in_range.y = 60
        self.enemy_out_of_range = Mock(spec=BasicEnemy)
        self.enemy_out_of_range.x = 200
        self.enemy_out_of_range.y = 200

    def test_is_enemy_in_range(self):
        # Test if the tower correctly identifies an enemy in range
        self.assertTrue(self.tower.is_enemy_in_range(self.enemy_in_range))
        self.assertFalse(self.tower.is_enemy_in_range(self.enemy_out_of_range))

    def test_attack(self):
        # Test tower's attack on an enemy
        self.tower.attack(self.enemy_in_range, [])
        self.enemy_in_range.take_damage.assert_called_with(self.tower.damage)

    def test_cooldown_after_attack(self):
        # Test cooldown period after an attack
        self.tower.update([self.enemy_in_range], [])
        self.assertEqual(self.tower.cooldown, self.tower.attack_speed)

    def test_no_attack_on_cooldown(self):
        # Test that tower does not attack while on cooldown
        self.tower.cooldown = 1  # Setting cooldown to a non-zero value
        self.tower.update([self.enemy_in_range], [])
        self.enemy_in_range.take_damage.assert_not_called()

    def tearDown(self):
        # Teardown if necessary
        pass

if __name__ == '__main__':
    unittest.main()
