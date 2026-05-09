import json
import os

import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE, SCREEN_WIDTH
from src.screens.screen import Screen
from src.utils.resource_path import resource_path
from src.utils.layout import anchor
import src.utils.constants as C
from datetime import datetime


class GameDataScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "assets/images/screens/game_data_screen.png")
        self.load_buttons = []
        self.save_buttons = []
        self.save_slot_relative_paths = [
            "src/save_data/savegame_slot1.json",
            "src/save_data/savegame_slot2.json",
            "src/save_data/savegame_slot3.json",
            "src/save_data/savegame_slot4.json",
            "src/save_data/savegame_slot5.json",
            "src/save_data/savegame_slot6.json"
        ]
        self.save_slot_files = [resource_path(path) for path in self.save_slot_relative_paths]
        self.mode = 'load'
        self.load_save_button_size = UI_BUTTON_SIZE[0] * 6, UI_BUTTON_SIZE[1]
        self.create_buttons(ui_manager)

        btn_w, btn_h = 100, 50
        tx, ty = anchor(btn_w, btn_h, h='right', v='top', margin=C.SPACE_MD)
        self.toggle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((tx, ty), (btn_w, btn_h)),
            text='Switch to Save',
            manager=ui_manager,
            object_id='toggle_button'
        )
        self.add_ui_element(self.toggle_button)

        self.update_button_visibility()
        self.close_screen()

    def update_button_visibility(self):
        for button in self.load_buttons + self.save_buttons:
            button.visible = False
        if self.mode == 'load':
            for button in self.load_buttons:
                button.visible = True
        elif self.mode == 'save':
            for button in self.save_buttons:
                button.visible = True

    def open_screen(self):
        super().open_screen()
        self.update_button_visibility()

    def create_buttons(self, ui_manager):
        screen_width = SCREEN_WIDTH
        button_width = self.load_save_button_size[0]
        x_position = (screen_width - button_width) / 2
        vertical_pad = 20
        for i, filename in enumerate(self.save_slot_files):
            slot_label = self.get_slot_label(filename, i)

            load_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([x_position, 150 + i * (self.load_save_button_size[1] + vertical_pad)], self.load_save_button_size),
                text=f"Load {slot_label}",
                manager=ui_manager,
                object_id=f"load_button_{i}",
                visible=self.mode == 'load'
            )
            self.add_ui_element(load_button)
            self.load_buttons.append(load_button)

            save_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([x_position, 150 + i * (self.load_save_button_size[1] + vertical_pad)], self.load_save_button_size),
                text=f"Save {slot_label}",
                manager=ui_manager,
                object_id=f"save_button_{i}",
                visible=self.mode == 'save'
            )
            self.add_ui_element(save_button)
            self.save_buttons.append(save_button)

    def get_slot_label(self, filename, index):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                unlocked = data['player'].get('unlocked_levels', [])
                last_level = max(unlocked) if unlocked else 0
                total_score = data['player']['totalScore']
                mod_time = os.path.getmtime(filename)
                save_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                return f"Slot {index + 1}: Level {last_level}, Score: {total_score}, Saved: {save_date}"
        else:
            return f"Slot {index + 1}: Empty"

    def on_button_pressed(self, ui_element, game):
        if ui_element == self.toggle_button:
            self.toggle_mode()
            return
        buttons = self.save_buttons if self.mode == 'save' else self.load_buttons
        for i, button in enumerate(buttons):
            if ui_element == button:
                self.selected_slot = i
                self.initiate_action(self.mode, self.save_slot_files[i], game)
                break

    def on_confirmation(self, game):
        if self.mode == 'load':
            game.load_game(self.save_slot_files[self.selected_slot])
        elif self.mode == 'save':
            game.save_game(self.save_slot_files[self.selected_slot])
        game.state_manager.change_state(game.previous_state)
        self.close_screen()

    def initiate_action(self, mode, file_path, game):
        self.show_confirmation_dialog(mode, file_path, game)

    def show_confirmation_dialog(self, action, file_path, game):
        confirm_message = f"Are you sure you want to {action} this game in the selected slot?"
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((250, 200), (300, 200)),
            manager=game.UI_manager,
            window_title="Confirm Action",
            action_long_desc=confirm_message,
            action_short_name="Confirm"
        )

    def toggle_mode(self):
        self.mode = 'save' if self.mode == 'load' else 'load'
        for button in self.load_buttons + self.save_buttons:
            button.visible = (self.mode == 'load' and button in self.load_buttons) or \
                             (self.mode == 'save' and button in self.save_buttons)
        self.toggle_button.set_text('Switch to Load' if self.mode == 'save' else 'Switch to Save')
