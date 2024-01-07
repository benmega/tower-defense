# tower.py
from src.entities.entity import Entity
from src.config.config import TOWER_IMAGE_PATH, DEBUG


class Tower(Entity):
    def __init__(self, x=10, y=10, attack_range=100, damage=10, attack_speed=20,image_path=TOWER_IMAGE_PATH,build_cost=0,upgrade_cost=0,width=10,height=10):
        super().__init__(x, y, image_path=TOWER_IMAGE_PATH)
        self.x = x  # X-coordinate of the tower's position
        self.y = y  # Y-coordinate of the tower's position
        self.width = width
        self.height = height
        self.attack_range = attack_range  # Range within which the tower can attack
        self.damage = damage  # Damage dealt per attack
        self.attack_speed = attack_speed  # Time between attacks
        self.cooldown = 0  # Cooldown to track attack timing
        self.image_path = image_path
        self.upgrade_level = 0
        self.upgrade_effects = {"range": 0, "damage": 0}
        self.tower_type = "BasicTower"
        self.projectile_type = "BasicProjectile"
        self.build_cost = build_cost
        self.upgrade_cost = upgrade_cost
        self.targeting_mode = "closest"  # or "strongest", "weakest", etc.
        self.animation_state = ...
        self.effect_sprites = ...
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

    # Additional methods can be added as needed, like upgrading the tower
    def update(self, enemies, active_projectiles):
        """
        Update the tower's state, potentially launching attacks if enemies are in range.
        """
        self.cooldown -= 1  # Decrease cooldown by 1 per frame
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    self.attack(enemy, active_projectiles)
                    break  # Attack the first enemy in range and stop checking