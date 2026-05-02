import unittest
import types
import sys

# Keep this test independent from optional pygame_gui installation.
sys.modules.setdefault("pygame_gui", types.SimpleNamespace())
from src.managers.event_manager import EventManager


class FakeOptionsScreen:
    def __init__(self):
        self.calls = []

    def on_slider_moved(self, ui_element, value):
        self.calls.append((ui_element, value))


class FakeUIManager:
    def __init__(self):
        self.options_screen = FakeOptionsScreen()


class FakeGame:
    def __init__(self):
        self.UI_manager = FakeUIManager()


class TestEventManagerSliderDispatch(unittest.TestCase):
    def test_dispatch_slider_uses_two_argument_options_contract(self):
        manager = EventManager()
        game = FakeGame()
        slider = object()

        manager._dispatch_slider(slider, 42, game)

        self.assertEqual(game.UI_manager.options_screen.calls, [(slider, 42)])


if __name__ == "__main__":
    unittest.main()
