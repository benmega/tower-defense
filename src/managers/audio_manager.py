import pygame
import sys
import os

from src.config.config import BACKGROUND_MUSIC_VOLUME, SOUND_EFFECTS_VOLUME
from src.game.game_state import GameState
<<<<<<< HEAD
<<<<<<< HEAD
from src.utils.helpers import resource_path

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = BACKGROUND_MUSIC_VOLUME
        self.sfx_volume = SOUND_EFFECTS_VOLUME
        self.build_sound = pygame.mixer.Sound(resource_path('assets/sounds/hammer-hit-on-wood.wav'))
=======
from src.utils.constants import SFX_BUTTON_CLICK, SFX_BUTTON_HOVER
=======
from src.utils import constants as C
>>>>>>> claude/suspicious-raman-d0a593

'''
    sources = { "background_music" : "https://www.youtube.com/watch?v=pgLjYsVP4H0"
'''

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

class AudioManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer module
        self.music_volume = BACKGROUND_MUSIC_VOLUME  # Default music volume
        self.sfx_volume = SOUND_EFFECTS_VOLUME  # Default sound effects volume
<<<<<<< HEAD
        self.build_sound = pygame.mixer.Sound('assets/sounds/hammer-hit-on-wood.wav')
        self.click_sound = pygame.mixer.Sound(SFX_BUTTON_CLICK)
        self.hover_sound = pygame.mixer.Sound(SFX_BUTTON_HOVER)
        self.click_sound.set_volume(self.sfx_volume)
        self.hover_sound.set_volume(self.sfx_volume * 0.4)
>>>>>>> claude/dazzling-herschel-e80896
        self.state_music_map = {
            GameState.MAIN_MENU: resource_path('assets/sounds/main_menu_background.mp3'),
            GameState.CAMPAIGN_MAP: resource_path('assets/sounds/campaign_map_background.mp3'),
            GameState.PLAYING: resource_path('assets/sounds/playing_background.mp3'),
=======
        self.build_sound = pygame.mixer.Sound(get_asset_path('assets/sounds/hammer-hit-on-wood.wav'))
        self.state_music_map = {
            GameState.MAIN_MENU: get_asset_path('assets/sounds/main_menu_background.mp3'),
            GameState.CAMPAIGN_MAP: get_asset_path('assets/sounds/campaign_map_background.mp3'),
            GameState.PLAYING: get_asset_path('assets/sounds/playing_background.mp3'),
            # Add other states as necessary
>>>>>>> claude/unruffled-ramanujan-1882ca
        }
        self.current_music = None

<<<<<<< HEAD
=======
        # Preload SFX sounds
        self._sfx_cache = {}
        try:
            self._sfx_cache['enemy_death'] = pygame.mixer.Sound(C.SFX_ENEMY_DEATH)
            self._sfx_cache['level_complete'] = pygame.mixer.Sound(C.SFX_LEVEL_COMPLETE)
            self._sfx_cache['level_defeat'] = pygame.mixer.Sound(C.SFX_LEVEL_DEFEAT)
            self._sfx_cache['skill_unlocked'] = pygame.mixer.Sound(C.SFX_SKILL_UNLOCKED)
            self._sfx_cache['level_start'] = pygame.mixer.Sound(C.SFX_LEVEL_START)
            self._sfx_cache['campaign_win'] = pygame.mixer.Sound(C.SFX_CAMPAIGN_WIN)
            # Set volume for all preloaded sounds
            for sound in self._sfx_cache.values():
                sound.set_volume(self.sfx_volume)
        except Exception as e:
            print(f"Failed to preload SFX sounds: {e}")
>>>>>>> claude/suspicious-raman-d0a593
    def play_sound(self, sound_path):
        full_path = get_asset_path(sound_path) if not os.path.isabs(sound_path) else sound_path
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def play_music(self, music_path, loops=-1):
        full_path = get_asset_path(music_path) if not os.path.isabs(music_path) else music_path
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, music_volume=None, sfx_volume=None):
        if music_volume is not None:
            self.music_volume = music_volume
            pygame.mixer.music.set_volume(music_volume)
        if sfx_volume is not None:
            self.sfx_volume = sfx_volume

<<<<<<< HEAD
    def play_ui_click(self):
        self.click_sound.set_volume(self.sfx_volume)
        self.click_sound.play()

    def play_ui_hover(self):
        self.hover_sound.set_volume(self.sfx_volume * 0.4)
        self.hover_sound.play()
=======
    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
>>>>>>> claude/laughing-ardinghelli-b72776

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