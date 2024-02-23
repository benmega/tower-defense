from src.config.config import PLAYER_GOLD, PLAYER_HEALTH
import os
import json

from src.screens.skills_screen import all_skills


class Player:
    def __init__(self, update_ui_callback):
        self.gold = PLAYER_GOLD
        self.health = PLAYER_HEALTH
        self.totalScore = 0
        self.levelScore = 0
        self.player_progress = {'unlocked_levels': [0]}  # list of completed levels
        self.player_data = {}
        self.update_ui_callback = update_ui_callback  # Function to call when UI needs to be updated
        self.scores = {}  # Scores for each level
        self.completed_levels = []
        self.unlocked_levels = [0]  # Start with the first level unlocked
        self.skills = {}  # Skills or buffs
        self.points = 10000  # Starting with an arbitrary number of points for upgrading skills

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
            "totalScore": self.totalScore,
            "levelScores": self.scores,
            "unlocked_levels": self.unlocked_levels,
            "skills": self.skills,
        }

    def from_dict(self, data):
        self.gold = data["gold"]
        self.health = data["health"]
        self.totalScore = data["totalScore"]
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


    def can_upgrade_skill(self, skill_key):
        skill_info = all_skills.get(skill_key)
        if not skill_info:
            return False  # Skill does not exist

        current_level = self.skills.get(skill_key, 0)
        if current_level >= skill_info["max_level"]:
            return False  # Skill is already at max level

        # Check if player has enough points to upgrade the skill
        cost_for_next_level = skill_info["cost_per_level"][current_level]
        if self.points < cost_for_next_level:
            return False  # Not enough points

        # Check for prerequisites
        prerequisites = skill_info.get("prerequisites", [])
        for prereq in prerequisites:
            if self.skills.get(prereq, 0) == 0:
                return False  # Prerequisite skill not met

        return True

    def upgrade_skill(self, skill_key):
        if not self.can_upgrade_skill(skill_key):
            print("Cannot upgrade skill.")
            return

        skill_info = all_skills[skill_key]
        current_level = self.skills.get(skill_key, 0)
        cost_for_next_level = skill_info["cost_per_level"][current_level]

        # Deduct points and increase skill level
        self.points -= cost_for_next_level
        new_level = current_level + 1
        self.skills[skill_key] = new_level

        print(f"Upgraded {skill_key} to level {new_level}. Points remaining: {self.points}.")
        self._update_ui()

    # Remember to implement the _update_ui method if not already done
    def _update_ui(self):
        # Update UI with new points and skill levels
        if self.update_ui_callback:
            self.update_ui_callback()

    def start_level(self):
        # TODO Make skills modify
        self.gold = PLAYER_GOLD + self.skills.get('additional_gold', 0) * 100
        self.health = PLAYER_HEALTH + + self.skills.get('additional_health', 0) * 100
        self.levelScore = 0
