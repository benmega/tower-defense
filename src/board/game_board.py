# game_board.py

import pygame

from src.config.config import TILE_SIZE, GRASS_IMAGE_PATH, ENTRANCE_IMAGE_PATH, PATH_IMAGE_PATH, EXIT_IMAGE_PATH
from src.utils.helpers import load_scaled_image


class GameBoard:
    """
    Core game class responsible for initializing the game, running the main loop, handling game state transitions (
    like starting, game over), and managing high-level game events. Potential TODOs: Implementing efficient game
    state management, optimizing the main game loop for performance, and handling transitions between different parts
    of the game smoothly.
    """

    def __init__(self, width, height):
        """

        :param width: Width in tiles of the game board
        :param height: Height in tiles of the game board
        """
        self.width = width
        self.height = height
        self.grass_image = load_scaled_image(GRASS_IMAGE_PATH, TILE_SIZE)
        self.path_image = load_scaled_image(PATH_IMAGE_PATH, TILE_SIZE)
        self.entrance_image = load_scaled_image(ENTRANCE_IMAGE_PATH, TILE_SIZE)
        self.exit_image = load_scaled_image(EXIT_IMAGE_PATH, TILE_SIZE)
<<<<<<< HEAD
        if not self.grass_image:
            print("WARNING: Failed to load grass image. Game board may not render properly.")
=======
        # Load lava and water images for future use
        try:
            self.lava_image = load_scaled_image('assets/images/gameBoardTiles/lava.png', TILE_SIZE)
            self.water_image = load_scaled_image('assets/images/gameBoardTiles/water.png', TILE_SIZE)
        except Exception as e:
            print(f"Failed to load lava/water images: {e}")
            self.lava_image = self.grass_image
            self.water_image = self.grass_image
>>>>>>> claude/suspicious-raman-d0a593
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.path = [(0, 0), (0, 500), (500, 500)]
        self.path_layout = self.create_path_layout(self.path)
        # Animation accumulators
        self._path_anim_time = 0.0
        self._tile_anim_offset = 0.0

    def get_tower_at(self, grid_x, grid_y):
        """grid_x and way are tile grid numbers not pixels"""
        # TODO Have grid update
        return self.grid[grid_y][grid_x] if self.is_valid_position(grid_x, grid_y) else None

    def get_tile_image(self, x, y, path=None):
        """

        :param x: in pixels not grids
        :param y: in pixels not grids
        :param path: in pixels not grids
        :return:
        """
        if path:
            self.path = path
        self.path_layout = self.create_path_layout(self.path)
        tile_type = self.path_layout[y][x]
        if tile_type == 'G':
            return self.grass_image
        elif tile_type == 'P':
            return self.path_image
        elif tile_type == 'E':
            return self.entrance_image
        elif tile_type == 'X':
            return self.exit_image
        else:
            return self.grass_image  # Default to grass if unknown type

    def draw_board(self, screen, path, time_delta=0):
        # Update animation timers
        self._path_anim_time += time_delta
        self._tile_anim_offset += time_delta * 20  # scroll speed in pixels/sec
        # Draw the background
        self.draw_background(screen, path)
        # Draw animated path direction indicators
        self.draw_path_chevrons(screen, path)

    def draw_background(self, screen, path):
        for y in range(self.height):
            for x in range(self.width):
                image = self.get_tile_image(x, y, path)
                if image:
                    screen.blit(image, (x * TILE_SIZE[0], y * TILE_SIZE[1]))

    def draw_path_chevrons(self, screen, path):
        """Draw animated chevrons along the path to show direction of travel."""
        if not path or len(path) < 2:
            return

        spacing = TILE_SIZE[0]
        speed = 20  # pixels per second
        anim_offset = (self._path_anim_time * speed) % spacing
        color = (255, 215, 0, 60)  # gold with low alpha

        # Create overlay surface for all chevrons
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            length = (dx * dx + dy * dy) ** 0.5
            if length == 0:
                continue

            # Unit direction vector
            ndx, ndy = dx / length, dy / length

            # Draw chevrons along this segment
            pos = anim_offset
            while pos < length:
                cx = x1 + ndx * pos
                cy = y1 + ndy * pos

                # Perpendicular direction for chevron width
                px, py = -ndy, ndx
                size = 6

                # Create chevron triangle pointing in direction of travel
                tip = (int(cx + ndx * size), int(cy + ndy * size))
                base1 = (int(cx + px * size * 0.6 - ndx * size), int(cy + py * size * 0.6 - ndy * size))
                base2 = (int(cx - px * size * 0.6 - ndx * size), int(cy - py * size * 0.6 - ndy * size))

                pygame.draw.polygon(overlay, color, [tip, base1, base2])
                pos += spacing

        screen.blit(overlay, (0, 0))

    def create_path_layout(self, path):
        """
        :param path: list of (x,y) tuples where turns occur. x and y are in pixels not grids
        :return: layout grid
        """
        if not path or len(path) < 2:
            print("ERROR: Invalid path - must have at least 2 points")
            return [['G' for _ in range(self.width)] for _ in range(self.height)]

        # Convert path points to grid coordinates TODO set path to be grid based
        path = [(min(x // TILE_SIZE[0], self.width - 1), min(y // TILE_SIZE[1], self.height - 1)) for x, y in path]

        # Initialize layout with grass
        layout = [['G' for _ in range(self.width)] for _ in range(self.height)]

        def fill_path(x_1, y_1, x_2, y_2):
            if x_1 == x_2:  # Vertical path
                start_y, end_y = sorted([y_1, y_2])
                for y in range(start_y, end_y + 1):
                    if 0 <= y < self.height:
                        layout[y][x_1] = 'P'
            elif y_1 == y_2:  # Horizontal path
                startX, endX = sorted([x_1, x_2])
                for x in range(startX, endX + 1):
                    if 0 <= x < self.width:
                        layout[y_1][x] = 'P'

        # Iterate through path points
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            fill_path(x1, y1, x2, y2)

        # Mark entrance and exit
        layout[path[0][1]][path[0][0]] = 'E'  # Entrance
        layout[path[-1][1]][path[-1][0]] = 'X'  # Exit

        return layout

    def is_valid_position(self, grid_x, grid_y):
        '''grid_x and way are tile grid numbers not pixels'''
        return 0 <= grid_x < self.width and 0 <= grid_y < self.height

    def is_within_panel(self, mouse_pos):
        # assumes board is at (0,0)
        x, y = mouse_pos
        '''grid_x and way are pixel based not tile based'''
        return x < self.width * TILE_SIZE[0] and y < self.height * TILE_SIZE[1]

    def can_build_at(self, mouse_pos):
        if not self.is_within_panel(mouse_pos):
            return False
        gridX, gridY = mouse_pos[0] // TILE_SIZE[0], mouse_pos[1] // TILE_SIZE[1]
        if self.path_layout[gridY][gridX] != 'G':  # Building on grass only is allowed
            return False
        return True
