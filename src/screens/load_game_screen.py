import json

import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE
from src.screens.screen import Screen


class LoadGameScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "assets/images/screens/load_game_screen.png")
        self.load_buttons = []
        self.save_slot_files = [
            "src/save_data/savegame_slot1.json",
            "src/save_data/savegame_slot2.json",
            "src/save_data/savegame_slot3.json",
            "src/save_data/savegame_slot4.json",
            "src/save_data/savegame_slot5.json",
            "src/save_data/savegame_slot6.json"
        ]

        for i, filename in enumerate(self.save_slot_files):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([50, 100 + i * (UI_BUTTON_SIZE[1] + 10)], UI_BUTTON_SIZE),
                text=f"Load Slot {i + 1}",
                manager=ui_manager,
                object_id=f"load_button_{i}",
                visible=False
            )
            self.add_ui_element(button)
            self.load_buttons.append(button)

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(self.load_buttons):
                    if event.ui_element == button:
                        self.load_game(game, self.save_slot_files[i])

    def load_game(self, game, filename):
        try:
            with open(filename, 'r') as f:
                player_data = json.load(f)
                print(player_data)
                game.player.load_data(player_data)
                game.campaign_map.update_player_progress(player_data['player'])
                self.close_screen()
                game.change_state(game.previous_state)
        except FileNotFoundError:
            print(f"Save file not found: {filename}")
