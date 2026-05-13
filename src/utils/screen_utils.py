import pygame


def capture_screen():
    """Capture and return a copy of the current display surface."""
    return pygame.display.get_surface().copy()
