# level.py
class Level:
    def __init__(self, enemy_wave_list, path, level_number):
        self.enemy_wave_list = enemy_wave_list
        self.path = path
        self.level_number = level_number
        self.current_wave = 0

    def get_next_wave(self):
        if self.current_wave < len(self.enemy_wave_list):
            wave = self.enemy_wave_list[self.current_wave]
            self.current_wave += 1
            return wave
        return None

