import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen
from src.utils.helpers import load_scaled_image


class CampaignMap(Screen):
    def __init__(self, ui_manager, player_progress):
        super().__init__(ui_manager, 'assets/images/screens/campaignMap/campaign_map.png')
        self.isActive = False
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
        # self.player_progress = {
        #    'unlocked_levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}  # A dictionary or list that tracks player progress
        self.level_buttons = []

        self.map_image = load_scaled_image('assets/images/screens/campaignMap/campaign_map.png',
                                           (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level_visibility = {}  # New d
        self.initilize_buttons()

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([350, 425], UI_BUTTON_SIZE),
            text='Back',
            manager=self.ui_manager,
            visible=False
        )

    def initilize_buttons(self):
        self.level_buttons.clear()
        for index, position in enumerate(self.level_positions):
            unlocked = self.is_level_unlocked(index)
            image_path = 'assets/images/screens/campaignMap/unlocked_level.png' if unlocked else 'assets/images/screens/campaignMap/locked_level.png'
            button_image = load_scaled_image(image_path, (20, 20))  # Adjust as needed
            button_rect = button_image.get_rect(center=position)
            self.level_buttons.append((button_image, button_rect, unlocked))

    def draw(self, screen):
        super().draw(screen)  # Draw the background and UI elements
        for button_image, button_rect, _ in self.level_buttons:
            screen.blit(button_image, button_rect)  # Draw each custom button

    def is_level_unlocked(self, level_index):
        return level_index in self.player_progress['unlocked_levels']

    def handle_events(self, event, game):
        super().handle_events(event,game)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_clicks(event, game)

    def handle_clicks(self, event, game):
        mouse_pos = event.pos
        for index, (_, button_rect, unlocked) in enumerate(self.level_buttons):
            if button_rect.collidepoint(mouse_pos) and unlocked:
                game.initialize_game()  # Set up the game for the selected level
                game.level_manager.start_level(index)
                print(f"Starting level {index}")
                break  # Exit loop after handling the click

    def update_player_progress(self, new_progress):
        self.player_progress = new_progress
        self.initilize_buttons()  # Refresh buttons based on new progress
