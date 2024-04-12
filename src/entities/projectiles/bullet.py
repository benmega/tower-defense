# bullet.py

class Bullet:
    def __init__(self, x, y, speed, damage, target):
        self.x = x                # X-coordinate of the bullet's position
        self.y = y                # Y-coordinate of the bullet's position
        self.speed = speed        # Speed at which the bullet moves
        self.damage = damage      # Damage that the bullet can inflict
        self.target = target      # Target enemy that the bullet is moving towards

    def move(self):
        """
        Move the bullet towards its target. This method would be called each game tick.
        """
        # Implement movement logic here
        # Typically, this involves calculating the direction to the target and updating grid_x and grid_y accordingly
        pass

    def hit_target(self):
        """
        Check if the bullet has hit its target and apply damage if so.
        """
        if self.reached_target():
            self.target.take_damage(self.damage)
            # Additional effects upon hitting can be added here
            return True
        return False

    def reached_target(self):
        """
        Determine if the bullet has reached its target.
        """
        # Simple distance check - this could be more complex based on your game's requirements
        return (self.x == self.target.x) and (self.y == self.target.y)

# Example usage
# Assuming enemy is an instance of an Enemy class
bullet = Bullet(x=0, y=0, speed=5, damage=10, target=enemy)
bullet.move()
if bullet.hit_target():
    print("Target hit!")
