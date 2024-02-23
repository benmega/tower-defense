import pygame_gui
import pygame

from src.config.config import UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.managers import audio_manager
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

    def handle_events(self, event, game):
        super().handle_events(event, game)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.music_volume_slider:
                    pygame.mixer.music.set_volume(event.value)
                elif event.ui_element == self.sfx_volume_slider:
                    game.audio_manager.set_sfx_volume(event.value)
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button: # Handle back button press
                    game.change_state(GameState.MAIN_MENU, self)
                elif event.ui_element == self.fullscreen_toggle:
                    # TODO Handle fullscreen toggle
                    print("Toggle fullscreen mode")