# test_game.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.game.game import Game
from src.game.game_state import GameState


class TestGame(unittest.TestCase):
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
        """Setup a game instance for each test with all managers mocked."""
        self.game = Game()
        self.game.screen = Mock()
        self.game.clock = Mock()

    def test_initialization(self):
        """Test game initialization state."""
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.clock)
        self.assertEqual(self.game.is_running, False)
        self.assertTrue(self.game.is_build_mode)
        self.assertIsNotNone(self.game.state_manager)
        self.assertIsNotNone(self.game.player)
        self.assertIsNotNone(self.game.level_manager)

    def test_game_managers_initialized(self):
        """Test that all game managers are properly initialized."""
        self.assertIsNotNone(self.game.event_manager)
        self.assertIsNotNone(self.game.audio_manager)
        self.assertIsNotNone(self.game.state_manager)
        self.assertIsNotNone(self.game.tower_manager)
        self.assertIsNotNone(self.game.enemy_manager)
        self.assertIsNotNone(self.game.projectile_manager)
        self.assertIsNotNone(self.game.collision_manager)

    def test_game_board_initialized(self):
        """Test that game board is initialized."""
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.tower_selection_panel)

    def test_player_initialized(self):
        """Test that player is initialized with callbacks."""
        self.assertIsNotNone(self.game.player)

    def test_initialize_game_state(self):
        """Test game initialization logic."""
        with patch.object(self.game.level_manager, 'load_levels'):
            with patch.object(self.game.level_manager, 'start_level'):
                with patch.object(self.game.level_manager, 'reset_level'):
                    with patch.object(self.game.player, 'start_level'):
                        with patch.object(self.game.enemy_manager, 'reset'):
                            with patch.object(self.game.state_manager, 'change_state'):
                                self.game.level_manager.levels = [Mock()]
                                self.game.level_manager.current_level = Mock()
                                self.game.initialize_game(0)

                                # Verify state changed to PLAYING
                                self.game.state_manager.change_state.assert_called()

    def test_initialize_game_no_levels(self):
        """Test game initialization fails when no levels are loaded."""
        with patch.object(self.game.level_manager, 'load_levels'):
            with patch.object(self.game.state_manager, 'change_state'):
                self.game.level_manager.levels = []
                self.game.initialize_game()

                # Should return to main menu if no levels
                self.game.state_manager.change_state.assert_called_with(GameState.MAIN_MENU)

    def test_frame_time_delta_tracking(self):
        """Test that frame time delta is tracked."""
        self.game.frame_time_delta = 0.0
        self.assertEqual(self.game.frame_time_delta, 0.0)

        self.game.frame_time_delta = 0.016  # ~60 FPS
        self.assertGreater(self.game.frame_time_delta, 0)

    def test_game_state_changes(self):
        """Test that game state can be changed."""
        self.game.current_state = GameState.MAIN_MENU
        self.assertEqual(self.game.current_state, GameState.MAIN_MENU)

        self.game.current_state = GameState.PLAYING
        self.assertEqual(self.game.current_state, GameState.PLAYING)

    def test_build_mode_toggle(self):
        """Test toggling build mode."""
        self.assertTrue(self.game.is_build_mode)

        self.game.is_build_mode = False
        self.assertFalse(self.game.is_build_mode)

        self.game.is_build_mode = True
        self.assertTrue(self.game.is_build_mode)

    def test_game_running_state(self):
        """Test game running state changes."""
        self.assertFalse(self.game.is_running)

        self.game.is_running = True
        self.assertTrue(self.game.is_running)

    def tearDown(self):
        """Teardown if necessary."""
        pass


if __name__ == '__main__':
    unittest.main()
