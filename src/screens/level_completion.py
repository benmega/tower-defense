import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, GAME_BOARD_SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image

def capture_screen():
    # Capture the current display surface
    return pygame.display.get_surface().copy()


class LevelCompletionScreen:
    def __init__(self, ui_manager, screen_type='completion'):
        self.visible = False
        self.ui_manager = ui_manager
        self.screen_type = screen_type  # 'completion' or 'defeat'
        self.width, self.height = GAME_BOARD_SCREEN_SIZE[0] * 0.4, GAME_BOARD_SCREEN_SIZE[1] * 0.5
        self.x = GAME_BOARD_SCREEN_SIZE[0] // 2 - self.width // 2
        self.y = GAME_BOARD_SCREEN_SIZE[1] // 2 - self.height // 2
        self.button_size = UI_BUTTON_SIZE
        self.button_x = self.x + (self.width - self.button_size[0]) // 2
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
        self.background_image = self.load_background_image()
        self.overlay = None
        self.capturedScreen = None

    def load_background_image(self):
        # Load the appropriate background based on screen type
        image_path = 'assets/images/screens/level_completion.png' if self.screen_type == 'completion' else 'assets/images/screens/level_defeat_2.jpg'
        return load_scaled_image(image_path, (self.width, self.height))
    def draw(self, screen):
        if not self.visible:
            return
        if not self.capturedScreen:
            self.capturedScreen = capture_screen()

        screen.blit(self.capturedScreen, (0,0))
        if self.overlay:
            screen.blit(self.overlay, (0, 0))

        # Draw the background image
        screen.blit(self.background_image, (self.x, self.y))

    def update(self, time_delta):
        # Update logic for the screen, such as animating stars or buttons
        self.ui_manager.update(time_delta)

    def open_screen(self):
        self.visible = True
        self.next_level_button.visible = True
        self.replay_button.visible = True
        self.main_menu_button.visible = True
        self.background_image = self.load_background_image()
        # self.capturedScreen = capture_screen() #TODO try using this line
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay

    def close_screen(self):
        self.visible = False
        self.next_level_button.visible = False
        self.replay_button.visible = False
        self.main_menu_button.visible = False

    def handle_events(self, event, game):
        # Handle button clicks to transition to the appropriate game state
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.next_level_button:
                    if self.screen_type == 'completion':  # Logic for completing the level and moving to the next
                        game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
                    else:  # Logic for defeat screen, simply going back to the map
                        game.state_manager.change_state(GameState.CAMPAIGN_MAP, self)
                    game.UI_manager.player_info_panel.set_visibility(False)
                elif event.ui_element == self.replay_button:
                    game.initialize_game()
                    self.close_screen()
                elif event.ui_element == self.main_menu_button:
                    game.state_manager.change_state(GameState.MAIN_MENU, self)
