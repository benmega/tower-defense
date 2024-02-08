import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class OptionsScreen:
    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager
        self.isActive = False
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 425), UI_BUTTON_SIZE),
            text='Back',
            manager=self.ui_manager,
            visible = self.isActive
        )
        # # Example options
        self.fullscreen_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), UI_BUTTON_SIZE),
            text='Toggle Fullscreen',
            manager=self.ui_manager,
            visible = self.isActive
        )
        self.background_image = load_scaled_image('assets/images/screens/options_screen.png',
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
    def handle_events(self, event,game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    print("Go back to main menu")
                    game.current_state = GameState.MAIN_MENU
                    game.main_menu.open_menu()
                    self.close_screen()
                elif event.ui_element == self.fullscreen_toggle:
                    print("Toggle fullscreen mode")
                    # TODO: Code to toggle fullscreen

    def open_screen(self):
        self.isActive = True
        self.fullscreen_toggle.visible = True
        self.back_button.visible = True

    def close_screen(self):
        self.isActive = False
        self.fullscreen_toggle.visible = False
        self.back_button.visible = False
    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.ui_manager.draw_ui(self.screen)
