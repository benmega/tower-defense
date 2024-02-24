# import pygame_gui
# import pygame
#
# from src.config.config import UI_BUTTON_SIZE
# from src.game.game_state import GameState
# from src.screens.screen import Screen
# from src.utils.helpers import load_scaled_image
#
# class LevelDefeatScreen:
#     def __init__(self, game):
#         self.isActive = None
#         self.game = game
#         self.ui_manager = game.UI_manager
#         self.screen = game.screen
#         self.width, self.height = self.screen.get_width() * 0.4, self.screen.get_height() * 0.5
#         self.x = self.screen.get_width() // 2 - self.width // 2
#         self.y = self.screen.get_height() // 2 - self.height // 2
#         self.button_size = UI_BUTTON_SIZE
#         self.button_x = self.x + (self.width - self.button_size[0]) // 2
#
#         # Note: Next Level button removed since it's not applicable for a defeat screen
#
#         self.replay_button = pygame_gui.elements.UIButton(
#             relative_rect=pygame.Rect([self.button_x, self.y + self.height // 3], UI_BUTTON_SIZE),  # Adjust position as needed
#             text='Replay',
#             manager=self.ui_manager,
#             object_id=pygame_gui.core.ObjectID(class_id="@button"),
#             visible=False
#         )
#         self.main_menu_button = pygame_gui.elements.UIButton(
#             relative_rect=pygame.Rect([self.button_x, self.y + 2 * self.height // 3], UI_BUTTON_SIZE),  # Adjust position as needed
#             text='Main Menu',
#             manager=self.ui_manager,
#             object_id=pygame_gui.core.ObjectID(class_id="@button"),
#             visible=False
#         )
#         self.background_image = load_scaled_image('assets/images/screens/level_defeat.png',
#                                                   (self.width, self.height))
#         self.background = None
#
#     # The rest of the methods (update, open_screen, close_screen, draw, handle_events) can remain largely the same.
#     # TODO Adjust the `handle_events` method to remove or modify the next level button logic, as it's not applicable here.
