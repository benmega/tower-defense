import math
import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, GAME_BOARD_SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image
from src.utils.layout import center_rect, stack_rects


def capture_screen():
    return pygame.display.get_surface().copy()


def draw_star(surface, color, center, size):
    """Draw a 5-pointed star."""
    points = []
    for i in range(10):
        angle = math.pi / 5 * i - math.pi / 2
        r = size if i % 2 == 0 else size * 0.4
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((x, y))
    if len(points) >= 3:
        pygame.draw.polygon(surface, color, points)


class LevelCompletionScreen:
    def __init__(self, ui_manager, screen_type='completion'):
        self.visible = False
        self.ui_manager = ui_manager
        self.screen_type = screen_type
        self.stars = 1

        modal_w = int(SCREEN_WIDTH * 0.38)
        modal_h = int(SCREEN_HEIGHT * 0.48)
        modal_rect = center_rect(modal_w, modal_h)

        self.x, self.y = modal_rect.x, modal_rect.y
        self.width, self.height = modal_w, modal_h

        self.button_size = UI_BUTTON_SIZE
        button_rects = stack_rects(count=3, item_w=int(modal_w - 40), item_h=44, gap=12,
                                    top=int(self.y + modal_h // 2))

        next_level_button_text = 'Next Level' if self.screen_type == 'completion' else 'Back to Map'
        self.next_level_button = pygame_gui.elements.UIButton(
            relative_rect=button_rects[0],
            text=next_level_button_text,
            manager=self.ui_manager,
            object_id="@button",
            visible=False
        )

        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=button_rects[1],
            text='Replay',
            manager=self.ui_manager,
            object_id="@button",
            visible=False
        )

        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=button_rects[2],
            text='Main Menu',
            manager=self.ui_manager,
            object_id="@button",
            visible=False
        )
<<<<<<< HEAD

=======
>>>>>>> claude/laughing-ardinghelli-b72776
        self.background_image = self.load_background_image()
        self.overlay = None
        self.capturedScreen = None

    def load_background_image(self):
        image_path = ('assets/images/screens/level_completion.png' if self.screen_type == 'completion'
                      else 'assets/images/screens/level_defeat_2.jpg')
        return load_scaled_image(image_path, (self.width, self.height))

    def draw(self, screen):
        if not self.visible:
            return

        if not self.capturedScreen:
            self.capturedScreen = capture_screen()

        screen.blit(self.capturedScreen, (0, 0))

        if self.overlay:
            screen.blit(self.overlay, (0, 0))

        screen.blit(self.background_image, (self.x, self.y))

        if self.screen_type == 'completion':
            self._draw_stars(screen)

    def _draw_stars(self, screen):
        """Draw 1-3 stars above the buttons."""
        star_y = self.y + 40
        star_color = (255, 215, 0)

        if self.stars >= 1:
            draw_star(screen, star_color, (self.x + self.width // 2 - 30, star_y), 12)
        if self.stars >= 2:
            draw_star(screen, star_color, (self.x + self.width // 2, star_y), 12)
        if self.stars >= 3:
            draw_star(screen, star_color, (self.x + self.width // 2 + 30, star_y), 12)

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def open_screen(self, stars: int = 1):
        self.visible = True
        self.stars = stars
        self.next_level_button.visible = True
        self.replay_button.visible = True
        self.main_menu_button.visible = True
        self.background_image = self.load_background_image()
        self.capturedScreen = capture_screen()

        if self.screen_type == 'defeat':
            self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
            self.overlay.fill((180, 0, 0, 60))
        else:
            self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 128))

    def close_screen(self):
        self.visible = False
        self.next_level_button.visible = False
        self.replay_button.visible = False
        self.main_menu_button.visible = False

<<<<<<< HEAD
    # level_completion_screen.py
    def on_button_pressed(self, ui_element, game):
        if ui_element == self.next_level_button:
            game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
            game.UI_manager.player_info_panel.set_visibility(False)
        elif ui_element == self.replay_button:
            game.initialize_game()
            self.close_screen()
        elif ui_element == self.main_menu_button:
            game.state_manager.change_state(GameState.MAIN_MENU, self)
=======
    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.next_level_button:
                    game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
                    game.UI_manager.player_info_panel.set_visibility(False)
                elif event.ui_element == self.replay_button:
                    game.initialize_game(game.level_manager.current_level_index)
                    self.close_screen()
                elif event.ui_element == self.main_menu_button:
                    game.state_manager.change_state(GameState.MAIN_MENU, self)
>>>>>>> claude/festive-edison-84275f
