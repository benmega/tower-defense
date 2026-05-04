import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE, GAME_BOARD_SCREEN_SIZE
import src.utils.constants as constants


class TowerInfoPanel:
    def __init__(self, ui_manager):
        self.visible = False
        self.ui_manager = ui_manager
        self.tower = None

        # Panel dimensions
        self.panel_width = 220
        self.panel_height = 200
        self.panel_x = GAME_BOARD_SCREEN_SIZE[0] + 15
        self.panel_y = SCREEN_HEIGHT - self.panel_height - 20

        btn_x = self.panel_x + (self.panel_width - UI_BUTTON_SIZE[0]) // 2
        btn_y_start = self.panel_y + 110

        self.upgrade_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y_start), UI_BUTTON_SIZE),
            text='Upgrade',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.sell_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((btn_x, btn_y_start + UI_BUTTON_SIZE[1] + 5), UI_BUTTON_SIZE),
            text='Sell',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )

    def show(self, tower):
        self.visible = True
        self.tower = tower
        self.upgrade_button.visible = tower.can_upgrade()
        self.sell_button.visible = True

    def hide(self):
        self.visible = False
        self.tower = None
        self.upgrade_button.visible = False
        self.sell_button.visible = False

    def draw(self, screen):
        if not self.visible or not self.tower:
            return

        # Panel background
        pygame.draw.rect(
            screen, constants.RGB_BG_DARK,
            (self.panel_x, self.panel_y, self.panel_width, self.panel_height),
            border_radius=constants.RADIUS_MD
        )
        pygame.draw.rect(
            screen, constants.RGB_AMBER,
            (self.panel_x, self.panel_y, self.panel_width, self.panel_height),
            1, border_radius=constants.RADIUS_MD
        )

        # Tower info text
        font = pygame.font.Font(None, 20)
        tower = self.tower

        lines = [
            f"{tower.tower_type}",
            f"Damage: {int(tower.damage)}",
            f"Range: {int(tower.attack_range)}",
            f"Speed: {tower.attack_speed}",
            f"Value: {tower.sell_value}g"
        ]

        y = self.panel_y + 10
        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (self.panel_x + 10, y))
            y += 18

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.upgrade_button and self.tower:
                    if game.player.spend_gold(self.tower.upgrade_cost):
                        self.tower.upgrade()
                        # Update button visibility
                        self.upgrade_button.visible = self.tower.can_upgrade()
                elif event.ui_element == self.sell_button and self.tower:
                    game.tower_manager.sell_tower(self.tower, game.player)
                    self.hide()
