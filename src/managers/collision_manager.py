import pygame

class CollisionManager:
    def __init__(self):
        # Initialize any necessary data structures or variables
        pass

    def check_collision(self, entity1, entity2):
        """ Checks for collision between two entities. """
        rect1 = pygame.Rect(entity1.x, entity1.y, entity1.width, entity1.height)
        rect2 = pygame.Rect(entity2.x, entity2.y, entity2.width, entity2.height)
        return rect1.colliderect(rect2)

    def resolve_collision(self, entity1, entity2):
        """ Resolve what happens when two entities collide. """
        if hasattr(entity1, 'on_collision') and callable(getattr(entity1, 'on_collision')):
            entity1.on_collision(entity2)
        if hasattr(entity2, 'on_collision') and callable(getattr(entity2, 'on_collision')):
            entity2.on_collision(entity1)

    def handle_collisions(self, entities):
        """ Handles collisions between multiple entities. """
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if self.check_collision(entity1, entity2):
                    self.resolve_collision(entity1, entity2)

    # Additional methods for specific collision scenarios can be added here
