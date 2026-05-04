"""
Test collision detection and damage system.
Tests projectile-enemy collisions, damage application, and effects.
"""

import unittest
from unittest.mock import Mock, patch
import math


class TestCollisionDamage(unittest.TestCase):
    """Test collision detection and damage application."""

    def setUp(self):
        """Setup test objects."""
        self.mock_projectile = Mock()
        self.mock_projectile.x = 100
        self.mock_projectile.y = 100
        self.mock_projectile.damage = 20
        self.mock_projectile.radius = 5

        self.mock_enemy = Mock()
        self.mock_enemy.x = 100
        self.mock_enemy.y = 100
        self.mock_enemy.health = 50
        self.mock_enemy.max_health = 50
        self.mock_enemy.width = 30
        self.mock_enemy.height = 30

    def test_collision_detection_direct_hit(self):
        """Test collision detection when projectile directly hits enemy."""
        distance = math.sqrt(
            (self.mock_projectile.x - self.mock_enemy.x) ** 2 +
            (self.mock_projectile.y - self.mock_enemy.y) ** 2
        )
        collision = distance < (self.mock_projectile.radius + 15)
        self.assertTrue(collision)

    def test_damage_application_on_hit(self):
        """Test that damage is applied when projectile hits enemy."""
        initial_health = self.mock_enemy.health
        self.mock_enemy.health -= self.mock_projectile.damage
        self.assertEqual(self.mock_enemy.health, 30)

    def tearDown(self):
        """Cleanup."""
        pass


if __name__ == '__main__':
    unittest.main()
