import random as _random

from src.entities.entity import Entity
from src.config.config import (
    DEBUG, TOWER_TYPES, TILE_SIZE, TOWER_SELL_RATE, TOWER_DEFAULT_SPLASH_RADIUS,
    TOWER_CRIT_DAMAGE_MULTIPLIER, TOWER_SPLASH_DAMAGE_FACTOR, TOWER_HEAL_ON_HIT_AMOUNT,
    TOWER_MAX_UPGRADE_LEVEL, TOWER_UPGRADE_DAMAGE_MULTIPLIER, TOWER_UPGRADE_RANGE_MULTIPLIER,
    TOWER_UPGRADE_COST_FACTOR, TOWER_PREVIEW_ALPHA,
)
import src.config.config as configuration
from src.utils.helpers import load_scaled_image

class Tower(Entity):
    def __init__(self, x, y, tower_type="Basic", attack_range=None, damage=None, attack_speed=None,
                 upgrade_cost=0, width=None, height=None):
        type_info = TOWER_TYPES[tower_type]
        self.image_path = type_info['image_path']
        super().__init__(x, y, image_path=self.image_path)
        self.image = load_scaled_image(self.image_path, TILE_SIZE).convert_alpha()
        self.x = x // TILE_SIZE[0] * TILE_SIZE[0]
        self.y = y // TILE_SIZE[1] * TILE_SIZE[1]
        self.width = width if width is not None else TILE_SIZE[0]
        self.height = height if height is not None else TILE_SIZE[1]
        self.attack_range = attack_range if attack_range is not None else type_info['attack_range']
        self.damage = damage if damage is not None else type_info['damage']
        self.attack_speed = attack_speed if attack_speed is not None else type_info['attack_speed']
        self._base_attack_speed = self.attack_speed  # baseline cooldown SpeedBoost auras revert to
        self.cooldown = 0
        self.upgrade_level = 0
        self.tower_type = tower_type
        self.projectile_type = tower_type
        self.build_cost = type_info['cost']
        self.upgrade_cost = upgrade_cost
        self.sell_value = int(self.build_cost * TOWER_SELL_RATE)
        # Combat skill modifiers — populated by TowerManager.apply_initial_skill_effects
        self.crit_chance = 0.0      # probability of 2x damage (critical_hit_chance skill)
        self.heal_chance = 0.0      # probability of healing player 1 HP on hit (healing_ability skill)
        self.heal_callback = None   # set to Player.heal by TowerManager
        self.splash_chance = 0.0    # probability of splash AoE on hit (splash_damage skill)
        self.splash_radius = TOWER_DEFAULT_SPLASH_RADIUS  # pixel radius of splash damage
        self.armor_pierce = 0.0     # fraction of enemy armor bypassed (armor_piercing skill)

    def is_enemy_in_range(self, enemy):
        enemy_x, enemy_y = enemy.rect.x, enemy.rect.y
        distance = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
        return distance <= self.attack_range

    def attack(self, target, projectile_manager):
        if DEBUG:
            print("Creating a projectile")
        damage = self.damage * TOWER_CRIT_DAMAGE_MULTIPLIER if (
            self.crit_chance > 0 and _random.random() < self.crit_chance) else self.damage
        if self.heal_chance > 0 and _random.random() < self.heal_chance and self.heal_callback:
            self.heal_callback(TOWER_HEAL_ON_HIT_AMOUNT)
        projectile_manager.create_projectile(
            self.x, self.y, self.projectile_type, target,
            damage_override=damage,
            armor_pierce=self.armor_pierce,
        )

    def _apply_splash(self, primary_target, enemies):
        """Deal splash-skill damage to enemies near the primary target (splash_damage skill)."""
        splash_dmg = self.damage * TOWER_SPLASH_DAMAGE_FACTOR
        tx, ty = primary_target.rect.centerx, primary_target.rect.centery
        for enemy in enemies:
            if enemy is primary_target or enemy.state == 'dead':
                continue
            dx = enemy.rect.centerx - tx
            dy = enemy.rect.centery - ty
            if (dx * dx + dy * dy) ** 0.5 <= self.splash_radius:
                enemy.take_damage(splash_dmg, armor_pierce=self.armor_pierce)

    def update(self, enemies, projectile_manager):
        self.cooldown -= configuration.GAME_SPEED_MULTIPLIER
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    self.attack(enemy, projectile_manager)
                    if self.splash_chance > 0 and _random.random() < self.splash_chance:
                        self._apply_splash(enemy, enemies)
                    break

    def can_upgrade(self):
        return self.upgrade_level < TOWER_MAX_UPGRADE_LEVEL

    def upgrade(self):
        if self.can_upgrade():
            self.upgrade_level += 1
            self.damage = int(self.damage * TOWER_UPGRADE_DAMAGE_MULTIPLIER)
            self.attack_range = int(self.attack_range * TOWER_UPGRADE_RANGE_MULTIPLIER)
            self.upgrade_cost = int(self.build_cost * (TOWER_UPGRADE_COST_FACTOR * (self.upgrade_level + 1)))

    _preview_surfaces_cache = {}

    @staticmethod
    def get_preview_surface(tower_type):
        if tower_type not in Tower._preview_surfaces_cache:
            image_path = TOWER_TYPES[tower_type]['image_path']
            surface = load_scaled_image(image_path, TILE_SIZE)
            surface.set_alpha(TOWER_PREVIEW_ALPHA)
            Tower._preview_surfaces_cache[tower_type] = surface
        return Tower._preview_surfaces_cache[tower_type]