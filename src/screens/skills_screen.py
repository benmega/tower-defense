import pygame
import pygame_gui
from pygame_gui.elements.ui_tool_tip import UITooltip

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.screens.screen import Screen
from src.utils.helpers import load_scaled_image
from src.utils.layout import anchor
import src.utils.constants as C

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
        self.skill_buttons = []

        CELL_W = int(SCREEN_WIDTH * 0.35)
        CELL_H = 48
        GAP = C.SPACE_SM
        MARGIN_TOP = int(SCREEN_HEIGHT * 0.22)
        MARGIN_LEFT = int(SCREEN_WIDTH * 0.08)

        self.grid_layout = {
            'cell_w': CELL_W,
            'cell_h': CELL_H,
            'gap': GAP,
            'margin_top': MARGIN_TOP,
            'margin_left': MARGIN_LEFT,
            'cols': 2
        }

        self.initialize_skill_buttons()
        self.initialize_skill_points_label()

    def initialize_skill_buttons(self):
        layout = self.grid_layout
        skill_keys = list(all_skills.keys())
        for index, skill_key in enumerate(skill_keys):
            column, row = index % layout['cols'], index // layout['cols']
            skill_info = all_skills[skill_key]
            skill_level = self.player.skills.get(skill_key, 0)

            if skill_level >= skill_info['max_level']:
                cost_text = 'MAX'
            else:
                cost_text = f"{skill_info['cost_per_level'][skill_level]}pts"

            button_text = f"{skill_key} (Lv {skill_level})\nNext: {cost_text}"

            x = layout['margin_left'] + column * (layout['cell_w'] + layout['gap'])
            y = layout['margin_top'] + row * (layout['cell_h'] + layout['gap'])

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([x, y], (layout['cell_w'], layout['cell_h'])),
                text=button_text,
                manager=self.ui_manager,
                tool_tip_text=skill_info['description'],
                visible=self.visible
            )

            is_maxed = skill_level >= skill_info['max_level']
            if is_maxed:
                button.disable()

            self.add_ui_element(button)
            self.skill_buttons.append(button)

    def initialize_skill_points_label(self):
        label_w, label_h = 200, 50
        lx, ly = anchor(label_w, label_h, h='right', v='top', margin=C.SPACE_MD)

        self.skill_points_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect([lx, ly], [label_w, label_h]),
            text=f"Skill Points: {self.player.points}",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(self.skill_points_label)

    def handle_events(self, event, game):
        super().handle_events(event, game)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            for button_index, button in enumerate(self.skill_buttons):
                if event.ui_element == button:
                    self.upgrade_skill(button_index, game)
                    break

    def upgrade_skill(self, skill_index, game):
        all_skills_keys = list(all_skills.keys())
        skill_key = all_skills_keys[skill_index]
        skill_info = all_skills[skill_key]

        if game.player.can_upgrade_skill(skill_key):
            game.player.upgrade_skill(skill_key)
            new_level = game.player.skills[skill_key]

            if new_level >= skill_info['max_level']:
                cost_text = 'MAX'
                self.skill_buttons[skill_index].disable()
            else:
                cost_text = f"{skill_info['cost_per_level'][new_level]}pts"

            button_text = f"{skill_key} (Lv {new_level})\nNext: {cost_text}"
            self.skill_buttons[skill_index].set_text(button_text)
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")

    def open_screen(self):
        super().open_screen()
        for button_index, button in enumerate(self.skill_buttons):
            all_skills_keys = list(all_skills.keys())
            skill_key = all_skills_keys[button_index]
            skill_info = all_skills[skill_key]
            skill_level = self.player.skills.get(skill_key, 0)

            if skill_level >= skill_info['max_level']:
                cost_text = 'MAX'
                button.disable()
            else:
                cost_text = f"{skill_info['cost_per_level'][skill_level]}pts"
                button.enable()

            button_text = f"{skill_key} (Lv {skill_level})\nNext: {cost_text}"
            button.set_text(button_text)
            button.visible = True

        if self.skill_points_label:
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")
            self.skill_points_label.visible = True

    def close_screen(self):
        super().close_screen()

    def draw(self, screen):
        super().draw(screen)
