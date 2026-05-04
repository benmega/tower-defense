import unittest
from unittest.mock import Mock, patch

import pygame

from src.entities.entity import Entity


class TestEntityCoordinateContract(unittest.TestCase):
    def _mock_image_loader(self, *_args, **_kwargs):
        mock_image = Mock()
        surface = pygame.Surface((16, 16))
        mock_image.convert_alpha.return_value = surface
        return mock_image

    def test_x_y_alias_rect_coordinates(self):
        with patch("src.entities.entity.load_scaled_image", side_effect=self._mock_image_loader):
            entity = Entity(10, 20, "unused.png")

        self.assertEqual(entity.rect.topleft, (10, 20))
        self.assertEqual((entity.x, entity.y), (10, 20))

        entity.x = 30
        entity.y = 40

        self.assertEqual(entity.rect.topleft, (30, 40))
        self.assertEqual((entity.x, entity.y), (30, 40))

    def test_draw_uses_rect_position_authority(self):
        with patch("src.entities.entity.load_scaled_image", side_effect=self._mock_image_loader):
            entity = Entity(0, 0, "unused.png")

        entity.rect.topleft = (25, 35)
        screen = Mock()

        entity.draw(screen)

        screen.blit.assert_called_once_with(entity.image, (25, 35))


if __name__ == "__main__":
    unittest.main()
