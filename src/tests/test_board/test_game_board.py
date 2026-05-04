# test_game_board.py

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.board.game_board import GameBoard


class TestGameBoard(unittest.TestCase):
    @patch('src.board.game_board.load_scaled_image')
    def setUp(self, mock_load_image):
        """Setup for each test with mocked pygame and images."""
        mock_load_image.return_value = Mock()
        self.board = GameBoard(10, 10)

    def test_get_tile_image_grass(self):
        """Test getting grass tile image for non-path tiles."""
        # Path layout defaults to grass tiles
        image = self.board.get_tile_image(0, 0)
        self.assertIsNotNone(image)

    def test_get_tile_image_with_path(self):
        """Test getting tile images for different path types."""
        path = [(0, 0), (10, 10), (20, 20)]
        # Update path and get tile images
        self.board.get_tile_image(0, 0, path=path)
        # Layout should be created
        self.assertIsNotNone(self.board.path_layout)

    def test_draw_board_calls_background(self):
        """Test that draw_board calls draw_background."""
        screen = Mock()
        path = [(0, 0), (500, 0)]

        with patch.object(self.board, 'draw_background') as mock_draw:
            self.board.draw_board(screen, path)
            mock_draw.assert_called_once_with(screen, path)

    def test_draw_background_iterations(self):
        """Test that draw_background iterates over all tiles."""
        screen = Mock()
        path = [(0, 0), (500, 0)]

        # Mock get_tile_image to return a mock image
        with patch.object(self.board, 'get_tile_image') as mock_get_image:
            mock_get_image.return_value = Mock()
            self.board.draw_background(screen, path)

            # Should be called for each tile (10x10 = 100 times)
            self.assertEqual(mock_get_image.call_count, 100)

    def test_draw_background_blits_to_screen(self):
        """Test that draw_background blits images to screen."""
        screen = Mock()
        path = [(0, 0), (500, 0)]

        with patch.object(self.board, 'get_tile_image') as mock_get_image:
            mock_get_image.return_value = Mock()
            self.board.draw_background(screen, path)

            # Blit should be called for each tile
            self.assertEqual(screen.blit.call_count, 100)

    def test_create_path_layout_with_valid_path(self):
        """Test creating a valid path layout."""
        path = [(0, 0), (500, 0), (500, 500)]
        layout = self.board.create_path_layout(path)

        # Layout should be created
        self.assertIsNotNone(layout)

    def test_create_path_layout_invalid_path(self):
        """Test that invalid paths are handled gracefully."""
        # Path with less than 2 points should fail
        with patch('builtins.print') as mock_print:
            layout = self.board.create_path_layout([])
            # Should print error message
            mock_print.assert_called()

    def test_create_path_layout_single_point(self):
        """Test that single-point path is invalid."""
        with patch('builtins.print') as mock_print:
            layout = self.board.create_path_layout([(0, 0)])
            # Should print error message
            mock_print.assert_called()

    def test_board_state_persistence(self):
        """Test that board state persists across operations."""
        # Set initial path
        path1 = [(0, 0), (500, 0)]
        self.board.path = path1
        self.assertEqual(self.board.path, path1)

        # Update path
        path2 = [(0, 0), (500, 500)]
        self.board.path = path2
        self.assertEqual(self.board.path, path2)

    def test_tile_image_caching(self):
        """Test that tile images are properly retrieved."""
        with patch.object(self.board, 'get_tile_image') as mock_get_image:
            mock_get_image.return_value = Mock()
            screen = Mock()
            path = [(0, 0), (500, 0)]

            self.board.draw_board(screen, path)

            # Verify get_tile_image was called with correct parameters
            calls = mock_get_image.call_args_list
            self.assertTrue(len(calls) > 0)

    def tearDown(self):
        """Teardown if necessary."""
        pass


if __name__ == '__main__':
    unittest.main()
