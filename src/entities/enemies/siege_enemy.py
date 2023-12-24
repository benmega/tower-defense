from src.entities.enemies.enemy import Enemy
# Siege Enemy
class SiegeEnemy(Enemy):
    def __init__(self, path, image_path='path/to/siege_enemy.png'):
        super().__init__(health=200, speed=1.5, path=path, image_path=image_path)
    # Additional siege logic can be added here
