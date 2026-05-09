from src.config.config import STEALTH_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy


class StealthEnemy(Enemy):
    STEALTH_ACTIVATION_TIME = 180  # frames (3 seconds at 60 FPS)
    STEALTH_DAMAGE_REDUCTION = 0.5

    def __init__(self, path, image_path=STEALTH_ENEMY_IMAGE_PATH):
        super().__init__(health=80, speed=2, path=path, image_path=image_path)
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

    def take_damage(self, amount):
        if self._is_stealthed:
            amount = int(amount * self.STEALTH_DAMAGE_REDUCTION)
        self._time_since_hit = 0
        self._become_visible()
        super().take_damage(amount)

    def on_collision(self, other_entity):
        self._time_since_hit = 0
        self._become_visible()
        super().on_collision(other_entity)
