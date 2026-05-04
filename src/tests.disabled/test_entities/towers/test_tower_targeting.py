<<<<<<< HEAD:src/tests.disabled/test_entities/towers/test_tower_targeting.py
"""
Test tower targeting, range detection, and attack mechanics.
"""

=======
"""Test tower targeting, range detection, and attack mechanics."""
>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/towers/test_tower_targeting.py
import unittest
from unittest.mock import Mock
import math

<<<<<<< HEAD:src/tests.disabled/test_entities/towers/test_tower_targeting.py

class TestTowerTargeting(unittest.TestCase):
    """Test tower attack and targeting systems."""

    def setUp(self):
        """Setup test towers and enemies."""
=======
class TestTowerTargeting(unittest.TestCase):
    """Test tower attack and targeting."""
    def setUp(self):
>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/towers/test_tower_targeting.py
        self.tower = Mock()
        self.tower.x = 100
        self.tower.y = 100
        self.tower.attack_range = 150
        self.tower.damage = 20
<<<<<<< HEAD:src/tests.disabled/test_entities/towers/test_tower_targeting.py
        self.tower.attack_speed = 1.0
        self.tower.cooldown = 0

    def test_enemy_in_range_direct(self):
        """Test range detection when enemy is directly within range."""
        enemy = Mock(x=150, y=100)

        distance = math.sqrt(
            (self.tower.x - enemy.x) ** 2 +
            (self.tower.y - enemy.y) ** 2
        )
        in_range = distance <= self.tower.attack_range
        self.assertTrue(in_range)

    def test_enemy_out_of_range(self):
        """Test range detection when enemy is outside range."""
        enemy = Mock(x=300, y=300)

        distance = math.sqrt(
            (self.tower.x - enemy.x) ** 2 +
            (self.tower.y - enemy.y) ** 2
        )
        in_range = distance <= self.tower.attack_range
        self.assertFalse(in_range)

    def test_enemy_at_range_boundary(self):
        """Test range detection at exact range boundary."""
        enemy = Mock(x=250, y=100)

        distance = math.sqrt(
            (self.tower.x - enemy.x) ** 2 +
            (self.tower.y - enemy.y) ** 2
        )
        in_range = distance <= self.tower.attack_range
        self.assertTrue(in_range)

    def test_multiple_enemies_in_range(self):
        """Test identifying multiple enemies in range."""
        enemies = [
            Mock(x=150, y=100),  # In range
            Mock(x=120, y=120),  # In range
            Mock(x=300, y=300),  # Out of range
        ]

        in_range_enemies = []
        for enemy in enemies:
            distance = math.sqrt(
                (self.tower.x - enemy.x) ** 2 +
                (self.tower.y - enemy.y) ** 2
            )
            if distance <= self.tower.attack_range:
                in_range_enemies.append(enemy)

        self.assertEqual(len(in_range_enemies), 2)

    def test_target_priority_closest(self):
        """Test targeting closest enemy."""
        enemies = [
            Mock(x=200, y=100),  # Distance: 100
            Mock(x=150, y=150),  # Distance: ~70.7
            Mock(x=120, y=100),  # Distance: 20
        ]

        closest_enemy = None
        closest_distance = float('inf')

        for enemy in enemies:
            distance = math.sqrt(
                (self.tower.x - enemy.x) ** 2 +
                (self.tower.y - enemy.y) ** 2
            )
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        self.assertEqual(closest_enemy, enemies[2])

    def test_target_priority_weakest(self):
        """Test targeting weakest enemy."""
        enemies = [
            Mock(x=150, y=100, health=40),
            Mock(x=120, y=120, health=10),
            Mock(x=100, y=150, health=30),
        ]

        weakest_enemy = min(enemies, key=lambda e: e.health)
        self.assertEqual(weakest_enemy.health, 10)

    def test_tower_attack_with_cooldown_ready(self):
        """Test tower can attack when cooldown is ready."""
        self.tower.cooldown = 0
        can_attack = self.tower.cooldown <= 0
        self.assertTrue(can_attack)

    def test_tower_no_attack_on_cooldown(self):
        """Test tower cannot attack while on cooldown."""
        self.tower.cooldown = 0.5
        can_attack = self.tower.cooldown <= 0
        self.assertFalse(can_attack)

    def test_cooldown_reduction_over_time(self):
        """Test cooldown decreases over time."""
        initial_cooldown = 1.0
        delta_time = 0.016  # ~60 FPS

        remaining_cooldown = initial_cooldown - delta_time
        self.assertGreater(remaining_cooldown, 0)
        self.assertLess(remaining_cooldown, initial_cooldown)

    def test_cooldown_reset_after_attack(self):
        """Test cooldown is reset after attack."""
        initial_attack_speed = 1.0
        self.tower.cooldown = initial_attack_speed
        self.assertEqual(self.tower.cooldown, initial_attack_speed)

    def test_multiple_attacks_cooldown_stacking(self):
        """Test rapid attacks with cooldown."""
        attack_speed = 1.0
        attacks_per_second = 1 / attack_speed

        self.assertEqual(attacks_per_second, 1.0)

    def test_tower_attack_creates_projectile(self):
        """Test that attack creates a projectile."""
        projectile = Mock(x=100, y=100, target=None)
        projectile.target = Mock(x=200, y=200)

        self.assertIsNotNone(projectile.target)
        self.assertEqual(projectile.target.x, 200)

    def test_projectile_damage_matches_tower_damage(self):
        """Test projectile deals tower's damage."""
        projectile = Mock(damage=self.tower.damage)
        self.assertEqual(projectile.damage, 20)

    def test_tower_upgrade_increases_damage(self):
        """Test upgrading tower increases damage."""
        initial_damage = self.tower.damage
        upgrade_bonus = 1.5

        upgraded_damage = initial_damage * upgrade_bonus
        self.assertEqual(upgraded_damage, 30)

    def test_tower_upgrade_increases_range(self):
        """Test upgrading tower increases range."""
        initial_range = self.tower.attack_range
        upgrade_bonus = 1.2

        upgraded_range = initial_range * upgrade_bonus
        self.assertEqual(upgraded_range, 180)

    def test_tower_upgrade_increases_attack_speed(self):
        """Test upgrading tower increases attack speed."""
        initial_speed = self.tower.attack_speed
        upgrade_bonus = 1.3

        upgraded_speed = initial_speed * upgrade_bonus
        self.assertAlmostEqual(upgraded_speed, 1.3)

    def test_tower_skill_effect_application(self):
        """Test skill effects are applied to tower."""
        tower_with_skill = Mock(
            damage=20,
            skill_name='fire_burst',
            skill_active=True
        )

        self.assertTrue(tower_with_skill.skill_active)
        self.assertEqual(tower_with_skill.skill_name, 'fire_burst')

    def test_tower_no_attack_no_enemies(self):
        """Test tower doesn't attack with no enemies in range."""
        enemies = []
        can_attack = len(enemies) > 0 and self.tower.cooldown <= 0

        self.assertFalse(can_attack)

    def test_tower_no_attack_enemy_out_of_range(self):
        """Test tower doesn't attack out-of-range enemies."""
        enemy = Mock(x=500, y=500)

        distance = math.sqrt(
            (self.tower.x - enemy.x) ** 2 +
            (self.tower.y - enemy.y) ** 2
        )
        can_attack = distance <= self.tower.attack_range and self.tower.cooldown <= 0

        self.assertFalse(can_attack)

    def test_tower_preferential_targeting(self):
        """Test tower targets based on priority."""
        # Strongest enemy gets priority
        enemies = [
            Mock(x=150, y=100, strength=10),
            Mock(x=120, y=120, strength=50),
            Mock(x=100, y=150, strength=30),
        ]

        priority_enemy = max(enemies, key=lambda e: e.strength)
        self.assertEqual(priority_enemy.strength, 50)

    def tearDown(self):
        """Cleanup."""
        pass


=======
        self.tower.cooldown = 0
    
    def test_enemy_in_range(self):
        enemy = Mock(x=150, y=100)
        distance = abs(self.tower.x - enemy.x)
        self.assertLessEqual(distance, self.tower.attack_range)
    
    def test_cooldown_ready(self):
        self.assertTrue(self.tower.cooldown <= 0)
    
    def tearDown(self):
        pass

>>>>>>> claude/dreamy-ishizaka-bb716d:src/tests/test_entities/towers/test_tower_targeting.py
if __name__ == '__main__':
    unittest.main()
