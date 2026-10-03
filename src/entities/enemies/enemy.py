import pygame

import src.config.config as configuration
from src.utils.helpers import load_scaled_image
from src.config.config import ENEMY_IMAGE_PATH, TILE_SIZE, DEBUG, ENEMY_GOLD_VALUE, ENEMY_SCORE_VALUE, \
    ENEMY_DAMAGE_TO_PLAYER


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, speed, path, image_path=ENEMY_IMAGE_PATH):
        super().__init__()
        if not path or len(path) == 0:
            raise ValueError("Invalid path provided to Enemy")
        self.image = load_scaled_image(image_path, TILE_SIZE).convert_alpha()
        self.rect = self.image.get_rect(topleft=path[0])
        self.health = health
        self.max_health = health
        self.speed = speed
        self.path = path
        self.path_index = 0
        self.active = True
        self.state = 'moving'  # Possible states: 'moving', 'attacking', 'idle', 'finished'
        self.reached_goal = False
        self.score_value = ENEMY_SCORE_VALUE
        self.base_gold_value = ENEMY_GOLD_VALUE
        self.gold_value = max(5, int(health / 10))
        self.damage_to_player = ENEMY_DAMAGE_TO_PLAYER
        self.original_speed = speed
        self.slow_effect_active = False
        self.slow_effect_duration = 0
        self.poisoned = False
        self.poison_damage = 0
        self.poison_duration = 0
        self.armor = 0.0  # fraction of incoming damage blocked (0.0–1.0)
        self.debuff_active = False
        self.damage_taken_multiplier = 1.0
        self.debuff_duration = 0
        self.beam_active = False
        self.beam_damage = 0
        self.beam_duration = 0

    def move(self):

        if self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            self.move_towards(next_x, next_y)
        else: #path complete
            self.state = 'finished'
            self.reached_goal = True

    def move_towards(self, next_x, next_y):
        dir_x, dir_y = next_x - self.rect.x, next_y - self.rect.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance != 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        # Apply game speed multiplier for fast-forward
        effective_speed = self.speed * configuration.GAME_SPEED_MULTIPLIER
        self.rect.x += dir_x * effective_speed
        self.rect.y += dir_y * effective_speed

        if abs(self.rect.x - next_x) <= self.speed and abs(self.rect.y - next_y) <= self.speed:
            self.rect.x, self.rect.y = next_x, next_y
            if self.path_index < len(self.path):
                self.path_index += 1

    def is_invisible(self):
        return self.state in ('dead', 'idle')

    def take_damage(self, amount, armor_pierce=0.0):
        if not self.is_invisible():
            reduction = max(0.0, self.armor - armor_pierce)
            self.health -= amount * self.damage_taken_multiplier * (1.0 - reduction)
            if self.health <= 0:
                self.die()

    def die(self):
        self.state = 'dead'
        self.active = False

    def update(self, entities=None):
        if self.state == 'dead' or not self.active:
            return  # Skip updating if the enemy is dead or inactive
        self.update_slow_effect()
        self.update_poison_effect()
        self.update_debuff_effect()
        self.update_beam_effect()
        self.move()

    def apply_slow_effect(self, percentage_reduction, duration):
        if not self.slow_effect_active or self.speed > self.original_speed * (1 - percentage_reduction):
            self.speed = self.original_speed * (1 - percentage_reduction)
            self.slow_effect_duration = duration
            self.slow_effect_active = True

    def update_slow_effect(self):
        if self.slow_effect_active:
            self.slow_effect_duration -= configuration.GAME_SPEED_MULTIPLIER
            if self.slow_effect_duration <= 0:
                self.speed = self.original_speed
                self.slow_effect_active = False

    def apply_poison_effect(self, damage_per_tick, duration):
        self.poisoned = True
        self.poison_damage = damage_per_tick
        self.poison_duration = duration

    def update_poison_effect(self):
        if self.poisoned:
            self.poison_duration -= configuration.GAME_SPEED_MULTIPLIER
            self.take_damage(self.poison_damage * configuration.GAME_SPEED_MULTIPLIER)
            if self.poison_duration <= 0:
                self.poisoned = False
                self.poison_damage = 0


    def apply_debuff_effect(self, multiplier, duration):
        if not self.debuff_active or multiplier > self.damage_taken_multiplier:
            self.damage_taken_multiplier = multiplier
            self.debuff_duration = duration
            self.debuff_active = True

    def update_debuff_effect(self):
        if self.debuff_active:
            self.debuff_duration -= configuration.GAME_SPEED_MULTIPLIER
            if self.debuff_duration <= 0:
                self.damage_taken_multiplier = 1.0
                self.debuff_active = False

    def apply_beam_effect(self, damage_per_tick, duration):
        self.beam_active = True
        self.beam_damage = damage_per_tick
        self.beam_duration = duration

    def update_beam_effect(self):
        if self.beam_active:
            self.beam_duration -= configuration.GAME_SPEED_MULTIPLIER
            self.take_damage(self.beam_damage * configuration.GAME_SPEED_MULTIPLIER)
            if self.beam_duration <= 0:
                self.beam_active = False
                self.beam_damage = 0

    def draw_health_bar(self, screen):
        if self.state == 'dead':
            return
        bar_w = self.rect.width
        bar_h = 4
        x = self.rect.left
        y = self.rect.top - 6
        fill = max(0, int(bar_w * self.health / self.max_health))
        pygame.draw.rect(screen, (180, 0, 0), (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, fill, bar_h))

        # Blue tint when slowed
        if self.slow_effect_active:
            tint = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            tint.fill((60, 120, 255, 70))
            screen.blit(tint, self.rect.topleft)
        # Green tint when poisoned
        if self.poisoned:
            tint = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            tint.fill((0, 200, 60, 80))
            screen.blit(tint, self.rect.topleft)
        # Purple tint when debuffed
        if self.debuff_active:
            tint = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            tint.fill((160, 60, 200, 80))
            screen.blit(tint, self.rect.topleft)
        # Orange tint while under a sustained beam
        if self.beam_active:
            tint = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            tint.fill((255, 140, 0, 70))
            screen.blit(tint, self.rect.topleft)

    def apply_gold_boost(self, boost_factor):
        self.gold_value = int(max(self.gold_value, self.base_gold_value * boost_factor))