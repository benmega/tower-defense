from src.config.config import PLAYER_GOLD, PLAYER_HEALTH


class Player:
    def __init__(self):
        self.gold = PLAYER_GOLD
        self.health = PLAYER_HEALTH
        self.score = 0
        self.player_progress = {'unlocked_levels':[]} # list of completed levels

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    # def take_damage(self, damage):
    #     self.health -= damage
    #     if self.health <= 0:
    #         self.health = 0
    #         self.on_death()

    def heal(self, amount):
        self.health += amount

    # def on_death(self):
    #     print("Player has died.")
    #     if self.on_death_callback:
    #         self.on_death_callback()