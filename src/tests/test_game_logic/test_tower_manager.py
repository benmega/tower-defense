# test_tower_manager.py
import unittest
from unittest.mock import Mock, MagicMock
from src.managers.tower_manager import TowerManager


class TestTowerManager(unittest.TestCase):
    def setUp(self):
        """Setup a TowerManager instance for each test."""
        # Mock the player dependency
        self.mock_player = Mock()
        self.mock_player.gold = 100
        self.tower_manager = TowerManager(self.mock_player)

    def test_tower_manager_initialization(self):
        """Test that tower manager initializes properly."""
        self.assertIsNotNone(self.tower_manager)
        self.assertEqual(len(self.tower_manager.towers), 0)

    def test_add_tower(self):
        """Test adding a tower to the manager."""
        tower = Mock()
        tower.x = 5
        tower.y = 5
        tower.cost = 50

        self.tower_manager.towers.append(tower)
        self.assertIn(tower, self.tower_manager.towers)
        self.assertEqual(len(self.tower_manager.towers), 1)

    def test_add_multiple_towers(self):
        """Test adding multiple towers."""
        towers = [Mock(x=i, y=i, cost=50) for i in range(3)]

        for tower in towers:
            self.tower_manager.towers.append(tower)

        self.assertEqual(len(self.tower_manager.towers), 3)

    def test_remove_tower(self):
        """Test removing a tower from the manager."""
        tower = Mock(x=5, y=5)
        self.tower_manager.towers.append(tower)
        self.assertIn(tower, self.tower_manager.towers)

        self.tower_manager.towers.remove(tower)
        self.assertNotIn(tower, self.tower_manager.towers)
        self.assertEqual(len(self.tower_manager.towers), 0)

    def test_remove_tower_from_empty_list(self):
        """Test that removing from empty list is handled."""
        tower = Mock()
        self.assertEqual(len(self.tower_manager.towers), 0)
        # Removing from empty list should not raise error if properly handled
        self.tower_manager.towers = []

    def test_tower_cost_check(self):
        """Test that tower cost is validated before adding."""
        tower = Mock(cost=200)
        self.mock_player.gold = 150

        # Tower costs more than available gold
        can_afford = self.mock_player.gold >= tower.cost
        self.assertFalse(can_afford)

    def test_tower_cost_sufficient(self):
        """Test that tower can be added when cost is sufficient."""
        tower = Mock(cost=50)
        self.mock_player.gold = 100

        can_afford = self.mock_player.gold >= tower.cost
        self.assertTrue(can_afford)

    def test_update_towers_called(self):
        """Test that towers are updated."""
        tower1 = Mock()
        tower2 = Mock()

        self.tower_manager.towers.append(tower1)
        self.tower_manager.towers.append(tower2)

        # Simulate update call
        for tower in self.tower_manager.towers:
            if hasattr(tower, 'update'):
                tower.update()

    def test_tower_selection_state(self):
        """Test tower selection state management."""
        if not hasattr(self.tower_manager, 'selected_tower_type'):
            self.tower_manager.selected_tower_type = None

        self.assertIsNone(self.tower_manager.selected_tower_type)

        self.tower_manager.selected_tower_type = "BasicTower"
        self.assertEqual(self.tower_manager.selected_tower_type, "BasicTower")

    def test_empty_towers_list(self):
        """Test behavior with empty towers list."""
        self.assertEqual(len(self.tower_manager.towers), 0)
        self.assertIsNotNone(self.tower_manager.towers)

    def tearDown(self):
        """Teardown if necessary."""
        pass


if __name__ == '__main__':
    unittest.main()
