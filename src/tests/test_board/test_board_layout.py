# test_board_layout.py

import unittest
from unittest.mock import Mock, patch
from src.board.game_board import GameBoard


class TestBoardLayout(unittest.TestCase):
    @patch('src.board.game_board.load_scaled_image')
    def setUp(self, mock_load_image):
        """Setup for each test with mocked image loading."""
        mock_load_image.return_value = Mock()
        self.board = GameBoard(10, 10)  # 10x10 grid

    def test_board_initialization(self):
        """Test that the board initializes with correct dimensions."""
        self.assertEqual(self.board.width, 10)
        self.assertEqual(self.board.height, 10)
        self.assertIsNotNone(self.board.grid)
        self.assertEqual(len(self.board.grid), 10)
        self.assertEqual(len(self.board.grid[0]), 10)

    def test_valid_position_check(self):
        """Test boundary checking for valid positions."""
        # Valid positions
        self.assertTrue(self.board.is_valid_position(0, 0))
        self.assertTrue(self.board.is_valid_position(5, 5))
        self.assertTrue(self.board.is_valid_position(9, 9))

        # Invalid positions
        self.assertFalse(self.board.is_valid_position(-1, 0))
        self.assertFalse(self.board.is_valid_position(0, -1))
        self.assertFalse(self.board.is_valid_position(10, 0))
        self.assertFalse(self.board.is_valid_position(0, 10))
        self.assertFalse(self.board.is_valid_position(15, 15))

    def test_tower_placement(self):
        """Test if towers can be placed at specific grid positions."""
        tower = Mock()
        tower.x = 50
        tower.y = 50

        # Place tower at position
        grid_x, grid_y = 1, 1
        self.board.grid[grid_y][grid_x] = tower

        # Verify tower is at that position
        placed_tower = self.board.get_tower_at(grid_x, grid_y)
        self.assertEqual(placed_tower, tower)

    def test_tower_placement_valid_bounds(self):
        """Test tower placement respects board boundaries."""
        tower = Mock()

        # Try to place tower outside bounds
        tower_at_invalid = self.board.get_tower_at(-1, 0)
        self.assertIsNone(tower_at_invalid)

        tower_at_invalid = self.board.get_tower_at(10, 10)
        self.assertIsNone(tower_at_invalid)

    def test_grid_boundaries(self):
        """Test that the board correctly handles entities outside boundaries."""
        # Positions outside grid should return None
        self.assertIsNone(self.board.get_tower_at(-1, 5))
        self.assertIsNone(self.board.get_tower_at(5, -1))
        self.assertIsNone(self.board.get_tower_at(10, 5))
        self.assertIsNone(self.board.get_tower_at(5, 10))

    def test_multiple_tower_placements(self):
        """Test placing multiple towers on the board."""
        towers = [Mock(id=i) for i in range(3)]
        positions = [(0, 0), (5, 5), (9, 9)]

        for tower, (x, y) in zip(towers, positions):
            self.board.grid[y][x] = tower

        # Verify all towers are placed correctly
        self.assertEqual(self.board.get_tower_at(0, 0).id, 0)
        self.assertEqual(self.board.get_tower_at(5, 5).id, 1)
        self.assertEqual(self.board.get_tower_at(9, 9).id, 2)

    def test_tower_replacement(self):
        """Test replacing a tower at the same position."""
        tower1 = Mock(id=1)
        tower2 = Mock(id=2)

        # Place first tower
        self.board.grid[5][5] = tower1
        self.assertEqual(self.board.get_tower_at(5, 5).id, 1)

        # Replace with second tower
        self.board.grid[5][5] = tower2
        self.assertEqual(self.board.get_tower_at(5, 5).id, 2)

    def test_path_creation(self):
        """Test that the board creates a valid path layout."""
        path = [(0, 0), (500, 0), (500, 500)]
        self.board.path = path
        layout = self.board.create_path_layout(path)

        # Should create a non-empty layout
        self.assertIsNotNone(layout)
        self.assertTrue(len(layout) > 0)

    def tearDown(self):
        """Teardown if necessary."""
        pass


if __name__ == '__main__':
    unittest.main()
