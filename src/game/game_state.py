class GameState:
    def __init__(self):
        self.active_projectiles = []
        self.active_enemies = []
        # Add other shared state variables here

# In your game initialization
game_state = GameState()

# In your game loop or other functions
def game_loop(game_state):
    # Access and modify the game state
    for projectile in game_state.active_projectiles:
        projectile.move()
        projectile.draw(screen)
    # etc.
