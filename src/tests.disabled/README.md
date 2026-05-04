# Tower Defense Testing Guide

This directory contains the comprehensive test suite for the Tower Defense game. The test infrastructure is set up for enterprise-grade testing with proper coverage tracking, code quality checks, and CI/CD integration.

## Quick Start

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest src/tests/test_game_logic/test_game.py

# Run tests matching a pattern
pytest -k "test_tower" -v

# Run with parallel execution (faster)
pytest -n auto
```

### Checking Code Quality

```bash
# Format code with black
black src/

# Check code style
flake8 src/

# Type checking with mypy
mypy src/ --ignore-missing-imports

# All-in-one quality check
pre-commit run --all-files
```

## Test Structure

```
src/tests/
├── conftest.py                          # Shared fixtures and mocks
├── test_board/                          # Board layout and rendering tests
│   ├── test_board_layout.py
│   └── test_game_board.py
├── test_entities/                       # Entity tests
│   ├── test_player.py                   # Player resource management
│   ├── enemies/
│   │   ├── test_basic_enemy.py
│   │   ├── test_enemy_wave.py
│   │   └── test_enemy_pathfinding.py    # Enemy AI and movement
│   ├── projectiles/
│   │   └── test_projectile.py
│   └── towers/
│       ├── test_tower.py
│       └── test_tower_targeting.py      # Tower attack mechanics
├── test_game_logic/                     # Game systems
│   ├── test_game.py
│   ├── test_level.py
│   ├── test_tower_manager.py
│   ├── test_game_state_machine.py       # State transitions
│   ├── test_collision_damage.py         # Collision detection
│   ├── test_wave_timing.py              # Wave spawning
│   └── test_spawn_pipeline.py
├── test_managers/
│   └── test_event_manager.py
├── test_screens/
│   └── test_skills_screen.py
├── test_utils/
│   ├── test_helpers.py
│   └── test_pathfinding.py
└── utils/
    └── test_factories.py                # Object factories for tests
```

## Test Categories

### Unit Tests

Tests for individual components in isolation:

- **Entity Tests**: Tower, Enemy, Projectile, Player behavior
- **Manager Tests**: TowerManager, EnemyManager, CollisionManager, etc.
- **Utility Tests**: Helper functions, pathfinding algorithms
- **Logic Tests**: Game state machine, level progression

### Integration Tests

Tests for interactions between multiple systems:

- **Game Flow Tests**: Complete game scenarios (start → play → end)
- **Wave Integration**: Enemy spawning and wave progression
- **Collision System**: Projectiles hitting enemies and damage application

## Writing Tests

### Using Fixtures

The `conftest.py` provides ready-to-use fixtures for common test objects:

```python
def test_tower_attack(basic_tower, basic_enemy):
    """Test tower attacks enemy using fixtures."""
    # basic_tower and basic_enemy are pre-configured Mock objects
    assert basic_tower.damage == 10
    assert basic_enemy.health == 20
```

### Using Factories

Object factories create test objects with customizable properties:

```python
from src.tests.utils.test_factories import TowerFactory, EnemyFactory

def test_tower_targeting():
    """Create custom test objects with factories."""
    tower = TowerFactory.create(damage=20, attack_range=150)
    enemy = EnemyFactory.create_fast(speed=4.0)
    
    assert tower.damage == 20
    assert enemy.speed == 4.0
```

### Mocking

Use `unittest.mock` for dependencies:

```python
from unittest.mock import Mock, patch

def test_game_initialization():
    """Test with mocked dependencies."""
    with patch('src.game.pygame.display.set_mode'):
        game = Game()
        assert game.is_running == False
```

### Example Test

```python
import unittest
from unittest.mock import Mock
from src.tests.utils.test_factories import TowerFactory, EnemyFactory

class TestTowerDamage(unittest.TestCase):
    """Test tower damage system."""
    
    def test_tower_damages_enemy(self):
        """Test that tower damage reduces enemy health."""
        tower = TowerFactory.create(damage=15)
        enemy = EnemyFactory.create(health=50)
        
        # Apply damage
        enemy.health -= tower.damage
        
        # Verify
        self.assertEqual(enemy.health, 35)
    
    def test_enemy_dies_on_lethal_damage(self):
        """Test that enemy dies when health reaches 0."""
        tower = TowerFactory.create(damage=50)
        enemy = EnemyFactory.create(health=50)
        
        enemy.health -= tower.damage
        is_dead = enemy.health <= 0
        
        self.assertTrue(is_dead)
```

## Available Fixtures

### Core Fixtures

- `mock_pygame`: Access to mocked pygame module
- `mock_clock`: Game clock mock
- `mock_display`: Pygame display mock
- `mock_surface`: Pygame surface mock
- `mock_rect`: Pygame rect mock

### Game Object Fixtures

- `basic_tower`: Pre-configured tower mock
- `basic_enemy`: Pre-configured enemy mock
- `basic_player`: Pre-configured player mock

### Manager Fixtures

- `mock_entity_manager`: EntityManager mock
- `mock_collision_manager`: CollisionManager mock
- `mock_game_state`: GameState mock
- `mock_level`: Level mock

### Factories

- `tower_factory`: TowerFactory for creating test towers
- `enemy_factory`: EnemyFactory for creating test enemies
- `projectile_factory`: ProjectileFactory for test projectiles
- `player_factory`: PlayerFactory for test players

## Coverage Goals

Target coverage metrics for each module:

| Module | Target | Current |
|--------|--------|---------|
| Game Logic | 85% | ![progress bar] |
| Entity Systems | 80% | ![progress bar] |
| Managers | 75% | ![progress bar] |
| UI/Screens | 60% | ![progress bar] |
| Utils | 90% | ![progress bar] |
| **Overall** | **80%** | ![progress bar] |

View detailed coverage report:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Test Markers

Run tests with specific markers:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run with marker info
pytest --markers
```

Available markers:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow/long-running tests

## CI/CD Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

Results reported via GitHub Actions (`.github/workflows/tests.yml`):
- ✅ Tests passing on Python 3.8-3.11
- ✅ Code quality checks (flake8, black, mypy)
- ✅ Coverage tracking with codecov
- ✅ All checks must pass before merging PR

## Code Quality Standards

### Black (Code Formatting)

```bash
black src/
```

### Flake8 (Linting)

```bash
flake8 src/ --max-line-length=100
```

Max line length: 100 characters

### MyPy (Type Checking)

```bash
mypy src/ --ignore-missing-imports
```

### Pre-commit Hooks

Auto-format and check on commit:

```bash
pre-commit install
pre-commit run --all-files
```

## Common Testing Patterns

### Testing Tower Attacks

```python
def test_tower_attack_damage():
    tower = TowerFactory.create(damage=20)
    enemy = EnemyFactory.create(health=50)
    
    enemy.health -= tower.damage
    
    assert enemy.health == 30
    assert not (enemy.health <= 0)
```

### Testing Enemy Movement

```python
def test_enemy_moves_along_path():
    enemy = EnemyFactory.create(x=0, y=0, speed=2.0)
    target = (100, 0)
    
    # Move 10 frames at ~60 FPS = 0.167 seconds
    for _ in range(10):
        # Simulate movement logic
        enemy.x += enemy.speed * 0.016
    
    assert enemy.x > 0
```

### Testing Collisions

```python
def test_projectile_hits_enemy():
    projectile = ProjectileFactory.create(x=100, y=100, damage=20)
    enemy = EnemyFactory.create(x=100, y=100, health=50)
    
    distance = 0  # Same position = collision
    
    if distance < 20:  # collision radius
        enemy.health -= projectile.damage
    
    assert enemy.health == 30
```

### Testing State Transitions

```python
def test_game_state_transition():
    state_manager = Mock()
    state_manager.current_state = GameState.MAIN_MENU
    
    state_manager.current_state = GameState.PLAYING
    
    assert state_manager.current_state == GameState.PLAYING
```

## Troubleshooting

### Import Errors

If you see pygame import errors, ensure `conftest.py` mocks are loaded first:

```python
# conftest.py should be in src/tests/
# Tests should be in subdirectories: src/tests/test_*
```

### Test Discovery

Pytest automatically discovers tests matching:
- Files: `test_*.py` or `*_test.py`
- Classes: `Test*`
- Functions: `test_*`

### Fixture Scope

Fixtures have different scopes:
- `scope="function"` (default): Created/destroyed per test
- `scope="class"`: Created/destroyed per class
- `scope="module"`: Created/destroyed per module
- `scope="session"`: Created once per test session

## Performance Optimization

### Run tests in parallel

```bash
pip install pytest-xdist
pytest -n auto  # Use all available CPU cores
```

### Run only changed tests

```bash
pytest --lf  # Last failed
pytest --ff  # Failed first
```

### Profile slow tests

```bash
pytest --durations=10  # Show 10 slowest tests
```

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov=src`
4. Format code: `black src/`
5. Run quality checks: `flake8 src/`
6. Commit with tests included

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Black Code Formatter](https://github.com/psf/black)
- [Flake8 Linter](https://flake8.pycqa.org/)

## Questions?

For questions about testing, check the game wiki or create an issue.

---

**Last Updated**: 2026-05-04  
**Test Framework**: pytest 7.0+  
**Python Version**: 3.8+
