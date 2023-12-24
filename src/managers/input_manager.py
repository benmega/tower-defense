#import_manager.py

import pygame


class InputManager:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.mouse_position = (0, 0)
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.keys_pressed = pygame.key.get_pressed()

    def update(self):
        # Update input states
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.keys_pressed = pygame.key.get_pressed()

        # Check for specific inputs and trigger events
        self.check_mouse_input()
        self.check_keyboard_input()

    def check_mouse_input(self):
        """ Check mouse input and trigger corresponding events. """
        if self.mouse_buttons[0]:  # Left click
            # Example: Trigger an event for tower placement or selection
            self.event_manager.add_event({'type': 'build_tower', 'position': self.mouse_position})

    def check_keyboard_input(self):
        """ Check keyboard input and trigger corresponding events. """
        if self.keys_pressed[pygame.K_p]:  # Press 'P' to pause
            self.event_manager.add_event({'type': 'pause_game'})

        # Add more key checks as needed

    # Additional methods for handling specific input types
