from src.entities.enemies.enemy import Enemy
# Swarm Enemy
class SwarmEnemy(Enemy):
    def __init__(self, path, image_path='path/to/swarm_enemy.png'):
        super().__init__(health=30, speed=4, path=path, image_path=image_path)
