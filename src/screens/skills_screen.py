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


def _skill_display_name(key: str) -> str:
    return key.replace('_', ' ').title()


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

    def _prereqs_met(self, skill_key):
        prereqs = all_skills[skill_key].get('prerequisites', [])
        return all(self.player.skills.get(p, 0) > 0 for p in prereqs)

    def _skill_button_text(self, skill_key):
        skill_info = all_skills[skill_key]
        skill_level = self.player.skills.get(skill_key, 0)
        name = _skill_display_name(skill_key)
        if skill_level >= skill_info['max_level']:
            return f"{name} (MAX)"
        cost = skill_info['cost_per_level'][skill_level]
        return f"{name} Lv {skill_level}  [{cost}pts]"

    def _skill_tooltip(self, skill_key):
        skill_info = all_skills[skill_key]
        desc = skill_info['description']
        prereqs = skill_info.get('prerequisites', [])
        if prereqs:
            prereq_names = ', '.join(_skill_display_name(p) for p in prereqs)
            desc += f"  |  Requires: {prereq_names}"
        return desc

    def initialize_skill_buttons(self):
        self.skill_buttons.clear()
        layout = self.grid_layout
        skill_keys = list(all_skills.keys())
        for index, skill_key in enumerate(skill_keys):
            column, row = index % layout['cols'], index // layout['cols']
            skill_info = all_skills[skill_key]
            skill_level = self.player.skills.get(skill_key, 0)

            x = layout['margin_left'] + column * (layout['cell_w'] + layout['gap'])
            y = layout['margin_top'] + row * (layout['cell_h'] + layout['gap'])

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([x, y], (layout['cell_w'], layout['cell_h'])),
                text=self._skill_button_text(skill_key),
                manager=self.ui_manager,
                tool_tip_text=self._skill_tooltip(skill_key),
                visible=self.visible
            )

            is_maxed = skill_level >= skill_info['max_level']
            prereqs_met = self._prereqs_met(skill_key)
            if is_maxed or not prereqs_met:
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

    def on_button_pressed(self, ui_element, game):
        super().on_button_pressed(ui_element, game)
        if ui_element in self.skill_buttons:
            skill_index = self.skill_buttons.index(ui_element)
            self.upgrade_skill(skill_index, game)

    def upgrade_skill(self, skill_index, game):
        all_skills_keys = list(all_skills.keys())
        skill_key = all_skills_keys[skill_index]
        skill_info = all_skills[skill_key]

        if game.player.can_upgrade_skill(skill_key):
            game.player.upgrade_skill(skill_key)
            new_level = game.player.skills[skill_key]
            btn = self.skill_buttons[skill_index]
            btn.set_text(self._skill_button_text(skill_key))
            if new_level >= skill_info['max_level']:
                btn.disable()
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")
            game.audio_manager.play_sfx('skill_unlocked')
            # Re-evaluate all buttons: buying a skill may unlock prerequisites for others
            self._refresh_button_states()

    def _refresh_button_states(self):
        all_skills_keys = list(all_skills.keys())
        for i, button in enumerate(self.skill_buttons):
            skill_key = all_skills_keys[i]
            skill_info = all_skills[skill_key]
            skill_level = self.player.skills.get(skill_key, 0)
            button.set_text(self._skill_button_text(skill_key))
            is_maxed = skill_level >= skill_info['max_level']
            prereqs_met = self._prereqs_met(skill_key)
            if is_maxed or not prereqs_met:
                button.disable()
            else:
                button.enable()

    def open_screen(self):
        super().open_screen()
        self._refresh_button_states()
        if self.skill_points_label:
            self.skill_points_label.set_text(f"Skill Points: {self.player.points}")
            self.skill_points_label.visible = True

    def close_screen(self):
        super().close_screen()

    def draw(self, screen):
        super().draw(screen)
