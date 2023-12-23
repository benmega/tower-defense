class Projectile:
    def __init__(self, x, y, speed, damage, target):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'  # Possible states: 'in-flight', 'hit-target', 'expired'

    def move(self):
        # Enhanced movement logic based on projectile type
        # Example: Straight line movement
        dir_x, dir_y = self.target.x - self.x, self.target.y - self.y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance != 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        # Check if the projectile has reached its target or boundary
        if self.reached_target() or self.out_of_bounds():
            self.state = 'expired'

    def reached_target(self):
        # Improved hit detection logic
        return ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2) ** 0.5 <= self.speed

    def out_of_bounds(self):
        # Check if the projectile is out of the game boundaries
        # Placeholder for boundary conditions
        return False

    def hit_target(self):
        if self.state == 'in-flight' and self.reached_target():
            self.target.take_damage(self.damage)
            self.state = 'hit-target'
            return True
        return False

    # Additional methods for visual representation and other behaviors can be added here
