from src.config.config import TANK_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Tank Enemy
class TankEnemy(Enemy):
    def __init__(self, path, image_path=TANK_ENEMY_IMAGE_PATH ):
        super().__init__(health=300, speed=1, path=path, image_path=image_path)
