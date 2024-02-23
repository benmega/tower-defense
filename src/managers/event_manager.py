import pygame
import pygame_gui

from src.config.config import TOWER_TYPES
from src.game.game_state import GameState


class EventManager:
    def __init__(self):
        self.events = []

    def process_events(self, game):
        """ Process and handle all events in the queue. """
        for event in pygame.event.get():
            game.UI_manager.process_events(event)  # UI Manager should process events for all states to handle button clicks etc.
            if event.type == pygame.QUIT:
                game.is_running = False
            elif game.current_state == GameState.PLAYING:
                if event.type == pygame.USEREVENT:
                    game.level_manager.wave_panel.handle_events(event, game)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.tower_selection_panel.is_within_panel(event.pos):
                        game.tower_selection_panel.handle_mouse_click(event.pos)
                    elif game.is_build_mode:
                        game.tower_manager.add_tower_if_possible(event.pos[0], event.pos[1], player=game.player, game=game)
            elif game.current_state == GameState.MAIN_MENU:
                game.main_menu.handle_events(event, game)
            elif game.current_state == GameState.OPTIONS:
                game.options_screen.handle_events(event, game)
            elif game.current_state == GameState.LOAD_GAME:
                game.game_data_screen.handle_events(event, game)
            elif game.current_state == GameState.CAMPAIGN_MAP:
                game.campaign_map.handle_events(event, game)
            elif game.current_state == GameState.SKILLS:
                game.skills_screen.handle_events(event, game)
            elif game.current_state == GameState.LEVEL_COMPLETE:
                game.level_completion_screen.handle_events(event, game)
            elif game.current_state == GameState.GAME_OVER:
                # Here, handle game over specific events
                pass


        # Handle any custom events that are not pygame events
        # for event in self.events:
        #     if event.type == 'build_tower':
        #         self.handle_build_tower(event, game)
        #     elif event.type == 'start_level':
        #         self.handle_start_level(event, game)
        #     elif event.type == 'pause_game':
        #         self.handle_pause_game(event, game)
        #     # Add more event types as needed
        #     self.events.remove(event)


    def add_event(self, event):
        """ Add an event to the queue. """
        self.events.append(event)

