import pygame
import pygame_gui

from src.config.config import GAME_BOARD_SCREEN_SIZE


class PlayerInfoPanel:
    def __init__(self, ui_manager, player, screen):
        self.ui_manager = ui_manager
        self.player = player
        self.screen = screen
        self.ui_elements = []
        self.init_ui()
        self.set_visibility(False)

    def init_ui(self):
        # Assuming the screen's dimensions and positioning
        panel_width = self.screen.get_width() - GAME_BOARD_SCREEN_SIZE[0]
        start_x = self.screen.get_width() - panel_width - 2
        start_y = 10
        label_height = 35
        spacing = 1

        # Gold Label
        self.gold_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y), (panel_width, label_height)),
            text=f"Gold: {self.player.gold}",
            manager=self.ui_manager)
        self.ui_elements.append(self.gold_label)

        # Health Label
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + label_height + spacing), (panel_width, label_height)),
            text=f"Health: {self.player.health}",
            manager=self.ui_manager)
        self.ui_elements.append(self.health_label)

        # Score Label
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + 2 * (label_height + spacing)), (panel_width, label_height)),
            text=f"Score: {self.player.levelScore}",
            manager=self.ui_manager)
        self.ui_elements.append(self.score_label)

        # Enemy Count Label
        self.enemy_count_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + 3 * (label_height + spacing)), (panel_width, label_height)),
            text="Enemies: 0",
            manager=self.ui_manager)
        self.ui_elements.append(self.enemy_count_label)

    def update(self, enemy_manager):
        # Update the labels based on current player stats
        self.gold_label.set_text(f"Gold: {self.player.gold}")
        self.health_label.set_text(f"Health: {self.player.health}")
        self.score_label.set_text(f"Score: {self.player.levelScore}")
        self.enemy_count_label.set_text(f"Enemies: {len(enemy_manager.entities)}")

    def set_visibility(self, visible):
        for element in self.ui_elements:
            element.visible = visible
