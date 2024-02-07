import pygame
import os

def load_scaled_image(path, size):
    # Calculate the absolute path relative to the current script
    current_dir = os.path.dirname(__file__)  # Get the directory where the current script is located
    project_root = os.path.join(current_dir, '../..')  # Adjust this as needed
    absolute_path = os.path.join(project_root, path)  # Construct the absolute path

    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None


