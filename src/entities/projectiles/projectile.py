import pygame

import src.config.config as configuration
from src.entities.enemies.enemy import Enemy
from src.entities.entity import Entity
from src.config.config import (
    PROJECTILE_IMAGE_PATH, DEBUG, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, FPS,
    PROJECTILE_SPLASH_DAMAGE_FACTOR,
)
from src.utils.helpers import load_scaled_image


class Projectile(Entity):
    def __init__(self, x, y, target, speed=0, damage=0, image_path=PROJECTILE_IMAGE_PATH,
                 effect=None, poison_damage=0, poison_duration=0, gold_boost_factor=1,
                 armor_pierce=0.0, slow_effect=0.5, slow_duration=60,
                 splash_radius=0, explosion_radius=0, chain_targets=0,
                 chain_damage_reduction=0.0, chain_jump_range=0,
                 duration=0, damage_multiplier=1.0, **kwargs):
        super().__init__(x, y, image_path)
        self.size = tuple(element // 2 for element in TILE_SIZE)
        self.image = load_scaled_image(image_path, self.size).convert_alpha()
        self.isPiercing = False
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'
        self.effect = effect
        self.poison_damage = poison_damage
        self.poison_duration = poison_duration
        self.gold_boost_factor = gold_boost_factor
        self.armor_pierce = armor_pierce
        self.slow_effect = slow_effect
        self.slow_duration = slow_duration
        self.splash_radius = splash_radius
        self.explosion_radius = explosion_radius
        self.chain_targets = chain_targets
        self.chain_damage_reduction = chain_damage_reduction
        self.chain_jump_range = chain_jump_range
        self.duration = duration
        self.damage_multiplier = damage_multiplier

    def update(self):
        self.move()

    def move(self):
        if self.state == 'expired':
            return
        if DEBUG:
            print('projectile moving')
        dir_x, dir_y = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance > 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        effective_speed = self.speed * configuration.GAME_SPEED_MULTIPLIER
        self.rect.x += dir_x * effective_speed
        self.rect.y += dir_y * effective_speed

        if self.reached_target():
            self.target.take_damage(self.damage, armor_pierce=self.armor_pierce)
            self.state = 'expired'
        elif self.out_of_bounds():
            self.state = 'expired'

    def reached_target(self):
        effective_speed = self.speed * configuration.GAME_SPEED_MULTIPLIER
        return ((self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2) ** 0.5 <= effective_speed

    def out_of_bounds(self):
        return not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def on_collision(self, other_entity, enemies=None):
        if isinstance(other_entity, Enemy):
            other_entity.take_damage(self.damage, armor_pierce=self.armor_pierce)
            enemies = enemies or []
            if self.effect == 'slow':
                other_entity.apply_slow_effect(percentage_reduction=self.slow_effect, duration=self.slow_duration)
            elif self.effect == 'poison':
                other_entity.apply_poison_effect(self.poison_damage, self.poison_duration)
            elif self.effect == 'gold_boost':
                other_entity.apply_gold_boost(self.gold_boost_factor)
            elif self.effect == 'splash' and self.splash_radius > 0:
                self._apply_area_damage(other_entity, enemies, self.splash_radius)
            elif self.effect == 'explode' and self.explosion_radius > 0:
                self._apply_area_damage(other_entity, enemies, self.explosion_radius)
            elif self.effect == 'chain' and self.chain_targets > 0:
                self._apply_chain(other_entity, enemies)
            elif self.effect == 'continuous' and self.duration > 0:
                duration_frames = self.duration * FPS
                other_entity.apply_beam_effect(self.damage / duration_frames, duration_frames)
            elif self.effect == 'debuff' and self.duration > 0:
                other_entity.apply_debuff_effect(self.damage_multiplier, self.duration * FPS)
            if not self.isPiercing:
                self.state = 'expired'

    def _apply_area_damage(self, primary_target, enemies, radius):
        """Deal splash/explode damage to enemies near the primary target's impact point."""
        cx, cy = primary_target.rect.centerx, primary_target.rect.centery
        area_damage = self.damage * PROJECTILE_SPLASH_DAMAGE_FACTOR
        for enemy in enemies:
            if enemy is primary_target or enemy.state == 'dead':
                continue
            dx = enemy.rect.centerx - cx
            dy = enemy.rect.centery - cy
            if (dx * dx + dy * dy) ** 0.5 <= radius:
                enemy.take_damage(area_damage, armor_pierce=self.armor_pierce)

    def _apply_chain(self, initial_target, enemies):
        """Jump chain-lightning damage between nearby enemies, weakening with each jump."""
        hit = {initial_target}
        current_target = initial_target
        current_damage = self.damage
        for _ in range(self.chain_targets):
            current_damage *= (1 - self.chain_damage_reduction)
            cx, cy = current_target.rect.centerx, current_target.rect.centery
            candidates = [
                enemy for enemy in enemies
                if enemy not in hit and enemy.state != 'dead'
                and ((enemy.rect.centerx - cx) ** 2 + (enemy.rect.centery - cy) ** 2) ** 0.5 <= self.chain_jump_range
            ]
            if not candidates:
                break
            next_target = min(
                candidates,
                key=lambda enemy: (enemy.rect.centerx - cx) ** 2 + (enemy.rect.centery - cy) ** 2
            )
            next_target.take_damage(current_damage, armor_pierce=self.armor_pierce)
            hit.add(next_target)
            current_target = next_target
