import pygame
import pygame_gui

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
            if event.type == pygame.USEREVENT:
                self.handle_user_event(event, game)
            self.handle_state_specific_events(event, game)

    def handle_user_event(self, event, game):
        # Handle global USEREVENT, such as those from pygame_gui
        # This is where you'd handle dialog confirmations, etc.
        if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            # Perform actions based on the confirmed dialog
            pass  # Placeholder for actual logic TODO add logic

    def handle_state_specific_events(self, event, game):
        if game.current_state == GameState.PLAYING:
            self.handle_playing_events(event, game)
        elif game.current_state in [GameState.MAIN_MENU, GameState.OPTIONS,
                                    GameState.LOAD_GAME, GameState.CAMPAIGN_MAP,
                                    GameState.SKILLS, GameState.LEVEL_COMPLETE, GameState.LEVEL_DEFEAT,
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
            GameState.MAIN_MENU: game.UI_manager.main_menu.handle_events,
            GameState.OPTIONS: game.UI_manager.options_screen.handle_events,
            GameState.LOAD_GAME: game.UI_manager.game_data_screen.handle_events,
            GameState.CAMPAIGN_MAP: game.UI_manager.campaign_map.handle_events,
            GameState.SKILLS: game.UI_manager.skills_screen.handle_events,
            GameState.LEVEL_COMPLETE: game.UI_manager.level_end_screen.handle_events,
            GameState.LEVEL_DEFEAT: game.UI_manager.level_end_screen.handle_events,
        }
        handler = state_handlers.get(game.current_state)
        if handler:
            handler(event, game)

    def add_event(self, event):
        """ Add an event to the queue. """
        self.events.append(event)
