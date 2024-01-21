from src.config.config import DEBUG
from src.managers.entity_manager import EntityManager


class TowerManager(EntityManager):
    def __init__(self):
        super().__init__()
        self.towers = []

    def add_tower(self, tower):
        """ Adds a new tower at specified coordinates if it's a valid position. """
        if self.is_valid_position(tower.x, tower.y) and self.has_enough_resources(tower):
            self.towers.append(tower)
            self.deduct_resources(tower)
        else:
            print("Invalid position or insufficient resources")


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
        if DEBUG == True:
            print(f'drawing {len(self.towers)} towers')
        for tower in self.towers:
            tower.draw(screen)

    def select_tower_type(self, tower_type):
        """ Selects the type of tower to build. """
        self.selected_tower_type = tower_type

    def is_valid_position(self, x, y):
        """ Checks if the position is valid for placing a tower. """
        # TODO Implement logic to determine if the position is valid (e.g., not on a path)
        return True

    def has_enough_resources(self, tower):
        """ Checks if the player has enough resources to build the selected tower. """
        # TODO Implement logic to check player resources against tower cost
        return True

    def deduct_resources(self, tower):
        """ Deducts resources from the player based on the tower cost. """
        # TODO Implement logic to deduct resources
        pass

    def update(self, enemies, projectile_manager):
        """ Updates each tower and handles their attacks. """
        for tower in self.towers:
            tower.update(enemies, projectile_manager)

    # Additional methods as needed, such as collision detection, selecting towers, etc.
