import pygame

from src.config.config import BACKGROUND_MUSIC_VOLUME, SOUND_EFFECTS_VOLUME
from src.game.game_state import GameState
from src.utils import constants as C
from src.utils.resource_path import resource_path

'''
    sources = { "background_music" : "https://www.youtube.com/watch?v=pgLjYsVP4H0"
'''


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = BACKGROUND_MUSIC_VOLUME
        self.sfx_volume = SOUND_EFFECTS_VOLUME

        try:
            self.build_sound = pygame.mixer.Sound(resource_path('assets/sounds/hammer-hit-on-wood.wav'))
        except Exception:
            self.build_sound = None

        try:
            self.click_sound = pygame.mixer.Sound(resource_path(C.SFX_BUTTON_CLICK))
            self.hover_sound = pygame.mixer.Sound(resource_path(C.SFX_BUTTON_HOVER))
            self.click_sound.set_volume(self.sfx_volume)
            self.hover_sound.set_volume(self.sfx_volume * 0.4)
        except Exception:
            self.click_sound = None
            self.hover_sound = None

        self.state_music_map = {
            GameState.MAIN_MENU: resource_path('assets/sounds/main_menu_background.mp3'),
            GameState.CAMPAIGN_MAP: resource_path('assets/sounds/campaign_map_background.mp3'),
            GameState.PLAYING: resource_path('assets/sounds/playing_background.mp3'),
        }
        self.current_music = None

        # Preload game-event SFX
        self._sfx_cache = {}
        sfx_map = {
            'enemy_death':    C.SFX_ENEMY_DEATH,
            'level_complete': C.SFX_LEVEL_COMPLETE,
            'level_defeat':   C.SFX_LEVEL_DEFEAT,
            'skill_unlocked': C.SFX_SKILL_UNLOCKED,
            'level_start':    C.SFX_LEVEL_START,
            'campaign_win':   C.SFX_CAMPAIGN_WIN,
        }
        for key, path in sfx_map.items():
            try:
                sound = pygame.mixer.Sound(resource_path(path))
                sound.set_volume(self.sfx_volume)
                self._sfx_cache[key] = sound
            except Exception as e:
                print(f"Failed to preload SFX '{key}': {e}")

    def play_sound(self, sound_path):
        try:
            sound = pygame.mixer.Sound(resource_path(sound_path))
            sound.set_volume(self.sfx_volume)
            sound.play()
        except Exception as e:
            print(f"Failed to play sound {sound_path}: {e}")

    def play_music(self, music_path, loops=-1):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
        except Exception as e:
            print(f"Failed to play music {music_path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, music_volume=None, sfx_volume=None):
        if music_volume is not None:
            self.music_volume = music_volume
            pygame.mixer.music.set_volume(music_volume)
        if sfx_volume is not None:
            self.sfx_volume = sfx_volume

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self._sfx_cache.values():
            sound.set_volume(volume)

    def play_ui_click(self):
        if self.click_sound:
            self.click_sound.set_volume(self.sfx_volume)
            self.click_sound.play()

    def play_ui_hover(self):
        if self.hover_sound:
            self.hover_sound.set_volume(self.sfx_volume * 0.4)
            self.hover_sound.play()

    def play_music_for_state(self, game_state):
        music_path = self.state_music_map.get(game_state)
        if music_path and music_path != self.current_music:
            self.play_music(music_path)
            self.current_music = music_path

    def play_sfx(self, sfx_name):
        """Play a preloaded SFX sound by name."""
        sound = self._sfx_cache.get(sfx_name)
        if sound:
            sound.play()
        else:
            print(f"SFX '{sfx_name}' not found in cache")
