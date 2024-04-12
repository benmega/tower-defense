from src.screens.main_menu import MainMenu


class ScreenManager:
    def __init__(self, game):
        self.game = game
        self.screens = {
            "main_menu": MainMenu(game.screen, game.UI_manager),
            # Initialize other screens here
        }

    def open_screen(self, screen_name):
        # Logic to open a specific screen
        screen = self.screens.get(screen_name)
        if screen:
            screen.open_screen()
            # Additional logic for setting up the screen
