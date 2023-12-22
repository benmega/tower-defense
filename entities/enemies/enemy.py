# enemy.py

class Enemy:
    def __init__(self, health, speed, path):
        self.health = health
        self.speed = speed
        self.path = path
        self.path_index = 0  # Current index in the path
        self.x, self.y = path[0]  # Starting position

    def move(self):
        """
        Move the enemy along the predefined path.
        """
        if self.path_index < len(self.path) - 1:
            self.path_index += 1
            self.x, self.y = self.path[self.path_index]
        else:
            self.reach_destination()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """
        Remove the enemy from the game.
        """
        # Implement removal logic here (handled by the game board or main game logic)
        pass

    def reach_destination(self):
        """
        Handle what happens when the enemy reaches the end of the path.
        This could affect the player's health or game state.
        """
        # Implement destination reach logic here
        pass
