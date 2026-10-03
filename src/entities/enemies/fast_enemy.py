from src.config.config import FAST_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy
# Fast Enemy
class FastEnemy(Enemy):
    def __init__(self, path, image_path=FAST_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Fast']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
