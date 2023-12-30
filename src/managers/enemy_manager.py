import pygame

from src.managers.entity_manager import EntityManager


class EnemyManager(EntityManager):
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.current_wave = None

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

        self.update_enemies()

    def add_enemy(self, enemy):
        """ Add a new enemy to the manager. """
        self.enemies.append(enemy)

    def update_enemies(self):
        """ Update each enemy's position and check for removal conditions. """
        for enemy in self.enemies[:]:  # Iterate over a copy to allow removal within the loop
            enemy.move()
            if enemy.health <= 0 or enemy.state == 'dead' or enemy.reached_goal:
                self.enemies.remove(enemy)

    def get_enemies(self):
        """ Return the list of currently active enemies. """
        return self.enemies

    def reset(self):
        """ Reset the enemy manager for a new level. """
        self.enemies.clear()
        self.current_wave = None

    # Additional methods can be added as needed
    def draw_enemies(self,screen):
        pass