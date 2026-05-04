# test_helpers.py
import unittest
from src.utils import helpers
import os
import pygame

class TestHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Pygame to test image loading
        pygame.init()
        # Ensure there's an example image file in the correct directory for testing
        cls.example_image_path = 'path/to/valid/image.png'
        cls.expected_dimensions = (64, 64)  # Example expected dimensions after scaling

    def test_load_scaled_image(self):
        # Test loading an image with a valid path and scaling it
        if not os.path.exists(self.example_image_path):
            self.fail(f"Test image not found at path: {self.example_image_path}")

        image = helpers.load_scaled_image(self.example_image_path, self.expected_dimensions)
        self.assertIsNotNone(image, "The loaded image should not be None")
        self.assertEqual(image.get_size(), self.expected_dimensions, "The image dimensions should match the expected dimensions")

    def test_other_helper_function(self):
        # This is a placeholder for testing another utility function. Replace 'other_helper_function'
        # and 'expected_result' with actual function name and expected result.
        result = helpers.other_helper_function()
        expected_result = ...
        self.assertEqual(result, expected_result, "The result should match the expected result")

    @classmethod
    def tearDownClass(cls):
        # Quit Pygame when tests are done
        pygame.quit()

# Add more test methods for other helper functions as needed

if __name__ == '__main__':
    unittest.main()
