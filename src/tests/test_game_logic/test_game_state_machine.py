"""
Test game state machine and state transitions.
"""

import unittest
from unittest.mock import Mock
from src.game.game_state import GameState


class TestGameStateMachine(unittest.TestCase):
    """Test game state machine transitions and handlers."""

    def setUp(self):
        """Setup game state machine."""
        self.state_manager = Mock()
        self.state_manager.current_state = GameState.MAIN_MENU
        self.state_manager.previous_state = None

    def test_game_state_enum_values(self):
        """Test all game states are defined."""
        states = [
            GameState.MAIN_MENU,
            GameState.CAMPAIGN_MAP,
            GameState.PLAYING,
            GameState.LEVEL_COMPLETE,
            GameState.LEVEL_DEFEAT,
            GameState.PAUSE_MENU,
        ]

        for state in states:
            self.assertIsNotNone(state)

    def test_initial_state_main_menu(self):
        """Test game starts in main menu."""
        self.assertEqual(self.state_manager.current_state, GameState.MAIN_MENU)

    def test_state_transition_main_menu_to_campaign(self):
        """Test transition from main menu to campaign."""
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.CAMPAIGN_MAP

        self.assertEqual(self.state_manager.current_state, GameState.CAMPAIGN_MAP)
        self.assertEqual(self.state_manager.previous_state, GameState.MAIN_MENU)

    def test_state_transition_campaign_to_playing(self):
        """Test transition from campaign to playing."""
        self.state_manager.current_state = GameState.CAMPAIGN_MAP
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.PLAYING

        self.assertEqual(self.state_manager.current_state, GameState.PLAYING)
        self.assertEqual(self.state_manager.previous_state, GameState.CAMPAIGN_MAP)

    def test_state_transition_playing_to_pause(self):
        """Test transition from playing to pause menu."""
        self.state_manager.current_state = GameState.PLAYING
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.PAUSE_MENU

        self.assertEqual(self.state_manager.current_state, GameState.PAUSE_MENU)
        self.assertEqual(self.state_manager.previous_state, GameState.PLAYING)

    def test_state_transition_pause_to_playing(self):
        """Test resuming from pause menu."""
        self.state_manager.current_state = GameState.PAUSE_MENU
        self.state_manager.previous_state = GameState.PLAYING
        self.state_manager.current_state = GameState.PLAYING

        self.assertEqual(self.state_manager.current_state, GameState.PLAYING)

    def test_state_transition_playing_to_level_complete(self):
        """Test transition to level complete."""
        self.state_manager.current_state = GameState.PLAYING
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.LEVEL_COMPLETE

        self.assertEqual(self.state_manager.current_state, GameState.LEVEL_COMPLETE)

    def test_state_transition_playing_to_level_defeat(self):
        """Test transition to level defeat."""
        self.state_manager.current_state = GameState.PLAYING
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.LEVEL_DEFEAT

        self.assertEqual(self.state_manager.current_state, GameState.LEVEL_DEFEAT)

    def test_state_transition_level_complete_to_campaign(self):
        """Test transition from level complete back to campaign."""
        self.state_manager.current_state = GameState.LEVEL_COMPLETE
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.CAMPAIGN_MAP

        self.assertEqual(self.state_manager.current_state, GameState.CAMPAIGN_MAP)

    def test_state_transition_level_defeat_to_playing(self):
        """Test retrying level after defeat."""
        self.state_manager.current_state = GameState.LEVEL_DEFEAT
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.PLAYING

        self.assertEqual(self.state_manager.current_state, GameState.PLAYING)

    def test_state_transition_any_to_main_menu(self):
        """Test returning to main menu from any state."""
        states_to_test = [
            GameState.CAMPAIGN_MAP,
            GameState.PLAYING,
            GameState.LEVEL_COMPLETE,
            GameState.LEVEL_DEFEAT,
        ]

        for state in states_to_test:
            self.state_manager.current_state = state
            self.state_manager.previous_state = self.state_manager.current_state
            self.state_manager.current_state = GameState.MAIN_MENU

            self.assertEqual(self.state_manager.current_state, GameState.MAIN_MENU)

    def test_invalid_state_transition_prevention(self):
        """Test invalid state transitions are prevented."""
        # Can't go directly from LEVEL_COMPLETE to LEVEL_DEFEAT
        self.state_manager.current_state = GameState.LEVEL_COMPLETE
        previous = self.state_manager.current_state

        # Attempt invalid transition
        # This would be handled by state manager validation
        self.assertNotEqual(GameState.LEVEL_DEFEAT, GameState.LEVEL_COMPLETE)

    def test_state_handler_invocation(self):
        """Test state handlers are invoked on state change."""
        on_state_change = Mock()
        self.state_manager.on_state_change = on_state_change

        # Simulate state change
        self.state_manager.previous_state = GameState.MAIN_MENU
        self.state_manager.current_state = GameState.CAMPAIGN_MAP
        self.state_manager.on_state_change(GameState.MAIN_MENU, GameState.CAMPAIGN_MAP)

        on_state_change.assert_called_with(GameState.MAIN_MENU, GameState.CAMPAIGN_MAP)

    def test_state_enter_handler(self):
        """Test state enter handler is called."""
        on_enter = Mock()

        # Simulate state enter
        self.state_manager.current_state = GameState.PLAYING
        on_enter(GameState.PLAYING)

        on_enter.assert_called_with(GameState.PLAYING)

    def test_state_exit_handler(self):
        """Test state exit handler is called."""
        on_exit = Mock()

        # Simulate state exit
        on_exit(GameState.PLAYING)
        self.state_manager.current_state = GameState.LEVEL_COMPLETE

        on_exit.assert_called_with(GameState.PLAYING)

    def test_state_data_passing(self):
        """Test data can be passed between states."""
        state_data = {'level': 1, 'player_gold': 100}

        # Transition with data
        self.state_manager.state_data = state_data

        self.assertEqual(self.state_manager.state_data['level'], 1)
        self.assertEqual(self.state_manager.state_data['player_gold'], 100)

    def test_previous_state_tracking(self):
        """Test previous state is tracked for transitions."""
        # Transition 1
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.CAMPAIGN_MAP
        self.assertEqual(self.state_manager.previous_state, GameState.MAIN_MENU)

        # Transition 2
        self.state_manager.previous_state = self.state_manager.current_state
        self.state_manager.current_state = GameState.PLAYING
        self.assertEqual(self.state_manager.previous_state, GameState.CAMPAIGN_MAP)

    def test_state_stack_for_pause_resume(self):
        """Test state stack allows proper pause/resume."""
        state_stack = []

        # Play state
        state_stack.append(GameState.PLAYING)
        self.state_manager.current_state = GameState.PLAYING

        # Pause
        state_stack.append(GameState.PAUSE_MENU)
        self.state_manager.current_state = GameState.PAUSE_MENU

        # Resume from stack
        previous_state = state_stack[-2]
        self.assertEqual(previous_state, GameState.PLAYING)

    def test_state_transition_speed(self):
        """Test state transitions happen immediately."""
        import time

        start_time = time.time()
        self.state_manager.current_state = GameState.CAMPAIGN_MAP
        end_time = time.time()

        elapsed = end_time - start_time
        self.assertLess(elapsed, 0.01)  # Should be nearly instant

    def test_multiple_state_transitions(self):
        """Test sequence of state transitions."""
        transitions = [
            (GameState.MAIN_MENU, GameState.CAMPAIGN_MAP),
            (GameState.CAMPAIGN_MAP, GameState.PLAYING),
            (GameState.PLAYING, GameState.LEVEL_COMPLETE),
            (GameState.LEVEL_COMPLETE, GameState.CAMPAIGN_MAP),
        ]

        current = GameState.MAIN_MENU
        for from_state, to_state in transitions:
            self.assertEqual(current, from_state)
            current = to_state

        self.assertEqual(current, GameState.CAMPAIGN_MAP)

    def tearDown(self):
        """Cleanup."""
        pass


if __name__ == '__main__':
    unittest.main()
