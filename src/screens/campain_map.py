import pygame

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class CampaignMap:
    def __init__(self, screen, ui_manager, player_progress):
        self.isActive = None
        self.screen = screen
        self.ui_manager = ui_manager
        self.level_positions = [
            (766, 700), (787, 678), (864, 681), (879, 645), (781, 630),
            (817, 602), (752, 603), (741, 573), (801, 526), (828, 522),
            (796, 492), (743, 502), (688, 534), (718, 469), (704, 427),
            (645, 413), (592, 382), (546, 372), (560, 358), (410, 380),
            (336, 430), (296, 395), (360, 351), (356, 328), (364, 276),
            (410, 306), (465, 282), (490, 268), (481, 247), (468, 197)
        ]
        self.player_progress = player_progress
        #self.player_progress = {
        #    'unlocked_levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}  # A dictionary or list that tracks player progress
        self.level_buttons = []

        self.map_image = load_scaled_image('assets/images/screens/campaignMap/campaign_map.png',
                                           (SCREEN_WIDTH, SCREEN_HEIGHT))

        for index, position in enumerate(self.level_positions):
            # Assuming you have an `is_level_unlocked` method to check if a level is unlocked
            if self.is_level_unlocked(index):
                button_image = load_scaled_image('assets/images/screens/campaignMap/locked_level.png', (20, 20))
            else:
                button_image = load_scaled_image('assets/images/screens/campaignMap/unlocked_level.png', (20, 20))

            button_rect = button_image.get_rect(topleft=position)
            self.level_buttons.append((button_image, button_rect))

    def is_level_unlocked(self, level_index):
        # Implement your logic to check if a level is unlocked
        return level_index in self.player_progress['unlocked_levels']

    def draw(self):
        self.screen.blit(self.map_image, (0, 0))  # Draw the map

        self.ui_manager.draw_ui(self.screen)
        for button_image, button_rect in self.level_buttons:
            self.screen.blit(button_image, button_rect)  # Draw the level buttons

    def handle_events(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_clicks(event, game)
            # print(event.pos) # for button placement

    def handle_clicks(self, event, game):
        mouse_pos = event.pos
        for index, (button_image, button_rect) in enumerate(self.level_buttons):
            if button_rect.collidepoint(mouse_pos):
                # Logic to start the level, if it's unlocked
                if self.is_level_unlocked(index):
                    game.initialize_game()  # Call initialize_game to set up the game
                    game.level_manager.start_level(index)
                    print(f"Starting level {index}")
                    # Start the level here

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def open_scene(self):
        self.isActive = True

    def close_scene(self):
        self.isActive = False
