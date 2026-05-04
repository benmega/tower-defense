# import pygame
# import pygame_gui
#
# from src.game.game_state import GameState
#
#
# class EventManager:
#     def __init__(self):
#         self.events = []
#
#     def process_events(self, game):
#         """ Process and handle all events in the queue. """
#         for event in pygame.event.get():
#             game.UI_manager.process_events(event)  # Process UI events globally
#             if event.type == pygame.QUIT:
#                 game.is_running = False
#             # if event.type == pygame.USEREVENT:
#                 # self.handle_user_event(event, game)
#             self.handle_state_specific_events(event, game)
#
#     # def handle_user_event(self, event, game):
#     #     # Handle global USEREVENT, such as those from pygame_gui
#     #     # This is where you'd handle dialog confirmations, etc.
#     #     if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
#     #         # Perform actions based on the confirmed dialog
#     #         pass  # Placeholder for actual logic TODO add logic
#
#     # def handle_state_specific_events(self, event, game):
#     #     # if game.current_state == GameState.PLAYING:
#     #     #     self.handle_playing_events(event, game)
#     #     # elif game.current_state in [GameState.MAIN_MENU, GameState.OPTIONS,
#     #     #                             GameState.LOAD_GAME, GameState.CAMPAIGN_MAP,
#     #     #                             GameState.SKILLS, GameState.LEVEL_COMPLETE, GameState.LEVEL_DEFEAT,
#     #     #                             GameState.GAME_OVER]:
#     #     self.handle_menu_and_ui_states(event, game)
#
#     def handle_playing_events(self, event, game):
#         # Handle events specific to the PLAYING state
#         if event.type == pygame.USEREVENT:
#             game.level_manager.wave_panel.handle_events(event, game)
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if game.tower_selection_panel.is_within_panel(event.pos):
#                 game.tower_selection_panel.handle_mouse_click(event.pos)
#             elif game.is_build_mode:
#                 game.tower_manager.add_tower_if_possible(event.pos[0], event.pos[1], game.player, game)
#
#     def handle_state_specific_events(self, event, game):
#         state_handlers = {
#             GameState.PLAYING: self.handle_playing_events,
#             GameState.MAIN_MENU: game.UI_manager.main_menu.handle_events,
#             GameState.OPTIONS: game.UI_manager.options_screen.handle_events,
#             GameState.LOAD_GAME: game.UI_manager.game_data_screen.handle_events,
#             GameState.CAMPAIGN_MAP: game.UI_manager.campaign_map.handle_events,
#             GameState.SKILLS: game.UI_manager.skills_screen.handle_events,
#             GameState.LEVEL_COMPLETE: game.UI_manager.level_end_screen.handle_events,
#             GameState.LEVEL_DEFEAT: game.UI_manager.level_end_screen.handle_events,
#         }
#         handler = state_handlers.get(game.current_state)
#         if handler:
#             handler(event, game)
#
#     def add_event(self, event):
#         self.events.append(event)


# src/game/event_manager.py
import pygame
import pygame_gui
from src.game.game_state import GameState

class EventManager:
    def __init__(self):
        self.events = []

    def process_events(self, game):
        for event in pygame.event.get():
<<<<<<< HEAD
            game.UI_manager.process_events(event)

=======
            game.UI_manager.process_events(event)  # Process UI events globally
            if event.type == pygame.USEREVENT and hasattr(event, 'user_type'):
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    game.audio_manager.play_ui_click()
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    game.audio_manager.play_ui_hover()
>>>>>>> claude/dazzling-herschel-e80896
            if event.type == pygame.QUIT:
                game.is_running = False
                return

            if event.type == pygame.USEREVENT:
                self._handle_ui_event(event, game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_event(event, game)

<<<<<<< HEAD
    def _handle_ui_event(self, event, game):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            self._dispatch_button(event.ui_element, game)
        elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self._dispatch_slider(event.ui_element, event.value, game)
        elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            game.UI_manager.game_data_screen.on_confirmation(game)
=======
    def handle_user_event(self, event, game):
        # Handle global USEREVENT, such as those from pygame_gui
        # This is where you'd handle dialog confirmations, etc.
        if hasattr(event, 'user_type') and event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            # Perform actions based on the confirmed dialog
            pass  # Placeholder for actual logic TODO add logic
>>>>>>> claude/laughing-ardinghelli-b72776

<<<<<<< HEAD
    def _handle_mouse_event(self, event, game):
        if game.current_state == GameState.CAMPAIGN_MAP:
            game.UI_manager.campaign_map.on_click(event.pos, game)
        elif game.current_state == GameState.PLAYING and game.is_build_mode:
            if game.tower_selection_panel.is_within_panel(event.pos):
                game.tower_selection_panel.on_click(event.pos, game)
            else:
                game.tower_manager.add_tower_if_possible(event.pos[0], event.pos[1], game.player, game)
=======
    def handle_state_specific_events(self, event, game):
        if game.current_state == GameState.PLAYING:
            self.handle_playing_events(event, game)
        elif game.current_state == GameState.PAUSED:
            game.UI_manager.pause_screen.handle_events(event, game)
        elif game.current_state in [GameState.MAIN_MENU, GameState.OPTIONS,
                                    GameState.LOAD_GAME, GameState.CAMPAIGN_MAP,
                                    GameState.SKILLS, GameState.LEVEL_COMPLETE, GameState.LEVEL_DEFEAT,
                                    GameState.GAME_OVER]:
            self.handle_menu_and_ui_states(event, game)

    def handle_playing_events(self, event, game):
        # Handle events specific to the PLAYING state
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state_manager.change_state(GameState.PAUSED)
        if event.type == pygame.USEREVENT:
            game.level_manager.wave_panel.handle_events(event, game)
            # Handle HUD button clicks
            game.UI_manager.player_info_panel.handle_events(event, game)
            # Handle tower info panel events
            if hasattr(game, 'tower_info_panel'):
                game.tower_info_panel.handle_events(event, game)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.tower_selection_panel.is_within_panel(event.pos):
                game.tower_selection_panel.handle_mouse_click(event.pos)
            else:
                # First, check if clicking on a placed tower
                clicked_tower = game.tower_manager.handle_click(event.pos)
                if clicked_tower:
                    # Tower was clicked - select it (don't try to place)
                    pass
                elif game.is_build_mode and game.tower_manager.selected_tower_type is not None:
                    # No tower clicked, and we're in build mode - try to place
                    success = game.tower_manager.add_tower_if_possible(
                        event.pos[0], event.pos[1], game.player, game
                    )
                    # Exit build mode after placement attempt
                    if success:
                        game.is_build_mode = False
>>>>>>> claude/great-franklin-30172d

    def _dispatch_button(self, ui_element, game):
        state = game.current_state
        ui = game.UI_manager

        mapping = {
            GameState.MAIN_MENU: ui.main_menu.on_button_pressed,
            GameState.OPTIONS: ui.options_screen.on_button_pressed,
            GameState.LOAD_GAME: ui.game_data_screen.on_button_pressed,
            GameState.CAMPAIGN_MAP: ui.campaign_map.on_button_pressed,
            GameState.SKILLS: ui.skills_screen.on_button_pressed,
            GameState.LEVEL_COMPLETE: ui.level_end_screen.on_button_pressed,
            GameState.LEVEL_DEFEAT: ui.level_end_screen.on_button_pressed,
            GameState.PLAYING: game.level_manager.wave_panel.on_button_pressed,
        }

        if state in mapping:
            mapping[state](ui_element, game)

    def _dispatch_slider(self, ui_element, value, game):
        ui = game.UI_manager.options_screen
        ui.on_slider_moved(ui_element, value)

    def add_event(self, event):
        self.events.append(event)
