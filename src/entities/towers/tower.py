from src.entities.entity import Entity
from src.config.config import DEBUG, TOWER_TYPES, TILE_SIZE
import src.config.config as configuration
from src.utils.helpers import load_scaled_image

DEFAULT_TOWER_RANGE = 100


class Tower(Entity):
    def __init__(self, x, y, tower_type="Basic", attack_range=100, damage=10, attack_speed=20, upgrade_cost=0, width=10, height=10):
        self.image_path = TOWER_TYPES[tower_type]['image_path']
        super().__init__(x, y, image_path=self.image_path)
        self.image = load_scaled_image(self.image_path, TILE_SIZE).convert_alpha()
        self.x = x // TILE_SIZE[0] * TILE_SIZE[0]  # X-coordinate of the tower's position. Rounded to nearest grid multiple
        self.y = y // TILE_SIZE[1] * TILE_SIZE[1]  # Y-coordinate of the tower's position
        self.width = width
        self.height = height
        self.attack_range = attack_range  # Range within which the tower can attack
        self.damage = damage  # Damage dealt per attack
        self.attack_speed = attack_speed  # Time between attacks
        self.cooldown = 0  # Cooldown to track attack timing
        self.upgrade_level = 0
        self.upgrade_effects = {"range": 0, "damage": 0}
        self.tower_type = tower_type
        self.projectile_type = tower_type
        self.build_cost = TOWER_TYPES[self.tower_type]['cost']
        self.upgrade_cost = upgrade_cost
        self.targeting_mode = "closest"  # or "strongest", "weakest", etc.
        self.animation_state = None
        self.effect_sprites = []
        self.state = "active"  # "disabled", "enhanced", etc.
        self.special_abilities = {"slow": 0.5, "AOE_radius": 50}
        self.sell_value = int(self.build_cost * 0.75)


    def attackMultiple(self, enemies):
        """
        Attack enemies within range. This method can be called each game tick,
        or however often you want towers to be able to attack.
        """
        for enemy in enemies:
            if self.is_enemy_in_range(enemy):
                enemy.take_damage(self.damage)
                # You can add more logic here, such as attacking only the first enemy in range


    def is_enemy_in_range(self, enemy):
        """
        Check if an enemy is within the attack range of the tower.
        """
        enemy_x, enemy_y = enemy.rect.x, enemy.rect.y
        distance = ((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2) ** 0.5
        return distance <= self.attack_range

    def attack(self, target, projectile_manager):
        """
        Create a projectile and target the specified enemy.
        """
        if DEBUG:
            print("Creating a projectile")
        target_x, target_y = target.rect.x, target.rect.y
        projectile_manager.create_projectile(self.x, self.y, self.projectile_type, target)
        if DEBUG:
            print(f"Projectile created at ({self.x}, {self.y}) with target ({target_x}, {target_y})")

    def update(self, enemies, projectile_manager):
        """
        Update the tower's state, potentially launching attacks if enemies are in range.
        """
        self.cooldown -= configuration.GAME_SPEED_MULTIPLIER
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    self.attack(enemy, projectile_manager)
                    break  # Attack the first enemy in range and stop checking

    def can_upgrade(self):
        """Check if this tower can be upgraded."""
        return self.upgrade_level < 3

    def upgrade(self):
        """Upgrade the tower, increasing damage and range."""
        if self.can_upgrade():
            self.upgrade_level += 1
            self.damage = int(self.damage * 1.25)
            self.attack_range = int(self.attack_range * 1.1)
            self.upgrade_cost = int(self.build_cost * (0.5 * (self.upgrade_level + 1)))

    _preview_surfaces_cache = {}

    @staticmethod
    def get_preview_surface(tower_type):
        """Get a semi-transparent preview surface for a tower type."""
        if tower_type not in Tower._preview_surfaces_cache:
            from src.utils.helpers import load_scaled_image
            image_path = TOWER_TYPES[tower_type]['image_path']
            surface = load_scaled_image(image_path, TILE_SIZE)
            surface.set_alpha(140)
            Tower._preview_surfaces_cache[tower_type] = surface
        return Tower._preview_surfaces_cache[tower_type]