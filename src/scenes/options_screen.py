import pygame
import pygame_gui

class OptionsScreen:
    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 425), (100, 50)),
            text='Back',
            manager=self.ui_manager
        )
        # Example options
        self.fullscreen_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text='Toggle Fullscreen',
            manager=self.ui_manager
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    print("Go back to main menu")
                    # TODO: Code to go back to the main menu
                elif event.ui_element == self.fullscreen_toggle:
                    print("Toggle fullscreen mode")
                    # TODO: Code to toggle fullscreen

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self):
        self.ui_manager.draw_ui(self.screen)
