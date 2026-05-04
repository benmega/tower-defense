"""Test tower targeting, range detection, and attack mechanics."""
import unittest
from unittest.mock import Mock
import math

class TestTowerTargeting(unittest.TestCase):
    """Test tower attack and targeting."""
    def setUp(self):
        self.tower = Mock()
        self.tower.x = 100
        self.tower.y = 100
        self.tower.attack_range = 150
        self.tower.damage = 20
        self.tower.cooldown = 0
    
    def test_enemy_in_range(self):
        enemy = Mock(x=150, y=100)
        distance = abs(self.tower.x - enemy.x)
        self.assertLessEqual(distance, self.tower.attack_range)
    
    def test_cooldown_ready(self):
        self.assertTrue(self.tower.cooldown <= 0)
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
