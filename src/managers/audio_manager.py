import pygame

'''
    sources = { "background_music" : "https://www.youtube.com/watch?v=pgLjYsVP4H0"
'''

class AudioManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer module
        self.music_volume = 0.5  # Default music volume
        self.sfx_volume = 0.5  # Default sound effects volume
        self.build_sound = pygame.mixer.Sound('assets/sounds/hammer-hit-on-wood.wav')

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
            # This assumes you manage your sound effects objects to set their volumes individually
