import pygame_gui
import pygame
from src.game.player_info_panel import PlayerInfoPanel
from src.screens.campain_map import CampaignMap
from src.screens.level_completion import LevelCompletionScreen
from src.screens.main_menu import MainMenu
from src.screens.game_data_screen import GameDataScreen
from src.screens.options_screen import OptionsScreen
from src.screens.skills_screen import SkillsScreen


def capture_screen():
    # Capture the current display surface
    return pygame.display.get_surface().copy()


class UIManager(pygame_gui.UIManager):
    def __init__(self, window_size, theme_path, game):
        super().__init__(window_size, theme_path)

        # Ensure 'game.screen' is already initialized in the Game class before passing it here
        self.screen = game.screen

        # Initialize screens with necessary parameters
        self.main_menu = MainMenu(self.screen, self)
        self.game_data_screen = GameDataScreen(self)
        self.campaign_map = CampaignMap(self, [0])  # Pass relevant initialization parameters
        self.level_end_screen = LevelCompletionScreen(ui_manager=self, screen_type='defeat')
        self.player_info_panel = PlayerInfoPanel(self, game.player, self.screen)
        self.skills_screen = SkillsScreen(self, game.player)
        self.options_screen = OptionsScreen(self, game.audio_manager)

        # Dictionary for managing custom screens
        self.custom_screens = {
            'main_menu': self.main_menu,
            'options_screen': self.options_screen,
            'game_data_screen': self.game_data_screen,
            'campaign_map': self.campaign_map,
            'level_end_screen': self.level_end_screen,
            'skills_screen': self.skills_screen
            # Add other screens as necessary
        }


    def set_screen(self, screen):
        self.screen = screen
        # Make sure to pass the screen to the components that need it
        self.main_menu.set_screen(screen)  # Implement a set_screen method in MainMenu or directly assign if public
        # Similarly, update other components that require the screen

    def show_main_menu(self):
        self.main_menu.visible = True
        # Hide other components as necessary

    def hide_main_menu(self):
        self.main_menu.visible = False

    def draw_ui(self, screen):
        # Iterate through custom screens and draw if visible
        for screen_name, custom_screen in self.custom_screens.items():
            if getattr(custom_screen, 'visible', False):
                custom_screen.draw(screen)

        super().draw_ui(screen)

    def update(self, time_delta):
        super().update(time_delta)
        # Update custom UI components if necessary

    def show_screen(self, screen_name):
        # Hide all screens first
        self.hide_all_screens()

        # Now, show the requested screen
        if screen_name == "main_menu":
            self.main_menu.visible = True
        elif screen_name == "options":
            self.options_screen.visible = True
        # Add conditions for other screens

    def hide_all_screens(self):
        self.main_menu.visible = False
        self.options_screen.visible = False
        # Add lines to hide other screens
