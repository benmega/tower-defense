from src.config.config import HEALER_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Healer Enemy
class HealerEnemy(Enemy):
    def __init__(self, path, image_path=HEALER_ENEMY_IMAGE_PATH ):
        super().__init__(health=100, speed=1, path=path, image_path=image_path)
    # Additional healing logic can be added here
