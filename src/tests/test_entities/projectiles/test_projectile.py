# test_projectile.py

import unittest
from unittest.mock import Mock
from src.entities.projectiles.projectile import Projectile
from src.entities.enemies.basic_enemy import BasicEnemy

class TestProjectile(unittest.TestCase):
    def setUp(self):
        # Setup a projectile and a mock enemy for each test
        self.enemy = Mock(spec=BasicEnemy)
        self.enemy.x = 100
        self.enemy.y = 100
        self.projectile = Projectile(0, 0, 5, 10, self.enemy)  # Starting at (0, 0), speed 5, damage 10

    def test_initial_state(self):
        # Test initial state of the projectile
        self.assertEqual(self.projectile.x, 0)
        self.assertEqual(self.projectile.y, 0)
        self.assertEqual(self.projectile.state, 'in-flight')

    def test_movement_towards_target(self):
        # Test movement towards the target
        self.projectile.move()
        self.assertNotEqual(self.projectile.x, 0)
        self.assertNotEqual(self.projectile.y, 0)

    def test_hit_target(self):
        # Test hitting the target
        while self.projectile.state == 'in-flight':
            self.projectile.move()
        self.assertEqual(self.projectile.state, 'expired')
        self.assertTrue(self.projectile.hit_target())

    def test_out_of_bounds(self):
        # Test behavior when projectile goes out of bounds
        # Assuming out_of_bounds method checks for some boundary condition
        # For example, let's say if projectile goes beyond 200 units in any direction, it's out of bounds
        for _ in range(50):  # Move the projectile far enough
            self.projectile.move()
        self.assertTrue(self.projectile.out_of_bounds())

    def tearDown(self):
        # Teardown if necessary
        pass

if __name__ == '__main__':
    unittest.main()
