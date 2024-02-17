import pygame
import pygame_gui

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
    def __init__(self, ui_manager, player_skills):
        super().__init__(ui_manager, "assets/images/screens/skills_background.png")
        self.player_skills = player_skills  # This could be a reference to the player's skills data structure
        self.skill_buttons = []  # To hold buttons for each skill
        self.initialize_skill_buttons()

    def initialize_skill_buttons(self):
        self.skill_buttons = []
        y_offset = 100  # Starting Y offset for the first button
        for skill_key, skill_info in all_skills.items():
            skill_level = self.player_skills.get(skill_key, {}).get("level", 0)
            skill_points_needed = skill_info["cost_per_level"][skill_level] if skill_level < skill_info[
                "max_level"] else "Max"
            button_text = f"{skill_info['description']}: Level {skill_level} (Next: {skill_points_needed} points)"

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([50, y_offset], UI_BUTTON_SIZE),
                text=button_text,
                manager=self.ui_manager,
                visible=False  # Initially invisible; made visible when the screen is opened
            )
            self.add_ui_element(button)
            self.skill_buttons.append(button)
            y_offset += 60  # Increment Y offset for the next button

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
            self.skill_buttons[skill_index].set_text(f"{skill['description']}: Level {new_level}")

    def open_screen(self):
        super().open_screen()  # Make sure to call the superclass method to handle common open screen logic
        # Additional logic specific to opening the skills screen, if any

    def close_screen(self):
        super().close_screen()  # Call superclass method to handle common close screen logic
        # Additional logic for closing the skills screen, if necessary

    def draw(self, screen):
        super().draw(screen)  # Call the superclass draw method
        # You can add custom drawing code here if needed, for example, drawing skill descriptions or dependencies
