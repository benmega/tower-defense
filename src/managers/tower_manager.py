import pygame
import math
from functools import partial

from src.config.config import DEBUG, TILE_SIZE, TOWER_TYPES, TOWER_MIN_ATTACK_SPEED
from src.managers.entity_manager import EntityManager
from src.entities.towers.tower import Tower
from src.entities.towers.tower_types import FlameTower, MultiTower, SpeedBoostTower
from src.screens.skills_screen import all_skills
from src.utils import constants as C
from src.utils.resource_path import resource_path


class TowerManager(EntityManager):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.towers = []
        self.selected_tower_type = None
        self.selected_tower = None
        self.show_ranges = False
        self.tower_types = {t: partial(Tower, tower_type=t) for t in TOWER_TYPES}
        self.tower_types['Flame'] = FlameTower
        self.tower_types['Multi'] = MultiTower
        self.tower_types['SpeedBoost'] = SpeedBoostTower
        try:
            self.build_sound = pygame.mixer.Sound(resource_path('assets/sounds/tower_build_effect_2.mp3'))
        except Exception:
            self.build_sound = None

    def add_tower(self, x, y):
        """Adds a new tower at specified coordinates."""
        tower_class = self.tower_types.get(self.selected_tower_type, None)
        if tower_class:
            tower = tower_class(x, y)  # Create an instance of the tower
            self.apply_initial_skill_effects(tower)  # Apply any skill effects
            self.towers.append(tower)
            self.play_build_sound()
        else:
            if DEBUG:
                print(f"Unknown tower type: {self.selected_tower_type}")

    def play_build_sound(self):
        if self.build_sound:
            self.build_sound.play()

    def get_towers(self):
        return self.towers

    def draw_towers(self, screen):
        """ Draws all towers onto the screen. """
        if DEBUG:
            print(f'drawing {len(self.towers)} towers')
        for tower in self.towers:
            tower.draw(screen)

    def select_tower_type(self, tower_type):
        """ Selects the type of tower to build. """
        self.selected_tower_type = tower_type

    def is_valid_position(self, x, y, game):
        """ Checks if the position is valid for placing a tower. """
        mouse_pos = (x,y)
        return game.board.can_build_at(mouse_pos)

    def apply_initial_skill_effects(self, tower):
        """Applies initial skill effects to a tower upon creation."""
        skills = self.player.skills
        damage_boost = skills.get('damage_boost', 0)
        speed_boost = skills.get('attack_speed', 0)
        range_boost = skills.get('range_extension', 0)
        tower.damage = int(tower.damage * (1 + damage_boost * all_skills['damage_boost']['effect_per_level']))
        tower.attack_range = int(tower.attack_range * (1 + range_boost * all_skills['range_extension']['effect_per_level']))
        # Lower attack_speed (cooldown) means faster
        tower.attack_speed = max(
            TOWER_MIN_ATTACK_SPEED,
            int(tower.attack_speed * (1 - speed_boost * all_skills['attack_speed']['effect_per_level']))
        )
        # Combat skill modifiers
        tower.crit_chance = skills.get('critical_hit_chance', 0) * all_skills['critical_hit_chance']['effect_per_level']
        tower.heal_chance = skills.get('healing_ability', 0) * all_skills['healing_ability']['effect_per_level']
        tower.splash_chance = skills.get('splash_damage', 0) * all_skills['splash_damage']['effect_per_level']
        tower.armor_pierce = skills.get('armor_piercing', 0) * all_skills['armor_piercing']['effect_per_level']
        tower.heal_callback = self.player.heal
        tower._base_attack_speed = tower.attack_speed

    def update(self, enemies, projectile_manager):
        for tower in self.towers:
            tower.update(enemies, projectile_manager)
        self._apply_speed_boost_auras()

    def _apply_speed_boost_auras(self):
        """Recompute each tower's attack speed fresh every frame from its base cooldown,
        so overlapping/expiring SpeedBoost auras never stack."""
        boosters = [t for t in self.towers if isinstance(t, SpeedBoostTower)]
        for tower in self.towers:
            if isinstance(tower, SpeedBoostTower):
                continue
            best_boost = 0.0
            for booster in boosters:
                if self._in_aura_range(booster, tower):
                    best_boost = max(best_boost, booster.boost_amount)
            if best_boost > 0:
                tower.attack_speed = max(
                    TOWER_MIN_ATTACK_SPEED, int(tower._base_attack_speed * (1 - best_boost))
                )
            else:
                tower.attack_speed = tower._base_attack_speed

    @staticmethod
    def _in_aura_range(booster, tower):
        dx = booster.x - tower.x
        dy = booster.y - tower.y
        return (dx * dx + dy * dy) ** 0.5 <= booster.attack_range

    def add_tower_if_possible(self, x, y, player, game):
        """Attempts to add a tower at the specified location if the player has enough resources."""
        build_type = self.selected_tower_type
        build_cost = TOWER_TYPES[build_type]['cost']
        discount_pct = player.skills.get('tower_build_discount', 0) * all_skills['tower_build_discount']['effect_per_level']
        adjusted_cost = max(1, int(build_cost * (1.0 - discount_pct)))

        if player.gold >= adjusted_cost:
            if self.is_valid_position(x, y, game):
                self.add_tower(x, y)
                player.spend_gold(adjusted_cost)
                # Emit tower placement particles
                tower_center_x = x + TILE_SIZE[0] // 2
                tower_center_y = y + TILE_SIZE[1] // 2
                game.particles.emit(tower_center_x, tower_center_y,
                                  count=14, color=C.RGB_AMBER, speed=3.0, spread=math.pi*2, life=0.7)
                return True
            else:
                if DEBUG:
                    print("Invalid position for tower.")
        else:
            if DEBUG:
                print("Not enough gold to build tower.")
        return False

    def handle_click(self, pos):
        """Handle clicks on the game board. Selects a tower if clicked. Returns the selected tower or None."""
        self.selected_tower = None
        for tower in self.towers:
            tower_rect = pygame.Rect(tower.x, tower.y, tower.width, tower.height)
            if tower_rect.collidepoint(pos):
                self.selected_tower = tower
                return tower
        return None

    def toggle_ranges(self):
        """Toggle the visibility of tower range circles."""
        self.show_ranges = not self.show_ranges

    def sell_tower(self, tower, player):
        """Sell a tower and refund its value to the player."""
        if tower in self.towers:
            player.add_gold(tower.sell_value)
            self.towers.remove(tower)
            if self.selected_tower == tower:
                self.selected_tower = None

    def handle_hover(self, pos):
        """Check if mouse is hovering over a tower. Returns the tower or None."""
        for tower in self.towers:
            tower_rect = pygame.Rect(tower.x, tower.y, tower.width, tower.height)
            if tower_rect.collidepoint(pos):
                return tower
        return None
