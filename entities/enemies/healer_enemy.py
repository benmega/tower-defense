from entities.enemies.enemy import Enemy
# Healer Enemy
class HealerEnemy(Enemy):
    def __init__(self, path, image_path='path/to/healer_enemy.png'):
        super().__init__(health=100, speed=2, path=path, image_path=image_path)
    # Additional healing logic can be added here
