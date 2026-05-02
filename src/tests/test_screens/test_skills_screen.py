import sys
import types
import unittest


class _FakeButton:
    def __init__(self, relative_rect=None, text="", manager=None, tool_tip_text=None, visible=False):
        self.relative_rect = relative_rect
        self.text = text
        self.manager = manager
        self.tool_tip_text = tool_tip_text
        self.visible = visible

    def set_text(self, text):
        self.text = text


class _FakeLabel(_FakeButton):
    pass


pygame_stub = types.ModuleType("pygame")
pygame_stub.Rect = lambda pos, size: (pos, size)
sys.modules.setdefault("pygame", pygame_stub)

pygame_gui_stub = types.ModuleType("pygame_gui")
pygame_gui_stub.elements = types.SimpleNamespace(UIButton=_FakeButton, UILabel=_FakeLabel)
sys.modules.setdefault("pygame_gui", pygame_gui_stub)

pygame_gui_elements_module = types.ModuleType("pygame_gui.elements")
pygame_gui_elements_module.UIButton = _FakeButton
pygame_gui_elements_module.UILabel = _FakeLabel
sys.modules.setdefault("pygame_gui.elements", pygame_gui_elements_module)

pygame_gui_tooltip_module = types.ModuleType("pygame_gui.elements.ui_tool_tip")
pygame_gui_tooltip_module.UITooltip = object
sys.modules.setdefault("pygame_gui.elements.ui_tool_tip", pygame_gui_tooltip_module)

from src.screens import screen as screen_module
from src.screens.skills_screen import SkillsScreen, all_skills


class _FakePlayer:
    def __init__(self):
        self.points = 10
        self.skills = {}
        self.last_upgraded_skill = None

    def can_upgrade_skill(self, _skill_key):
        return True

    def upgrade_skill(self, skill_key):
        self.last_upgraded_skill = skill_key
        self.skills[skill_key] = self.skills.get(skill_key, 0) + 1
        self.points -= 1


class _FakeStateManager:
    def __init__(self):
        self.calls = []

    def change_state(self, *args):
        self.calls.append(args)


class _FakeGame:
    def __init__(self, player):
        self.player = player
        self.state_manager = _FakeStateManager()
        self.previous_state = object()


class TestSkillsScreen(unittest.TestCase):
    def setUp(self):
        screen_module.load_scaled_image = lambda _path, _size: None
        self.player = _FakePlayer()
        self.skills_screen = SkillsScreen(ui_manager=object(), player=self.player)

    def test_initialize_skill_buttons_registers_all_buttons(self):
        self.assertEqual(len(self.skills_screen.skill_buttons), len(all_skills))

    def test_initialize_skill_buttons_rebuilds_without_duplicates(self):
        self.skills_screen.initialize_skill_buttons()
        self.assertEqual(len(self.skills_screen.skill_buttons), len(all_skills))

    def test_on_button_pressed_triggers_upgrade_for_skill_button(self):
        game = _FakeGame(self.player)
        first_button = self.skills_screen.skill_buttons[0]

        self.skills_screen.on_button_pressed(first_button, game)

        first_skill_key = list(all_skills.keys())[0]
        self.assertEqual(self.player.last_upgraded_skill, first_skill_key)


if __name__ == "__main__":
    unittest.main()
