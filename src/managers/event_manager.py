import pygame


class EventManager:
    def __init__(self):
        self.events = []


    def process_events(self, game):
        """ Process and handle all events in the queue. """
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

    def handle_build_tower(self, event, game):
        """ Handle the 'build_tower' event. """
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