from src.config.config import TOWER_TYPES, DEBUG
from src.effects.damage_effects import AoeDamageEffect
from src.entities.towers.tower import Tower

class BasicTower(Tower):
    def __init__(self, x, y, tower_type='Basic'):
        super().__init__(x, y)
        #self.tower_type = 'Basic'
        # BasicTower specific initialization

class AdvancedTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Advanced')
        # AdvancedTower specific initialization

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Sniper')
        # SniperTower specific initialization

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Cannon')
        # CannonTower specific initialization

class FlameTower(Tower):
    def __init__(self, x, y):
        # Initialize with specific parameters for the FlameTower
        super().__init__(x, y, tower_type='Flame')
        self.aoe_radius = 50  # The radius within which enemies will be affected by the AOE damage

    def update(self, enemies, projectile_manager):
        """
        Override the update method to perform AOE damage.
        """
        ifPrimaryTarget = True
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            # Instead of breaking after finding the first enemy in range,
            # we continue to check all enemies to apply AOE damage.
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    if ifPrimaryTarget:
                        self.attack(enemy, projectile_manager)
                        ifPrimaryTarget = False
                    else:
                        self.apply_aoe_damage(enemy, enemies)

    def apply_aoe_damage(self, primary_target, enemies):
        """
        Apply damage to the primary target and any other enemies within the AOE radius.
        """
        # Create an AOE damage effect at the tower's location
        effect = AoeDamageEffect((self.x, self.y), self.aoe_radius)
        #all_effects.add(effect)
        # TODO Manage all effects
        # Apply damage as before
        for enemy in enemies:
            if self.is_enemy_in_affect_range(enemy):
                enemy.take_damage(self.damage)
    def is_enemy_in_affect_range(self, enemy):
        """
        Check if an enemy is within the AOE effect range of the tower.
        """
        enemy_x, enemy_y = enemy.rect.center
        distance = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
        return distance <= self.aoe_radius



class FrostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Frost')
        self.slow_percentage = 0.5  # 50% reduction in speed
        self.slow_duration = 60  # Duration of slow effect in frames or ticks

    def attack(self, target, projectile_manager):
        """
        Create a projectile and target the specified enemy.
        """
        target_x, target_y = target.rect.x, target.rect.y
        projectile_manager.create_projectile(self.x, self.y, self.projectile_type, target, effect='slow')

class ElectricTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Electric')
        # ElectricTower specific initialization, could chain attack to nearby enemies

class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Laser')
        # LaserTower specific initialization, high damage and precision

class MissileTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Missile')
        # MissileTower specific initialization, long range and high damage

class PoisonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Poison')
        # No need to pass poison_damage or poison_duration here since it's handled within the projectile

    def attack(self, target, projectile_manager):
        """
        Override the attack method to create a poison projectile without explicitly passing 'damage'.
        """

        # Ensure self.projectile_type is a string that corresponds to a key in PROJECTILE_TYPES
        # For example, 'Poison' if your PROJECTILE_TYPES dictionary has a 'Poison' key for poison projectiles
        projectile_type = 'Poison'  # This should be dynamically set based on the tower type

        if DEBUG:
            print("Creating a poison projectile")
        projectile_manager.create_projectile(
            self.x, self.y, target=target,projectile_type=projectile_type,
        )
        if DEBUG:
            print(f"Poison projectile created at ({self.x}, {self.y}) targeting ({target.rect.x}, {target.rect.y})")


class SplashTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Splash')
        # SplashTower specific initialization, deals damage to multiple enemies

class MultiTargetTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='Multi')
        # MultiTargetTower specific initialization, can target multiple enemies simultaneously

class SpeedBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y,tower_type='SpeedBoost')
        # SpeedBoostTower specific initialization, increases attack speed of nearby towers


class GoldBoostTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='GoldBoost')

    def attack(self, target, projectile_manager):
        projectile_manager.create_projectile(
            self.x, self.y, self.projectile_type, target,
            effect='gold_boost'
        )


class DebuffTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, tower_type='Debuff')
        # DebuffTower specific initialization, weakens enemies in range (reduces their speed, damage resistance, etc.)
