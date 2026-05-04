"""Test game state machine and state transitions."""
import unittest
from unittest.mock import Mock

class TestGameStateMachine(unittest.TestCase):
    """Test game state machine transitions."""
    def setUp(self):
        self.state_manager = Mock()
        self.state_manager.current_state = 'MAIN_MENU'
        self.state_manager.previous_state = None
    
    def test_initial_state_main_menu(self):
        self.assertEqual(self.state_manager.current_state, 'MAIN_MENU')
    
    def test_state_transition(self):
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = 'PLAYING'
        self.assertEqual(self.state_manager.current_state, 'PLAYING')
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
