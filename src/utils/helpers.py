import pygame

from src.utils.resource_path import resource_path

# Alias so callers that import get_asset_path continue to work.
get_asset_path = resource_path


def load_scaled_image(path, size):
    if not path or not size:
        return None

    try:
        full_path = resource_path(path)
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {full_path}: {e}")
        return None
