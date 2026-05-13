import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE, GAME_BOARD_SCREEN_SIZE, TOWER_TYPES
import src.utils.constants as constants


class TowerInfoPanel:
    def __init__(self, ui_manager):
        self.visible = False
        self.ui_manager = ui_manager
        self.tower = None

        # Panel dimensions
        self.panel_width = 230
        self.panel_height = 230
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

    def show(self, tower, player_gold=None):
        self.visible = True
        self.tower = tower
        if tower.can_upgrade():
            can_afford = player_gold is None or player_gold >= tower.upgrade_cost
            label = f'Upgrade ({tower.upgrade_cost}g)' if can_afford else f'Upgrade ({tower.upgrade_cost}g) ✗'
            self.upgrade_button.set_text(label)
            self.upgrade_button.visible = True
            if can_afford:
                self.upgrade_button.enable()
            else:
                self.upgrade_button.disable()
        else:
            self.upgrade_button.set_text('Max Level')
            self.upgrade_button.disable()
            self.upgrade_button.visible = True
        self.sell_button.set_text(f'Sell ({tower.sell_value}g)')
        self.sell_button.enable()
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

        font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 17)
        tower = self.tower

        # Next-level stats for upgrade preview
        next_dmg = int(tower.damage * 1.25) if tower.can_upgrade() else None
        next_range = int(tower.attack_range * 1.1) if tower.can_upgrade() else None

        lines = [
            (f"{tower.tower_type}  [Lv {tower.upgrade_level}]", font, constants.RGB_AMBER),
            (f"Damage: {int(tower.damage)}" + (f" → {next_dmg}" if next_dmg else ""), font, (255, 255, 255)),
            (f"Range:  {int(tower.attack_range)}" + (f" → {next_range}" if next_range else ""), font, (255, 255, 255)),
            (f"Speed:  {tower.attack_speed}", font, (255, 255, 255)),
        ]
        desc = TOWER_TYPES.get(tower.tower_type, {}).get('description', '')
        if desc:
            lines.append((desc, small_font, (180, 180, 180)))

        y = self.panel_y + 10
        for text_str, f, color in lines:
            surf = f.render(text_str, True, color)
            screen.blit(surf, (self.panel_x + 10, y))
            y += f.size("A")[1] + 2

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.upgrade_button and self.tower:
                    if game.player.spend_gold(self.tower.upgrade_cost):
                        self.tower.upgrade()
                        import src.utils.constants as C
                        game.particles.emit(self.tower.x + 16, self.tower.y + 16,
                                           count=18, color=C.RGB_AMBER, speed=3.5, life=0.7)
                        game.tower_manager.play_build_sound()
                        # Update button visibility
                        self.upgrade_button.visible = self.tower.can_upgrade()
                elif event.ui_element == self.sell_button and self.tower:
                    tower = self.tower
                    game.tower_manager.sell_tower(tower, game.player)
                    import src.utils.constants as C
                    game.particles.emit(tower.x + 16, tower.y + 16,
                                       count=12, color=C.RGB_GOLD_BRIGHT, speed=2.5, life=0.6)
                    game.tower_manager.play_build_sound()
                    self.hide()
