from src.config.config import PLAYER_GOLD, PLAYER_HEALTH
import os
import json





class Player:
    def __init__(self, update_ui_callback):
        self.gold = PLAYER_GOLD
        self.health = PLAYER_HEALTH
        self.score = 0
        self.player_progress = {'unlocked_levels': [0]}  # list of completed levels
        self.player_data = {}
        self.update_ui_callback = update_ui_callback  # Function to call when UI needs to be updated
        self.scores = {}  # Scores for each level
        self.completed_levels = []
        self.unlocked_levels = [0]  # Start with the first level unlocked
        self.skills = {}  # Skills or buffs

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

    def save_game(self, filename="src/save_data/savegame_slot1.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.player_data, f, indent=4)

    def load_data(self, player_data):
        self.gold = player_data['player']['gold']
        self.health = player_data['player']['health']
        self.scores = player_data['player']['score']
        self.unlocked_levels = player_data['player']['unlocked_levels']
        self.skills = player_data['player']['skills']

    def to_dict(self):
        return {
            "gold": self.gold,
            "health": self.health,
            "score": self.score,
            "unlocked_levels": self.unlocked_levels,
            "skills": self.skills,
        }

    def from_dict(self, data):
        self.gold = data["gold"]
        self.health = data["health"]
        self.score = data["score"]
        self.unlocked_levels = data["unlocked_levels"]
        self.skills = data["skills"]

    def complete_level(self, level_index):
        if level_index not in self.completed_levels:
            self.completed_levels.append(level_index)
            # Unlock the next level if applicable
            next_level = level_index + 1
            if next_level not in self.unlocked_levels:
                self.unlocked_levels.append(next_level)
                self.player_progress['unlocked_levels'].append(next_level)