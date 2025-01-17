import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_MENU_START_BUTTON_POSITION, \
    MAIN_MENU_EXIT_BUTTON_POSITION, MAIN_MENU_SETTINGS_BUTTON_POSITION, UI_BUTTON_SIZE, \
    MAIN_MENU_BACKGROUND_PATH, MAIN_MENU_CONTINUE_BUTTON_POSITION
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class MainMenu:
    def __init__(self, screen, ui_manager):

        self.screen = screen
        self.ui_manager = ui_manager
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(MAIN_MENU_START_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Start Game',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=True
        )
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(MAIN_MENU_CONTINUE_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Continue Game',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=True
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(MAIN_MENU_SETTINGS_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Settings',
            manager=self.ui_manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(MAIN_MENU_EXIT_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Exit',
            manager=self.ui_manager
        )
        self.background_image = load_scaled_image(MAIN_MENU_BACKGROUND_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible = True

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
                elif event.ui_element == self.continue_button:
                    game.state_manager.change_state(GameState.LOAD_GAME, self)
                elif event.ui_element == self.settings_button:
                    game.state_manager.change_state(GameState.OPTIONS, self)
                elif event.ui_element == self.exit_button:
                    pygame.quit()
                    exit()

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

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
