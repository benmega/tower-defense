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

    project_directory = project_directory + "/assets"
    print_directory_structure(project_directory)

# Define the base path for the tests directory
base_path = "/"


main()


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