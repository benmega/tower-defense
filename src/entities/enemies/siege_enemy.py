from src.config.config import SIEGE_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Siege Enemy
class SiegeEnemy(Enemy):
    def __init__(self, path, image_path=SIEGE_ENEMY_IMAGE_PATH):
        super().__init__(health=200, speed=1, path=path, image_path=image_path)
    # Additional siege logic can be added here
