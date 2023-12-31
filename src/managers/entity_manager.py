import pygame.sprite


class EntityManager:
    def __init__(self):
        self.entities = pygame.sprite.Group()

    def add(self, entity):
        self.entities.add(entity)

    def remove(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update_entities(self):
        for e in self.entities: #TODO avoid duplication
            e.update()
       # self.entities.update() #TODO avoid duplication


    def draw(self, screen):
        for entity in self.entities:
            entity.draw(screen)


    # Additional shared methods like collision detection, etc.
