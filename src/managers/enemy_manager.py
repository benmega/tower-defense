import pygame

from src.managers.entity_manager import EntityManager


class EnemyManager(EntityManager):
    def __init__(self, level_manager, defeat_callback=None, reach_end_callback=None, ):
        super().__init__()
        self.entities = pygame.sprite.Group()
        self.current_wave = None
        self.level_manager = level_manager
        self.defeat_callback = defeat_callback
        self.reach_end_callback = reach_end_callback

    def update(self):
        """Update active enemies; spawning is owned by Level/LevelManager."""
        self.update_entities()
        for enemy in list(self.entities):  # Make a copy of the group list to iterate over
            if enemy.state == 'dead':
                if self.defeat_callback:
                    self.defeat_callback(enemy)
                self.entities.remove(enemy)
            elif enemy.reached_goal:
                if self.reach_end_callback:
                    self.reach_end_callback(enemy.damage_to_player)
                self.entities.remove(enemy)

    def update_entities(self):
        """Override to pass enemies list to each enemy's update for interactions."""
        for enemy in list(self.entities):
            enemy.update(self.entities)

    def add_enemy(self, enemy):
        """ Add a new enemy to the manager. """
        self.entities.add(enemy)

    def get_enemies(self):
        """ Return the list of currently active enemies. """
        return self.entities

    def reset(self):
        """ Reset the enemy manager for a new level. """
        self.entities = pygame.sprite.Group()
        self.current_wave = None

    def draw(self, screen):
        self.entities.draw(screen)
