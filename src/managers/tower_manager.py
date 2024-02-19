from src.config.config import DEBUG
from src.managers.entity_manager import EntityManager
from src.entities.towers.tower_types import *


class TowerManager(EntityManager):
    def __init__(self, player):
        super().__init__()
        self.player = player  # Reference to the player object to access skills
        self.towers = []
        self.selected_tower_type = 'Basic'
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

    def add_tower(self, x, y):
        """Adds a new tower at specified coordinates."""
        tower_class = self.tower_types.get(self.selected_tower_type, None)
        if tower_class:
            tower = tower_class(x, y)  # Create an instance of the tower
            self.apply_initial_skill_effects(tower)  # Apply any skill effects
            self.towers.append(tower)
        else:
            print(f"Unknown tower type: {self.selected_tower_type}")

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
        #return game.board.is_within_panel(mouse_pos)
        return game.board.can_build_at(mouse_pos)

    def has_enough_resources_to_build(self):
        """ Checks if the player has enough resources to build the selected tower. """
        # TODO Implement logic to check player resources against tower cost
        return True

    def deduct_resources(self, tower):
        """ Deducts resources from the player based on the tower cost. """
        # TODO Implement logic to deduct resources
        return True

    def apply_initial_skill_effects(self, tower):
        """Applies initial skill effects to a tower upon creation."""
        # Example: Increase initial damage based on a skill
        damage_boost_level = self.player.skills.get('damage_boost', 0)
        tower.damage *= (1 + damage_boost_level * 0.05)  # Assuming each level increases damage by 5%

    def update(self, enemies, projectile_manager):
        """Updated to consider skills affecting towers during the game."""
        for tower in self.towers:
            # Example: Increase attack speed based on a skill
            attack_speed_increase = self.player.skills.get('attack_speed', 0)
            tower.attack_speed += attack_speed_increase
            tower.update(enemies, projectile_manager)

    # Additional methods as needed, such as collision detection, selecting towers, etc.

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
                return True
            else:
                print("Invalid position for tower.")
        else:
            print("Not enough gold to build tower.")
        return False
