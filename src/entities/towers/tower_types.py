import src.config.config as configuration
from src.config.config import TOWER_TYPES
from src.effects.damage_effects import AoeDamageEffect
from src.entities.towers.tower import Tower

class BasicTower(Tower):
    def __init__(self, x, y, tower_type='Basic'):
        super().__init__(x, y)

class AdvancedTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Advanced')

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Sniper')

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Cannon')

class FlameTower(Tower):
    def __init__(self, x, y):
        # Initialize with specific parameters for the FlameTower
        super().__init__(x, y, tower_type='Flame')
        self.aoe_radius = 50  # The radius within which enemies will be affected by the AOE damage

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
            if self.is_enemy_in_affect_range(enemy):
                enemy.take_damage(self.damage)

    def is_enemy_in_affect_range(self, enemy):
        enemy_x, enemy_y = enemy.rect.center
        distance = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
        return distance <= self.aoe_radius



class FrostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Frost')
        self.slow_percentage = 0.5
        self.slow_duration = 60

class ElectricTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Electric')

class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Laser')

class MissileTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Missile')

class PoisonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Poison')


class SplashTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Splash')

class MultiTargetTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Multi')

class SpeedBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='SpeedBoost')

class GoldBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='GoldBoost')

class DebuffTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Debuff')
