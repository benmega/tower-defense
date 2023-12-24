# Basic Enemy
from src.entities.enemies.enemy import Enemy


class BasicEnemy(Enemy):
    def __init__(self, path, image_path='assets/images/enemies/basic_enemy.png'):
        super().__init__(health=100, speed=2, path=path, image_path=image_path)