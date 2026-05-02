import pygame_gui
import pygame

from src.config.config import UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen


class OptionsScreen(Screen):
    def __init__(self, ui_manager, audio_manager):
        super().__init__(ui_manager, 'assets/images/screens/options_screen.png')
        self.audio_manager = audio_manager
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
        # Use the audio manager's current settings to initialize sliders
        self.music_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((350, 150), (300, 100)),
            start_value=self.audio_manager.music_volume,
            value_range=(0, 100),
            manager=self.ui_manager,
            visible=False
        )
        self.sfx_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((350, 300), (300, 100)),
            start_value=self.audio_manager.sfx_volume,
            value_range=(0, 100),
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(self.music_volume_slider)
        self.add_ui_element(self.sfx_volume_slider)

    def on_slider_moved(self, ui_element, value):
        if ui_element == self.music_volume_slider:
            self.audio_manager.set_music_volume(value)
        elif ui_element == self.sfx_volume_slider:
            self.audio_manager.set_sfx_volume(value)

    def on_button_pressed(self, ui_element, game):
        if ui_element == self.back_button:
            game.state_manager.change_state(GameState.MAIN_MENU, self)
        elif ui_element == self.fullscreen_toggle:
            # TODO implement fullscreen toggle
            print("Toggle fullscreen mode")
