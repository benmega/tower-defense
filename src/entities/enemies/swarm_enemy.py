from src.config.config import SWARM_ENEMY_IMAGE_PATH, ENEMY_TYPES
from src.entities.enemies.enemy import Enemy
# Swarm Enemy
class SwarmEnemy(Enemy):
    def __init__(self, path, image_path=SWARM_ENEMY_IMAGE_PATH):
        stats = ENEMY_TYPES['Swarm']
        super().__init__(health=stats['health'], speed=stats['speed'], path=path, image_path=image_path)
