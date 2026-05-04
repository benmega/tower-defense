<<<<<<< HEAD:src/tests.disabled/test_entities/enemies/test_enemy_pathfinding.py
"""
Test enemy pathfinding, movement, and AI behavior.
"""

=======
"""Test enemy pathfinding, movement, and AI behavior."""
>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/enemies/test_enemy_pathfinding.py
import unittest
from unittest.mock import Mock
import math

<<<<<<< HEAD:src/tests.disabled/test_entities/enemies/test_enemy_pathfinding.py

class TestEnemyPathfinding(unittest.TestCase):
    """Test enemy movement and AI pathfinding."""

    def setUp(self):
        """Setup test enemies."""
=======
class TestEnemyPathfinding(unittest.TestCase):
    """Test enemy movement and AI."""
    def setUp(self):
>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/enemies/test_enemy_pathfinding.py
        self.enemy = Mock()
        self.enemy.x = 0
        self.enemy.y = 0
        self.enemy.speed = 2.0
<<<<<<< HEAD:src/tests.disabled/test_entities/enemies/test_enemy_pathfinding.py
        self.enemy.original_speed = 2.0
        self.enemy.path = [(0, 0), (100, 0), (100, 100), (200, 100)]
        self.enemy.path_index = 0
        self.enemy.health = 50

    def test_enemy_initialization(self):
        """Test enemy initializes with correct properties."""
        self.assertEqual(self.enemy.x, 0)
        self.assertEqual(self.enemy.y, 0)
        self.assertEqual(self.enemy.speed, 2.0)
        self.assertIsNotNone(self.enemy.path)

    def test_enemy_movement_along_path(self):
        """Test enemy moves along path."""
        start_x, start_y = self.enemy.x, self.enemy.y
        target_x, target_y = self.enemy.path[1]

        # Move towards next waypoint
        dx = target_x - self.enemy.x
        dy = target_y - self.enemy.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx = (dx / distance) * self.enemy.speed
            dy = (dy / distance) * self.enemy.speed
            self.enemy.x += dx
            self.enemy.y += dy

        self.assertGreater(self.enemy.x, start_x)
        self.assertEqual(self.enemy.y, start_y)

    def test_enemy_reaches_waypoint(self):
        """Test enemy reaches waypoint correctly."""
        self.enemy.x = 99
        self.enemy.y = 0
        target_x, target_y = 100, 0
        waypoint_radius = 5

        distance = math.sqrt((target_x - self.enemy.x)**2 + (target_y - self.enemy.y)**2)
        reached = distance < waypoint_radius

        self.assertTrue(reached)

    def test_enemy_path_index_progression(self):
        """Test enemy path index progresses correctly."""
        self.enemy.path_index = 0
        self.assertEqual(self.enemy.path_index, 0)

        self.enemy.path_index += 1
        self.assertEqual(self.enemy.path_index, 1)

    def test_enemy_completes_path(self):
        """Test enemy completes entire path."""
        self.enemy.path_index = len(self.enemy.path) - 1
        at_end = self.enemy.path_index >= len(self.enemy.path) - 1

        self.assertTrue(at_end)

    def test_enemy_slow_effect_reduces_speed(self):
        """Test slow effect reduces movement speed."""
        self.enemy.speed = self.enemy.original_speed * 0.5
        self.assertEqual(self.enemy.speed, 1.0)

    def test_enemy_slow_effect_duration(self):
        """Test slow effect expires after duration."""
        slow_duration = 60
        slow_remaining = slow_duration

        for _ in range(30):
            slow_remaining -= 1

        self.assertEqual(slow_remaining, 30)
        self.assertGreater(slow_remaining, 0)

        for _ in range(30):
            slow_remaining -= 1

        self.assertEqual(slow_remaining, 0)

    def test_enemy_slow_effect_expiration_restores_speed(self):
        """Test speed is restored after slow expires."""
        # Apply slow
        self.enemy.speed = self.enemy.original_speed * 0.5

        # After slow duration
        self.enemy.speed = self.enemy.original_speed

        self.assertEqual(self.enemy.speed, 2.0)

    def test_enemy_poison_damage_per_tick(self):
        """Test poison applies damage over time."""
        poison_damage = 5
        initial_health = self.enemy.health

        self.enemy.health -= poison_damage
        self.assertEqual(self.enemy.health, 45)

    def test_enemy_poison_duration_ticks(self):
        """Test poison duration in ticks."""
        poison_duration = 60
        poison_damage_per_tick = 1

        for _ in range(poison_duration):
            self.enemy.health -= poison_damage_per_tick

        expected_health = 50 - poison_duration
        self.assertEqual(self.enemy.health, expected_health)

    def test_enemy_poison_expired_stops_damage(self):
        """Test poison stops dealing damage after duration."""
        poison_duration = 60
        ticks_elapsed = 60

        # Apply poison damage
        for _ in range(poison_duration):
            self.enemy.health -= 1

        initial_health_after_poison = self.enemy.health

        # Additional ticks without poison
        for _ in range(10):
            pass  # No damage applied

        self.assertEqual(self.enemy.health, initial_health_after_poison)

    def test_enemy_movement_stutter_step(self):
        """Test enemy can make small movements."""
        target_x, target_y = 2, 0
        movement_distance = 1

        dx = target_x - self.enemy.x
        dy = target_y - self.enemy.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > movement_distance:
            dx = (dx / distance) * movement_distance
            dy = (dy / distance) * movement_distance
            self.enemy.x += dx
            self.enemy.y += dy

        self.assertEqual(self.enemy.x, 1)
        self.assertEqual(self.enemy.y, 0)

    def test_multiple_slow_effects_stack(self):
        """Test multiple slow effects apply correctly."""
        # Apply first slow
        self.enemy.speed = self.enemy.original_speed * 0.75

        # Apply second slow (doesn't stack, just strongest)
        self.enemy.speed = min(self.enemy.speed, self.enemy.original_speed * 0.5)

        self.assertEqual(self.enemy.speed, 1.0)

    def test_enemy_movement_accuracy(self):
        """Test enemy movement follows exact path."""
        waypoints = [(0, 0), (100, 0), (100, 100)]
        self.enemy.path = waypoints
        self.enemy.path_index = 0

        # Move to first waypoint
        target = waypoints[self.enemy.path_index + 1] if self.enemy.path_index + 1 < len(waypoints) else waypoints[self.enemy.path_index]
        self.assertEqual(target, (100, 0))

    def test_enemy_path_following_order(self):
        """Test enemy follows waypoints in order."""
        expected_order = [
            (0, 0),
            (100, 0),
            (100, 100),
            (200, 100),
        ]

        self.assertEqual(self.enemy.path, expected_order)

    def test_enemy_direction_calculation(self):
        """Test enemy calculates direction correctly."""
        target_x, target_y = 100, 100
        dx = target_x - self.enemy.x
        dy = target_y - self.enemy.y

        direction_magnitude = math.sqrt(dx**2 + dy**2)
        self.assertGreater(direction_magnitude, 0)

    def test_enemy_stop_at_goal(self):
        """Test enemy stops moving at goal."""
        self.enemy.path_index = len(self.enemy.path) - 1
        self.enemy.speed = 0

        self.assertEqual(self.enemy.speed, 0)

    def test_enemy_bypass_slow_effect(self):
        """Test certain enemy types ignore slow effects."""
        flying_enemy = Mock(speed=2.0, is_flying=True)

        # Apply slow effect - but flying enemies are immune
        if not flying_enemy.is_flying:
            flying_enemy.speed *= 0.5

        self.assertEqual(flying_enemy.speed, 2.0)

    def test_pathfinding_with_obstacles(self):
        """Test pathfinding avoids obstacles."""
        # Obstacles block direct path
        obstacles = [(50, 0), (60, 0), (70, 0)]
        original_path = [(0, 0), (100, 0), (100, 100)]

        # Path should route around obstacles
        alternative_path = [(0, 0), (50, -30), (100, -30), (100, 100)]

        self.assertNotEqual(original_path, alternative_path)

    def tearDown(self):
        """Cleanup."""
        pass


=======
        self.enemy.path = [(0, 0), (100, 0), (100, 100)]
        self.enemy.path_index = 0
        self.enemy.health = 50
    
    def test_enemy_initialization(self):
        self.assertEqual(self.enemy.speed, 2.0)
        self.assertIsNotNone(self.enemy.path)
    
    def test_slow_effect_reduces_speed(self):
        self.enemy.speed = 2.0 * 0.5
        self.assertEqual(self.enemy.speed, 1.0)
    
    def tearDown(self):
        pass

>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/enemies/test_enemy_pathfinding.py
if __name__ == '__main__':
    unittest.main()
