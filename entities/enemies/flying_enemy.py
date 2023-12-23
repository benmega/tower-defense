from entities.enemies.enemy import Enemy
# Flying Enemy
class FlyingEnemy(Enemy):
    def __init__(self, path, image_path='path/to/flying_enemy.png'):
        super().__init__(health=120, speed=3, path=path, image_path=image_path)
