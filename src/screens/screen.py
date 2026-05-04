import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
import src.utils.constants as C
from src.utils.helpers import load_scaled_image
import warnings


class Screen:
    FADE_DURATION = C.ANIM_NORMAL  # seconds

    def __init__(self, ui_manager, background_image_path):
        self.ui_manager = ui_manager
        self.visible = False
        self.ui_elements = []
        self.background_image = load_scaled_image(background_image_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = self.create_return_button()

        self._fade_alpha = 255
        self._fading_in = False
        self._fading_out = False
        self._fade_timer = 0.0

    def on_enter(self):
        self._fade_alpha = 255
        self._fading_in = True
        self._fading_out = False
        self._fade_timer = 0.0

    def on_exit(self):
        self._fading_out = True
        self._fading_in = False
        self._fade_timer = 0.0

    def create_return_button(self):
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([SCREEN_WIDTH - UI_BUTTON_SIZE[0] - 10, 10], UI_BUTTON_SIZE),
            text="Return",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(button)
        return button

    def add_ui_element(self, ui_element):
        self.ui_elements.append(ui_element)

    def set_ui_elements_visibility(self, visible):
        for element in self.ui_elements:
            try:
                element.visible = visible
            except AttributeError as e:
                warnings.warn(f"Attempted to set visibility on an unsupported object: {e}")

    def open_screen(self):
        self.visible = True
        self.set_ui_elements_visibility(True)
        self.on_enter()

    def close_screen(self):
        self.on_exit()
        self.visible = False
        self.set_ui_elements_visibility(False)

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.return_button:
                    game.state_manager.change_state(game.previous_state, self)

    def update(self, time_delta):
        if self.visible:
            self.ui_manager.update(time_delta)
            if self._fading_in:
                self._fade_timer += time_delta
                self._fade_alpha = max(0, int(255 * (1 - self._fade_timer / self.FADE_DURATION)))
                if self._fade_timer >= self.FADE_DURATION:
                    self._fading_in = False
                    self._fade_alpha = 0
            elif self._fading_out:
                self._fade_timer += time_delta
                self._fade_alpha = min(255, int(255 * self._fade_timer / self.FADE_DURATION))

    def draw(self, screen):
        if not self.visible:
            return
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        self._draw_fade_overlay(screen)

    def _draw_fade_overlay(self, surface):
        if self._fade_alpha > 0:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self._fade_alpha))
            surface.blit(overlay, (0, 0))
