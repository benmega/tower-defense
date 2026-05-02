import sys
import types

# Provide a tiny pygame_gui stub for module imports in test envs.
pygame_gui_stub = types.ModuleType("pygame_gui")
pygame_gui_stub.elements = types.SimpleNamespace(UIButton=object)
pygame_gui_stub.core = types.SimpleNamespace(ObjectID=object)
sys.modules.setdefault("pygame_gui", pygame_gui_stub)

from src.managers.enemy_manager import EnemyManager
from src.managers.level_manager import LevelManager


class _DummyLevel:
    def __init__(self, spawn_payload, completed=False):
        self._spawn_payload = spawn_payload
        self._completed = completed

    def update_level(self, _current_time):
        return self._spawn_payload

    def is_completed(self):
        return self._completed


class _DummyLevelManagerRef:
    def __init__(self):
        self.current_level = type("CurrentLevel", (), {"active_waves": []})()


class _WaveThatMustNotRun:
    def __init__(self):
        self.update_calls = 0

    def update(self, _current_time):
        self.update_calls += 1
        return []


def test_level_manager_update_levels_returns_flat_list():
    level_manager = LevelManager.__new__(LevelManager)
    level_manager.start_next_level = lambda: None
    level_manager.get_current_level = lambda: _DummyLevel(["enemy_a", "enemy_b"])

    result = LevelManager.update_levels(level_manager)

    assert result == ["enemy_a", "enemy_b"]


def test_level_manager_update_levels_wraps_non_list_payload():
    level_manager = LevelManager.__new__(LevelManager)
    level_manager.start_next_level = lambda: None
    level_manager.get_current_level = lambda: _DummyLevel("enemy_a")

    result = LevelManager.update_levels(level_manager)

    assert result == ["enemy_a"]


def test_enemy_manager_update_does_not_spawn_from_waves():
    level_manager_ref = _DummyLevelManagerRef()
    blocked_wave = _WaveThatMustNotRun()
    level_manager_ref.current_level.active_waves.append(blocked_wave)

    enemy_manager = EnemyManager(level_manager_ref)
    enemy_manager.update()

    assert blocked_wave.update_calls == 0
