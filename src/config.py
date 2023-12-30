# Configuration settings for the game

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (32, 32)
DEFAULT_GRID_SIZE = (32, 32)

# Player starting health
PLAYER_HEALTH = 100

# Player starting resources/money
PLAYER_RESOURCES = 1000

# Player score
PLAYER_SCORE = 0

# Default enemy attributes
ENEMY_HEALTH = 50
ENEMY_SPEED = 2
ENEMY_IMAGE_PATH = 'assets/images/enemies/enemy.png'

# Spawn settings
ENEMY_SPAWN_INTERVAL = 2000  # Milliseconds
MAX_ENEMIES_PER_LEVEL = 20


# Tower default attributes
TOWER_RANGE = 100
TOWER_DAMAGE = 10
TOWER_ATTACK_SPEED = 1.5  # Attacks per second
TOWER_COST = 100
TOWER_IMAGE_PATH = 'assets/images/towers/basic_tower.png'

# Upgrades
TOWER_UPGRADE_COST = {
    "range": 50,
    "damage": 75,
    "speed": 60,
}


# Projectile attributes
PROJECTILE_SPEED = 5
PROJECTILE_DAMAGE = 10
PROJECTILE_IMAGE_PATH = 'assets/images/projectiles/basic_projectile.png'


# Level configuration
LEVEL_COUNT = 10
LEVEL_BACKGROUND_PATH = 'assets/images/backgrounds/level_background.png'


# UI elements
UI_FONT = 'Arial'
UI_FONT_SIZE = 14
UI_HEALTH_BAR_COLOR = (255, 0, 0)
UI_SCORE_POSITION = (10, 10)
UI_HEALTH_POSITION = (10, 30)


# Sound effects and music
SOUND_EFFECTS_VOLUME = 0.7
BACKGROUND_MUSIC_PATH = 'assets/audio/background_music.mp3'
BACKGROUND_MUSIC_VOLUME = 0.5

# Other settings
DEBUG_MODE = True
SAVE_GAME_PATH = 'save_data/game_save.json'
