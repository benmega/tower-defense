# Configuration settings for the game
DEBUG = False
SCREEN_WIDTH: int
SCREEN_HEIGHT: int
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (30, 30)
DEFAULT_GRID_SIZE = (25, 20)
GAME_BOARD_WIDTH = DEFAULT_GRID_SIZE[0]
GAME_BOARD_HEIGHT = DEFAULT_GRID_SIZE[1]

# Player starting health
PLAYER_HEALTH = 100
PLAYER_GOLD = 1000
PLAYER_SCORE = 0

# Default enemy attributes
ENEMY_HEALTH = 50
ENEMY_SPEED = 2
ENEMY_SCORE_VALUE = 100
ENEMY_GOLD_VALUE = 10
ENEMY_DAMAGE_TO_PLAYER = 10
ENEMY_IMAGE_PATH = 'assets/images/enemies/enemy.png'
SIEGE_ENEMY_IMAGE_PATH = 'assets/images/enemies/tank_enemy.png'
FAST_ENEMY_IMAGE_PATH = 'assets/images/enemies/fast_enemy.png'
FLYING_ENEMY_IMAGE_PATH = 'assets/images/enemies/flying_enemy.png'
HEALER_ENEMY_IMAGE_PATH = 'assets/images/enemies/healer_enemy.png'
STEALTH_ENEMY_IMAGE_PATH = 'assets/images/enemies/stealth_enemy.png'
SWARM_ENEMY_IMAGE_PATH = 'assets/images/enemies/swarm_enemy.png'
TANK_ENEMY_IMAGE_PATH = 'assets/images/enemies/tank_enemy.png'
BASIC_ENEMY_IMAGE_PATH = 'assets/images/enemies/basic_enemy.png'


# Spawn settings
ENEMY_SPAWN_INTERVAL = 2000  # Milliseconds
MAX_ENEMIES_PER_LEVEL = 20


# Tower default attributes
TOWER_RANGE = 100
TOWER_DAMAGE = 10
TOWER_ATTACK_SPEED = 1  # Attacks per second
TOWER_COST = 200
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
LEVEL_BACKGROUND_PATH = 'assets/images/backgrounds/grass.png'
GRASS_IMAGE_PATH = 'assets/images/backgrounds/grass.png'
ENTRANCE_IMAGE_PATH = 'assets/images/backgrounds/entrance.png'
EXIT_IMAGE_PATH = 'assets/images/backgrounds/exit.png'
PATH_IMAGE_PATH = 'assets/images/backgrounds/path.png'
LEVELS_JSON_PATH = 'src/config/TestLevels.json'

# UI elements
UI_FONT = 'Arial'
UI_FONT_SIZE = 14
UI_FONT_COLOR = (255,255,255)
UI_HEALTH_BAR_COLOR = (255, 0, 0)
UI_LABEL_HEIGHT = 50
UI_SCORE_POSITION = (SCREEN_WIDTH-200, 10)
UI_HEALTH_POSITION = (SCREEN_WIDTH-200, 10+UI_LABEL_HEIGHT)
UI_RESOURCES_POSITION = (SCREEN_WIDTH-200, 10+UI_LABEL_HEIGHT*2)
UI_ENEMY_COUNT_POSITION = (SCREEN_WIDTH-200, 10+UI_LABEL_HEIGHT*3)
MAIN_MENU_START_BUTTON_POSITION = (360, 253)
MAIN_MENU_LOAD_BUTTON_POSITION = (360, 300)
MAIN_MENU_SETTINGS_BUTTON_POSITION = (360, 350)
MAIN_MENU_EXIT_BUTTON_POSITION = (360, 407)

# Sound effects and music
SOUND_EFFECTS_VOLUME = 0.7
BACKGROUND_MUSIC_PATH = 'assets/audio/background_music.mp3'
BACKGROUND_MUSIC_VOLUME = 0.5

# Other settings
DEBUG_MODE = DEBUG
SAVE_GAME_PATH = '../save_data/game_save.json'

