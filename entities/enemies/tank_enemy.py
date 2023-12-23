from entities.enemies.enemy import Enemy
# Tank Enemy
class TankEnemy(Enemy):
    def __init__(self, path, image_path='path/to/tank_enemy.png'):
        super().__init__(health=300, speed=1, path=path, image_path=image_path)
