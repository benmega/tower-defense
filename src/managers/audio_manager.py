import pygame

from src.config.config import BACKGROUND_MUSIC_VOLUME, SOUND_EFFECTS_VOLUME
from src.game.game_state import GameState
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

'''
    sources = { "background_music" : "https://www.youtube.com/watch?v=pgLjYsVP4H0"
'''

class AudioManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer module
        self.music_volume = BACKGROUND_MUSIC_VOLUME  # Default music volume
        self.sfx_volume = SOUND_EFFECTS_VOLUME  # Default sound effects volume
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
        }
        self.current_music = None

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

    def play_ui_click(self):
        self.click_sound.set_volume(self.sfx_volume)
        self.click_sound.play()

    def play_ui_hover(self):
        self.hover_sound.set_volume(self.sfx_volume * 0.4)
        self.hover_sound.play()

    def play_music_for_state(self, game_state):
        music_path = self.state_music_map.get(game_state)
        if music_path and music_path != self.current_music:
            self.play_music(music_path)
            self.current_music = music_path