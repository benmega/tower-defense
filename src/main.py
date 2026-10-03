import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.game.game import Game

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
