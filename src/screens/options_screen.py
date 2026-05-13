import pygame_gui
import pygame

from src.config.config import UI_BUTTON_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.game_state import GameState
from src.screens.screen import Screen
from src.utils.layout import stack_rects, anchor
import src.utils.constants as C


class OptionsScreen(Screen):
    def __init__(self, ui_manager, audio_manager):
        super().__init__(ui_manager, 'assets/images/screens/options_screen.png')
        self.audio_manager = audio_manager

        btn_w, btn_h = int(UI_BUTTON_SIZE[0]), int(UI_BUTTON_SIZE[1])
        sx, sy = anchor(btn_w, btn_h, h='center', v='bottom', margin=C.SPACE_MD * 2)

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([sx, sy], UI_BUTTON_SIZE),
            text='Back',
            manager=self.ui_manager,
            visible=False
        )

        self.fullscreen_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([sx, sy - 60], UI_BUTTON_SIZE),
            text='Toggle Fullscreen',
            manager=self.ui_manager,
            visible=False
        )

        self.add_ui_element(self.back_button)
        self.add_ui_element(self.fullscreen_toggle)

        # Create sliders using layout helpers
        slider_rects = stack_rects(count=2, item_w=300, item_h=30, gap=40,
                                    top=int(SCREEN_HEIGHT * 0.25))

        self.music_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rects[0],
            start_value=self.audio_manager.music_volume,
            value_range=(0, 100),
            manager=self.ui_manager,
            visible=False
        )

        self.sfx_volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rects[1],
            start_value=self.audio_manager.sfx_volume,
            value_range=(0, 100),
            manager=self.ui_manager,
            visible=False
        )

        self.add_ui_element(self.music_volume_slider)
        self.add_ui_element(self.sfx_volume_slider)

        # Add labels for sliders
        label_y_music = slider_rects[0].y - 30
        label_y_sfx = slider_rects[1].y - 30

        self.music_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([slider_rects[0].x, label_y_music], [200, 25]),
            text='Music Volume',
            manager=self.ui_manager,
            visible=False
        )

        self.sfx_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([slider_rects[1].x, label_y_sfx], [200, 25]),
            text='Sound Effects Volume',
            manager=self.ui_manager,
            visible=False
        )

        self.add_ui_element(self.music_label)
        self.add_ui_element(self.sfx_label)

        # Value display labels (to the right of sliders)
        value_label_x = slider_rects[0].x + slider_rects[0].width + 15
        self.music_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([value_label_x, slider_rects[0].y], [60, 30]),
            text=f"{int(self.audio_manager.music_volume)}%",
            manager=self.ui_manager,
            visible=False
        )

        self.sfx_value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([value_label_x, slider_rects[1].y], [60, 30]),
            text=f"{int(self.audio_manager.sfx_volume)}%",
            manager=self.ui_manager,
            visible=False
        )

        self.add_ui_element(self.music_value_label)
        self.add_ui_element(self.sfx_value_label)

    def on_slider_moved(self, ui_element, value):
        if ui_element == self.music_volume_slider:
            pygame.mixer.music.set_volume(value / 100)
            self.music_value_label.set_text(f"{int(value)}%")
        elif ui_element == self.sfx_volume_slider:
            self.audio_manager.set_sfx_volume(value)
            self.sfx_value_label.set_text(f"{int(value)}%")

    def on_button_pressed(self, ui_element, game):
        if ui_element == self.back_button:
            self.close_screen()
            dest = game.previous_state if game.previous_state else GameState.MAIN_MENU
            game.state_manager.change_state(dest)
        elif ui_element == self.fullscreen_toggle:
            pygame.display.toggle_fullscreen()
