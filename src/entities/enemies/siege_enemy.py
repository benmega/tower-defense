from src.config.config import SIEGE_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy
# Siege Enemy
class SiegeEnemy(Enemy):
    def __init__(self, path, image_path=SIEGE_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Siege']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
        self.armor = stats['armor']
