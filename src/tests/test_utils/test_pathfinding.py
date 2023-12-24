# test_pathfinding.py
import unittest
from src.utils import pathfinding
import time

class TestPathfinding(unittest.TestCase):
    def setUp(self):
        # Initialize a simple grid for pathfinding tests
        self.grid = self.create_grid(10, 10)  # 10x10 grid
        self.start = (0, 0)  # Starting point
        self.end = (9, 9)  # End point

    def create_grid(self, width, height, obstacles=None):
        # Create a grid with optional obstacles
        grid = [[0] * width for _ in range(height)]
        if obstacles:
            for obstacle in obstacles:
                grid[obstacle[1]][obstacle[0]] = 1  # Mark obstacle in grid
        return grid

    def test_find_path(self):
        # Test if the path is correctly found in a simple case
        path = pathfinding.find_path(self.grid, self.start, self.end)
        self.assertIsNotNone(path, "Path should be found in an obstacle-free grid")

    def test_no_path_scenario(self):
        # Add an obstacle that blocks the path completely
        obstacles = [(i, 0) for i in range(1, 10)]
        self.grid = self.create_grid(10, 10, obstacles)
        path = pathfinding.find_path(self.grid, self.start, self.end)
        self.assertIsNone(path, "No path should be found when the destination is completely blocked")

    def test_performance_on_large_grid(self):
        large_grid = self.create_grid(100, 100)  # 100x100 grid
        # Measure the time taken to find a path
        start_time = time.time()
        pathfinding.find_path(large_grid, self.start, self.end)
        end_time = time.time()
        self.assertLess(end_time - start_time, 1, "Pathfinding should complete within a reasonable time")

    def test_path_optimality(self):
        # Assuming a direct line is the shortest path in an obstacle-free grid
        path = pathfinding.find_path(self.grid, self.start, self.end)
        expected_length = 18  # Expected steps in the path
        self.assertEqual(len(path), expected_length, "Path should be the shortest possible")

    def test_dynamic_obstacles(self):
        # Simulate an obstacle appearing on the previously found path
        path = pathfinding.find_path(self.grid, self.start, self.end)
        self.grid[path[1][1]][path[1][0]] = 1  # Add obstacle to the second step in the path
        new_path = pathfinding.find_path(self.grid, self.start, self.end)
        self.assertNotEqual(path, new_path, "New path should be different after an obstacle appears")

    def tearDown(self):
        # Reset the grid to avoid interference between tests
        self.grid = None

# Additional test methods for other functionalities related to pathfinding

if __name__ == '__main__':
    unittest.main()
