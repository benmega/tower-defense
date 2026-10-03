from src.config.config import TANK_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy
# Tank Enemy
class TankEnemy(Enemy):
    def __init__(self, path, image_path=TANK_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Tank']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
        self.armor = stats['armor']
