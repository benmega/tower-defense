# Define this at the top of your Game class file
from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    OPTIONS = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    CAMPAIGN_MAP = auto()
    LEVEL_COMPLETE = auto()
    LOAD_GAME = auto()
    SKILLS = auto()
    LEVEL_DEFEAT = auto()