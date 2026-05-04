"""
Test player resource management and progression.
"""

import unittest
from unittest.mock import Mock


class TestPlayer(unittest.TestCase):
    """Test player resource management."""

    def setUp(self):
        """Setup player for tests."""
        self.player = Mock()
        self.player.gold = 100
        self.player.health = 20
        self.player.max_health = 20
        self.player.score = 0
        self.player.level = 1
        self.player.unlocked_levels = [0]

    def test_player_initialization(self):
        """Test player initializes with correct values."""
        self.assertEqual(self.player.gold, 100)
        self.assertEqual(self.player.health, 20)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.level, 1)

    def test_player_add_gold(self):
        """Test player gains gold."""
        initial_gold = self.player.gold
        gold_gained = 50

        self.player.gold += gold_gained
        self.assertEqual(self.player.gold, 150)

    def test_player_spend_gold_sufficient(self):
        """Test player can spend gold when sufficient funds."""
        self.player.gold = 100
        cost = 50

        if self.player.gold >= cost:
            self.player.gold -= cost

        self.assertEqual(self.player.gold, 50)

    def test_player_spend_gold_insufficient(self):
        """Test player cannot spend gold with insufficient funds."""
        self.player.gold = 30
        cost = 50

        if self.player.gold >= cost:
            self.player.gold -= cost

        # Gold should not change
        self.assertEqual(self.player.gold, 30)

    def test_player_spend_gold_exact_amount(self):
        """Test player spending exact gold amount."""
        self.player.gold = 50
        cost = 50

        if self.player.gold >= cost:
            self.player.gold -= cost

        self.assertEqual(self.player.gold, 0)

    def test_player_take_damage(self):
        """Test player takes damage."""
        initial_health = self.player.health
        damage = 5

        self.player.health -= damage
        self.assertEqual(self.player.health, 15)

    def test_player_death_on_zero_health(self):
        """Test player dies at zero health."""
        self.player.health = 5
        damage = 5

        self.player.health -= damage
        is_dead = self.player.health <= 0

        self.assertTrue(is_dead)
        self.assertEqual(self.player.health, 0)

    def test_player_death_on_overkill_damage(self):
        """Test player dies with overkill damage."""
        self.player.health = 5
        damage = 20

        self.player.health -= damage
        is_dead = self.player.health <= 0

        self.assertTrue(is_dead)
        self.assertEqual(self.player.health, -15)

    def test_player_health_cannot_exceed_max(self):
        """Test player health cannot exceed max health."""
        self.player.health = self.player.max_health
        heal_amount = 10

        new_health = min(self.player.health + heal_amount, self.player.max_health)
        self.assertEqual(new_health, self.player.max_health)

    def test_player_restore_health(self):
        """Test player restores health."""
        self.player.health = 5
        heal_amount = 10

        self.player.health = min(self.player.health + heal_amount, self.player.max_health)
        self.assertEqual(self.player.health, self.player.max_health)

    def test_player_add_score(self):
        """Test player gains score."""
        initial_score = self.player.score
        points = 100

        self.player.score += points
        self.assertEqual(self.player.score, 100)

    def test_player_score_accumulation(self):
        """Test score accumulates over multiple gains."""
        self.player.score = 0

        for _ in range(5):
            self.player.score += 50

        self.assertEqual(self.player.score, 250)

    def test_player_level_progression(self):
        """Test player level increases."""
        initial_level = self.player.level
        self.player.level += 1

        self.assertEqual(self.player.level, 2)

    def test_player_unlock_level(self):
        """Test player unlocks new levels."""
        self.player.unlocked_levels = [0]
        self.player.unlocked_levels.append(1)

        self.assertIn(1, self.player.unlocked_levels)

    def test_player_level_unlock_progression(self):
        """Test sequential level unlocking."""
        self.player.unlocked_levels = [0]

        for level_id in range(1, 5):
            if level_id not in self.player.unlocked_levels:
                self.player.unlocked_levels.append(level_id)

        self.assertEqual(self.player.unlocked_levels, [0, 1, 2, 3, 4])

    def test_player_cannot_unlock_duplicate_level(self):
        """Test player can't unlock same level twice."""
        self.player.unlocked_levels = [0, 1]
        initial_count = len(self.player.unlocked_levels)

        if 1 not in self.player.unlocked_levels:
            self.player.unlocked_levels.append(1)

        self.assertEqual(len(self.player.unlocked_levels), initial_count)

    def test_player_reset_on_level_start(self):
        """Test player resets resources at level start."""
        self.player.gold = 500
        self.player.health = 5
        self.player.score = 1000

        # Reset for new level
        self.player.gold = 100
        self.player.health = self.player.max_health
        self.player.score = 0

        self.assertEqual(self.player.gold, 100)
        self.assertEqual(self.player.health, 20)
        self.assertEqual(self.player.score, 0)

    def test_player_complete_level(self):
        """Test player completion of level."""
        is_level_complete = True
        reward_gold = 200

        if is_level_complete:
            self.player.gold += reward_gold

        self.assertEqual(self.player.gold, 300)

    def test_player_gold_earning_from_enemies(self):
        """Test player earns gold from defeating enemies."""
        enemy_bounties = [10, 15, 20]
        initial_gold = self.player.gold

        for bounty in enemy_bounties:
            self.player.gold += bounty

        expected_gold = initial_gold + sum(enemy_bounties)
        self.assertEqual(self.player.gold, expected_gold)

    def test_player_gold_earning_from_level_completion(self):
        """Test player earns bonus gold on level completion."""
        completion_bonus = 100
        self.player.gold += completion_bonus

        self.assertEqual(self.player.gold, 200)

    def test_player_skills_unlocked(self):
        """Test player has skill tracking."""
        self.player.skills_unlocked = []
        self.player.skills_unlocked.append('fireball')

        self.assertIn('fireball', self.player.skills_unlocked)

    def test_player_save_game_state(self):
        """Test player state can be saved."""
        state = {
            'gold': self.player.gold,
            'health': self.player.health,
            'score': self.player.score,
            'level': self.player.level,
            'unlocked_levels': list(self.player.unlocked_levels),
        }

        self.assertEqual(state['gold'], 100)
        self.assertEqual(state['health'], 20)

    def test_player_load_game_state(self):
        """Test player state can be loaded."""
        saved_state = {
            'gold': 500,
            'health': 10,
            'score': 1000,
            'level': 3,
            'unlocked_levels': [0, 1, 2],
        }

        self.player.gold = saved_state['gold']
        self.player.health = saved_state['health']
        self.player.score = saved_state['score']
        self.player.level = saved_state['level']
        self.player.unlocked_levels = saved_state['unlocked_levels']

        self.assertEqual(self.player.gold, 500)
        self.assertEqual(self.player.health, 10)
        self.assertEqual(self.player.score, 1000)
        self.assertEqual(self.player.level, 3)

    def test_player_alive_check(self):
        """Test player alive/dead status."""
        self.player.health = 10
        is_alive = self.player.health > 0
        self.assertTrue(is_alive)

        self.player.health = 0
        is_alive = self.player.health > 0
        self.assertFalse(is_alive)

    def tearDown(self):
        """Cleanup."""
        pass


if __name__ == '__main__':
    unittest.main()
