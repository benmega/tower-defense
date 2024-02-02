import pygame

from src.managers.entity_manager import EntityManager


class EnemyManager(EntityManager):
    def __init__(self, defeat_callback=None):
        super().__init__()
        self.entities = pygame.sprite.Group()
        self.current_wave = None
        self.defeat_callback = defeat_callback



    def set_current_wave(self, wave):
        """ Set the current enemy wave for spawning. """
        self.current_wave = wave


    def update(self):
        """ Update the state of all enemies and spawn new ones from the current wave. """
        current_time = pygame.time.get_ticks()
        if self.current_wave:
            new_enemy = self.current_wave.update(current_time)
            if new_enemy:
                self.add_enemy(new_enemy)

        self.update_entities()
        for enemy in list(self.entities):  # Make a copy of the group list to iterate over
            if enemy.state == 'dead':
                if self.defeat_callback:
                    self.defeat_callback(enemy)
                self.entities.remove(enemy)
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
