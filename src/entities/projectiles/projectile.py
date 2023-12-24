import pygame

class Projectile:
    def __init__(self, x, y, speed, damage, target, image_path="assets/images/projectile.png"):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.target = target
        self.state = 'in-flight'  # Possible states: 'in-flight', 'hit-target', 'expired'
        self.image = pygame.image.load(image_path)  # Load projectile image
        self.image_path = image_path

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
        # Implement boundary conditions based on your game's design
        # Example placeholder for a 800x600 window
        return not (0 <= self.x <= 800 and 0 <= self.y <= 600)

    def hit_target(self):
        if self.state == 'in-flight' and self.reached_target():
            self.target.take_damage(self.damage)
            self.state = 'hit-target'
            return True
        return False

    def draw(self, screen):
        # Draw the projectile on the screen at its current position
        screen.blit(self.image, (self.x, self.y))
