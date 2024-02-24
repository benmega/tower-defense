import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, GAME_BOARD_SCREEN_SIZE
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class LevelCompletionScreen:
    def __init__(self, game, screen_type='completion'):
        self.isActive = None
        self.game = game
        self.ui_manager = game.UI_manager
        self.screen = game.screen
        self.screen_type = screen_type  # 'completion' or 'defeat'
        self.width, self.height = GAME_BOARD_SCREEN_SIZE[0] * 0.4, GAME_BOARD_SCREEN_SIZE[1] * 0.5
        self.x = GAME_BOARD_SCREEN_SIZE[0] // 2 - self.width // 2
        self.y = GAME_BOARD_SCREEN_SIZE[1] // 2 - self.height // 2
        self.button_size = UI_BUTTON_SIZE
        self.button_x = self.x + (self.width - self.button_size[0]) // 2

        # Adjust the button text based on the screen type
        next_level_button_text = 'Next Level' if self.screen_type == 'completion' else 'Back to Map'
        self.next_level_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([self.button_x, self.y + self.height // 4], UI_BUTTON_SIZE),
            text=next_level_button_text,
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([self.button_x, self.y + 2 * self.height // 4], UI_BUTTON_SIZE),
            text='Replay',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([self.button_x, self.y + 3 * self.height // 4], UI_BUTTON_SIZE),
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
        overlay = pygame.Surface([self.screen.get_width(), self.screen.get_height()], flags=pygame.SRCALPHA)
        overlay.fill([0, 0, 0, 128])  # Adjust alpha as needed
        self.screen.blit(overlay, (0, 0))
        # Draw the level completion UI background image
        self.screen.blit(self.background_image, (self.x, self.y))
        # Make sure to draw the UI elements last so that they are on top of everything else
        self.ui_manager.draw_ui(self.screen)

    def handle_events(self, event, game):
        # Handle button clicks to transition to the appropriate game state
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.next_level_button:
                    if self.screen_type == 'completion': # Logic for completing the level and moving to the next
                        game.change_state(GameState.CAMPAIGN_MAP, self)
                    else: # Logic for defeat screen, simply going back to the map
                        game.change_state(GameState.CAMPAIGN_MAP, self)
                    game.player_info_panel.set_visibility(False)
                elif event.ui_element == self.replay_button:
                    game.change_state(GameState.PLAYING, self)
                    game.initialize_game()
                elif event.ui_element == self.main_menu_button:
                    game.change_state(GameState.MAIN_MENU, self)
                    game.set_gameboard_ui_visibility(False)
