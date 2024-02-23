import pygame
import pygame_gui

from src.config.config import TOWER_TYPES
from src.game.game_state import GameState


import pygame
from src.game.game_state import GameState

class EventManager:
    def __init__(self):
        self.events = []

    def process_events(self, game):
        """ Process and handle all events in the queue. """
        for event in pygame.event.get():
            game.UI_manager.process_events(event)  # Process UI events globally

            if event.type == pygame.QUIT:
                game.is_running = False

            # Add a general USEREVENT handler if needed
            if event.type == pygame.USEREVENT:
                self.handle_user_event(event, game)

            # Delegate to state-specific event handlers
            self.handle_state_specific_events(event, game)

    def handle_user_event(self, event, game):
        # Handle global USEREVENT, such as those from pygame_gui
        # This is where you'd handle dialog confirmations, etc.
        # Example:
        if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            # Perform actions based on the confirmed dialog
            pass  # Placeholder for actual logic TODO add logic

    def handle_state_specific_events(self, event, game):
        if game.current_state == GameState.PLAYING:
            self.handle_playing_events(event, game)
        elif game.current_state in [GameState.MAIN_MENU, GameState.OPTIONS,
                                    GameState.LOAD_GAME, GameState.CAMPAIGN_MAP,
                                    GameState.SKILLS, GameState.LEVEL_COMPLETE,
                                    GameState.GAME_OVER]:
            self.handle_menu_and_ui_states(event, game)

    def handle_playing_events(self, event, game):
        # Handle events specific to the PLAYING state
        if event.type == pygame.USEREVENT:
            game.level_manager.wave_panel.handle_events(event, game)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.tower_selection_panel.is_within_panel(event.pos):
                game.tower_selection_panel.handle_mouse_click(event.pos)
            elif game.is_build_mode:
                game.tower_manager.add_tower_if_possible(event.pos[0], event.pos[1], game.player, game)

    def handle_menu_and_ui_states(self, event, game):
        # Handle events for various menu and UI states
        state_handlers = {
            GameState.MAIN_MENU: game.main_menu.handle_events,
            GameState.OPTIONS: game.options_screen.handle_events,
            GameState.LOAD_GAME: game.game_data_screen.handle_events,
            GameState.CAMPAIGN_MAP: game.campaign_map.handle_events,
            GameState.SKILLS: game.skills_screen.handle_events,
            GameState.LEVEL_COMPLETE: game.level_completion_screen.handle_events,
            # Add more states as necessary
        }
        handler = state_handlers.get(game.current_state)
        if handler:
            handler(event, game)


    def add_event(self, event):
        """ Add an event to the queue. """
        self.events.append(event)

    # # @staticmethod
    # # def handle_build_tower(event, game):
    # #     """ Handle the 'build_tower' event. """
    # #     build_type = game.tower_manager.selected_tower_type
    # #     build_cost = TOWER_TYPES[build_type]['cost']
    # #     if game.player.gold >= build_cost:
    # #         game.tower_manager.add_tower(event.pos[0],event.pos[1], game)
    # #         game.player.gold -= build_cost
    # #         game.UI_manager.resources = game.player.gold
    #
    # def handle_start_level(self, event, game):
    #     """ Handle the 'start_level' event. """
    #     # Implementation to handle starting a new level
    #     # Example: game.start_level(event.level_number)
    #
    # def handle_pause_game(self, event, game):
    #     """ Handle the 'pause_game' event. """
    #     # Implementation to handle pausing the game
    #     # Example: game.pause()

