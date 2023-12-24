import pygame

class ScreenManager:
    def __init__(self):
        self.current_screen = None
        self.screens = {}

    def register_screen(self, screen_name, screen):
        """ Registers a new screen with the manager. """
        self.screens[screen_name] = screen

    def switch_to_screen(self, screen_name):
        """ Switches to the specified screen. """
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]
            self.current_screen.on_enter()  # Handle any initialization needed when entering the screen

    def update(self):
        """ Updates the current screen. """
        if self.current_screen:
            self.current_screen.update()

    def draw(self, screen):
        """ Draws the current screen. """
        if self.current_screen:
            self.current_screen.draw(screen)

    def handle_events(self, events):
        """ Passes events to the current screen for handling. """
        if self.current_screen:
            self.current_screen.handle_events(events)

    def on_exit(self):
        """ Handles any cleanup when exiting a screen. """
        if self.current_screen:
            self.current_screen.on_exit()
