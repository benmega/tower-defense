import pygame
from board.game_board import GameBoard
from entities.enemies.enemy import Enemy
from entities.towers.tower import Tower

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (32, 32)
ENEMY_IMAGE_PATH = 'assets/images/enemy.png'
TOWER_IMAGE_PATH = 'assets/images/tower.png'
PROJECTILE_IMAGE_PATH = 'assets/images/projectile.png'


def load_scaled_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense Game")

    running = True
    clock = pygame.time.Clock()

    game_board = GameBoard(width=100, height=100)
    path = [(0, 0), (200, 100), (200, 200), (0, 400)]

    enemy = Enemy(health=100, speed=1, path=path, image_path=ENEMY_IMAGE_PATH)
    game_board.add_enemy(enemy)

    tower_image = load_scaled_image(TOWER_IMAGE_PATH, TILE_SIZE)
    tower_positions = [(20, 30), (50, 50), (70, 20)]
    for pos in tower_positions:
        game_board.add_tower(Tower(pos[0], pos[1], attack_range=3, damage=10, attack_speed=30))

    active_projectiles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        for enemy in game_board.enemies:
            enemy.move()

        # Rendering
        screen.fill(BACKGROUND_COLOR)
        for enemy in game_board.enemies:
            enemy_image = load_scaled_image(enemy.image_path, TILE_SIZE)
            if enemy_image:
                screen.blit(enemy_image, (enemy.x, enemy.y))

        for tower in game_board.towers:
            tower.update(game_board.enemies)
            screen.blit(tower_image, (tower.x, tower.y))

        for projectile in active_projectiles:
            projectile.move()
            if projectile.hit_target():
                active_projectiles.remove(projectile)
            else:
                projectile_image = load_scaled_image(PROJECTILE_IMAGE_PATH, TILE_SIZE)
                if projectile_image:
                    screen.blit(projectile_image, (projectile.x, projectile.y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()