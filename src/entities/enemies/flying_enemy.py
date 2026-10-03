from src.config.config import FLYING_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy
# Flying Enemy
class FlyingEnemy(Enemy):
    def __init__(self, path, image_path=FLYING_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Flying']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
