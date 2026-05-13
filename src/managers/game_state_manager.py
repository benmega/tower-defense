import pygame

from src.game.game_state import GameState
from src.screens.level_completion import LevelCompletionScreen
from src.utils.screen_utils import capture_screen


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
        # Restore music volume to normal when resuming from pause
        self.game.audio_manager.set_volume(music_volume=0.5)
        self.game.audio_manager.play_sfx('level_start')

    def open_pause_screen(self):
        level_index = self.game.level_manager.current_level_index
        self.game.UI_manager.pause_screen.open_screen(level_index=level_index)
        # Lower music volume while paused
        self.game.audio_manager.set_volume(music_volume=0.3)

    def open_complete_screen(self):
        self.game.UI_manager.level_end_screen.capturedScreen = capture_screen()
        screen = self.game.UI_manager.level_end_screen
        health = self.game.player.health
        stars = 3 if health >= 100 else (2 if health > 50 else 1)
        self.game.player.complete_level(self.game.level_manager.current_level_index, stars=stars)
        self.game.UI_manager.campaign_map.update_player_progress(
            self.game.player.player_data['unlocked_levels'],
            level_stars=self.game.player.level_stars,
        )

        if not screen:
            self.game.UI_manager.level_end_screen = LevelCompletionScreen(self.game.UI_manager,
                                                                          screen_type='completion')
        if screen.screen_type != 'completion':
            screen.screen_type = 'completion'

        # Auto-save progress
        try:
            self.game.save_game(1)
        except Exception as e:
            print(f"Auto-save failed: {e}")

        level = self.game.level_manager.current_level
        total_waves = len(level.enemy_wave_list) if level else 0
        current_idx = self.game.level_manager.current_level_index
        has_next = current_idx + 1 < len(self.game.level_manager.levels)
        self.game.audio_manager.play_sfx('level_complete')
        self.game.UI_manager.level_end_screen.open_screen(
            stars=stars,
            score=self.game.player.levelScore,
            wave=total_waves,
            total_waves=total_waves,
            has_next_level=has_next,
        )

    def open_defeat_screen(self):
        self.game.UI_manager.level_end_screen.capturedScreen = capture_screen()
        self.game.UI_manager.level_end_screen.screen_type = 'defeat'
        self.game.audio_manager.play_sfx('level_defeat')
        level = self.game.level_manager.current_level
        wave_reached = (level.current_wave_index + 1) if level else 0
        total_waves = len(level.enemy_wave_list) if level else 0
        self.game.UI_manager.level_end_screen.open_screen(
            score=self.game.player.levelScore,
            wave=wave_reached,
            total_waves=total_waves,
        )
        self.game.UI_manager.campaign_map.update_player_progress(
            self.game.player.unlocked_levels,
            level_stars=self.game.player.level_stars,
        )


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
