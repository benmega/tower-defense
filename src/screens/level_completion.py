import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, \
    LEVEL_COMPLETION_MAIN_MENU_BUTTON_POSITION, LEVEL_COMPLETION_REPLAY_BUTTON_POSITION, \
    LEVEL_COMPLETION_NEXT_LEVEL_BUTTON_POSITION
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class LevelCompletionScreen:
    def __init__(self, game):
        self.isActive = None
        self.game = game
        self.ui_manager = game.UI_manager
        self.screen = game.screen
        self.width, self.height = SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.5
        self.next_level_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(LEVEL_COMPLETION_NEXT_LEVEL_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Next Level',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(LEVEL_COMPLETION_REPLAY_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Replay',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(LEVEL_COMPLETION_MAIN_MENU_BUTTON_POSITION, UI_BUTTON_SIZE),
            text='Main Menu',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.background_image = load_scaled_image('assets/images/screens/level_completion.png',
                                                  (self.width, self.height))
        self.background = None

    def update(self, time_delta):
        # Update logic for the screen, such as animating stars or buttons
        self.ui_manager.update(time_delta)


    def open_screen(self):
        self.isActive = True
        self.next_level_button.visible = True
        self.replay_button.visible = True
        self.main_menu_button.visible = True
    def close_screen(self):
        self.isActive = False
        self.next_level_button.visible = False
        self.replay_button.visible = False
        self.main_menu_button.visible = False
    def draw(self):
        # Draw the greyed-out background first
        self.screen.blit(self.background, (0, 0))
        # Apply overlay directly to the screen
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Adjust alpha as needed
        self.screen.blit(overlay, (0, 0))
        # Draw the level completion UI background image
        self.screen.blit(self.background_image, (SCREEN_WIDTH//2 - self.width//2, SCREEN_HEIGHT//2 - self.height//2))
        # Make sure to draw the UI elements last so they are on top of everything else
        self.ui_manager.draw_ui(self.screen)

    def handle_events(self, event, game):
        # Handle button clicks to transition to the appropriate game state
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.next_level_button:
                    game.current_state = GameState.PLAYING
                    game.level_manager.start_next_level()
                    self.close_screen()
                elif event.ui_element == self.replay_button:
                    game.current_state = GameState.PLAYING
                    game.level_manager.reset_level()
                    self.close_screen()
                elif event.ui_element == self.main_menu_button:
                    game.current_state = GameState.MAIN_MENU
                    game.main_menu.open_menu()
                    self.close_screen()