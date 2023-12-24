# test_basic_enemy.py

import unittest
from src.entities.enemies.basic_enemy import BasicEnemy

class TestBasicEnemy(unittest.TestCase):
    def setUp(self):
        # Setup a basic enemy instance for each test
        self.path = [(0, 0), (10, 0), (10, 10)]
        self.enemy = BasicEnemy(100, 1, self.path)

    def test_initial_position(self):
        # Test if the enemy is correctly positioned at the start of the path
        self.assertEqual(self.enemy.x, self.path[0][0])
        self.assertEqual(self.enemy.y, self.path[0][1])

    def test_movement(self):
        # Test if the enemy moves along the path
        self.enemy.move()
        self.assertNotEqual((self.enemy.x, self.enemy.y), self.path[0])

    def test_health_reduction(self):
        # Test if health reduces correctly when taking damage
        initial_health = self.enemy.health
        self.enemy.take_damage(10)
        self.assertEqual(self.enemy.health, initial_health - 10)

    def test_death(self):
        # Test if enemy correctly dies when health reaches zero
        self.enemy.take_damage(self.enemy.health)
        self.assertEqual(self.enemy.health, 0)
        self.assertEqual(self.enemy.state, 'dead')

    def test_reached_goal(self):
        # Test if the enemy correctly identifies reaching the end of the path
        for _ in range(len(self.path)):
            self.enemy.move()
        self.assertEqual(self.enemy.state, 'idle')

    def tearDown(self):
        # Teardown if necessary
        pass

if __name__ == '__main__':
    unittest.main()
