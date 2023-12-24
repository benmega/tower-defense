import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
    else:
        print(f"Directory already exists: {path}")

def create_file(path):
    with open(path, 'w') as file:
        pass
    print(f"File created: {path}")

import os

def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

def main():
    # Replace 'your_project_directory_path' with the path to your project directory
    project_directory =  os.getcwd()


    print_directory_structure(project_directory)

import os

# Define the structure of the tests directory
tests_structure = {
    "tests": {
        "conftest.py": None,
        "test_entities": {
            "test_towers.py": None,
            "test_enemies.py": None,
            "test_projectiles.py": None
        },
        "test_game_logic": {
            "test_game.py": None,
            "test_level.py": None,
            "test_tower_manager.py": None
        },
        "test_utils": {
            "test_helpers.py": None,
            "test_pathfinding.py": None
        },
        "test_board": {
            "test_game_board.py": None,
            "test_board_layout.py": None
        },
        "integration_tests": {
            "test_game_flow.py": None,
            "test_enemy_wave_integration.py": None
        }
    }
}

def create_directory_structure(base_path, structure):
    """ Recursively creates a directory structure with files """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if content is None:  # If it's a file
            open(path, 'w').close()  # Create an empty file
        else:
            os.makedirs(path, exist_ok=True)
            create_directory_structure(path, content)  # Recursively create subdirectories and files

# Define the base path for the tests directory
base_path = "/src/tests"

# Create the directory structure
create_directory_structure(base_path, tests_structure)

f"Created tests directory structure at '{base_path}'"




current_structure = '''
towerDefense/
├── assets/                  # All game assets like images, sounds, etc.
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
├── src/                     # Source code directory
│   ├── main.py              # Main game file to start the game
│   │
│   ├── game/                # Core game logic
│   │   ├── game.py          # Main game class
│   │   └── game_state.py    # GameState class to manage game states
│   │
│   ├── managers/            # Different manager classes
│   │   ├── asset_manager.py
│   │   ├── audio_manager.py
│   │   ├── collision_manager.py
│   │   ├── event_manager.py
│   │   ├── input_manager.py
│   │   ├── scene_manager.py
│   │   ├── ui_manager.py
│   │   └── ai_manager.py
│   │
│   ├── entities/            # Game entities like towers, enemies, etc.
│   │   ├── towers/
│   │   │   └── tower.py
│   │   ├── enemies/
│   │   │   └── enemy.py
│   │   └── projectiles/
│   │       └── projectile.py
│   │
│   ├── ui/                  # UI components like buttons, menus
│   │   └── hud.py
│   │
│   ├── utils/               # Utility functions and classes
│   │   └── helpers.py
│   │
│   └── physics/             # Physics and collision logic
│       └── physics_engine.py
│
├── tests/                   # Unit tests and other tests
│
├── venv/                    # Virtual environment for dependencies
│
└── README.md                # Project documentation

'''