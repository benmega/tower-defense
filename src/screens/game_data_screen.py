import json
import pygame
import pygame_gui

from src.config.config import UI_BUTTON_SIZE
from src.screens.screen import Screen

class GameDataScreen(Screen):
    def __init__(self, ui_manager):
        super().__init__(ui_manager, "assets/images/screens/load_game_screen.png")
        self.load_buttons = []
        self.save_buttons = []
        self.save_slot_files = [
            "src/save_data/savegame_slot1.json",
            "src/save_data/savegame_slot2.json",
            "src/save_data/savegame_slot3.json",
            "src/save_data/savegame_slot4.json",
            "src/save_data/savegame_slot5.json",
            "src/save_data/savegame_slot6.json"
        ]

        # Create Load buttons
        for i, filename in enumerate(self.save_slot_files):
            load_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([50, 100 + i * (UI_BUTTON_SIZE[1] + 10)], UI_BUTTON_SIZE),
                text=f"Load Slot {i + 1}",
                manager=ui_manager,
                object_id=f"load_button_{i}",
                visible=False
            )
            self.add_ui_element(load_button)
            self.load_buttons.append(load_button)

        # Create Save buttons
        for i, filename in enumerate(self.save_slot_files):
            save_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect([300, 100 + i * (UI_BUTTON_SIZE[1] + 10)], UI_BUTTON_SIZE),
                text=f"Save Slot {i + 1}",
                manager=ui_manager,
                object_id=f"save_button_{i}",
                visible=False
            )
            self.add_ui_element(save_button)
            self.save_buttons.append(save_button)

    def handle_events(self, event, game):
        super().handle_events(event, game)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Check Load buttons
                for i, button in enumerate(self.load_buttons):
                    if event.ui_element == button:
                        game.load_game(self.save_slot_files[i])
                        self.close_screen()
                        game.change_state(game.previous_state)
                        break  # Exit loop after finding the matching button

                # Check Save buttons
                for i, button in enumerate(self.save_buttons):
                    if event.ui_element == button:
                        game.save_game(self.save_slot_files[i])
                        self.close_screen()
                        game.change_state(game.previous_state)
                        # No need to change state after saving
                        break  # Exit loop after finding the matching button
