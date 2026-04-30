import pygame
from src.utils.resource_path import resource_path


def load_scaled_image(path, size):
    if not path or not size:
        return None
    abs_path = resource_path(path)
    try:
        image = pygame.image.load(abs_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {abs_path}: {e}")
        return None
