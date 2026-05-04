import pygame

class CollisionManager:
    def __init__(self):
        pass

    @staticmethod
    def _get_rect(entity):
        """Prefer sprite rect; fall back to x/y/width/height for legacy entities."""
        if hasattr(entity, "rect") and entity.rect is not None:
            return entity.rect
        return pygame.Rect(entity.x, entity.y, entity.width, entity.height)

    def check_collision(self, entity1, entity2):
        """ Checks for collision between two entities. """
        rect1 = self._get_rect(entity1)
        rect2 = self._get_rect(entity2)
        return rect1.colliderect(rect2)

    def resolve_collision(self, entity1, entity2):
        """ Resolve what happens when two entities collide. """
        if hasattr(entity1, 'on_collision') and callable(getattr(entity1, 'on_collision')):
            entity1.on_collision(entity2)
        if hasattr(entity2, 'on_collision') and callable(getattr(entity2, 'on_collision')):
            entity2.on_collision(entity1)

    def handle_collisions(self, entities):
        """ Handles collisions between individual entities. """
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if self.check_collision(entity1, entity2):
                    self.resolve_collision(entity1, entity2)


    def handle_group_collisions(self, group1, group2):
        """
        Checks and handles collisions between two groups.

        :param group1: First group of sprites (pygame.sprite.Group).
        :param group2: Second group of sprites (pygame.sprite.Group).
        """
        # Ensure group1 and group2 are pygame.sprite.Group objects
        if not isinstance(group1, pygame.sprite.Group):
            group1 = pygame.sprite.Group(group1)
        if not isinstance(group2, pygame.sprite.Group):
            group2 = pygame.sprite.Group(group2)

        # Check for collisions between the groups
        collisions = pygame.sprite.groupcollide(group1, group2, dokilla=False, dokillb=False)

        # Handle each collision
        for entity1, entities2 in collisions.items():
            for entity2 in entities2:
                if hasattr(entity1, 'on_collision') and callable(getattr(entity1, 'on_collision')):
                    entity1.on_collision(entity2)
                if hasattr(entity2, 'on_collision') and callable(getattr(entity2, 'on_collision')):
                    entity2.on_collision(entity1)
