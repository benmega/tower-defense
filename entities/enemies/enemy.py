# enemy.py

class Enemy:
    def __init__(self, health, speed, path, image_path):
        self.health = health
        self.speed = speed
        self.path = path
        self.path_index = 0  # Current index in the path
        self.x, self.y = path[0]  # Starting position at the first waypoint
        self.image_path = image_path

    def move(self):
        """
        Move the enemy along the predefined path.
        """

        #print(f"Moving enemy from ({self.x}, {self.y})")

        if self.path_index < len(self.path):
            next_x, next_y = self.path[self.path_index]
            self.move_towards(next_x, next_y)
        # TODO Add else condition to handle the end of the path if needed
        else:
            print("Reached the end of the path.")
        #print(f"Moved enemy to ({self.x}, {self.y})")

    def move_towards(self, next_x, next_y):
        """
        Move the enemy towards the next waypoint.
        """
        # Calculate direction vector
        dir_x, dir_y = next_x - self.x, next_y - self.y
        distance = (dir_x**2 + dir_y**2)**0.5

        # Normalize direction
        if distance != 0:
            dir_x, dir_y = dir_x / distance, dir_y / distance

        # Move enemy
        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        # Check if reached the next waypoint (with a threshold)
        if abs(self.x - next_x) <= self.speed and abs(self.y - next_y) <= self.speed:
            print(f"Reached waypoint: ({next_x}, {next_y})")
            self.x, self.y = next_x, next_y  # Snap to waypoint
            if self.path_index < len(self.path) - 1:
                self.path_index += 1



    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Handle enemy death
        pass