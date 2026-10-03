from src.config.config import PROJECTILE_TYPES
from src.entities.projectiles.projectile import Projectile
from src.managers.entity_manager import EntityManager


class ProjectileManager(EntityManager):
    def __init__(self):
        super().__init__()
        self.projectiles = []

    def create_projectile(self, x, y, projectile_type, target,
                          damage_override=None, armor_pierce=0.0):
        proj_config = dict(PROJECTILE_TYPES[projectile_type])
        if damage_override is not None:
            proj_config['damage'] = damage_override
        projectile = Projectile(x, y, target, armor_pierce=armor_pierce, **proj_config)
        self.projectiles.append(projectile)

    def update_entities(self):
        for projectile in self.projectiles[:]:  # Iterate over a copy to avoid modification issues
            projectile.move()
            if projectile.state == 'expired':
                self.projectiles.remove(projectile)

    def draw_projectiles(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
