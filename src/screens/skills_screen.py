import pygame
import pygame_gui
from pygame_gui.elements.ui_tool_tip import UITooltip

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.screens.screen import Screen
from src.utils.helpers import load_scaled_image

all_skills = {
    "additional_gold": {
        "description": "Increases starting gold",
        "max_level": 10,
        "cost_per_level": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "prerequisites": []
    },
    "gold_per_kill": {
        "description": "Increases gold earned per kill",
        "max_level": 10,
        "cost_per_level": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "prerequisites": []
    },
    "additional_health": {
        "description": "Increases player's health",
        "max_level": 10,
        "cost_per_level": [2, 3, 5, 7, 9, 11, 13, 15, 17, 20],
        "prerequisites": []
    },
    "damage_boost": {
        "description": "Increases tower damage",
        "max_level": 10,
        "cost_per_level": [3, 4, 5, 7, 9, 12, 15, 18, 21, 25],
        "prerequisites": ["additional_gold"]
    },
    "attack_speed": {
        "description": "Increases tower attack speed",
        "max_level": 8,
        "cost_per_level": [3, 5, 7, 9, 12, 15, 19, 24],
        "prerequisites": ["gold_per_kill"]
    },
    "range_extension": {
        "description": "Increases tower range",
        "max_level": 5,
        "cost_per_level": [4, 8, 12, 17, 23],
        "prerequisites": ["additional_health"]
    },
    "critical_hit_chance": {
        "description": "Increases chance of towers dealing critical damage",
        "max_level": 7,
        "cost_per_level": [5, 10, 15, 21, 28, 36, 45],
        "prerequisites": ["damage_boost"]
    },
    "healing_ability": {
        "description": "Grants towers a chance to heal a portion of damage dealt",
        "max_level": 6,
        "cost_per_level": [6, 12, 18, 25, 33, 42],
        "prerequisites": ["attack_speed", "damage_boost"]
    },
    "tower_build_discount": {
        "description": "Reduces the cost of building new towers",
        "max_level": 8,
        "cost_per_level": [2, 4, 6, 8, 11, 14, 18, 23],
        "prerequisites": ["range_extension"]
    },
    "resource_generation": {
        "description": "Towers passively generate a small amount of gold over time",
        "max_level": 4,
        "cost_per_level": [5, 10, 16, 23],
        "prerequisites": ["critical_hit_chance"]
    },
    "splash_damage": {
        "description": "Grants towers a chance to deal splash damage",
        "max_level": 5,
        "cost_per_level": [7, 14, 22, 31, 41],
        "prerequisites": ["healing_ability", "critical_hit_chance"]
    },
    "armor_piercing": {
        "description": "Towers ignore a portion of enemy armor",
        "max_level": 7,
        "cost_per_level": [3, 7, 12, 18, 25, 33, 42],
        "prerequisites": ["splash_damage", "tower_build_discount"]
    }
}


class SkillsScreen(Screen):
    def __init__(self, ui_manager, player):
        super().__init__(ui_manager, "assets/images/screens/skills_background.png")
        self.player = player
        self.skill_buttons = []  # To hold buttons for each skill
        self.skill_points_label = None  # To display the player's skill points
        self.grid_columns = 2  # Number of columns in the grid
        self.grid_cell_size = [380, 50]  # Width and height of each grid cell
        self.grid_margin = 200  # Margin from the top and left of the screen
        self.grid_spacing = 10  # Spacing between buttons
        self.initialize_skill_buttons()
        self.initialize_skill_points_label()

    def initialize_skill_buttons(self):
        skill_keys = list(all_skills.keys())
        for index, skill_key in enumerate(skill_keys):
            column, row = index % self.grid_columns, index // self.grid_columns
            skill_info, skill_level = all_skills[skill_key], self.player.skills.get(skill_key, 0)
            skill_points_needed = skill_info["cost_per_level"][skill_level] if skill_level < skill_info[
                "max_level"] else "Max"
            button_text = f"{skill_info['description']}: Level {skill_level} (Next: {skill_points_needed} points)"

            x, y = self.grid_margin + column * (self.grid_cell_size[0] + self.grid_spacing), self.grid_margin + row * (
                        self.grid_cell_size[1] + self.grid_spacing)
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect([x, y], self.grid_cell_size),
                                                  text=button_text, manager=self.ui_manager,
                                                  tool_tip_text=skill_info['description'], visible=self.visible)
            self.add_ui_element(button)

    def initialize_skill_points_label(self):
        # Create and add the skill points label to the UI elements
        self.skill_points_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([50, 50], [200, 50]),  # Adjust size and position as needed
            text=f"Skill Points: {self.player.points}",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(self.skill_points_label)

    def handle_events(self, event, game):
        super().handle_events(event, game)  # Handle common events, including the return button
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            for button in self.skill_buttons:
                if event.ui_element == button:
                    # Handle skill button press
                    skill_index = self.skill_buttons.index(button)
                    self.upgrade_skill(skill_index, game)
                    break

    def upgrade_skill(self, skill_index, game):
        # Assuming you have a list of skill keys that corresponds to the skill buttons
        all_skills_keys = list(all_skills.keys())
        skill_key = all_skills_keys[skill_index]  # This should be a list of keys in the order they appear in the UI
        skill = all_skills[skill_key]  # Access the skill using its key

        if game.player.can_upgrade_skill(skill_key):  # Assuming this method checks if the skill can be upgraded
            game.player.upgrade_skill(skill_key)  # Pass the skill key to upgrade
            # Update the button text to reflect the new skill level
            new_level = game.player.skills[skill_key]  # Assuming player.skills stores levels of each skill
            self.skill_buttons[skill_index].set_text(f"{skill_key}: Level {new_level}")
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")

    def open_screen(self):
        super().open_screen()  # Make sure to call the superclass method to handle common open screen logic
        # Update the text on each skill button based on the player's current skill levels
        for button, skill_key in zip(self.skill_buttons, all_skills.keys()):
            skill_level = self.player.skills.get(skill_key, 0)
            skill_info = all_skills[skill_key]
            skill_points_needed = skill_info["cost_per_level"][skill_level] if skill_level < skill_info[
                "max_level"] else "Max"
            button_text = f"{skill_key}: Level {skill_level} (Next: {skill_points_needed} points)"
            button.set_text(button_text)
            button.visible = True

        # Update the skill points label
        if self.skill_points_label:
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")
            self.skill_points_label.visible = True

    def close_screen(self):
        super().close_screen()  # Call superclass method to handle common close screen logic
        # Additional logic for closing the skills screen, if necessary

    def draw(self, screen):
        print('skill screen drawn')
        super().draw(screen)  # Call the superclass draw method
        # You can add custom drawing code here if needed, for example, drawing skill descriptions or dependencies
