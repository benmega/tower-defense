class Missile:
    def __init__(self, x, y, speed, damage, target):
        self.x = x                # X-coordinate of the missile's position
        self.y = y                # Y-coordinate of the missile's position
        self.speed = speed        # Speed at which the missile moves
        self.damage = damage      # Damage that the missile can inflict
        self.target = target      # Target enemy that the missile is tracking

    def move(self):
        """
        Move the missile towards its moving target.
        """
        if self.target is not None:
            # Calculate direction towards the target
            dir_x, dir_y = self.target.x - self.x, self.target.y - self.y
            distance = (dir_x**2 + dir_y**2)**0.5

            # Normalize direction
            dir_x, dir_y = dir_x / distance, dir_y / distance

            # Update missile position
            self.x += dir_x * self.speed
            self.y += dir_y * self.speed

    def hit_target(self):
        """
        Check if the missile has reached its target and apply damage.
        """
        if self.reached_target():
            self.explode()
            return True
        return False

    def reached_target(self):
        """
        Determine if the missile has reached near its target (within a certain range).
        """
        return ((self.target.x - self.x)**2 + (self.target.y - self.y)**2)**0.5 <= self.speed

    def explode(self):
        """
        Handle the explosion of the missile, dealing damage to the target.
        This could also be expanded to include AoE damage to nearby enemies.
        """
        self.target.take_damage(self.damage)
        # Additional explosion effects here (like AoE damage)
