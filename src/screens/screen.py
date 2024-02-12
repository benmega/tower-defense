from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.utils.helpers import load_scaled_image


class Screen:
    def __init__(self, screen, ui_manager, background_image_path):
        self.screen = screen
        self.ui_manager = ui_manager
        self.isActive = False
        self.ui_elements = []  # List to hold UI elements like buttons
        self.background_image = load_scaled_image(background_image_path, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def add_ui_element(self, ui_element):
        self.ui_elements.append(ui_element)

    def open_screen(self):
        self.isActive = True
        for element in self.ui_elements:
            element.visible = True

    def close_screen(self):
        self.isActive = False
        for element in self.ui_elements:
            element.visible = False

    def handle_events(self, event, game):
        raise NotImplementedError("handle_events must be implemented by subclasses.")

    def update(self, time_delta):
        if self.isActive:
            self.ui_manager.update(time_delta)

    def draw(self):
        if self.isActive:
            self.screen.blit(self.background_image, (0, 0))
            self.ui_manager.draw_ui(self.screen)
