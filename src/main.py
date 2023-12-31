# Constants
'''
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (32, 32)
ENEMY_IMAGE_PATH = '../assets/images/enemies/enemy.png'
TOWER_IMAGE_PATH = '../assets/images/towers/tower.png'
PROJECTILE_IMAGE_PATH = '../assets/images/projectiles/projectile.png'
'''

from src.game.game import Game

if __name__ == "__main__":
    game_instance  = Game()
    game_instance.run()