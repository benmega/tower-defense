# game.py

from board.game_board import GameBoard
from entities import Tower, Enemy

class Game:
    def __init__(self):
        self.board = GameBoard(10, 10)  # Assuming a 10x10 board for this example
        self.enemies = []  # List of enemies
        self.towers = []   # List of towers
        self.is_running = False
        self.initialize_game()  # Setup for game start

    def initialize_game(self):
        # Initialize game elements here, like placing towers and spawning enemies
        pass

    def start(self):
        self.is_running = True
        while self.is_running:
            self.update()
            # You may want to implement a frame rate control here

    def update(self):
        # Main game update logic for each frame
        self.update_enemies()
        self.update_towers()
        self.check_game_over()

    def update_enemies(self):
        # Update each enemy's position, check for reaching the end, etc.
        for enemy in self.enemies:
            enemy.move()
            if enemy.health <= 0:
                self.enemies.remove(enemy)

    def update_towers(self):
        # Update towers, let them attack enemies
        for tower in self.towers:
            tower.attack(self.enemies)

    def check_game_over(self):
        # Check if the game should end (e.g., player health reaches 0)
        pass

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_tower(self, tower):
        self.towers.append(tower)
        self.board.add_tower(tower)

    # Other game methods like handling user input, rendering, etc.

# Example usage
if __name__ == "__main__":
    game = Game()
    game.start()
