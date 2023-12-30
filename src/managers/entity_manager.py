class EntityManager:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)

    def remove(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update(self):
        for entity in self.entities:
            entity.update()

    def draw(self, screen):
        for entity in self.entities:
            entity.draw(screen)

    # Additional shared methods like collision detection, etc.
