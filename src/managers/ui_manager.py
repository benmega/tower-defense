import pygame_gui
import pygame
from src.game.player_info_panel import PlayerInfoPanel
from src.screens.campain_map import CampaignMap
from src.screens.level_completion import LevelCompletionScreen
from src.screens.main_menu import MainMenu
from src.screens.game_data_screen import GameDataScreen
from src.screens.options_screen import OptionsScreen
from src.screens.skills_screen import SkillsScreen
from src.screens.pause_screen import PauseScreen


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
        self.pause_screen = PauseScreen(self)
        self.skills_screen = SkillsScreen(self, game.player)
        self.options_screen = OptionsScreen(self, game.audio_manager)

        # Dictionary for managing custom screens
        self.custom_screens = {
            'main_menu': self.main_menu,
            'options_screen': self.options_screen,
            'game_data_screen': self.game_data_screen,
            'campaign_map': self.campaign_map,
            'level_end_screen': self.level_end_screen,
            'skills_screen': self.skills_screen,
            'pause_screen': self.pause_screen,
            'player_info_panel': self.player_info_panel
            # Add other screens as necessary
        }


    def draw_ui(self, screen):
        # Iterate through custom screens and draw if visible
        for screen_name, custom_screen in self.custom_screens.items():
            if getattr(custom_screen, 'visible', False):
                custom_screen.draw(screen)

        super().draw_ui(screen)

    def update(self, time_delta):
        super().update(time_delta)
