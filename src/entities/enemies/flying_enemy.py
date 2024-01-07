from src.config.config import FLYING_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Flying Enemy
class FlyingEnemy(Enemy):
    def __init__(self, path, image_path=FLYING_ENEMY_IMAGE_PATH):
        super().__init__(health=120, speed=2, path=path, image_path=image_path)
