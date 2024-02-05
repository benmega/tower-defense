import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.game_state import GameState
from src.utils.helpers import load_scaled_image


class MainMenu:
    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text='Start Game',
            manager=self.ui_manager,
            visible=True
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 350), (100, 50)),
            text='Options',
            manager=self.ui_manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 425), (100, 50)),
            text='Exit',
            manager=self.ui_manager
        )
        self.background_image = load_scaled_image('assets/images/screens/main_menu_screen.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    print("Start the game!")
                    game.current_state = GameState.PLAYING
                    game.initialize_game()  # Call initialize_game to set up the game
                    game.level_manager.load_levels()
                    game.level_manager.start_level(0)
                    self.exit_button.visible = False
                    self.start_button.visible = False
                    self.options_button.visible = False
                elif event.ui_element == self.options_button:
                    print("Open options screen!")
                    game.current_state = GameState.OPTIONS

                elif event.ui_element == self.exit_button:
                    pygame.quit()
                    exit()

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        # Draw rectangles for debugging button positions

        #pygame.draw.rect(self.screen, (255, 0, 0), self.start_button.relative_rect, 1)  # Red outline
        #pygame.draw.rect(self.screen, (0, 255, 0), self.options_button.relative_rect,1)  # Green outline
        #pygame.draw.rect(self.screen, (0, 0, 255), self.exit_button.relative_rect, 1)  # Blue outline
        self.ui_manager.draw_ui(self.screen)

