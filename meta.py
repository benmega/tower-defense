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

def main():
    base_path = 'entities'

    # Directories and subdirectories
    directories = [
        base_path,
        os.path.join(base_path, 'towers'),
        os.path.join(base_path, 'enemies'),
        os.path.join(base_path, 'projectiles'),
        os.path.join(base_path, 'gems'),
        os.path.join(base_path, 'power_ups'),
        os.path.join(base_path, 'obstacles')
    ]

    # Files in each directory
    files = [
        os.path.join(base_path, '__init__.py'),
        os.path.join(base_path, 'entity.py'),
        os.path.join(base_path, 'movable_entity.py'),
        os.path.join(base_path, 'towers', 'tower.py'),
        os.path.join(base_path, 'enemies', 'enemy.py'),
        os.path.join(base_path, 'projectiles', 'projectile.py'),
        os.path.join(base_path, 'gems', 'gem.py'),
        os.path.join(base_path, 'power_ups', 'power_up.py'),
        os.path.join(base_path, 'obstacles', 'obstacle.py')
    ]

    # Creating directories
    for directory in directories:
        create_directory(directory)

    # Creating files
    for file in files:
        create_file(file)

if __name__ == "__main__":
    main()
