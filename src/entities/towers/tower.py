# tower.py
from src.entities.entity import Entity
from src.entities.projectiles.projectile import Projectile


class Tower(Entity):
    def __init__(self, x, y, attack_range, damage, attack_speed,image_path='assets/images/tower.png'):
        super().__init__(x, y, image_path='assets/images/tower.png')
        self.x = x  # X-coordinate of the tower's position
        self.y = y  # Y-coordinate of the tower's position
        self.attack_range = attack_range  # Range within which the tower can attack
        self.damage = damage  # Damage dealt per attack
        self.attack_speed = attack_speed  # Time between attacks
        self.cooldown = 0  # Cooldown to track attack timing
        self.image_path = image_path

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
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.attack_range

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

    def attack(self, enemy, active_projectiles):
        """
        Create a projectile and target the specified enemy.
        """

        print("Creating a projectile")
        projectile = Projectile(self.x, self.y, 5, self.damage, enemy)
        active_projectiles.append(projectile)
        print(f"Projectile created at ({projectile.x}, {projectile.y}) with target ({enemy.x}, {enemy.y})")
