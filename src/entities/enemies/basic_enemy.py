# Basic Enemy
from src.config.config import BASIC_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy


class BasicEnemy(Enemy):
    def __init__(self, path, image_path=BASIC_ENEMY_IMAGE_PATH ):
        super().__init__(health=100, speed=1, path=path, image_path=image_path)