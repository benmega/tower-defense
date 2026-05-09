import glob
import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE, MAIN_MENU_BACKGROUND_PATH
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image
from src.utils.layout import stack_rects
import src.utils.constants as C


class MainMenu:
    FADE_DURATION = C.ANIM_NORMAL

    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager

        btn_w, btn_h = 220, 44
        rects = stack_rects(count=4, item_w=btn_w, item_h=btn_h, gap=14,
                            top=int(SCREEN_HEIGHT * 0.44))

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=rects[0],
            text='Start Game',
            manager=self.ui_manager,
            object_id="@button",
            visible=True
        )
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=rects[1],
            text='Continue Game',
            manager=self.ui_manager,
            object_id="@button",
            visible=True
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=rects[2],
            text='Settings',
            manager=self.ui_manager,
            visible=True
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=rects[3],
            text='Exit',
            manager=self.ui_manager,
            visible=True
        )

        save_files = glob.glob('src/save_data/*.json')
        if not save_files:
            self.continue_button.disable()

        self.background_image = load_scaled_image(MAIN_MENU_BACKGROUND_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible = True
        self._fade_alpha = 255
        self._fading_in = False
        self._fade_timer = 0.0

    def on_enter(self):
        self._fade_alpha = 255
        self._fading_in = True
        self._fade_timer = 0.0

    def on_button_pressed(self, ui_element, game):
        if ui_element == self.start_button:
            game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
        elif ui_element == self.continue_button:
            game.state_manager.change_state(GameState.LOAD_GAME, self)
        elif ui_element == self.settings_button:
            game.state_manager.change_state(GameState.OPTIONS, self)
        elif ui_element == self.exit_button:
            pygame.quit()
            exit()

    def update(self, time_delta):
        self.ui_manager.update(time_delta)
        if self._fading_in:
            self._fade_timer += time_delta
            self._fade_alpha = max(0, int(255 * (1 - self._fade_timer / self.FADE_DURATION)))
            if self._fade_timer >= self.FADE_DURATION:
                self._fading_in = False
                self._fade_alpha = 0

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        if self._fade_alpha > 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self._fade_alpha))
            screen.blit(overlay, (0, 0))

    def close_screen(self):
        self.exit_button.visible = False
        self.start_button.visible = False
        self.settings_button.visible = False
        self.continue_button.visible = False
        self.visible = False

    def open_menu(self):
        self.exit_button.visible = True
        self.start_button.visible = True
        self.settings_button.visible = True
        self.continue_button.visible = True
        self.visible = True
