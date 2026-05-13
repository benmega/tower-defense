import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.game.game_state import GameState
import src.utils.constants as constants


class PauseScreen:
    def __init__(self, ui_manager):
        self.visible = False
        self.ui_manager = ui_manager
        self.overlay = None
        self.capturedScreen = None
        self.level_index = None

        panel_w, panel_h = 300, 280
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
        btn_x = SCREEN_WIDTH // 2 - UI_BUTTON_SIZE[0] // 2
        btn_start_y = panel_y + 50
        btn_stride = UI_BUTTON_SIZE[1] + constants.SPACE_LG

        self.resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_start_y), UI_BUTTON_SIZE),
            text='Resume',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_start_y + btn_stride), UI_BUTTON_SIZE),
            text='Restart Level',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_start_y + btn_stride * 2), UI_BUTTON_SIZE),
            text='Options',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_start_y + btn_stride * 3), UI_BUTTON_SIZE),
            text='Quit to Menu',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )

    def open_screen(self, level_index=None):
        self.visible = True
        self.resume_button.visible = True
        self.restart_button.visible = True
        self.options_button.visible = True
        self.quit_button.visible = True
        self.level_index = level_index
        # Capture the current screen before showing pause overlay
        self.capturedScreen = pygame.display.get_surface().copy()
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self.overlay.fill(constants.RGB_OVERLAY)

    def close_screen(self):
        self.visible = False
        self.resume_button.visible = False
        self.restart_button.visible = False
        self.options_button.visible = False
        self.quit_button.visible = False

    def draw(self, screen):
        if not self.visible:
            return
        if self.capturedScreen:
            screen.blit(self.capturedScreen, (0, 0))
        if self.overlay:
            screen.blit(self.overlay, (0, 0))

        panel_w, panel_h = 300, 280
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
        pygame.draw.rect(
            screen, constants.RGB_BG_DARK,
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=constants.RADIUS_MD
        )
        pygame.draw.rect(
            screen, constants.RGB_AMBER,
            (panel_x, panel_y, panel_w, panel_h),
            2, border_radius=constants.RADIUS_MD
        )

        font = pygame.font.Font(None, 48)
        title = font.render("PAUSED", True, constants.RGB_AMBER)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=panel_y + 10)
        screen.blit(title, title_rect)

        if self.level_index is not None:
            sub_font = pygame.font.Font(None, 24)
            sub = sub_font.render(f"Level {self.level_index + 1}", True, (180, 180, 180))
            sub_rect = sub.get_rect(centerx=SCREEN_WIDTH // 2, y=panel_y + 52)
            screen.blit(sub, sub_rect)

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.resume_button:
                    self.close_screen()
                    game.state_manager.change_state(GameState.PLAYING)
                elif event.ui_element == self.restart_button:
                    self.close_screen()
                    level_index = game.level_manager.current_level_index
                    game.initialize_game(level_index)
                elif event.ui_element == self.options_button:
                    game.state_manager.change_state(GameState.OPTIONS)
                elif event.ui_element == self.quit_button:
                    self.close_screen()
                    game.set_gameboard_ui_visibility(False)
                    game.state_manager.change_state(GameState.MAIN_MENU)
