from src.config.config import STEALTH_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy


class StealthEnemy(Enemy):
    _STATS = ENEMY_TYPES['Stealth']
    STEALTH_ACTIVATION_TIME = _STATS['stealth_activation_frames']  # frames (3 seconds at 60 FPS)
    STEALTH_DAMAGE_REDUCTION = _STATS['stealth_damage_reduction']
    STEALTH_ALPHA = _STATS['stealth_alpha']

    def __init__(self, path, image_path=STEALTH_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Stealth']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
        self._time_since_hit = 0
        self._is_stealthed = False
        self._original_alpha = 255

    def update(self, entities=None):
        super().update(entities)
        if self.state != 'dead' and self.active:
            self._update_stealth()

    def _update_stealth(self):
        self._time_since_hit += 1
        if self._time_since_hit >= self.STEALTH_ACTIVATION_TIME and not self._is_stealthed:
            self._become_stealthed()
        elif self._is_stealthed and self._time_since_hit < self.STEALTH_ACTIVATION_TIME:
            self._become_visible()

    def _become_stealthed(self):
        self._is_stealthed = True
        self.image.set_alpha(100)

    def _become_visible(self):
        self._is_stealthed = False
        self.image.set_alpha(255)

    def take_damage(self, amount, armor_pierce=0.0):
        if self._is_stealthed:
            amount = int(amount * self.STEALTH_DAMAGE_REDUCTION)
        self._time_since_hit = 0
        self._become_visible()
        super().take_damage(amount, armor_pierce=armor_pierce)

    def on_collision(self, other_entity, enemies=None):
        self._time_since_hit = 0
        self._become_visible()
        super().on_collision(other_entity, enemies)
