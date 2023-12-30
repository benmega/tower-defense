import pygame
from src.entities.projectiles.projectile import Projectile
from src.managers.entity_manager import EntityManager


class ProjectileManager(EntityManager):
    def __init__(self):
        super().__init__()
        self.projectiles = []

    def create_projectile(self, x, y, projectile_type, target):
        #self.x, self.y, self.damage, self.projectile_speed, target
        if projectile_type == "BasicProjectile":
            projectile = Projectile(x,y,target,5,10)
        elif projectile_type == "missle":
            projectile = Projectile(x, y, target, 10, 100)
        elif projectile_type == "bullet":
            projectile = Projectile(x, y, target, 100, 1000)
        else:
            projectile = Projectile(x, y, target, 5, 10)

        self.projectiles.append(projectile)

    def update_projectiles(self):
        for projectile in self.projectiles[:]:  # Iterate over a copy to avoid modification issues
            projectile.move()
            if projectile.state == 'expired':
                self.projectiles.remove(projectile)

    def draw_projectiles(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
