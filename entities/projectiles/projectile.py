# projectile.py

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.x = x            # X-coordinate of the projectile's position
        self.y = y            # Y-coordinate of the projectile's position
        self.speed = speed    # Speed at which the projectile moves
        self.damage = damage  # Damage that the projectile can inflict

    def move(self):
        """
        Move the projectile. This method would be called each game tick.
        The actual movement logic depends on the type of projectile.
        """
        # Implement basic movement logic here, or override in subclass
        pass

    def hit_target(self, target):
        """
        Check if the projectile has hit a target and apply damage.
        Override this method in subclasses for specific hit logic.
        """
        # Basic hit logic, can be more complex in specific projectile types
        if self.reached_target(target):
            target.take_damage(self.damage)
            return True
        return False

    def reached_target(self, target):
        """
        Determine if the projectile has reached a target.
        Override for different types of projectiles.
        """
        # Simple distance check - can be more complex in subclasses
        return (self.x == target.x) and (self.y == target.y)

# Example usage
# Assuming enemy is an instance of an Enemy class
projectile = Projectile(x=0, y=0, speed=5, damage=10)
projectile.move()
if projectile.hit_target(enemy):
    print("Enemy hit!")
