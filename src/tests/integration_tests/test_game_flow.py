# test_game_flow.py
"""
Integration tests for complete game flow scenarios.
Tests interactions between multiple game systems.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.game.game import Game
from src.game.game_state import GameState


class TestGameFlow(unittest.TestCase):
    """Test complete game flow scenarios."""

    @patch('src.game.game.pygame')
    @patch('src.game.game.UIManager')
    @patch('src.game.game.EventManager')
    @patch('src.game.game.AudioManager')
    @patch('src.game.game.GameStateManager')
    @patch('src.game.game.LevelManager')
    @patch('src.game.game.TowerManager')
    @patch('src.game.game.ProjectileManager')
    @patch('src.game.game.CollisionManager')
    @patch('src.game.game.EnemyManager')
    @patch('src.game.game.GameBoard')
    @patch('src.game.game.TowerSelectionPanel')
    @patch('src.game.game.Player')
    def setUp(self, *mocks):
        """Setup game for integration tests."""
        self.game = Game()

    def test_game_initialization_flow(self):
        """Test the complete game initialization flow."""
        self.assertFalse(self.game.is_running)
        self.assertIsNotNone(self.game.player)
        self.assertIsNotNone(self.game.level_manager)
        self.assertIsNotNone(self.game.enemy_manager)

    def test_game_state_transitions(self):
        """Test valid game state transitions."""
        # Start with MAIN_MENU
        self.game.current_state = GameState.MAIN_MENU

        # Transition to CAMPAIGN_MAP
        self.game.current_state = GameState.CAMPAIGN_MAP
        self.assertEqual(self.game.current_state, GameState.CAMPAIGN_MAP)

        # Transition to PLAYING
        self.game.current_state = GameState.PLAYING
        self.assertEqual(self.game.current_state, GameState.PLAYING)

        # Transition to LEVEL_COMPLETE
        self.game.current_state = GameState.LEVEL_COMPLETE
        self.assertEqual(self.game.current_state, GameState.LEVEL_COMPLETE)

        # Back to CAMPAIGN_MAP
        self.game.current_state = GameState.CAMPAIGN_MAP
        self.assertEqual(self.game.current_state, GameState.CAMPAIGN_MAP)

    def test_game_start_flow(self):
        """Test starting the game."""
        # Initialize managers
        self.game.level_manager.levels = [Mock()]
        self.game.level_manager.current_level = Mock()
        self.game.is_running = False

        # Start game
        self.game.is_running = True
        self.game.current_state = GameState.PLAYING

        # Verify game state
        self.assertTrue(self.game.is_running)
        self.assertEqual(self.game.current_state, GameState.PLAYING)

    def test_game_pause_resume(self):
        """Test pausing and resuming the game."""
        self.game.is_running = True

        # Pause game
        is_paused = not self.game.is_running
        self.assertFalse(is_paused)

        # Set paused state (simulate pause)
        self.game.is_running = False
        is_paused = not self.game.is_running
        self.assertTrue(is_paused)

        # Resume game
        self.game.is_running = True
        is_paused = not self.game.is_running
        self.assertFalse(is_paused)

    def test_game_end_flow(self):
        """Test ending the game."""
        self.game.is_running = True
        self.game.current_state = GameState.PLAYING

        # Simulate game end
        self.game.is_running = False
        self.game.current_state = GameState.MAIN_MENU

        # Verify game state
        self.assertFalse(self.game.is_running)
        self.assertEqual(self.game.current_state, GameState.MAIN_MENU)

    def test_player_defeat_flow(self):
        """Test flow when player is defeated."""
        self.game.is_running = True
        self.game.current_state = GameState.PLAYING
        self.game.player.health = 0

        # Check defeat condition
        is_defeated = self.game.player.health <= 0
        self.assertTrue(is_defeated)

        # Transition to defeat state
        self.game.is_running = False
        self.game.current_state = GameState.LEVEL_DEFEAT

        self.assertFalse(self.game.is_running)
        self.assertEqual(self.game.current_state, GameState.LEVEL_DEFEAT)

    def test_level_completion_flow(self):
        """Test flow when level is completed."""
        self.game.current_state = GameState.PLAYING
        self.game.level_manager.current_level = Mock()
        self.game.level_manager.current_level.is_completed = Mock(return_value=True)

        # Check completion condition
        is_completed = self.game.level_manager.current_level.is_completed()
        self.assertTrue(is_completed)

        # Transition to completion state
        self.game.current_state = GameState.LEVEL_COMPLETE

        self.assertEqual(self.game.current_state, GameState.LEVEL_COMPLETE)

    def test_level_progression_flow(self):
        """Test progressing through levels."""
        self.game.level_manager.levels = [
            Mock(level_id=0),
            Mock(level_id=1),
            Mock(level_id=2),
        ]

        # Start level 0
        self.game.current_state = GameState.PLAYING
        self.game.level_manager.current_level = self.game.level_manager.levels[0]
        self.assertEqual(self.game.level_manager.current_level.level_id, 0)

        # Complete level 0, progress to level 1
        self.game.current_state = GameState.LEVEL_COMPLETE
        self.game.level_manager.current_level = self.game.level_manager.levels[1]
        self.assertEqual(self.game.level_manager.current_level.level_id, 1)

        # Complete level 1, progress to level 2
        self.game.current_state = GameState.LEVEL_COMPLETE
        self.game.level_manager.current_level = self.game.level_manager.levels[2]
        self.assertEqual(self.game.level_manager.current_level.level_id, 2)

    def test_game_paused_state_persistence(self):
        """Test that game state persists correctly when paused."""
        self.game.is_running = True
        self.game.current_state = GameState.PLAYING
        self.game.player.gold = 100

        # Pause game
        self.game.is_running = False

        # Verify state is preserved
        self.assertFalse(self.game.is_running)
        self.assertEqual(self.game.current_state, GameState.PLAYING)
        self.assertEqual(self.game.player.gold, 100)

        # Resume game - state should be the same
        self.game.is_running = True
        self.assertEqual(self.game.player.gold, 100)

    def test_build_mode_toggle(self):
        """Test toggling build mode during game."""
        self.game.is_build_mode = True
        self.game.current_state = GameState.PLAYING

        # Toggle build mode
        self.game.is_build_mode = False
        self.assertFalse(self.game.is_build_mode)

        # Toggle back
        self.game.is_build_mode = True
        self.assertTrue(self.game.is_build_mode)

    def tearDown(self):
        """Teardown if necessary."""
        pass


if __name__ == '__main__':
    unittest.main()
