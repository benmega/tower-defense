import pygame
import pygame_gui

import src.config.config as configuration
from src.config.config import GAME_BOARD_SCREEN_SIZE, UI_BUTTON_SIZE, SCREEN_HEIGHT
from src.game.game_state import GameState
import src.utils.constants as constants


class PlayerInfoPanel:
    def __init__(self, ui_manager, player, screen):
        self.ui_manager = ui_manager
        self.player = player
        self.screen = screen
        self.visible = False
        self.ui_elements = []
        self.enemy_manager_ref = None
        self.init_ui()
        self.set_visibility(False)

    def init_ui(self):
        # Panel positioning
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

        # Score Label
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + (label_height + spacing)), (panel_width, label_height)),
            text=f"Score: {self.player.levelScore}",
            manager=self.ui_manager)
        self.ui_elements.append(self.score_label)

        # Enemy Count Label
        self.enemy_count_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + 2 * (label_height + spacing)), (panel_width, label_height)),
            text="Enemies: 0",
            manager=self.ui_manager)
        self.ui_elements.append(self.enemy_count_label)

        # Wave counter label
        self.wave_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + 3 * (label_height + spacing)), (panel_width, label_height)),
            text="Wave: -",
            manager=self.ui_manager)
        self.ui_elements.append(self.wave_label)

        # Health bar (label only, drawn in draw() method)
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((start_x, start_y + 4 * (label_height + spacing)), (panel_width, 20)),
            text="",
            manager=self.ui_manager)
        self.ui_elements.append(self.health_label)

        # HUD Buttons
        button_start_y = start_y + 5 * (label_height + spacing) + 20
        btn_spacing = 5
        btn_width = int(panel_width / 4 - btn_spacing)

        self.build_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x, button_start_y), (btn_width, 30)),
            text="Build",
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.ui_elements.append(self.build_button)

        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + btn_width + btn_spacing, button_start_y), (btn_width, 30)),
            text="||",
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.ui_elements.append(self.pause_button)

        self.speed_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + 2 * (btn_width + btn_spacing), button_start_y), (btn_width, 30)),
            text="1x",
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.ui_elements.append(self.speed_button)

        self.ranges_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + 3 * (btn_width + btn_spacing), button_start_y), (btn_width, 30)),
            text="R",
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.ui_elements.append(self.ranges_button)

    def update(self, enemy_manager, current_level=None, level_index=None, is_build_mode=False):
        self.enemy_manager_ref = enemy_manager
        self.gold_label.set_text(f"Gold: {self.player.gold}")
        self.score_label.set_text(f"Score: {self.player.levelScore}")
        self.enemy_count_label.set_text(f"Enemies: {len(enemy_manager.entities)}")
        self.build_button.set_text("Cancel" if is_build_mode else "Build")
        if current_level is not None:
            wave_num = current_level.current_wave_index + 1
            total_waves = len(current_level.enemy_wave_list)
            level_tag = f"  (Lv {level_index + 1})" if level_index is not None else ""
            self.wave_label.set_text(f"Wave: {wave_num}/{total_waves}{level_tag}")

    def draw(self, screen):
        if not self.visible:
            return

        # Draw health bar
        panel_width = screen.get_width() - GAME_BOARD_SCREEN_SIZE[0]
        start_x = screen.get_width() - panel_width - 2
        health_bar_y = 10 + 4 * 36

        health_bar_width = panel_width - 20
        health_bar_height = 20
        x = start_x + 10
        y = health_bar_y

        # Background track
        pygame.draw.rect(screen, constants.RGB_BG_MID, (x, y, health_bar_width, health_bar_height), border_radius=4)

        # Fill
        max_health = getattr(self.player, 'max_health', 100)
        fill_w = int(health_bar_width * self.player.health / max_health) if max_health > 0 else 0
        color = constants.RGB_HEALTH_GREEN if self.player.health / max_health > 0.5 else constants.RGB_HEALTH_RED
        pygame.draw.rect(screen, color, (x, y, fill_w, health_bar_height), border_radius=4)

        # Border
        pygame.draw.rect(screen, constants.RGB_AMBER, (x, y, health_bar_width, health_bar_height), 1, border_radius=4)

        # Health text
        font = pygame.font.Font(None, 14)
        health_text = font.render(f"Health: {self.player.health}/{max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + health_bar_width // 2, y + health_bar_height // 2))
        screen.blit(health_text, text_rect)

        # Keyboard shortcuts hint
        hint_font = pygame.font.Font(None, 13)
        hints = ["1-9: Tower  R: Ranges", "Space: Skip wave  ESC: Pause"]
        hint_y = y + health_bar_height + 40  # below HUD buttons
        for hint in hints:
            hint_surf = hint_font.render(hint, True, (130, 130, 130))
            screen.blit(hint_surf, (x, hint_y))
            hint_y += 14

    def set_visibility(self, visible):
        self.visible = visible
        for element in self.ui_elements:
            element.visible = visible

    def handle_events(self, event, game):
        """Handle button clicks for HUD buttons."""
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.build_button:
                    game.is_build_mode = not game.is_build_mode
                    if not game.is_build_mode:
                        game.tower_selection_panel.deselect()
                elif event.ui_element == self.pause_button:
                    game.state_manager.change_state(GameState.PAUSED)
                elif event.ui_element == self.speed_button:
                    if configuration.GAME_SPEED_MULTIPLIER == 1.0:
                        configuration.GAME_SPEED_MULTIPLIER = 2.0
                        self.speed_button.set_text(">>2x")
                    else:
                        configuration.GAME_SPEED_MULTIPLIER = 1.0
                        self.speed_button.set_text("1x")
                elif event.ui_element == self.ranges_button:
                    game.tower_manager.toggle_ranges()
