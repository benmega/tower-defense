import pygame

from src.game.game_state import GameState


class EventManager:
    def __init__(self):
        self.events = []

    def process_events(self, game):
        """ Process and handle all events in the queue. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_running = False
            elif game.current_state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the click is for building a tower
                    #game.UI_manager.process_events(event)
                    self.handle_build_tower(event, game)
                    if game.is_build_mode:
                        pos = pygame.mouse.get_pos()
                        game.handle_build(pos)
            elif game.current_state == GameState.MAIN_MENU:
                # Here, handle main menu specific events
                game.main_menu.handle_events(event,game)
            elif game.current_state == GameState.OPTIONS:
                # Here, handle options menu specific events
                pass
            elif game.current_state == GameState.GAME_OVER:
                # Here, handle game over specific events
                pass

            # UI Manager should process events for all states to handle button clicks etc.
            game.UI_manager.process_events(event)

        # Handle any custom events that are not pygame events
        for event in self.events:
            if event.type == 'build_tower':
                self.handle_build_tower(event, game)
            elif event.type == 'start_level':
                self.handle_start_level(event, game)
            elif event.type == 'pause_game':
                self.handle_pause_game(event, game)
            # Add more event types as needed
            self.events.remove(event)

    def add_event(self, event):
        """ Add an event to the queue. """
        self.events.append(event)

    @staticmethod
    def handle_build_tower(event, game):
        """ Handle the 'build_tower' event. """
        from src.entities.towers.tower import Tower
        sampletower = Tower(event.pos[0], event.pos[1])
        if game.player.gold >= sampletower.build_cost:
            game.tower_manager.add_tower(sampletower)
            game.player.gold -= sampletower.build_cost
            game.UI_manager.resources = game.player.gold
        # Implementation to handle building a tower
        # Example: game.build_tower(event.position, event.tower_type)

    def handle_start_level(self, event, game):
        """ Handle the 'start_level' event. """
        # Implementation to handle starting a new level
        # Example: game.start_level(event.level_number)

    def handle_pause_game(self, event, game):
        """ Handle the 'pause_game' event. """
        # Implementation to handle pausing the game
        # Example: game.pause()

    # Additional methods for handling specific event types

