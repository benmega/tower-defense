import pygame
import pygame_gui

from src.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BUTTON_SIZE
from src.game.game_state import GameState
from src.screens.screen import Screen
from src.utils.helpers import load_scaled_image

class Camera:
    def __init__(self, map_size, viewport_size):
        self.position = pygame.Vector2(0, 0)
        self.map_size = pygame.Vector2(map_size)
        self.viewport_size = pygame.Vector2(viewport_size)
        self.move(SCREEN_WIDTH*3,SCREEN_HEIGHT*3) # TODO adjust as player progresses in game

    def center_on(self, target_position):
        self.position.x = target_position[0] - self.viewport_size[0] / 2
        self.position.y = target_position[1] - self.viewport_size[1] / 2

    def move(self, dx, dy):
        # Update camera position while ensuring it stays within map bounds
        self.position.x = max(0, min(self.map_size.x - self.viewport_size.x, self.position.x + dx))
        self.position.y = max(0, min(self.map_size.y - self.viewport_size.y, self.position.y + dy))

    def get_visible_area(self):
        # Return the current visible area of the map
        return pygame.Rect(self.position.x, self.position.y, self.viewport_size.x, self.viewport_size.y)


class CampaignMap(Screen):
    def __init__(self, ui_manager, player_progress):
        super().__init__(ui_manager, 'assets/images/screens/campaignMap/campaign_map.png')
        self.isActive = False
        self.ui_manager = ui_manager
        self.level_positions = [
            (770, 700), (793, 678), (864, 681), (879, 645), (781, 630),
            (817, 602), (752, 603), (741, 573), (801, 526), (828, 522),
            (796, 492), (743, 502), (688, 534), (718, 469), (704, 427),
            (645, 413), (592, 382), (546, 372), (560, 358), (410, 380),
            (336, 430), (296, 395), (360, 351), (356, 328), (364, 276),
            (410, 306), (465, 282), (490, 268), (481, 247), (468, 197)
        ]
        scale_factor = 3  # The map size increased by a factor of 3
        self.level_positions = [(x * scale_factor, y * scale_factor) for x, y in self.level_positions]
        self.player_progress = player_progress
        self.level_buttons = []

        self.map_image = load_scaled_image('assets/images/screens/campaignMap/campaign_map.png',
                                           (SCREEN_WIDTH*scale_factor, SCREEN_HEIGHT*scale_factor))
        self.level_visibility = {}
        self.level_button_sizes = (30*scale_factor, 30*scale_factor)
        self.initilize_buttons()
        self.skills_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([SCREEN_WIDTH - 300, 10], UI_BUTTON_SIZE),  # Adjust position as needed
            text='Skills',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
            visible=False
        )
        self.ui_elements.append(self.skills_button) # List to hold UI elements like buttons
        self.camera = Camera((self.map_image.get_width(), self.map_image.get_height()), (SCREEN_WIDTH, SCREEN_HEIGHT))


    def initilize_buttons(self):
        self.level_buttons.clear()
        for index, position in enumerate(self.level_positions):
            unlocked = self.is_level_unlocked(index)
            image_path = 'assets/images/screens/campaignMap/unlocked_level.png' if unlocked else 'assets/images/screens/campaignMap/locked_level.png'
            button_image = load_scaled_image(image_path, self.level_button_sizes)
            button_rect = button_image.get_rect(center=position)
            self.level_buttons.append((button_image, button_rect, unlocked))

    def draw(self, screen):
        visible_rect = self.camera.get_visible_area()
        visible_map = self.map_image.subsurface(visible_rect)
        screen.blit(visible_map, (0, 0))  # Blit the visible part of the map to the screen
        screen_rect = pygame.Rect(0, 0, self.camera.viewport_size.x, self.camera.viewport_size.y)

        # Adjust button positions based on camera position and draw them
        for button_image, button_rect, _ in self.level_buttons:
            adjusted_rect = button_rect.move(-self.camera.position.x, -self.camera.position.y)
            if screen_rect.colliderect(adjusted_rect):
                screen.blit(button_image, adjusted_rect.topleft)

    def is_level_unlocked(self, level_index):
        return level_index in self.player_progress['unlocked_levels']

    def handle_events(self, event, game):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.return_button:
                    game.change_state(GameState.MAIN_MENU, self)  # Assuming game object has a method to handle state change
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_clicks(event, game)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.skills_button:
                game.change_state(GameState.SKILLS, self)  # Assuming GameState.SKILLS is defined

    def handle_clicks(self, event, game):
        # Adjust mouse_pos to account for camera position
        mouse_pos = pygame.Vector2(event.pos) + self.camera.position

        for index, (_, button_rect, unlocked) in enumerate(self.level_buttons):
            if button_rect.collidepoint(mouse_pos) and unlocked:
                game.initialize_game(index)  # Set up the game for the selected level
                #game.change_state(GameState.PLAYING,self)
                # game.level_manager.start_level(index)
                # game.player.start_level()
                self.close_screen()
                break  # Exit loop after handling the click

    def update_player_progress(self, new_progress):
        self.player_progress = new_progress
        self.initilize_buttons()  # Refresh buttons based on new progress

    def update(self, time_delta):
        super().update(time_delta)  # Call the parent update if necessary
        self.handle_camera_movement()

    def handle_camera_movement(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        move_threshold = 50  # Pixels from the edge to start moving
        move_speed = 10  # Speed of camera movement

        if mouse_x < move_threshold:  # Mouse is near the left edge
            self.camera.move(-move_speed, 0)
        elif mouse_x > SCREEN_WIDTH - move_threshold:  # Mouse is near the right edge
            self.camera.move(move_speed, 0)

        if mouse_y < move_threshold:  # Mouse is near the top edge
            self.camera.move(0, -move_speed)
        elif mouse_y > SCREEN_HEIGHT - move_threshold:  # Mouse is near the bottom edge
            self.camera.move(0, move_speed)

    def create_return_button(self):
        # Create a button in the top right corner
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect([SCREEN_WIDTH - UI_BUTTON_SIZE[0] - 10, 10], UI_BUTTON_SIZE),
            text="Main Menu",
            manager=self.ui_manager,
            visible=False
        )
        self.add_ui_element(button)
        return button