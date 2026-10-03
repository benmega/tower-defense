import src.config.config as configuration
from src.config.config import TOWER_TYPES, PROJECTILE_TYPES
from src.effects.damage_effects import AoeDamageEffect
from src.entities.towers.tower import Tower


class FlameTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Flame')
        self.aoe_radius = TOWER_TYPES['Flame']['aoe_radius']

    def update(self, enemies, projectile_manager):
        is_primary_target = True
        self.cooldown -= configuration.GAME_SPEED_MULTIPLIER
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    if is_primary_target:
                        self.attack(enemy, projectile_manager)
                        is_primary_target = False
                    else:
                        self.apply_aoe_damage(enemy, enemies)

    def apply_aoe_damage(self, primary_target, enemies):
        AoeDamageEffect((self.x, self.y), self.aoe_radius)
        for enemy in enemies:
            if self._in_aoe_range(enemy):
                enemy.take_damage(self.damage)

    def _in_aoe_range(self, enemy):
        enemy_x, enemy_y = enemy.rect.center
        distance = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
        return distance <= self.aoe_radius


class MultiTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Multi')
        self.target_count = PROJECTILE_TYPES['Multi']['target_count']

    def update(self, enemies, projectile_manager):
        self.cooldown -= configuration.GAME_SPEED_MULTIPLIER
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            targets_hit = 0
            for enemy in enemies:
                if targets_hit >= self.target_count:
                    break
                if self.is_enemy_in_range(enemy):
                    self.attack(enemy, projectile_manager)
                    targets_hit += 1


class SpeedBoostTower(Tower):
    """Pure aura tower: boosts nearby towers' attack speed instead of firing projectiles."""

    def __init__(self, x, y):
        super().__init__(x, y, tower_type='SpeedBoost')
        self.boost_amount = PROJECTILE_TYPES['SpeedBoost']['boost_amount']

    def update(self, enemies, projectile_manager):
        pass
