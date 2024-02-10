import pygame

from src.config.config import TOWER_TYPES, UI_FONT_SIZE


class TowerSelectionPanel:
    def __init__(self, screen, tower_manager):
        self.screen = screen
        self.tower_manager = tower_manager
        self.panel_height = screen.get_height() * 0.20  # Adjust as needed
        self.panel_y = screen.get_height() - self.panel_height
        self.icon_size = screen.get_width() * 0.07  # Adjust based on your icon sizes
        self.font = pygame.font.Font(None, UI_FONT_SIZE)  # Adjust font as needed
        self.icons = {}  # To store preloaded and scaled images
        self.icon_padding = 5  # 5 pixels of padding

        # Preload and scale images
        for tower_type, tower_info in TOWER_TYPES.items():
            icon_path = tower_info['image_path']
            icon_image = pygame.image.load(icon_path).convert_alpha()
            self.icons[tower_type] = pygame.transform.scale(icon_image, [self.icon_size, self.icon_size])

    def draw(self):
        # Draw the panel background
        pygame.draw.rect(self.screen, [200, 200, 200], [0, self.panel_y, self.screen.get_width(), self.panel_height])

        # Draw each tower icon from preloaded images
        for index, (tower_type, tower_info) in enumerate(TOWER_TYPES.items()):
            x = 10 + index * (self.icon_size + self.icon_padding)  # 5 pixels padding between icons
            y = self.panel_y + (self.panel_height - self.icon_size) // 2

            # Use preloaded and scaled icon
            self.screen.blit(self.icons[tower_type], (x, y))

            # Highlight if selected
            if tower_type == self.tower_manager.selected_tower_type:
                pygame.draw.rect(self.screen, [255, 255, 0], [x, y, self.icon_size, self.icon_size], 3)  # Yellow border

            # Tower name above the icon
            name_text = self.font.render(tower_type, True, [0, 0, 0])
            name_text_rect = name_text.get_rect(center=(x + self.icon_size // 2, y - 20))
            self.screen.blit(name_text, name_text_rect)

            # Tower cost below the icon
            cost_text = self.font.render(f"Cost: {tower_info['cost']}", True, [0, 0, 0])
            cost_text_rect = cost_text.get_rect(center=(x + self.icon_size // 2, y + self.icon_size + 20))
            self.screen.blit(cost_text, cost_text_rect)

    def update_selected_tower(self, new_selected_tower_type):
        self.tower_manager.selected_tower_type = new_selected_tower_type

    def is_within_panel(self, mouse_pos):
        x, y = mouse_pos
        return y > self.panel_y

    def handle_mouse_click(self, mouse_pos):
        x, y = mouse_pos
        if self.is_within_panel(mouse_pos):  # Check if click is within the panel
            for index, tower_type in enumerate(TOWER_TYPES.keys()):
                icon_x = 10 + index * (self.icon_size + self.icon_padding)
                icon_y = self.panel_y + (self.panel_height - self.icon_size) // 2
                # Check if click is within the bounds of this tower's icon
                if icon_x <= x <= icon_x + self.icon_size and icon_y <= y <= icon_y + self.icon_size:
                    self.update_selected_tower(tower_type)
                    break
