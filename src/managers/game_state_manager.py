import pygame

from src.game.game_state import GameState
from src.screens.level_completion import LevelCompletionScreen

def capture_screen():
    # Capture the current display surface
    return pygame.display.get_surface().copy()
class GameStateTransitionHandler:
    def __init__(self, game):
        self.game = game

    def open_main_menu(self):
        self.game.UI_manager.main_menu.open_menu()
        self.game.audio_manager.play_music_for_state(GameState.MAIN_MENU)

    def open_options_screen(self):
        # Logic to open the options screen
        self.game.UI_manager.options_screen.open_screen()

    def open_game_data_screen(self):
        # Logic to open the game data/load game screen
        self.game.UI_manager.game_data_screen.open_screen()

    def open_campaign_map(self):
        # Logic to open the campaign map
        self.game.UI_manager.campaign_map.open_screen()
        self.game.audio_manager.play_music_for_state(GameState.CAMPAIGN_MAP)

    def open_skills_screen(self):
        # Logic to open the skills screen
        self.game.UI_manager.skills_screen.open_screen()

    def open_playing_scene(self):
        self.game.audio_manager.play_music_for_state(GameState.PLAYING)
        # self.game.audio_manager.play_music('assets/sounds/playing_background.mp3')

    def open_complete_screen(self):
        # Check if the screen is already initialized and set to completion mode; if not, initialize it
        screen = self.game.UI_manager.level_end_screen
        screen.background = capture_screen()
        self.game.player.complete_level(self.game.level_manager.current_level_index)
        self.game.UI_manager.campaign_map.update_player_progress(self.game.player.player_data['unlocked_levels'])

        if not screen:
            self.game.UI_manager.level_end_screen = LevelCompletionScreen(self, capture_screen(), screen_type='completion')
        if screen.screen_type != 'completion':
            screen.screen_type = 'completion'

        self.game.UI_manager.level_end_screen.open_screen()

    def open_defeat_screen(self):
        # self.game.UI_manager.level_end_screen.background = capture_screen()
        if not self.game.UI_manager.level_end_screen:
            self.game.UI_manager.level_end_screen = LevelCompletionScreen(self, capture_screen(), screen_type='defeat')
        # self.game.UI_manager.level_end_screen.screen_type = 'defeat'
        self.game.UI_manager.level_end_screen.open_screen('defeat')
        self.game.UI_manager.campaign_map.update_player_progress(self.game.player.player_data['unlocked_levels'])

class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.transition_handler = GameStateTransitionHandler(game)
        self.state_handlers = {
            GameState.MAIN_MENU: self.transition_handler.open_main_menu,
            GameState.OPTIONS: self.transition_handler.open_options_screen,
            GameState.LOAD_GAME: self.transition_handler.open_game_data_screen,
            GameState.CAMPAIGN_MAP: self.transition_handler.open_campaign_map,
            GameState.SKILLS: self.transition_handler.open_skills_screen,
            GameState.PLAYING: self.transition_handler.open_playing_scene,
            GameState.LEVEL_DEFEAT: self.transition_handler.open_defeat_screen,
            GameState.LEVEL_COMPLETE: self.transition_handler.open_complete_screen,
        }

    def change_state(self, new_state, screen=None):
        self.game.previous_state = self.game.current_state
        self.game.current_state = new_state
        handler = self.state_handlers.get(new_state)
        if handler:
            handler()
            if screen:
                screen.close_screen()
        else:
            print(f"No handler defined for state {new_state}")
