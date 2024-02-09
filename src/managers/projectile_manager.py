from src.config.config import PROJECTILE_TYPES
from src.entities.projectiles.projectile import Projectile
from src.managers.entity_manager import EntityManager


class ProjectileManager(EntityManager):
    def __init__(self):
        super().__init__()
        self.projectiles = []

    def create_projectile(self, x, y, projectile_type, target,effect=None):
        # self.x, self.y, self.damage, self.projectile_speed, target

        # damage = PROJECTILE_TYPES[projectile_type]['damage']
        # speed = PROJECTILE_TYPES[projectile_type]['speed']
        #
        # image_path = PROJECTILE_TYPES[projectile_type]['image_path']

        projectile = Projectile(x, y, target, **PROJECTILE_TYPES[projectile_type])
        self.projectiles.append(projectile)

    def update_entities(self):
        for projectile in self.projectiles[:]:  # Iterate over a copy to avoid modification issues
            projectile.move()
            if projectile.state == 'expired':
                self.projectiles.remove(projectile)

    def draw_projectiles(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
