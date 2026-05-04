import pygame

from src.game.game_state import GameState
<<<<<<< HEAD
from src.screens.level_completion import LevelCompletionScreen
<<<<<<< HEAD
from src.managers.ui_manager import capture_screen
=======
import src.utils.constants as constants
=======
>>>>>>> claude/laughing-ardinghelli-b72776


def capture_screen():
    return pygame.display.get_surface().copy()
>>>>>>> claude/great-franklin-30172d


class GameStateTransitionHandler:
    def __init__(self, game):
        self.game = game

    def open_main_menu(self):
        self.game.UI_manager.main_menu.open_menu()
        self.game.UI_manager.main_menu.on_enter()
        self.game.audio_manager.play_music_for_state(GameState.MAIN_MENU)

    def open_options_screen(self):
        self.game.UI_manager.options_screen.open_screen()
        self.game.UI_manager.options_screen.on_enter()

    def open_game_data_screen(self):
        self.game.UI_manager.game_data_screen.open_screen()
        self.game.UI_manager.game_data_screen.on_enter()

    def open_campaign_map(self):
        self.game.UI_manager.campaign_map.open_screen()
        self.game.UI_manager.campaign_map.on_enter()
        self.game.audio_manager.play_music_for_state(GameState.CAMPAIGN_MAP)

    def open_skills_screen(self):
        self.game.UI_manager.skills_screen.open_screen()
        self.game.UI_manager.skills_screen.on_enter()

    def open_playing_scene(self):
        self.game.audio_manager.play_music_for_state(GameState.PLAYING)
<<<<<<< HEAD
        # Restore music volume to normal when resuming from pause
        self.game.audio_manager.set_volume(music_volume=0.5)

    def open_pause_screen(self):
        self.game.UI_manager.pause_screen.open_screen()
        # Lower music volume to 30%
        self.game.audio_manager.set_volume(music_volume=0.3)
=======
        self.game.audio_manager.play_sfx('level_start')
>>>>>>> claude/suspicious-raman-d0a593

    def open_complete_screen(self):
<<<<<<< HEAD
<<<<<<< HEAD
        # Play success sound
        self.game.audio_manager.play_sound(constants.SFX_SUCCESS)
        # Check if the screen is already initialized and set to completion mode; if not, initialize it
=======
>>>>>>> claude/festive-edison-84275f
        self.game.UI_manager.level_end_screen.capturedScreen = capture_screen()
        screen = self.game.UI_manager.level_end_screen
        self.game.player.complete_level(self.game.level_manager.current_level_index)
        self.game.UI_manager.campaign_map.update_player_progress(self.game.player.player_data['unlocked_levels'])

        if not screen:
            self.game.UI_manager.level_end_screen = LevelCompletionScreen(self.game.UI_manager,
                                                                          screen_type='completion')
        if screen.screen_type != 'completion':
            screen.screen_type = 'completion'

        self.game.audio_manager.play_sfx('level_complete')
=======
        self.game.UI_manager.level_end_screen.capturedScreen = capture_screen()
        screen = self.game.UI_manager.level_end_screen
        self.game.player.complete_level(self.game.level_manager.current_level_index)
        self.game.UI_manager.campaign_map.update_player_progress(self.game.player.unlocked_levels)
        screen.screen_type = 'completion'
>>>>>>> claude/laughing-ardinghelli-b72776
        self.game.UI_manager.level_end_screen.open_screen()

    def open_defeat_screen(self):
        self.game.UI_manager.level_end_screen.capturedScreen = capture_screen()
<<<<<<< HEAD
        if not self.game.UI_manager.level_end_screen:
            self.game.UI_manager.level_end_screen = LevelCompletionScreen(self.game.UI_manager,
                                                                          screen_type='defeat')
=======
>>>>>>> claude/laughing-ardinghelli-b72776
        self.game.UI_manager.level_end_screen.screen_type = 'defeat'
        self.game.audio_manager.play_sfx('level_defeat')
        self.game.UI_manager.level_end_screen.open_screen()
        self.game.UI_manager.campaign_map.update_player_progress(self.game.player.unlocked_levels)


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
            GameState.PAUSED: self.transition_handler.open_pause_screen,
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
