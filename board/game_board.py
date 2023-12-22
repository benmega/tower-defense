# game_board.py

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.towers = []

    def add_tower(self, tower):
        """
        Add a tower to the game board.
        """
        if self.is_valid_position(tower.x, tower.y):
            self.grid[tower.y][tower.x] = tower
            self.towers.append(tower)
        else:
            raise ValueError("Invalid position for tower")

    def is_valid_position(self, x, y):
        """
        Check if a position is within the bounds of the game board.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tower_at(self, x, y):
        """
        Return the tower at the given position, if any.
        """
        return self.grid[y][x] if self.is_valid_position(x, y) else None

    def update(self):
        """
        Update the game board state. This might include updating tower attacks, etc.
        """
        # Implement any updates needed for each game loop iteration
        pass

    # Additional methods can be added for board functionality

# Example usage
board = GameBoard(10, 10)
# Add towers and perform other operations as needed
