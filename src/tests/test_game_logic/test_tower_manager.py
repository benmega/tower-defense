# test_tower_manager.py
import unittest
from src.game.tower_manager import TowerManager
from src.entities.towers.tower import Tower

class TestTowerManager(unittest.TestCase):
    def setUp(self):
        # Setup a TowerManager instance for each test
        self.tower_manager = TowerManager()

    def test_add_tower(self):
        # Test adding a tower
        tower = Tower(x=5, y=5, attack_range=100, damage=10, attack_speed=1)
        self.tower_manager.add_tower(tower)
        self.assertIn(tower, self.tower_manager.towers)
        # TODO: Add more assertions to check if the tower is added correctly

    def test_remove_tower(self):
        # Test removing a tower
        tower = Tower(x=5, y=5, attack_range=100, damage=10, attack_speed=1)
        self.tower_manager.add_tower(tower)
        self.tower_manager.remove_tower(tower)
        self.assertNotIn(tower, self.tower_manager.towers)
        # TODO: Add more tests for removing towers, including edge cases

    def test_update_towers(self):
        # Test updating towers, like their attack logic
        # TODO: Setup scenarios for updating towers and add assertions

    def tearDown(self):
        # Teardown if necessary
        pass

if __name__ == '__main__':
    unittest.main()
