from src.config.config import SWARM_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Swarm Enemy
class SwarmEnemy(Enemy):
    def __init__(self, path, image_path=SWARM_ENEMY_IMAGE_PATH ):
        super().__init__(health=30, speed=1.5, path=path, image_path=image_path)
