# tower.py

class Tower:
    def __init__(self, x, y, attack_range, damage):
        self.x = x                # X-coordinate on the game board
        self.y = y                # Y-coordinate on the game board
        self.attack_range = attack_range  # Range within which the tower can attack enemies
        self.damage = damage      # Damage dealt to an enemy

    def attack(self, enemies):
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
        return (abs(self.x - enemy.x) ** 2 + abs(self.y - enemy.y) ** 2) ** 0.5 <= self.attack_range

    # Additional methods can be added as needed, like upgrading the tower
