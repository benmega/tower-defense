from src.config.config import TOWER_IMAGE_PATHS, TOWER_COSTS
from src.entities.towers.tower import Tower







class BasicTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, image_path=TOWER_IMAGE_PATHS['Basic'], build_cost=TOWER_COSTS['Basic'])
        self.tower_type = 'Basic'
        # BasicTower specific initialization

class AdvancedTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=150, damage=15, attack_speed=15, image_path=TOWER_IMAGE_PATHS['Advanced'], build_cost=TOWER_COSTS['Advanced'])
        self.tower_type = 'Advanced'
        # AdvancedTower specific initialization

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=300, damage=30, attack_speed=60, image_path=TOWER_IMAGE_PATHS['Sniper'], build_cost=TOWER_COSTS['Sniper'])
        self.tower_type = 'Sniper'
        # SniperTower specific initialization

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=120, damage=20, attack_speed=30, image_path=TOWER_IMAGE_PATHS['Cannon'], build_cost=TOWER_COSTS['Cannon'])
        self.tower_type = 'Cannon'
        # CannonTower specific initialization

class FlameTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=100, damage=8, attack_speed=10, image_path=TOWER_IMAGE_PATHS['Flame'], build_cost=TOWER_COSTS['Flame'])
        self.tower_type = 'Flame'
        # FlameTower specific initialization, perhaps AOE damage

class FrostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=120, damage=5, attack_speed=20, image_path=TOWER_IMAGE_PATHS['Frost'], build_cost=TOWER_COSTS['Frost'])
        self.tower_type = 'Frost'
        # FrostTower specific initialization, could slow enemies

class ElectricTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=150, damage=15, attack_speed=25, image_path=TOWER_IMAGE_PATHS['Electric'], build_cost=TOWER_COSTS['Electric'])
        self.tower_type = 'Electric'
        # ElectricTower specific initialization, could chain attack to nearby enemies

class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=200, damage=25, attack_speed=30, image_path=TOWER_IMAGE_PATHS['Laser'], build_cost=TOWER_COSTS['Laser'])
        self.tower_type = 'Laser'
        # LaserTower specific initialization, high damage and precision

class MissileTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=250, damage=30, attack_speed=50, image_path=TOWER_IMAGE_PATHS['Missile'], build_cost=TOWER_COSTS['Missile'])
        self.tower_type = 'Missile'
        # MissileTower specific initialization, long range and high damage

class PoisonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=120, damage=10, attack_speed=20, image_path=TOWER_IMAGE_PATHS['Poison'], build_cost=TOWER_COSTS['Poison'])
        self.tower_type = 'Poison'
        # PoisonTower specific initialization, could apply damage over time

class SplashTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=100, damage=20, attack_speed=30, image_path=TOWER_IMAGE_PATHS['Splash'], build_cost=TOWER_COSTS['Splash'])
        self.tower_type = 'Splash'
        # SplashTower specific initialization, deals damage to multiple enemies

class MultiTargetTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, attack_range=150, damage=15, attack_speed=25, image_path=TOWER_IMAGE_PATHS['Multi'], build_cost=TOWER_COSTS['Multi'])
        self.tower_type = 'Multi'
        # MultiTargetTower specific initialization, can target multiple enemies simultaneously

class SpeedBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, image_path=TOWER_IMAGE_PATHS['SpeedBoost'], build_cost=TOWER_COSTS['SpeedBoost'])
        self.tower_type = 'SpeedBoost'
        # SpeedBoostTower specific initialization, increases attack speed of nearby towers

class GoldBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, image_path=TOWER_IMAGE_PATHS['GoldBoost'], build_cost=TOWER_COSTS['GoldBoost'])
        self.tower_type = 'GoldBoost'
        # GoldBoostTower specific initialization, increases gold earned from defeating enemies

class DebuffTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, image_path=TOWER_IMAGE_PATHS['Debuff'], build_cost=TOWER_COSTS['Debuff'])
        self.tower_type = 'Debuff'
        # DebuffTower specific initialization, weakens enemies in range (reduces their speed, damage resistance, etc.)
