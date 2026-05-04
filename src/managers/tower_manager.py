import pygame
<<<<<<< HEAD
import os
=======
import math
>>>>>>> claude/suspicious-raman-d0a593

from src.config.config import DEBUG, TILE_SIZE
from src.managers.entity_manager import EntityManager
from src.entities.towers.tower_types import *
<<<<<<< HEAD
<<<<<<< HEAD
from src.utils.helpers import resource_path
=======
from src.utils.helpers import get_asset_path
>>>>>>> claude/unruffled-ramanujan-1882ca
=======
from src.utils import constants as C
>>>>>>> claude/suspicious-raman-d0a593


class TowerManager(EntityManager):
    def __init__(self, player):
        super().__init__()
        self.player = player  # Reference to the player object to access skills
        self.towers = []
        self.selected_tower_type = 'Basic'
        self.selected_tower = None
        self.show_ranges = False
        self.tower_types = {
            'Basic': BasicTower,
            'Advanced': AdvancedTower,
            'Sniper': SniperTower,
            'Cannon': CannonTower,
            'Flame': FlameTower,
            'Frost': FrostTower,
            'Electric': ElectricTower,
            'Laser': LaserTower,
            'Missile': MissileTower,
            'Poison': PoisonTower,
            'Splash': SplashTower,
            'Multi': MultiTargetTower,
            'SpeedBoost': SpeedBoostTower,
            'GoldBoost': GoldBoostTower,
            'Debuff': DebuffTower,
        }
<<<<<<< HEAD
        self.build_sound = pygame.mixer.Sound(resource_path('assets/sounds/tower_build_effect_2.mp3'))  # Preload sound
=======
        sound_path = get_asset_path('assets/sounds/tower_build_effect_2.mp3')
        self.build_sound = pygame.mixer.Sound(sound_path)  # Preload sound
>>>>>>> claude/unruffled-ramanujan-1882ca

    def add_tower(self, x, y):
        """Adds a new tower at specified coordinates."""
        tower_class = self.tower_types.get(self.selected_tower_type, None)
        if tower_class:
            tower = tower_class(x, y)  # Create an instance of the tower
            self.apply_initial_skill_effects(tower)  # Apply any skill effects
            self.towers.append(tower)
            self.play_build_sound()
        else:
            print(f"Unknown tower type: {self.selected_tower_type}")

    def play_build_sound(self):
        self.build_sound.play()

    def upgrade_tower(self, tower_id, upgrade_type):
        """ Upgrades a tower based on an upgrade type. """
        for tower in self.towers:
            if tower.id == tower_id:
                tower.upgrade(upgrade_type)
                break

    def remove_tower(self, tower_id):
        """ Removes a tower based on its ID. """
        self.towers = [tower for tower in self.towers if tower.id != tower_id]

    def get_towers(self):
        """ Returns a list of all towers. """
        return self.towers

    def handle_attacks(self, enemies):
        """ Calls each tower's attack method, passing in the list of enemies. """
        for tower in self.towers:
            tower.attack(enemies)

    def serialize_towers(self):
        """ Prepares tower data for saving to a file or for transitioning between levels. """
        return [tower.serialize() for tower in self.towers]

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
        damage_boost_level = self.player.skills.get('damage_boost', 0)
        tower.damage *= (1 + damage_boost_level * 0.05)  # Assuming each level increases damage by 5%

    def update(self, enemies, projectile_manager):
        for tower in self.towers:
            tower.update(enemies, projectile_manager)


    def add_tower_if_possible(self, x, y, player, game):
        """Attempts to add a tower at the specified location if the player has enough resources."""
        build_type = self.selected_tower_type
        build_cost = TOWER_TYPES[build_type]['cost']
        build_cost_reduction = player.skills.get('tower_build_discount', 0) * 10  # Adjust formula as needed
        adjusted_cost = max(0, build_cost - build_cost_reduction)

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
                print("Invalid position for tower.")
        else:
            print("Not enough gold to build tower.")
        return False

    def handle_click(self, pos):
        """Handle clicks on the game board. Selects a tower if clicked. Returns the selected tower or None."""
        self.selected_tower = None
        for tower in self.towers:
            # Check if click is within tower's rect
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
