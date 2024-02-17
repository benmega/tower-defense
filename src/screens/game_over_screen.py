import pygame_gui
import pygame

from src.config.config import UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen


class GameOverScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, 'assets/images/screens/defeat_screen.png')
        self.retry_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([350, 325], UI_BUTTON_SIZE),
            text='Retry',
            manager=self.ui_manager,
            visible=False
        )
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([350, 425], UI_BUTTON_SIZE),
            text='Main Menu',
            manager=self.ui_manager,
            visible=False
        )

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.retry_button:
                    print("Retrying level...")
                    game.retry_level()  # Assuming you implement this method
                    self.close_screen()
                elif event.ui_element == self.main_menu_button:
                    print("Returning to main menu...")
                    game.change_state(GameState.MAIN_MENU)
                    self.close_screen()
