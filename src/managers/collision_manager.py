import pygame

from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.projectile import Projectile


class CollisionManager:
    def __init__(self):
        # Initialize any necessary data structures or variables
        pass

    def check_collision(self, entity1, entity2):
        """ Checks for collision between two entities. """
        # Implement collision detection logic
        # For example, using bounding box or circle collision detection
        rect1 = pygame.Rect(entity1.x, entity1.y, entity1.width, entity1.height)
        rect2 = pygame.Rect(entity2.x, entity2.y, entity2.width, entity2.height)
        return rect1.colliderect(rect2)

    def resolve_collision(self, entity1, entity2):
        """ Resolve what happens when two entities collide. """
        # Implement logic based on types of entities
        # For example, if a projectile hits an enemy, reduce enemy health
        if isinstance(entity1, Projectile) and isinstance(entity2, Enemy):
            entity2.take_damage(entity1.damage)
            entity1.state = 'expired'  # Mark projectile for removal

        # Add more cases as necessary

    def handle_collisions(self, entities):
        """ Handles collisions between multiple entities. """
        # Implement logic to check for collisions between multiple entities
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if self.check_collision(entity1, entity2):
                    self.resolve_collision(entity1, entity2)

    # Additional methods for specific collision scenarios can be added here
