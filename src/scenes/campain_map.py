import pygame

class CampaignMap:
    def __init__(self, screen, map_image_path, level_positions, player_progress):
        self.screen = screen
        self.map_image = pygame.image.load(map_image_path)
        self.level_positions = level_positions  # A list of tuples indicating where levels are on the map
        self.player_progress = player_progress  # A dictionary or list that tracks player progress
        self.level_buttons = []

        for index, position in enumerate(self.level_positions):
            # Assuming you have an `is_level_unlocked` method to check if a level is unlocked
            if self.is_level_unlocked(index):
                button_image = pygame.image.load('path_to_unlocked_level_button.png')
            else:
                button_image = pygame.image.load('path_to_locked_level_button.png')

            button_rect = button_image.get_rect(topleft=position)
            self.level_buttons.append((button_image, button_rect))

    def is_level_unlocked(self, level_index):
        # Implement your logic to check if a level is unlocked
        return level_index in self.player_progress['unlocked_levels']

    def draw(self):
        self.screen.blit(self.map_image, (0, 0))  # Draw the map

        for button_image, button_rect in self.level_buttons:
            self.screen.blit(button_image, button_rect)  # Draw the level buttons

    def handle_click(self, mouse_pos):
        for index, (button_image, button_rect) in enumerate(self.level_buttons):
            if button_rect.collidepoint(mouse_pos):
                # Logic to start the level, if it's unlocked
                if self.is_level_unlocked(index):
                    print(f"Starting level {index}")
                    # Start the level here
