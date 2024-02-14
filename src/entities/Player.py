from src.config.config import PLAYER_GOLD, PLAYER_HEALTH


class Player:
    def __init__(self,update_ui_callback):
        self.gold = PLAYER_GOLD
        self.health = PLAYER_HEALTH
        self.score = 0
        self.player_progress = {'unlocked_levels':[]} # list of completed levels
        self.update_ui_callback = update_ui_callback  # Function to call when UI needs to be updated

    def add_gold(self, amount):
        self.gold += amount
        self._update_ui()

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            self._update_ui()
            return True
        return False

    def heal(self, amount):
        self.health += amount
        self._update_ui()

    def _update_ui(self):
        # Call the UI update callback if it's set
        if self.update_ui_callback:
            self.update_ui_callback()

    # def take_damage(self, damage):
    #     self.health -= damage
    #     if self.health <= 0:
    #         self.health = 0
    #         self.on_death()

    # def on_death(self):
    #     print("Player has died.")
    #     if self.on_death_callback:
    #         self.on_death_callback()