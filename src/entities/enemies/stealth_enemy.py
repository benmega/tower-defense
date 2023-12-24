from src.entities.enemies.enemy import Enemy
# Stealth Enemy
class StealthEnemy(Enemy):
    def __init__(self, path, image_path='path/to/stealth_enemy.png'):
        super().__init__(health=80, speed=3, path=path, image_path=image_path)
    # Additional stealth logic can be added here
