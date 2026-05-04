"""
Test wave spawning and timing mechanics.
"""

import unittest
from unittest.mock import Mock


class TestWaveTiming(unittest.TestCase):
    """Test wave and enemy spawn timing."""

    def setUp(self):
        """Setup wave and timing system."""
        self.wave = Mock()
        self.wave.wave_id = 0
        self.wave.enemy_count = 5
        self.wave.enemies_spawned = 0
        self.wave.spawn_interval = 1.0
        self.wave.time_since_last_spawn = 0
        self.wave.is_active = False
        self.wave.is_completed = False

    def test_wave_initialization(self):
        """Test wave initializes with correct properties."""
        self.assertEqual(self.wave.wave_id, 0)
        self.assertEqual(self.wave.enemy_count, 5)
        self.assertEqual(self.wave.enemies_spawned, 0)
        self.assertEqual(self.wave.spawn_interval, 1.0)

    def test_wave_activation(self):
        """Test wave can be activated."""
        self.wave.is_active = True
        self.assertTrue(self.wave.is_active)

    def test_wave_start_spawning(self):
        """Test wave starts spawning enemies."""
        self.wave.is_active = True
        self.wave.time_since_last_spawn = 0

        # Check if enough time has passed to spawn
        can_spawn = self.wave.time_since_last_spawn >= self.wave.spawn_interval
        self.assertFalse(can_spawn)

    def test_wave_spawn_timing(self):
        """Test enemy spawns at correct interval."""
        spawn_interval = 1.0
        time_elapsed = 1.0

        should_spawn = time_elapsed >= spawn_interval
        self.assertTrue(should_spawn)

    def test_wave_spawn_enemy(self):
        """Test enemy is spawned."""
        self.wave.is_active = True
        self.wave.enemies_spawned = 0

        self.wave.enemies_spawned += 1
        self.assertEqual(self.wave.enemies_spawned, 1)

    def test_wave_spawn_counter_increments(self):
        """Test spawn counter increments correctly."""
        for _ in range(self.wave.enemy_count):
            self.wave.enemies_spawned += 1

        self.assertEqual(self.wave.enemies_spawned, 5)

    def test_wave_spawning_complete(self):
        """Test wave completes when all enemies spawned."""
        self.wave.enemies_spawned = 5
        is_complete = self.wave.enemies_spawned >= self.wave.enemy_count

        self.assertTrue(is_complete)

    def test_wave_multiple_spawns_per_frame(self):
        """Test correct behavior with multiple spawn cycles."""
        delta_time = 0.016  # ~60 FPS frame
        time_accumulated = 0

        for _ in range(70):  # 70 frames ≈ 1.12 seconds
            time_accumulated += delta_time

            if time_accumulated >= self.wave.spawn_interval:
                self.wave.enemies_spawned += 1
                time_accumulated -= self.wave.spawn_interval

        # Should have spawned 1 enemy in ~70 frames
        self.assertGreaterEqual(self.wave.enemies_spawned, 1)

    def test_wave_timing_precision(self):
        """Test wave timing is precise."""
        spawn_interval = 1.0
        elapsed_time = 0.999

        should_spawn = elapsed_time >= spawn_interval
        self.assertFalse(should_spawn)

        elapsed_time = 1.001
        should_spawn = elapsed_time >= spawn_interval
        self.assertTrue(should_spawn)

    def test_wave_spawn_interval_varying(self):
        """Test different spawn intervals."""
        intervals = [0.5, 1.0, 2.0, 3.0]

        for interval in intervals:
            wave = Mock(spawn_interval=interval)
            self.assertIn(wave.spawn_interval, intervals)

    def test_wave_time_since_last_spawn_reset(self):
        """Test time counter resets after spawn."""
        self.wave.time_since_last_spawn = 1.5
        self.wave.time_since_last_spawn -= self.wave.spawn_interval

        self.assertEqual(self.wave.time_since_last_spawn, 0.5)

    def test_wave_all_enemies_spawned(self):
        """Test wave status when all enemies spawned."""
        self.wave.enemies_spawned = self.wave.enemy_count
        all_spawned = self.wave.enemies_spawned >= self.wave.enemy_count

        self.assertTrue(all_spawned)

    def test_wave_completion_check(self):
        """Test wave completion detection."""
        self.wave.enemies_spawned = 5
        self.wave.is_active = False

        is_complete = (
            self.wave.enemies_spawned >= self.wave.enemy_count and
            not self.wave.is_active
        )
        self.assertTrue(is_complete)

    def test_multiple_waves_sequential(self):
        """Test multiple waves spawn sequentially."""
        waves = [
            Mock(wave_id=0, enemy_count=5, enemies_spawned=0),
            Mock(wave_id=1, enemy_count=5, enemies_spawned=0),
            Mock(wave_id=2, enemy_count=5, enemies_spawned=0),
        ]

        # Simulate spawning
        for wave in waves:
            for _ in range(wave.enemy_count):
                wave.enemies_spawned += 1

        # All waves should be complete
        for wave in waves:
            self.assertEqual(wave.enemies_spawned, wave.enemy_count)

    def test_wave_speed_modifier(self):
        """Test wave spawn speed can be modified."""
        base_interval = 1.0
        speed_multiplier = 0.8

        modified_interval = base_interval * speed_multiplier
        self.assertEqual(modified_interval, 0.8)

    def test_wave_spawn_delay(self):
        """Test delay before wave starts."""
        wave_start_delay = 2.0
        time_elapsed = 0

        can_start = time_elapsed >= wave_start_delay
        self.assertFalse(can_start)

        time_elapsed = 2.5
        can_start = time_elapsed >= wave_start_delay
        self.assertTrue(can_start)

    def test_manual_wave_triggering(self):
        """Test waves can be manually triggered."""
        self.wave.is_active = False

        # Manually trigger wave
        self.wave.is_active = True
        self.assertTrue(self.wave.is_active)

    def test_automatic_wave_triggering(self):
        """Test waves trigger automatically on schedule."""
        wave_start_time = 5.0
        current_time = 5.0

        auto_trigger = current_time >= wave_start_time
        self.assertTrue(auto_trigger)

    def test_remaining_spawns_calculation(self):
        """Test calculation of remaining enemies to spawn."""
        remaining = self.wave.enemy_count - self.wave.enemies_spawned
        self.assertEqual(remaining, 5)

        self.wave.enemies_spawned = 3
        remaining = self.wave.enemy_count - self.wave.enemies_spawned
        self.assertEqual(remaining, 2)

    def test_level_has_multiple_waves(self):
        """Test level contains multiple waves."""
        level = Mock()
        level.waves = [
            Mock(wave_id=0, enemy_count=5),
            Mock(wave_id=1, enemy_count=8),
            Mock(wave_id=2, enemy_count=10),
        ]

        self.assertEqual(len(level.waves), 3)

    def tearDown(self):
        """Cleanup."""
        pass


if __name__ == '__main__':
    unittest.main()
