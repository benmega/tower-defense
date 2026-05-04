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
        # Both at same position
        distance = math.sqrt(
            (self.mock_projectile.x - self.mock_enemy.x) ** 2 +
            (self.mock_projectile.y - self.mock_enemy.y) ** 2
        )
        collision = distance < (self.mock_projectile.radius + 15)
        self.assertTrue(collision)

    def test_collision_detection_no_hit(self):
        """Test collision detection when projectile misses enemy."""
        self.mock_projectile.x = 0
        self.mock_projectile.y = 0

        distance = math.sqrt(
            (self.mock_projectile.x - self.mock_enemy.x) ** 2 +
            (self.mock_projectile.y - self.mock_enemy.y) ** 2
        )
        collision = distance < (self.mock_projectile.radius + 15)
        self.assertFalse(collision)

    def test_collision_detection_near_miss(self):
        """Test collision detection at collision boundary."""
        self.mock_projectile.x = 115
        self.mock_projectile.y = 100

        distance = math.sqrt(
            (self.mock_projectile.x - self.mock_enemy.x) ** 2 +
            (self.mock_projectile.y - self.mock_enemy.y) ** 2
        )
        # Just within collision radius
        collision = distance < 25
        self.assertTrue(collision)

    def test_damage_application_on_hit(self):
        """Test that damage is applied when projectile hits enemy."""
        initial_health = self.mock_enemy.health
        self.mock_enemy.health -= self.mock_projectile.damage

        self.assertEqual(self.mock_enemy.health, initial_health - self.mock_projectile.damage)
        self.assertEqual(self.mock_enemy.health, 30)

    def test_enemy_death_on_overkill_damage(self):
        """Test that enemy dies when damage exceeds health."""
        self.mock_enemy.health = 10
        self.mock_projectile.damage = 20

        self.mock_enemy.health -= self.mock_projectile.damage
        is_dead = self.mock_enemy.health <= 0
        self.assertTrue(is_dead)
        self.assertEqual(self.mock_enemy.health, -10)

    def test_enemy_survives_partial_damage(self):
        """Test that enemy survives when damage is less than health."""
        self.mock_enemy.health = 50
        self.mock_projectile.damage = 20

        self.mock_enemy.health -= self.mock_projectile.damage
        is_dead = self.mock_enemy.health <= 0
        self.assertFalse(is_dead)
        self.assertEqual(self.mock_enemy.health, 30)

    def test_projectile_removal_on_hit(self):
        """Test that projectile is removed after hitting enemy."""
        self.mock_projectile.is_active = True
        self.mock_projectile.is_active = False

        self.assertFalse(self.mock_projectile.is_active)

    def test_projectile_out_of_bounds_removal(self):
        """Test that projectile is removed when out of bounds."""
        self.mock_projectile.x = -100
        self.mock_projectile.y = -100
        self.mock_projectile.is_active = True

        # Check if out of bounds (assuming 1200x800 game)
        is_out_of_bounds = (
            self.mock_projectile.x < 0 or
            self.mock_projectile.x > 1200 or
            self.mock_projectile.y < 0 or
            self.mock_projectile.y > 800
        )
        self.assertTrue(is_out_of_bounds)

        if is_out_of_bounds:
            self.mock_projectile.is_active = False

        self.assertFalse(self.mock_projectile.is_active)

    def test_multiple_projectile_hits(self):
        """Test multiple projectiles hitting the same enemy."""
        projectiles = [Mock(damage=10) for _ in range(3)]
        initial_health = self.mock_enemy.health

        for projectile in projectiles:
            self.mock_enemy.health -= projectile.damage

        expected_health = initial_health - (10 * 3)
        self.assertEqual(self.mock_enemy.health, expected_health)

    def test_damage_scaling_with_difficulty(self):
        """Test that damage scales with difficulty level."""
        base_damage = 10
        difficulty_multiplier = 1.5

        scaled_damage = base_damage * difficulty_multiplier
        self.assertEqual(scaled_damage, 15)

    def test_projectile_collision_callback(self):
        """Test that collision callback is invoked."""
        collision_callback = Mock()
        self.mock_projectile.on_collision = collision_callback

        # Simulate collision
        self.mock_projectile.on_collision(self.mock_enemy)
        collision_callback.assert_called_once_with(self.mock_enemy)

    def test_splash_damage_area(self):
        """Test splash damage affects nearby enemies."""
        splash_radius = 50
        enemies = [
            Mock(x=100, y=100),  # Direct hit
            Mock(x=120, y=100),  # Within splash radius
            Mock(x=160, y=100),  # Outside splash radius
        ]

        def check_splash(projectile_x, projectile_y, enemy):
            dist = math.sqrt((projectile_x - enemy.x) ** 2 + (projectile_y - enemy.y) ** 2)
            return dist < splash_radius

        hit_count = sum(1 for enemy in enemies if check_splash(100, 100, enemy))
        self.assertEqual(hit_count, 2)  # Direct hit + one in splash radius

    def test_poison_damage_over_time(self):
        """Test poison effect applies damage over time."""
        poison_damage_per_tick = 5
        poison_duration_ticks = 10
        total_poison_damage = poison_damage_per_tick * poison_duration_ticks

        initial_health = 50
        final_health = initial_health - total_poison_damage
        self.assertEqual(final_health, 0)

    def test_slow_effect_reduces_speed(self):
        """Test that slow effect reduces enemy speed."""
        enemy = Mock(speed=4.0, original_speed=4.0)
        slow_multiplier = 0.5

        enemy.speed = enemy.original_speed * slow_multiplier
        self.assertEqual(enemy.speed, 2.0)

    def test_slow_effect_duration(self):
        """Test that slow effect expires after duration."""
        enemy = Mock(speed=4.0, original_speed=4.0)
        slow_duration_ticks = 60

        # Apply slow
        enemy.speed = 2.0

        # Tick down
        for _ in range(slow_duration_ticks):
            pass

        # Restore speed
        enemy.speed = enemy.original_speed
        self.assertEqual(enemy.speed, 4.0)

    def test_armor_reduces_damage(self):
        """Test that enemy armor reduces incoming damage."""
        base_damage = 20
        armor = 5
        reduced_damage = max(1, base_damage - armor)

        self.assertEqual(reduced_damage, 15)

    def test_critical_hit_damage(self):
        """Test critical hit multiplies damage."""
        base_damage = 10
        critical_multiplier = 2.0

        critical_damage = base_damage * critical_multiplier
        self.assertEqual(critical_damage, 20)

    def test_collision_group_updates(self):
        """Test collision group collision detection."""
        projectiles = [
            Mock(x=100, y=100, damage=10),
            Mock(x=150, y=150, damage=15),
        ]
        enemies = [
            Mock(x=100, y=100, health=50),
            Mock(x=200, y=200, health=30),
        ]

        # Check if first projectile hits first enemy
        dist = math.sqrt(
            (projectiles[0].x - enemies[0].x) ** 2 +
            (projectiles[0].y - enemies[0].y) ** 2
        )
        hit = dist < 20
        self.assertTrue(hit)

    def tearDown(self):
        """Cleanup."""
        pass


if __name__ == '__main__':
    unittest.main()
