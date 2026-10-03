from src.config.config import HEALER_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy


class HealerEnemy(Enemy):
    _STATS = ENEMY_TYPES['Healer']
    HEALING_RANGE = _STATS['healing_range']
    HEALING_PER_FRAME = _STATS['healing_per_frame']

    def __init__(self, path, image_path=HEALER_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Healer']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
        self.armor = stats['armor']

    def update(self, entities=None):
        super().update(entities)
        if self.state != 'dead' and self.active and entities:
            self._heal_nearby_enemies(entities)

    def _heal_nearby_enemies(self, entities):
        for enemy in entities:
            if enemy is self or enemy.state == 'dead' or not enemy.active:
                continue
            distance = self._distance_to(enemy)
            if distance <= self.HEALING_RANGE:
                enemy.health = min(enemy.health + self.HEALING_PER_FRAME, enemy.health + 100)

    def _distance_to(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        return (dx * dx + dy * dy) ** 0.5
