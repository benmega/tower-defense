import pygame
import pygame_gui

from src.config.config import DEFAULT_GRID_SIZE, UI_FONT_COLOR, UI_SCORE_POSITION, UI_HEALTH_POSITION, \
    UI_RESOURCES_POSITION


class UIManager(pygame_gui.UIManager):
    def __init__(self, window_resolution):
        # Initialize the base UIManager with the window resolution
        super().__init__(window_resolution)

        self.score = 0
        self.health = 100  # Example starting health
        self.resources = 1000  # Example starting resources

        # Initialize font module and create a font object
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def add_ui_element(self, ui_element):
        """ Adds a new UI element to the manager. """
        self.ui_elements.append(ui_element)

    def update_ui(self, game_state):
        """ Updates all UI elements based on the current game state. """
        self.update_score(game_state.player.score)
        self.update_health(game_state)
        self.update_resources(game_state.player.gold)
        # Additional updates based on game_state

    def draw_ui(self, screen):
        # Draw all pygame_gui elements
        super().draw_ui(screen)

        # Draw custom UI elements
        self.draw_score(screen)
        self.draw_health(screen)
        self.draw_resources(screen)

    def update_score(self, score):
        """ Updates the score based on the game state. """
        self.score = score


    def draw_score(self, screen):
        """ Draws the score on the screen. """
        score_text = f"Score: {self.score}"  # Text to be displayed
        score_surface = self.font.render(score_text, True, UI_FONT_COLOR)  # Render the text. (255, 255, 255) is white color

        # Blit the score surface onto the screen
        screen.blit(score_surface, UI_SCORE_POSITION)

    def update_health(self, game_state):
        """ Updates the player's health based on the game state. """
        self.health = game_state.health

    def draw_health(self, screen):
        health_text = f"Health: {self.health}"
        health_surface = self.font.render(health_text, True, UI_FONT_COLOR)
        health_position = (10, 50)  # Adjust position as needed
        screen.blit(health_surface, UI_HEALTH_POSITION)


    def update_resources(self, resources):
        """ Updates the player's resources based on the game state. """
        self.resources = resources

    def draw_resources(self, screen):
        resources = self.resources
        resources_text = f"Resources: {resources}"
        resources_surface = self.font.render(resources_text, True, UI_FONT_COLOR)
        screen.blit(resources_surface, UI_RESOURCES_POSITION)


    # Additional methods for managing UI elements, such as button clicks, menu interactions, etc.

