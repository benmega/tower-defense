import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.utils.helpers import load_scaled_image
import warnings  # Import at the top of your file


class Screen:
    def __init__(self, ui_manager, background_image_path):
        self.ui_manager = ui_manager
        self.visible = False
        self.ui_elements = []  # List to hold UI elements like buttons
        self.background_image = load_scaled_image(background_image_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = self.create_return_button()  # Create the return button


    def create_return_button(self):
        # Create a button in the top right corner
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([SCREEN_WIDTH - UI_BUTTON_SIZE[0] - 10, 10], UI_BUTTON_SIZE),
            text="Return",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(button)
        return button

    def add_ui_element(self, ui_element):
        self.ui_elements.append(ui_element)

    def open_screen(self):
        self.visible = True
        for element in self.ui_elements:
            try:
                element.visible = True
            except AttributeError as e:
                warnings.warn(f"Attempted to set visibility on an object that doesn't support it: {e}")

    def close_screen(self):
        self.visible = False
        for element in self.ui_elements:
            try:
                element.visible = False
            except AttributeError as e:
                warnings.warn(f"Attempted to set visibility on an object that doesn't support it: {e}")

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.return_button:
                    game.state_manager.change_state(game.previous_state, self)

    def update(self, time_delta):
        if self.visible:
            self.ui_manager.update(time_delta)

    def draw(self, screen):
        if not self.visible:
            return  # Skip drawing if the screen is not active
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        # self.ui_manager.draw_ui(screen)
