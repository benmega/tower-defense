# Configuration settings for the game

DEBUG = False
SCREEN_WIDTH: int
SCREEN_HEIGHT: int

SCREEN_WIDTH, SCREEN_HEIGHT = 1067, 800  # original 800, 600
SCALE = SCREEN_HEIGHT/600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
DEFAULT_GRID_SIZE = (24, 16)
GAME_BOARD_SCREEN_SIZE = int(SCREEN_WIDTH*0.75), int(SCREEN_HEIGHT*0.75)
TILE_SIZE = (GAME_BOARD_SCREEN_SIZE[0]//DEFAULT_GRID_SIZE[0], GAME_BOARD_SCREEN_SIZE[1]//DEFAULT_GRID_SIZE[1])

GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT = DEFAULT_GRID_SIZE

# Player starting health
PLAYER_HEALTH = 100
PLAYER_GOLD = 10000
PLAYER_SCORE = 0
PLAYER_EARLY_WAVE_BONUS_MULTIPLIER = 2

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


# Tower default attributes
TOWER_TYPES = {
    'Advanced': {
        'cost': 150,
        'image_path': 'assets/images/towers/advanced_tower.png',
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


# Projectile attributes

PROJECTILE_IMAGE_PATH = 'assets/images/projectiles/basic_projectile.png'
PROJECTILE_TYPES = {
    'Basic': {
        'image_path': 'assets/images/projectiles/basic_projectile.png',
        'speed': 5,
        'damage': 10,
        'effect': None,
    },
    'Advanced': {
        'image_path': 'assets/images/projectiles/advanced_projectile.png',
        'speed': 7,
        'damage': 15,
        'effect': None,
    },
    'Sniper': {
        'image_path': 'assets/images/projectiles/sniper_projectile.png',
        'speed': 10,
        'damage': 25,
        'effect': 'pierce',
        'pierce_targets': 2,  # Number of enemies the projectile can pass through
    },
    'Cannon': {
        'image_path': 'assets/images/projectiles/cannon_projectile.png',
        'speed': 4,
        'damage': 20,
        'effect': 'splash',
        'splash_radius': 50,
    },
    'Flame': {
        'image_path': 'assets/images/projectiles/flame_projectile.png',
        'speed': 6,
        'damage': 8,
        'effect': 'burn',
        'burn_duration': 3,
        'burn_damage': 2,
    },
    'Frost': {
        'image_path': 'assets/images/projectiles/frost_projectile.png',
        'speed': 5,
        'damage': 10,
        'effect': 'slow',
        'slow_duration': 2,
        'slow_effect': 0.5,
    },
    'Electric': {
        'image_path': 'assets/images/projectiles/electric_projectile.png',
        'speed': 8,
        'damage': 12,
        'effect': 'chain',
        'chain_targets': 3,
        'chain_damage_reduction': 0.2,
    },
    'Laser': {
        'image_path': 'assets/images/projectiles/laser_beam.png',
        'speed': 9,  # Instantaneous hit
        'damage': 18,
        'effect': 'continuous',
        'duration': 2,  # Seconds the beam stays active
    },
    'Missile': {
        'image_path': 'assets/images/projectiles/missile_projectile.png',
        'speed': 3,
        'damage': 30,
        'effect': 'explode',
        'explosion_radius': 75,
    },
    'Poison': {
        'image_path': 'assets/images/projectiles/poison_projectile.png',
        'speed': 3,
        'damage': 0,
        'effect': 'poison',
        'poison_duration': 50,
        'poison_damage': 0.7,
    },
    'Splash': {
        'image_path': 'assets/images/projectiles/splash_projectile.png',
        'speed': 6,
        'damage': 12,
        'effect': 'splash',
        'splash_radius': 60,
    },
    'Multi': {
        'image_path': 'assets/images/projectiles/multi_target_projectile.png',
        'speed': 7,
        'damage': 8,
        'effect': 'multi',
        'target_count': 3,  # Number of enemies simultaneously targeted
    },
    'SpeedBoost': {
        'image_path': 'assets/images/projectiles/speed_boost.png',
        'speed': 0,  # Not applicable
        'damage': 0,  # Not applicable
        'effect': 'speed_boost',
        'boost_amount': 0.2,  # Speed increase percentage for nearby towers
        'duration': 5,  # Seconds the boost lasts
    },
    'GoldBoost': {
        'image_path': 'assets/images/projectiles/gold_boost.png',
        'speed': 3,  # Not applicable
        'damage': 0,  # Not applicable
        'effect': 'gold_boost',
        'gold_boost_factor': 1.2,  # Multiplier to gold earned from enemies hit
    },
    'Debuff': {
        'image_path': 'assets/images/projectiles/debuff_projectile.png',
        'speed': 5,
        'damage': 0,  # Primarily for debuff effect
        'effect': 'debuff',
        'debuff_effect': 'slow',  # Example debuff effect
        'duration': 3,
    },
}


# Level configuration
LEVEL_COUNT = 10
LEVEL_BACKGROUND_PATH = 'assets/images/gameBoardTiles/grass.png'
GRASS_IMAGE_PATH = 'assets/images/gameBoardTiles/grass.png'
ENTRANCE_IMAGE_PATH = 'assets/images/gameBoardTiles/entrance.png'
EXIT_IMAGE_PATH = 'assets/images/gameBoardTiles/exit.png'
PATH_IMAGE_PATH = 'assets/images/gameBoardTiles/path.png'
LEVELS_JSON_PATH = 'src/config/levels/LevelsAll.json'

# UI elements
UI_FONT = 'Arial'
UI_FONT_SIZE = int(18 * SCALE)
UI_FONT_COLOR = (255, 255, 255)
UI_HEALTH_BAR_COLOR = (255, 0, 0)
UI_LABEL_WIDTH, UI_LABEL_HEIGHT = 100 * SCALE, 50 * SCALE
UI_LABEL_PAD_X = 200 * SCALE
UI_LABEL_PAD_Y = 10 * SCALE
UI_SCORE_POSITION = (SCREEN_WIDTH-UI_LABEL_PAD_X, UI_LABEL_PAD_Y)
UI_HEALTH_POSITION = (SCREEN_WIDTH-UI_LABEL_PAD_X, UI_LABEL_PAD_Y+UI_LABEL_HEIGHT)
UI_RESOURCES_POSITION = (SCREEN_WIDTH-UI_LABEL_PAD_X, UI_LABEL_PAD_Y+UI_LABEL_HEIGHT*2)
UI_ENEMY_COUNT_POSITION = (SCREEN_WIDTH-UI_LABEL_PAD_X, UI_LABEL_PAD_Y+UI_LABEL_HEIGHT*3)
UI_BUTTON_SIZE = (95*SCALE, 30*SCALE)

# Main Menu Elements
MAIN_MENU_BACKGROUND_PATH = 'assets/images/screens/main_menu_screen.png'
MAIN_MENU_START_BUTTON_POSITION = (360*SCALE, 253*SCALE)
MAIN_MENU_CONTINUE_BUTTON_POSITION = (360*SCALE, 300*SCALE)
MAIN_MENU_SETTINGS_BUTTON_POSITION = (360*SCALE, 350*SCALE)
MAIN_MENU_EXIT_BUTTON_POSITION = (360*SCALE, 407*SCALE)

# Level Completion Elements
# LEVEL_COMPLETION_NEXT_LEVEL_BUTTON_POSITION = (360 * SCALE, 253 * SCALE)
# LEVEL_COMPLETION_REPLAY_BUTTON_POSITION = (360 * SCALE, 300 * SCALE)
# LEVEL_COMPLETION_MAIN_MENU_BUTTON_POSITION = (360 * SCALE, 350 * SCALE)

# Sound effects and music
SOUND_EFFECTS_VOLUME = 0.5
BACKGROUND_MUSIC_PATH = 'assets/audio/main_menu_background.mp3'
BACKGROUND_MUSIC_VOLUME = 0

# Other settings
DEBUG_MODE = DEBUG
SAVE_GAME_PATH = '../save_data/game_save.json'
