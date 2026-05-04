"""
Centralized pytest configuration and shared fixtures for tower defense tests.
"""

<<<<<<< HEAD:src/tests/conftest.py
import sys
import types
from unittest.mock import Mock, MagicMock

import pytest

=======
class TestPathfinding(unittest.TestCase):
    def test_find_path(self):
        # Test the find_path function
        # TODO: Set up various grid layouts with and without obstacles
        # Test if the path is correctly found in each case
        pass

    def test_no_path_scenario(self):
        # Test scenarios where no path is available
        # TODO: Create grid layouts where no path is possible
        # Ensure the pathfinding algorithm correctly identifies these scenarios
        pass

    def test_performance_on_large_grid(self):
        # Test the pathfinding performance on a large grid
        # TODO: Create a large grid and measure the time taken to find a path
        # Consider setting a reasonable time limit for pathfinding
        pass
>>>>>>> claude/great-franklin-30172d:src/tests.disabled/conftest.py

# === PYGAME MOCKING ===
# Set up minimal pygame stubs before any imports that depend on pygame


def setup_pygame_mocks():
    """Create and register minimal pygame and pygame_gui mocks."""
    # Create pygame mock
    pygame_mock = types.ModuleType("pygame")
    pygame_mock.QUIT = 12
    pygame_mock.KEYDOWN = 2
    pygame_mock.KEYUP = 3
    pygame_mock.MOUSEBUTTONDOWN = 5
    pygame_mock.MOUSEBUTTONUP = 6
    pygame_mock.event = MagicMock()
    pygame_mock.event.get = MagicMock(return_value=[])
    pygame_mock.display = MagicMock()
    pygame_mock.display.set_caption = MagicMock()
    pygame_mock.display.set_mode = MagicMock()
    pygame_mock.Surface = MagicMock()
    pygame_mock.Rect = types.SimpleNamespace(
        colliderect=lambda self, other: False,
        collidepoint=lambda self, point: False,
    )
    pygame_mock.transform = MagicMock()
    pygame_mock.transform.scale = MagicMock(return_value=MagicMock())
    pygame_mock.time = MagicMock()
    pygame_mock.time.Clock = MagicMock
    pygame_mock.draw = MagicMock()
    pygame_mock.image = MagicMock()
    pygame_mock.image.load = MagicMock(return_value=MagicMock())
    pygame_mock.mixer = MagicMock()
    pygame_mock.mixer.Sound = MagicMock()
    pygame_mock.mixer.music = MagicMock()

    sys.modules["pygame"] = pygame_mock

    # Create pygame_gui mock
    pygame_gui_stub = types.ModuleType("pygame_gui")
    pygame_gui_stub.elements = types.SimpleNamespace(
        UIButton=MagicMock,
        UIPanel=MagicMock,
        UILabel=MagicMock,
        UIImage=MagicMock,
        UITextEntryLine=MagicMock,
    )
    pygame_gui_stub.core = types.SimpleNamespace(ObjectID=str)
    pygame_gui_stub.UIManager = MagicMock
    pygame_gui_stub.windows = types.SimpleNamespace(UIMessageWindow=MagicMock)

    sys.modules["pygame_gui"] = pygame_gui_stub


# Register mocks before any test collection
setup_pygame_mocks()


# === PYTEST FIXTURES ===


@pytest.fixture
def mock_pygame():
    """Provide access to the mocked pygame module."""
    return sys.modules.get("pygame")


@pytest.fixture
def mock_clock():
    """Create a mock game clock."""
    clock = Mock()
    clock.tick = Mock(return_value=16)  # ~60 FPS
    clock.get_time = Mock(return_value=16)
    return clock


@pytest.fixture
def mock_display():
    """Create a mock pygame display."""
    display = Mock()
    display.get_size = Mock(return_value=(1200, 800))
    display.get_width = Mock(return_value=1200)
    display.get_height = Mock(return_value=800)
    return display


@pytest.fixture
def mock_rect():
    """Create a mock pygame rect."""
    rect = Mock()
    rect.x = 0
    rect.y = 0
    rect.width = 50
    rect.height = 50
    rect.left = 0
    rect.right = 50
    rect.top = 0
    rect.bottom = 50
    rect.centerx = 25
    rect.centery = 25
    rect.colliderect = Mock(return_value=False)
    rect.collidepoint = Mock(return_value=False)
    return rect


@pytest.fixture
def mock_surface():
    """Create a mock pygame surface."""
    surface = Mock()
    surface.get_width = Mock(return_value=1200)
    surface.get_height = Mock(return_value=800)
    surface.get_size = Mock(return_value=(1200, 800))
    surface.fill = Mock()
    surface.blit = Mock()
    surface.copy = Mock(return_value=surface)
    return surface


# === GAME OBJECT FACTORIES ===


class TowerFactory:
    """Factory for creating test towers with custom properties."""

    @staticmethod
    def create(
        x=50,
        y=50,
        attack_range=100,
        damage=10,
        attack_speed=1.0,
        **kwargs
    ):
        """Create a Tower with the given properties."""
        from src.entities.towers.tower import Tower

        tower = Mock(spec=Tower)
        tower.x = x
        tower.y = y
        tower.attack_range = attack_range
        tower.damage = damage
        tower.attack_speed = attack_speed
        tower.cooldown = 0
        tower.is_enemy_in_range = Mock(return_value=False)
        tower.attack = Mock()
        tower.update = Mock()
        tower.take_damage = Mock()

        for key, value in kwargs.items():
            setattr(tower, key, value)

        return tower


class EnemyFactory:
    """Factory for creating test enemies with custom properties."""

    @staticmethod
    def create(
        x=100,
        y=100,
        health=20,
        max_health=20,
        speed=2.0,
        path=None,
        **kwargs
    ):
        """Create an Enemy with the given properties."""
        from src.entities.enemies.enemy import Enemy

        enemy = Mock(spec=Enemy)
        enemy.x = x
        enemy.y = y
        enemy.health = health
        enemy.max_health = max_health
        enemy.speed = speed
        enemy.path = path or []
        enemy.path_index = 0
        enemy.is_alive = Mock(return_value=health > 0)
        enemy.take_damage = Mock()
        enemy.move = Mock()
        enemy.apply_slow_effect = Mock()
        enemy.apply_poison_effect = Mock()
        enemy.update = Mock()

        for key, value in kwargs.items():
            setattr(enemy, key, value)

        return enemy


class ProjectileFactory:
    """Factory for creating test projectiles."""

    @staticmethod
    def create(x=50, y=50, speed=5.0, damage=10, target=None, **kwargs):
        """Create a Projectile with the given properties."""
        from src.entities.projectiles.projectile import Projectile

        projectile = Mock(spec=Projectile)
        projectile.x = x
        projectile.y = y
        projectile.speed = speed
        projectile.damage = damage
        projectile.target = target or Mock()
        projectile.is_active = Mock(return_value=True)
        projectile.move = Mock()
        projectile.reached_target = Mock(return_value=False)
        projectile.hit_target = Mock()
        projectile.update = Mock()

        for key, value in kwargs.items():
            setattr(projectile, key, value)

        return projectile


class PlayerFactory:
    """Factory for creating test player objects."""

    @staticmethod
    def create(gold=100, health=20, score=0, **kwargs):
        """Create a Player with the given properties."""
        from src.entities.Player import Player

        player = Mock(spec=Player)
        player.gold = gold
        player.health = health
        player.score = score
        player.add_gold = Mock()
        player.spend_gold = Mock(return_value=True)
        player.take_damage = Mock()
        player.restore_health = Mock()
        player.add_score = Mock()
        player.is_alive = Mock(return_value=health > 0)

        for key, value in kwargs.items():
            setattr(player, key, value)

        return player


@pytest.fixture
def tower_factory():
    """Provide the tower factory."""
    return TowerFactory


@pytest.fixture
def enemy_factory():
    """Provide the enemy factory."""
    return EnemyFactory


@pytest.fixture
def projectile_factory():
    """Provide the projectile factory."""
    return ProjectileFactory


@pytest.fixture
def player_factory():
    """Provide the player factory."""
    return PlayerFactory


# === COMMON TEST OBJECTS ===


@pytest.fixture
def basic_tower(tower_factory):
    """Create a basic tower for tests."""
    return tower_factory.create(x=50, y=50, attack_range=100, damage=10)


@pytest.fixture
def basic_enemy(enemy_factory):
    """Create a basic enemy for tests."""
    return enemy_factory.create(x=100, y=100, health=20, speed=2.0)


@pytest.fixture
def basic_player(player_factory):
    """Create a basic player for tests."""
    return player_factory.create(gold=100, health=20, score=0)


# === GAME STATE FIXTURES ===


@pytest.fixture
def mock_game_state():
    """Create a mock game state."""
    from src.game.game_state import GameState

    state = Mock()
    state.current_state = GameState.PLAYING
    state.previous_state = GameState.MAIN_MENU
    state.change_state = Mock()
    return state


@pytest.fixture
def mock_level():
    """Create a mock level."""
    level = Mock()
    level.level_id = 0
    level.waves = []
    level.active_waves = []
    level.is_completed = Mock(return_value=False)
    level.update_level = Mock(return_value=[])
    level.get_next_wave = Mock(return_value=None)
    return level


# === MANAGER FIXTURES ===


@pytest.fixture
def mock_entity_manager():
    """Create a mock entity manager."""
    manager = Mock()
    manager.entities = []
    manager.add = Mock()
    manager.remove = Mock()
    manager.update_entities = Mock()
    manager.draw = Mock()
    return manager


@pytest.fixture
def mock_collision_manager():
    """Create a mock collision manager."""
    manager = Mock()
    manager.check_collision = Mock(return_value=False)
    manager.resolve_collision = Mock()
    manager.handle_group_collisions = Mock()
    return manager


# === MARKERS ===


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
