import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen
from src.utils.helpers import load_scaled_image
from src.utils.layout import anchor
import src.utils.constants as C


class Camera:
    def __init__(self, map_size, viewport_size):
        self.position = pygame.Vector2(0, 0)
        self.map_size = pygame.Vector2(map_size)
        self.viewport_size = pygame.Vector2(viewport_size)
        self.move(SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3)

    def center_on(self, target_position):
        self.position.x = target_position[0] - self.viewport_size[0] / 2
        self.position.y = target_position[1] - self.viewport_size[1] / 2

    def move(self, dx, dy):
        self.position.x = max(0, min(self.map_size.x - self.viewport_size.x, self.position.x + dx))
        self.position.y = max(0, min(self.map_size.y - self.viewport_size.y, self.position.y + dy))

    def get_visible_area(self):
        return pygame.Rect(self.position.x, self.position.y, self.viewport_size.x, self.viewport_size.y)


def _generate_level_positions(count: int, cols: int = 6) -> list:
    """Lay out levels in a snake pattern across the entire map."""
    MAP_W = SCREEN_WIDTH * 3
    MAP_H = SCREEN_HEIGHT * 3
    positions = []

    # Calculate rows needed
    rows = (count + cols - 1) // cols

    # Spacing between levels
    col_spacing = MAP_W / (cols + 1)
    row_spacing = MAP_H / (rows + 1)

    for i in range(count):
        row = i // cols
        col = i % cols if row % 2 == 0 else (cols - 1 - i % cols)

        # Position with proper spacing across the entire map
        x = int(col_spacing * (col + 1))
        y = int(row_spacing * (row + 1))
        positions.append((x, y))

    return positions


class CampaignMap(Screen):
    def __init__(self, ui_manager, player_progress):
        super().__init__(ui_manager, 'assets/images/screens/campaignMap/campaign_map.png')
        self.visible = False
        self.ui_manager = ui_manager
        self.level_positions = _generate_level_positions(30)
        scale_factor = 3
        self.player_progress = player_progress
        self.level_buttons = []

        self.map_image = load_scaled_image('assets/images/screens/campaignMap/campaign_map.png',
                                           (SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor))
        self.level_visibility = {}
        self.level_button_sizes = (30 * scale_factor, 30 * scale_factor)
        self.initialize_buttons()

        btn_w, btn_h = int(UI_BUTTON_SIZE[0]), int(UI_BUTTON_SIZE[1])
        sx, sy = anchor(btn_w, btn_h, h='right', v='top', margin=C.SPACE_MD)
        self.skills_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([sx, sy], UI_BUTTON_SIZE),
            text='Skills',
            manager=self.ui_manager,
            object_id="@button",
            visible=False
        )
        self.ui_elements.append(self.skills_button)
        self.camera = Camera((self.map_image.get_width(), self.map_image.get_height()),
                             (SCREEN_WIDTH, SCREEN_HEIGHT))
        self._cam_vel_x = 0.0
        self._cam_vel_y = 0.0

    def initialize_buttons(self):
        self.level_buttons.clear()
        for index, position in enumerate(self.level_positions):
            unlocked = self.is_level_unlocked(index)
            image_path = ('assets/images/screens/campaignMap/unlocked_level.png' if unlocked
                          else 'assets/images/screens/campaignMap/locked_level.png')
            button_image = load_scaled_image(image_path, self.level_button_sizes)
            button_rect = button_image.get_rect(center=position)
            self.level_buttons.append((button_image, button_rect, unlocked))

    def draw(self, screen):
        visible_rect = self.camera.get_visible_area()
        visible_map = self.map_image.subsurface(visible_rect)
        screen.blit(visible_map, (0, 0))
        screen_rect = pygame.Rect(0, 0, self.camera.viewport_size.x, self.camera.viewport_size.y)

        for button_image, button_rect, _ in self.level_buttons:
            adjusted_rect = button_rect.move(-self.camera.position.x, -self.camera.position.y)
            if screen_rect.colliderect(adjusted_rect):
                screen.blit(button_image, adjusted_rect.topleft)

        self._draw_fade_overlay(screen)

    def is_level_unlocked(self, level_index):
        return level_index in self.player_progress

    def on_button_pressed(self, ui_element, game):
        if ui_element == self.return_button:
            game.state_manager.change_state(GameState.MAIN_MENU, self)
        elif ui_element == self.skills_button:
            game.state_manager.change_state(GameState.SKILLS, self)

    def on_click(self, pos, game):
        self.handle_clicks(pos, game)

    def handle_clicks(self, pos, game):
        mouse_pos = pygame.Vector2(pos) + self.camera.position

        for index, (_, button_rect, unlocked) in enumerate(self.level_buttons):
            if button_rect.collidepoint(mouse_pos) and unlocked:
                game.initialize_game(index)
                self.close_screen()
                break

    def update_player_progress(self, new_progress):
        self.player_progress = new_progress
        self.initialize_buttons()

    def update(self, time_delta):
        super().update(time_delta)
        self.handle_camera_movement()

    def handle_camera_movement(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        move_threshold = 50
        max_speed = 10

        target_dx = 0.0
        target_dy = 0.0

        if mouse_x < move_threshold:
            target_dx = -max_speed * (1 - mouse_x / move_threshold)
        elif mouse_x > SCREEN_WIDTH - move_threshold:
            target_dx = max_speed * (1 - (SCREEN_WIDTH - mouse_x) / move_threshold)

        if mouse_y < move_threshold:
            target_dy = -max_speed * (1 - mouse_y / move_threshold)
        elif mouse_y > SCREEN_HEIGHT - move_threshold:
            target_dy = max_speed * (1 - (SCREEN_HEIGHT - mouse_y) / move_threshold)

        self._cam_vel_x += (target_dx - self._cam_vel_x) * 0.12
        self._cam_vel_y += (target_dy - self._cam_vel_y) * 0.12

        if abs(self._cam_vel_x) > 0.1 or abs(self._cam_vel_y) > 0.1:
            self.camera.move(self._cam_vel_x, self._cam_vel_y)

    def create_return_button(self):
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([SCREEN_WIDTH - UI_BUTTON_SIZE[0] - 10, 10], UI_BUTTON_SIZE),
            text="Main Menu",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(button)
        return button
