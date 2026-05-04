import pygame

from src.config.config import BACKGROUND_MUSIC_VOLUME, SOUND_EFFECTS_VOLUME
from src.game.game_state import GameState
from src.utils import constants as C

'''
    sources = { "background_music" : "https://www.youtube.com/watch?v=pgLjYsVP4H0"
'''

class AudioManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer module
        self.music_volume = BACKGROUND_MUSIC_VOLUME  # Default music volume
        self.sfx_volume = SOUND_EFFECTS_VOLUME  # Default sound effects volume
        self.build_sound = pygame.mixer.Sound('assets/sounds/hammer-hit-on-wood.wav')
        self.state_music_map = {
            GameState.MAIN_MENU: 'assets/sounds/main_menu_background.mp3',
            GameState.CAMPAIGN_MAP: 'assets/sounds/campaign_map_background.mp3',
            GameState.PLAYING: 'assets/sounds/playing_background.mp3',
            # Add other states as necessary
        }
        self.current_music = None

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
    def play_sound(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def play_music(self, music_path, loops=-1):
        pygame.mixer.music.load(music_path)
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