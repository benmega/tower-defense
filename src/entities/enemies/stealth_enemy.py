from src.config.config import STEALTH_ENEMY_IMAGE_PATH
from src.entities.enemies.enemy import Enemy
# Stealth Enemy
class StealthEnemy(Enemy):
    def __init__(self, path, image_path=STEALTH_ENEMY_IMAGE_PATH ):
        super().__init__(health=80, speed=2, path=path, image_path=image_path)
    # Additional stealth logic can be added here
