import pygame

from src.config.config import ENEMY_IMAGE_PATH
from src.utils.resource_path import resource_path


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, key, path):
        """ Loads an image and stores it with the specified key. """
        image = pygame.image.load(resource_path(path))
        self.images[key] = image
        return image

    def get_image(self, key):
        """ Retrieves an image by its key. """
        return self.images.get(key)

    def load_sound(self, key, path):
        """ Loads a sound and stores it with the specified key. """
        sound = pygame.mixer.Sound(resource_path(path))
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        """ Retrieves a sound by its key. """
        return self.sounds.get(key)

    def load_font(self, key, path, size):
        """ Loads a font and stores it with the specified key. """
        font = pygame.font.Font(resource_path(path), size)
        self.fonts[key] = font
        return font

    def get_font(self, key):
        """ Retrieves a font by its key. """
        return self.fonts.get(key)

    def preload_assets(self):
        """ Preloads necessary assets for the game. """
        self.load_image('enemy', ENEMY_IMAGE_PATH)
        self.load_image('tower', 'assets/images/towers/basic_tower.png')
        
        # UI Elements
        self.load_image('ui_armor_badge', 'assets/images/UI/armor_badge.png')
        self.load_image('ui_skill_point', 'assets/images/UI/skill_point_icon.png')
        self.load_image('ui_gold', 'assets/images/UI/gold_icon.png')
        self.load_image('ui_score', 'assets/images/UI/score_icon.png')
        self.load_image('ui_health', 'assets/images/UI/health_icon.png')
        self.load_image('ui_sell', 'assets/images/UI/sell_icon.png')
        
        # Cursors & Status Icons
        self.load_image('cursor_normal', 'assets/images/UI/cursor_normal.png')
        self.load_image('cursor_target', 'assets/images/UI/cursor_target.png')
        self.load_image('element_fire', 'assets/images/UI/element_fire.png')
        self.load_image('element_ice', 'assets/images/UI/element_ice.png')
        self.load_image('element_poison', 'assets/images/UI/element_poison.png')
        self.load_image('element_lightning', 'assets/images/UI/element_lightning.png')
        self.load_image('status_stunned', 'assets/images/UI/status_stunned.png')
        self.load_image('status_burning', 'assets/images/UI/status_burning.png')
        self.load_image('btn_play', 'assets/images/UI/btn_play.png')
        self.load_image('btn_pause', 'assets/images/UI/btn_pause.png')
        self.load_image('btn_sound_on', 'assets/images/UI/btn_sound_on.png')
        self.load_image('btn_sound_off', 'assets/images/UI/btn_sound_off.png')

        # Skills
        self.load_image('skill_armor_pierce', 'assets/images/skills/armor_piercing.png')
        self.load_image('skill_gold_boost', 'assets/images/skills/additional_gold.png')
        self.load_image('skill_crit', 'assets/images/skills/critical_hit_chance.png')
        self.load_image('skill_discount', 'assets/images/skills/tower_build_discount.png')
        self.load_image('skill_dmg_boost', 'assets/images/skills/damage_boost.png')
        self.load_image('skill_resource_gen', 'assets/images/skills/resource_generation.png')
        self.load_image('skill_heal', 'assets/images/skills/healing_ability.png')
        self.load_image('skill_range', 'assets/images/skills/range_extension.png')
        self.load_image('skill_health', 'assets/images/skills/additional_health.png')
        self.load_image('skill_atk_speed', 'assets/images/skills/attack_speed.png')
        self.load_image('skill_splash', 'assets/images/skills/splash_damage.png')
        self.load_image('skill_gold_kill', 'assets/images/skills/gold_per_kill.png')

        # Effects
        self.load_image('fx_explosion_1', 'assets/images/effects/explosion_f1.png')
        self.load_image('fx_explosion_2', 'assets/images/effects/explosion_f2.png')
        self.load_image('fx_explosion_3', 'assets/images/effects/explosion_f3.png')
        self.load_image('fx_explosion_4', 'assets/images/effects/explosion_f4.png')

        # Map UI
        self.load_image('map_1star', 'assets/images/screens/campaignMap/level_1star.png')
        self.load_image('map_2stars', 'assets/images/screens/campaignMap/level_2stars.png')
        self.load_image('map_3stars', 'assets/images/screens/campaignMap/level_3stars.png')

        # Tiles
        self.load_image('tile_curve_ne', 'assets/images/gameBoardTiles/path_curve_ne.png')
        self.load_image('tile_curve_nw', 'assets/images/gameBoardTiles/path_curve_nw.png')
        self.load_image('tile_curve_se', 'assets/images/gameBoardTiles/path_curve_se.png')
        self.load_image('tile_curve_sw', 'assets/images/gameBoardTiles/path_curve_sw.png')

        self.load_sound('explosion', 'assets/sounds/explosion.wav')
        self.load_font('main_font', 'assets/fonts/main_font.ttf', 24)
