# Configuration settings for the game
DEBUG = False
SCREEN_WIDTH: int
SCREEN_HEIGHT: int
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
TILE_SIZE = (30, 30)
DEFAULT_GRID_SIZE = (27, 20)
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
TOWER_TYPES = {
    'Advanced': {
        'image_path': 'assets/images/towers/advanced_tower.png',
        'cost': 150,
    },
    'Basic': {
        'image_path': 'assets/images/towers/basic_tower.png',
        'cost': 100,
    },
    'Cannon': {
        'image_path': 'assets/images/towers/cannon_tower.png',
        'cost': 250,
    },
    'Debuff': {
        'image_path': 'assets/images/towers/debuff_tower.png',
        'cost': 800,
    },
    'Electric': {
        'image_path': 'assets/images/towers/electric_tower.png',
        'cost': 400,
    },
    'Flame': {
        'image_path': 'assets/images/towers/flame_tower.png',
        'cost': 300,
    },
    'Frost': {
        'image_path': 'assets/images/towers/frost_tower.png',
        'cost': 350,
    },
    'GoldBoost': {
        'image_path': 'assets/images/towers/gold_boost_tower.png',
        'cost': 750,
    },
    'Laser': {
        'image_path': 'assets/images/towers/laser_tower.png',
        'cost': 450,
    },
    'Missile': {
        'image_path': 'assets/images/towers/missile_tower.png',
        'cost': 500,
    },
    'Multi': {
        'image_path': 'assets/images/towers/multi_target_tower.png',
        'cost': 650,
    },
    'Poison': {
        'image_path': 'assets/images/towers/poison_tower.png',
        'cost': 550,
    },
    'Sniper': {
        'image_path': 'assets/images/towers/sniper_tower.png',
        'cost': 200,
    },
    'SpeedBoost': {
        'image_path': 'assets/images/towers/speed_boost_tower.png',
        'cost': 700,
    },
    'Splash': {
        'image_path': 'assets/images/towers/splash_tower.png',
        'cost': 600,
    },
}
#
# TOWER_COSTS = {
#     'Advanced': 150,
#     'Basic': 100,
#     'Cannon': 250,
#     'Debuff': 800,
#     'Electric': 400,
#     'Flame': 300,
#     'Frost': 350,
#     'GoldBoost': 750,
#     'Laser': 450,
#     'Missile': 500,
#     'Multi': 650,
#     'Poison': 550,
#     'Sniper': 200,
#     'SpeedBoost': 700,
#     'Splash': 600
# }
# TOWER_IMAGE_PATHS = {
#     'Advanced': 'assets/images/towers/advanced_tower.png',
#     'Basic': 'assets/images/towers/basic_tower.png',
#     'Cannon': 'assets/images/towers/cannon_tower.png',
#     'Debuff': 'assets/images/towers/debuff_tower.png',
#     'Electric': 'assets/images/towers/electric_tower.png',
#     'Flame': 'assets/images/towers/flame_tower.png',
#     'Frost': 'assets/images/towers/frost_tower.png',
#     'GoldBoost': 'assets/images/towers/gold_boost_tower.png',
#     'Laser': 'assets/images/towers/laser_tower.png',
#     'Missile': 'assets/images/towers/missile_tower.png',
#     'Multi': 'assets/images/towers/multi_target_tower.png',
#     #'Poison': 'assets/images/towers/poison_tower.png',
#     'Sniper': 'assets/images/towers/sniper_tower.png'
#     #'SpeedBoost': 'assets/images/towers/speed_boost_tower.png',
#     #'Splash': 'assets/images/towers/splash_tower.png',
# }
# # Upgrades
# TOWER_UPGRADE_COST = {
#     "range": 50,
#     "damage": 75,
#     "speed": 60,
# }


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
UI_BUTTON_SIZE = (95, 30)

# Main Menu Elements
MAIN_MENU_BACKGROUND_PATH = 'assets/images/screens/main_menu_screen.png'
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

