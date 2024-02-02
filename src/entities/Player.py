class Player:
    def __init__(self, initial_gold=100, initial_health=100):
        self.gold = initial_gold
        self.health = initial_health
        self.score = 0
        # You can add more attributes as needed

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.on_death()

    def heal(self, amount):
        self.health += amount

    def on_death(self):
        # Handle player's death (e.g., end game, display message, etc.)
        pass

    # You can add more methods related to player actions and stats