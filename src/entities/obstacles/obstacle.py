# obstacle.py

class Obstacle:
    def __init__(self, x, y, width, height, effect=None):
        self.x = x          # X-coordinate on the game board
        self.y = y          # Y-coordinate on the game board
        self.width = width  # Width of the obstacle
        self.height = height # Height of the obstacle
        self.effect = effect # Optional effect that the obstacle has on the game

    def apply_effect(self, target):
        """
        Apply the obstacle's effect to a target, if any.
        This could be slowing down enemies, blocking their path, etc.
        """
        if self.effect:
            # Implement effect logic here
            pass

    # Additional methods for obstacle behavior can be added here

# Example usage
wall = Obstacle(x=5, y=5, width=1, height=1)
# Assuming there's logic to place the wall on the game board
