import json

import pygame

from src.screens.screen import Screen
import pygame_gui
from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE

class LoadGameScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "assets/images/screens/load_game_screen.png")
        self.load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect([SCREEN_WIDTH / 2 - UI_BUTTON_SIZE[0] / 2, SCREEN_HEIGHT / 2 - UI_BUTTON_SIZE[1] / 2], UI_BUTTON_SIZE),
                                                        text="Load Game",
                                                        manager=ui_manager,
                                                        visible=False)
        self.add_ui_element(self.load_button)

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.load_button:
                    self.load_game(game)

    def load_game(self, game):
        filename = "src/save_data/savegame.json"
        try:
            with open(filename, 'r') as f:
                player_data = json.load(f)
                # Use this data to set up the game state
                print(player_data)  # For demonstration
                game.player.load_data(player_data)  # Assuming your Game class and Player class have methods to handle this
                self.close_screen()
                game.current_state = game.previous_state  # Assuming you have a way to track and revert to the previous game state
        except FileNotFoundError:
            print("Save file not found.")
