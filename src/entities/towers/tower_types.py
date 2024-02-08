from src.config.config import TOWER_TYPES
from src.entities.towers.tower import Tower

class BasicTower(Tower):
    def __init__(self, x, y, tower_type='Basic'):
        super().__init__(x, y)
        #self.tower_type = 'Basic'
        # BasicTower specific initialization

class AdvancedTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Advanced', attack_range=150, damage=15, attack_speed=15)
        # AdvancedTower specific initialization

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Sniper',attack_range=300, damage=30, attack_speed=60)
        # SniperTower specific initialization

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Cannon',attack_range=120, damage=20, attack_speed=30)
        # CannonTower specific initialization

class FlameTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Flame',attack_range=100, damage=8, attack_speed=10)
        # FlameTower specific initialization, perhaps AOE damage

class FrostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Frost', attack_range=120, damage=5, attack_speed=20)
        # FrostTower specific initialization, could slow enemies

class ElectricTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Electric', attack_range=150, damage=15, attack_speed=25 )
        # ElectricTower specific initialization, could chain attack to nearby enemies

class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Laser',attack_range=200, damage=25, attack_speed=30)
        # LaserTower specific initialization, high damage and precision

class MissileTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Missile', attack_range=250, damage=30, attack_speed=50)
        # MissileTower specific initialization, long range and high damage

class PoisonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Poison',attack_range=120, damage=10, attack_speed=20)
        # PoisonTower specific initialization, could apply damage over time

class SplashTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Splash', attack_range=100, damage=20, attack_speed=30)
        # SplashTower specific initialization, deals damage to multiple enemies

class MultiTargetTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Multi', attack_range=150, damage=15, attack_speed=25)
        # MultiTargetTower specific initialization, can target multiple enemies simultaneously

class SpeedBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='SpeedBoost')
        # SpeedBoostTower specific initialization, increases attack speed of nearby towers

class GoldBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='GoldBoost')
        # GoldBoostTower specific initialization, increases gold earned from defeating enemies

class DebuffTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Debuff')
        # DebuffTower specific initialization, weakens enemies in range (reduces their speed, damage resistance, etc.)
