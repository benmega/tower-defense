import pygame_gui
import pygame

from src.config.config import UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen


class OptionsScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, 'assets/images/screens/options_screen.png')
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([350, 425], UI_BUTTON_SIZE),
            text='Back',
            manager=self.ui_manager,
            visible=False
        )
        self.fullscreen_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([350, 275], UI_BUTTON_SIZE),
            text='Toggle Fullscreen',
            manager=self.ui_manager,
            visible=False
        )
        # Register UI elements with the base class
        self.add_ui_element(self.back_button)
        self.add_ui_element(self.fullscreen_toggle)

    def handle_events(self, event, game):
        super().handle_events(event, game)
        # Directly handle events here without calling super().handle_events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    # Handle back button press
                    game.change_state(GameState.MAIN_MENU)
                    self.close_screen()
                elif event.ui_element == self.fullscreen_toggle:
                    # Handle fullscreen toggle
                    print("Toggle fullscreen mode")