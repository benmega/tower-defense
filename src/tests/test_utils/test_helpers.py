# test_helpers.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.utils import helpers
import os


class TestHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize Pygame to test image loading."""
        # Import pygame from mocked version
        import sys
        if 'pygame' not in sys.modules:
            sys.modules['pygame'] = MagicMock()

    def test_resource_path_dev_mode(self):
        """Test resource_path function in development mode."""
        # In dev mode, frozen should be False
        with patch('sys.frozen', False, create=True):
            path = helpers.resource_path('src/config/theme.json')
            # Path should contain the relative path
            self.assertIn('src', path)
            self.assertIn('config', path)

    def test_resource_path_with_relative_path(self):
        """Test resource_path with various relative paths."""
        paths_to_test = [
            'assets/images/grass.png',
            'src/config/theme.json',
            'data/levels.json'
        ]

        for relative_path in paths_to_test:
            path = helpers.resource_path(relative_path)
            self.assertIsNotNone(path)
            self.assertIn(relative_path, path)

    def test_load_scaled_image_with_valid_inputs(self):
        """Test load_scaled_image with valid path and size."""
        with patch('src.utils.helpers.pygame.image.load') as mock_load:
            with patch('src.utils.helpers.pygame.transform.scale') as mock_scale:
                mock_image = Mock()
                mock_load.return_value = mock_image
                mock_scaled = Mock()
                mock_scale.return_value = mock_scaled

                result = helpers.load_scaled_image('assets/images/grass.png', (64, 64))
                self.assertEqual(result, mock_scaled)
                mock_load.assert_called_once()
                mock_scale.assert_called_once()

    def test_load_scaled_image_with_none_path(self):
        """Test load_scaled_image returns None for invalid path."""
        result = helpers.load_scaled_image(None, (64, 64))
        self.assertIsNone(result)

    def test_load_scaled_image_with_none_size(self):
        """Test load_scaled_image returns None for invalid size."""
        result = helpers.load_scaled_image('assets/images/grass.png', None)
        self.assertIsNone(result)

    def test_load_scaled_image_with_none_path_and_size(self):
        """Test load_scaled_image returns None when both path and size are None."""
        result = helpers.load_scaled_image(None, None)
        self.assertIsNone(result)

    def test_load_scaled_image_error_handling(self):
        """Test load_scaled_image handles pygame errors gracefully."""
        import sys
        pygame_mock = sys.modules.get('pygame', MagicMock())

        with patch('src.utils.helpers.pygame.image.load') as mock_load:
            # Simulate a pygame error
            if hasattr(pygame_mock, 'error'):
                mock_load.side_effect = pygame_mock.error("File not found")

            with patch('builtins.print') as mock_print:
                result = helpers.load_scaled_image('invalid/path.png', (64, 64))
                # Should return None and print error
                self.assertIsNone(result)

    def test_load_scaled_image_scaling_called(self):
        """Test that pygame.transform.scale is called with correct dimensions."""
        with patch('src.utils.helpers.pygame.image.load') as mock_load:
            with patch('src.utils.helpers.pygame.transform.scale') as mock_scale:
                mock_image = Mock()
                mock_load.return_value = mock_image
                mock_scale.return_value = Mock()

                size = (128, 128)
                helpers.load_scaled_image('assets/test.png', size)

                # Verify scale was called with the original image and the correct size
                mock_scale.assert_called_once_with(mock_image, size)

    def test_load_scaled_image_returns_scaled_image(self):
        """Test that load_scaled_image returns the scaled image."""
        with patch('src.utils.helpers.pygame.image.load') as mock_load:
            with patch('src.utils.helpers.pygame.transform.scale') as mock_scale:
                mock_image = Mock()
                mock_load.return_value = mock_image
                mock_scaled_image = Mock()
                mock_scale.return_value = mock_scaled_image

                result = helpers.load_scaled_image('assets/test.png', (64, 64))

                self.assertEqual(result, mock_scaled_image)

    @classmethod
    def tearDownClass(cls):
        """Cleanup after tests."""
        pass


if __name__ == '__main__':
    unittest.main()
