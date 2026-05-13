import pygame

from src.config.config import TOWER_TYPES, UI_FONT_SIZE
from src.utils.resource_path import resource_path


class TowerSelectionPanel:
    def __init__(self, screen, tower_manager):
        self.screen = screen
        self.tower_manager = tower_manager
        self.panel_height = int(screen.get_height() * 0.20)  # Adjust as needed
        self.panel_y = screen.get_height() - self.panel_height
        self.icon_size = int(screen.get_width() * 0.07)  # Adjust based on your icon sizes
        self.font = pygame.font.Font(None, UI_FONT_SIZE)  # Adjust font as needed
        self.icons = {}  # To store preloaded and scaled images
        self.icon_padding = 5  # 5 pixels of padding

        # Preload and scale images
        for tower_type, tower_info in TOWER_TYPES.items():
            icon_path = tower_info['image_path']
            icon_image = pygame.image.load(resource_path(icon_path)).convert_alpha()
            self.icons[tower_type] = pygame.transform.scale(icon_image, [self.icon_size, self.icon_size])

    def draw(self):
        # Draw the panel background
        pygame.draw.rect(self.screen, [200, 200, 200], [0, self.panel_y, self.screen.get_width(), self.panel_height])

        player_gold = getattr(self.tower_manager, 'player', None)
        player_gold = player_gold.gold if player_gold else None

        mouse_pos = pygame.mouse.get_pos()
        hovered_tower = None
        hovered_rect = None

        # Reusable dark overlay surface for unaffordable icons
        dim_surface = pygame.Surface((self.icon_size, self.icon_size), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 140))

        # Draw each tower icon from preloaded images
        for index, (tower_type, tower_info) in enumerate(TOWER_TYPES.items()):
            x = 10 + index * (self.icon_size + self.icon_padding)
            y = self.panel_y + (self.panel_height - self.icon_size) // 2
            cost = tower_info['cost']
            can_afford = player_gold is None or player_gold >= cost

            self.screen.blit(self.icons[tower_type], (x, y))

            # Dim icon if unaffordable
            if not can_afford:
                self.screen.blit(dim_surface, (x, y))

            # Highlight if selected
            if tower_type == self.tower_manager.selected_tower_type:
                pygame.draw.rect(self.screen, [255, 255, 0], [x, y, self.icon_size, self.icon_size], 3)

            # Tower name above the icon (includes hotkey hint for first 9)
            label = f"[{index + 1}] {tower_type}" if index < 9 else tower_type
            name_color = [80, 80, 80] if not can_afford else [0, 0, 0]
            name_text = self.font.render(label, True, name_color)
            name_text_rect = name_text.get_rect(center=(x + self.icon_size // 2, y - 20))
            self.screen.blit(name_text, name_text_rect)

            # Tower cost below the icon — red if unaffordable
            cost_color = [180, 40, 40] if not can_afford else [0, 0, 0]
            cost_text = self.font.render(f"Cost: {cost}", True, cost_color)
            cost_text_rect = cost_text.get_rect(center=(x + self.icon_size // 2, y + self.icon_size + 20))
            self.screen.blit(cost_text, cost_text_rect)

            # Track which icon is hovered
            if x <= mouse_pos[0] <= x + self.icon_size and y <= mouse_pos[1] <= y + self.icon_size:
                hovered_tower = tower_type
                hovered_rect = (x, y)

        # Draw status / warning text on the right
        selected = self.tower_manager.selected_tower_type
        if selected:
            selected_cost = TOWER_TYPES[selected]['cost']
            if player_gold is not None and player_gold < selected_cost:
                hint = f"Not enough gold! Need {selected_cost - player_gold} more."
                hint_color = [180, 40, 40]
            else:
                hint = "Right-click or ESC to cancel"
                hint_color = [100, 100, 100]
        else:
            hint = "(Select a tower to place)"
            hint_color = [100, 100, 100]
        status_text = self.font.render(hint, True, hint_color)
        self.screen.blit(status_text, (self.screen.get_width() - 400, self.panel_y + 10))

        # Draw tooltip for hovered tower
        if hovered_tower and hovered_rect:
            self._draw_tooltip(hovered_tower, hovered_rect)

    def _draw_tooltip(self, tower_type, icon_rect):
        tower_info = TOWER_TYPES[tower_type]
        description = tower_info.get('description', '')
        if not description:
            return
        tooltip_font = pygame.font.Font(None, 22)
        text_surf = tooltip_font.render(description, True, (255, 255, 255))
        padding = 8
        tw, th = text_surf.get_width() + padding * 2, text_surf.get_height() + padding * 2
        tx = max(0, min(icon_rect[0], self.screen.get_width() - tw))
        ty = self.panel_y - th - 4
        pygame.draw.rect(self.screen, (40, 40, 40), (tx, ty, tw, th), border_radius=4)
        pygame.draw.rect(self.screen, (120, 120, 120), (tx, ty, tw, th), 1, border_radius=4)
        self.screen.blit(text_surf, (tx + padding, ty + padding))

    def update_selected_tower(self, new_selected_tower_type):
        self.tower_manager.selected_tower_type = new_selected_tower_type

    def is_within_panel(self, mouse_pos):
        x, y = mouse_pos
        return y > self.panel_y

    def on_click(self, pos, game):
        x, y = pos
        if self.is_within_panel(pos):
            for index, tower_type in enumerate(TOWER_TYPES.keys()):
                icon_x = 10 + index * (self.icon_size + self.icon_padding)
                icon_y = self.panel_y + (self.panel_height - self.icon_size) // 2
                if icon_x <= x <= icon_x + self.icon_size and icon_y <= y <= icon_y + self.icon_size:
                    self.update_selected_tower(tower_type)
                    game.is_build_mode = True
                    break

    def handle_mouse_click(self, mouse_pos):
        # Legacy path kept for callers that don't have a game ref; build mode not toggled here.
        x, y = mouse_pos
        if self.is_within_panel(mouse_pos):
            for index, tower_type in enumerate(TOWER_TYPES.keys()):
                icon_x = 10 + index * (self.icon_size + self.icon_padding)
                icon_y = self.panel_y + (self.panel_height - self.icon_size) // 2
                if icon_x <= x <= icon_x + self.icon_size and icon_y <= y <= icon_y + self.icon_size:
                    self.update_selected_tower(tower_type)
                    break

    def deselect(self):
        """Deselect the currently selected tower."""
        self.tower_manager.selected_tower_type = None

    @property
    def selected_tower_type(self):
        """Expose selected_tower_type from tower_manager."""
        return self.tower_manager.selected_tower_type
