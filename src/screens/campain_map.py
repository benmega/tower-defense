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
        self.level_stars = {}  # str(level_index) -> best star count
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
        self._level_font = pygame.font.Font(None, 22)
        self._tooltip_font = pygame.font.Font(None, 22)
        self._center_camera_on_progress()

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

        # Draw connecting path lines between consecutive levels
        for i in range(len(self.level_positions) - 1):
            p1 = pygame.Vector2(self.level_positions[i]) - self.camera.position
            p2 = pygame.Vector2(self.level_positions[i + 1]) - self.camera.position
            color = (180, 140, 80) if self.level_buttons[i][2] else (80, 80, 80)
            pygame.draw.line(screen, color, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), 3)

        mouse_pos = pygame.mouse.get_pos()
        hovered_index = None

        for index, (button_image, button_rect, unlocked) in enumerate(self.level_buttons):
            adjusted_rect = button_rect.move(-self.camera.position.x, -self.camera.position.y)
            if screen_rect.colliderect(adjusted_rect):
                screen.blit(button_image, adjusted_rect.topleft)

                # Level number label centered on button
                num_surf = self._level_font.render(str(index + 1), True, (255, 255, 255))
                num_rect = num_surf.get_rect(center=(adjusted_rect.centerx, adjusted_rect.centery - 8))
                screen.blit(num_surf, num_rect)

                # Star rating below level number
                best_stars = self.level_stars.get(str(index), 0)
                if best_stars > 0:
                    star_str = "★" * best_stars + "☆" * (3 - best_stars)
                    star_surf = self._level_font.render(star_str, True, (255, 215, 0))
                    star_rect = star_surf.get_rect(center=(adjusted_rect.centerx, adjusted_rect.centery + 10))
                    screen.blit(star_surf, star_rect)

                if adjusted_rect.collidepoint(mouse_pos):
                    hovered_index = index

        # Hover tooltip
        if hovered_index is not None:
            _, _, unlocked = self.level_buttons[hovered_index]
            status = "Unlocked" if unlocked else "Locked"
            tip = f"Level {hovered_index + 1}  [{status}]"
            tip_surf = self._tooltip_font.render(tip, True, (255, 255, 255))
            padding = 8
            tw = tip_surf.get_width() + padding * 2
            th = tip_surf.get_height() + padding * 2
            tx = min(mouse_pos[0] + 12, SCREEN_WIDTH - tw - 4)
            ty = max(mouse_pos[1] - th - 4, 4)
            pygame.draw.rect(screen, (30, 30, 30), (tx, ty, tw, th), border_radius=4)
            pygame.draw.rect(screen, (120, 120, 120), (tx, ty, tw, th), 1, border_radius=4)
            screen.blit(tip_surf, (tx + padding, ty + padding))

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

    def _center_camera_on_progress(self):
        """Center the camera on the most recently unlocked level."""
        if self.player_progress:
            last_idx = max(self.player_progress) if hasattr(self.player_progress, '__iter__') else 0
            last_idx = min(last_idx, len(self.level_positions) - 1)
            self.camera.center_on(self.level_positions[last_idx])
        else:
            self.camera.center_on(self.level_positions[0])

    def update_player_progress(self, new_progress, level_stars=None):
        self.player_progress = new_progress
        if level_stars is not None:
            self.level_stars = level_stars
        self.initialize_buttons()
        self._center_camera_on_progress()

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
