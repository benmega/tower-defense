# game_board.py
import pygame
import pygame_gui
from pip._internal import configuration

# import pygame

from src.config.config import TILE_SIZE, GRASS_IMAGE_PATH, ENTRANCE_IMAGE_PATH, PATH_IMAGE_PATH, EXIT_IMAGE_PATH
from src.utils.helpers import load_scaled_image

class GameBoard:
    '''
    Core game class responsible for initializing the game, running the main loop, handling game state transitions (like starting, game over), and managing high-level game events.
    Potential TODOs: Implementing efficient game state management, optimizing the main game loop for performance, and handling transitions between different parts of the game smoothly.
    '''
    def __init__(self, width, height):
        '''

        :param width: Width in tiles of the game board
        :param height: Height in tiles of the game board
        '''
        self.width = width
        self.height = height
        self.grass_image = load_scaled_image(GRASS_IMAGE_PATH, TILE_SIZE)
        self.path_image = load_scaled_image(PATH_IMAGE_PATH, TILE_SIZE)
        self.entrance_image = load_scaled_image(ENTRANCE_IMAGE_PATH, TILE_SIZE)
        self.exit_image = load_scaled_image(EXIT_IMAGE_PATH, TILE_SIZE)
        self.grid = [[None for _ in range(width)] for _ in range(height)]



    def get_tower_at(self, x, y):
        '''x and way are tile grid numbers not pixels'''
        return self.grid[y][x] if self.is_valid_position(x, y) else None

    def get_tile_image(self, x, y, path):
        path_layout = self.create_path_layout(path)
        tile_type = path_layout[y][x]
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


    def draw_board(self, screen: object, path: object) -> object:
        # Draw the background
        self.draw_background(screen, path)


    def draw_background(self, screen, path):
        for y in range(self.height):
            for x in range(self.width):
                image = self.get_tile_image(x, y, path)
                screen.blit(image, (x * TILE_SIZE[0], y * TILE_SIZE[1]))

    def create_path_layout(self, path):

        # Convert path points to grid coordinates TODO set path to be grid based
        path = [(min(x // TILE_SIZE[0],self.width-1), min(y // TILE_SIZE[1],self.height-1)) for x, y in path]

        # Initialize layout with grass
        layout = [['G' for _ in range(self.width)] for _ in range(self.height)]


        def fill_path(x1, y1, x2, y2):
            if x1 == x2:  # Vertical path
                startY, endY = sorted([y1, y2])
                for y in range(startY, endY + 1):
                    if 0 <= y < self.height:
                        layout[y][x1] = 'P'
            elif y1 == y2:  # Horizontal path
                startX, endX = sorted([x1, x2])
                for x in range(startX, endX + 1):
                    if 0 <= x < self.width:
                        layout[y1][x] = 'P'

        # Iterate through path points
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            fill_path(x1, y1, x2, y2)

        # Mark entrance and exit
        layout[path[0][1]][path[0][0]] = 'E'  # Entrance
        layout[path[-1][1]][path[-1][0]] = 'X'  # Exit

        return layout

    def is_valid_position(self, x, y):
        '''x and way are tile grid numbers not pixels'''
        return 0 <= x < self.width and 0 <= y < self.height

    def is_within_panel(self, mouse_pos):
        # assumes board is at (0,0)
        x, y = mouse_pos
        '''x and way are pixel based not tile based'''
        return x < self.width * TILE_SIZE[0] and y < self.height * TILE_SIZE[1]