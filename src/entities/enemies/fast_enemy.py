from src.entities.enemies.enemy import Enemy
# Fast Enemy
class FastEnemy(Enemy):
    def __init__(self, path, image_path='assets/images/enemies/fast_enemy.png'):
        super().__init__(health=50, speed=5, path=path, image_path=image_path)
