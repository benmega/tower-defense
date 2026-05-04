"""
Test factories for creating game objects with customizable properties.

These factories provide convenient ways to create test objects without
needing to mock every dependency. Use them in tests to quickly set up
objects with reasonable defaults.

Example:
    tower = TowerFactory.create(x=100, y=100, damage=20)
    enemy = EnemyFactory.create(health=50, speed=3.0)
"""

from unittest.mock import Mock


class GameObjectFactory:
    """Base factory for game objects."""

    @staticmethod
    def create_rect(x=0, y=0, width=50, height=50):
        """Create a mock pygame rect."""
        rect = Mock()
        rect.x = x
        rect.y = y
        rect.width = width
        rect.height = height
        rect.left = x
        rect.right = x + width
        rect.top = y
        rect.bottom = y + height
        rect.centerx = x + width // 2
        rect.centery = y + height // 2

        def colliderect(other):
            return (
                rect.left < other.right
                and rect.right > other.left
                and rect.top < other.bottom
                and rect.bottom > other.top
            )

        def collidepoint(point):
            return (
                rect.left <= point[0] <= rect.right
                and rect.top <= point[1] <= rect.bottom
            )

        rect.colliderect = colliderect
        rect.collidepoint = collidepoint
        return rect


class TowerFactory(GameObjectFactory):
    """Factory for creating test towers."""

    @staticmethod
    def create(
        x=50,
        y=50,
        attack_range=100,
        damage=10,
        attack_speed=1.0,
        cooldown=0,
        **kwargs
    ):
        """
        Create a mock Tower instance.

        Args:
            x: X position
            y: Y position
            attack_range: Range at which tower can attack
            damage: Damage dealt per attack
            attack_speed: Attacks per second
            cooldown: Current cooldown value
            **kwargs: Additional properties to set on the tower

        Returns:
            Mock tower object with specified properties.
        """
        tower = Mock(name="Tower")
        tower.x = x
        tower.y = y
        tower.rect = GameObjectFactory.create_rect(x, y)
        tower.attack_range = attack_range
        tower.damage = damage
        tower.attack_speed = attack_speed
        tower.cooldown = cooldown
        tower.level = 1

        # Mock methods
        tower.is_enemy_in_range = Mock(return_value=False)
        tower.attack = Mock()
        tower.update = Mock()
        tower.take_damage = Mock()
        tower.upgrade = Mock()
        tower.draw = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(tower, key, value)

        return tower

    @staticmethod
    def create_sniper(**kwargs):
        """Create a sniper tower with higher range and damage."""
        return TowerFactory.create(
            attack_range=200, damage=30, attack_speed=0.5, **kwargs
        )

    @staticmethod
    def create_rapid_fire(**kwargs):
        """Create a rapid-fire tower with low damage but high attack speed."""
        return TowerFactory.create(damage=5, attack_speed=3.0, **kwargs)


class EnemyFactory(GameObjectFactory):
    """Factory for creating test enemies."""

    @staticmethod
    def create(
        x=100,
        y=100,
        health=20,
        max_health=20,
        speed=2.0,
        path=None,
        path_index=0,
        **kwargs
    ):
        """
        Create a mock Enemy instance.

        Args:
            x: X position
            y: Y position
            health: Current health
            max_health: Maximum health
            speed: Movement speed
            path: List of waypoints for the enemy to follow
            path_index: Current index in the path
            **kwargs: Additional properties to set on the enemy

        Returns:
            Mock enemy object with specified properties.
        """
        enemy = Mock(name="Enemy")
        enemy.x = x
        enemy.y = y
        enemy.rect = GameObjectFactory.create_rect(x, y)
        enemy.health = health
        enemy.max_health = max_health
        enemy.speed = speed
        enemy.original_speed = speed
        enemy.path = path or [(100, 100), (200, 200)]
        enemy.path_index = path_index
        enemy.is_alive = health > 0
        enemy.reached_goal = False

        # Mock methods
        enemy.take_damage = Mock()
        enemy.move = Mock()
        enemy.apply_slow_effect = Mock()
        enemy.apply_poison_effect = Mock()
        enemy.update = Mock()
        enemy.draw = Mock()
        enemy.on_collision = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(enemy, key, value)

        return enemy

    @staticmethod
    def create_fast(**kwargs):
        """Create a fast enemy with high speed but low health."""
        return EnemyFactory.create(health=10, speed=4.0, **kwargs)

    @staticmethod
    def create_tank(**kwargs):
        """Create a tank enemy with high health but low speed."""
        return EnemyFactory.create(health=50, max_health=50, speed=1.0, **kwargs)

    @staticmethod
    def create_flying(**kwargs):
        """Create a flying enemy that ignores terrain."""
        return EnemyFactory.create(health=15, speed=2.5, is_flying=True, **kwargs)


class ProjectileFactory(GameObjectFactory):
    """Factory for creating test projectiles."""

    @staticmethod
    def create(
        x=50,
        y=50,
        speed=5.0,
        damage=10,
        target=None,
        is_active=True,
        **kwargs
    ):
        """
        Create a mock Projectile instance.

        Args:
            x: X position
            y: Y position
            speed: Movement speed
            damage: Damage dealt on impact
            target: Target enemy object
            is_active: Whether the projectile is active
            **kwargs: Additional properties to set on the projectile

        Returns:
            Mock projectile object with specified properties.
        """
        projectile = Mock(name="Projectile")
        projectile.x = x
        projectile.y = y
        projectile.rect = GameObjectFactory.create_rect(x, y)
        projectile.speed = speed
        projectile.damage = damage
        projectile.target = target or Mock(x=200, y=200)
        projectile.is_active = is_active

        # Mock methods
        projectile.move = Mock()
        projectile.reached_target = Mock(return_value=False)
        projectile.hit_target = Mock()
        projectile.update = Mock()
        projectile.draw = Mock()
        projectile.apply_effects = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(projectile, key, value)

        return projectile

    @staticmethod
    def create_missile(**kwargs):
        """Create a missile projectile with high damage."""
        return ProjectileFactory.create(speed=4.0, damage=30, **kwargs)

    @staticmethod
    def create_laser(**kwargs):
        """Create a laser projectile with moderate damage."""
        return ProjectileFactory.create(speed=10.0, damage=15, **kwargs)


class PlayerFactory(GameObjectFactory):
    """Factory for creating test player objects."""

    @staticmethod
    def create(gold=100, health=20, max_health=20, score=0, level=1, **kwargs):
        """
        Create a mock Player instance.

        Args:
            gold: Current gold amount
            health: Current health
            max_health: Maximum health
            score: Current score
            level: Current level
            **kwargs: Additional properties to set on the player

        Returns:
            Mock player object with specified properties.
        """
        player = Mock(name="Player")
        player.gold = gold
        player.health = health
        player.max_health = max_health
        player.score = score
        player.level = level
        player.is_alive = health > 0

        # Mock methods
        player.add_gold = Mock()
        player.spend_gold = Mock(return_value=True)
        player.take_damage = Mock()
        player.restore_health = Mock()
        player.add_score = Mock()
        player.unlock_level = Mock()
        player.complete_level = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(player, key, value)

        return player


class WaveFactory:
    """Factory for creating test enemy waves."""

    @staticmethod
    def create(
        wave_id=0, enemy_count=5, enemy_type=None, spawn_interval=1.0, **kwargs
    ):
        """
        Create a mock EnemyWave instance.

        Args:
            wave_id: ID of the wave
            enemy_count: Number of enemies to spawn
            enemy_type: Type of enemies (e.g., "basic", "fast")
            spawn_interval: Time between enemy spawns
            **kwargs: Additional properties

        Returns:
            Mock wave object with specified properties.
        """
        wave = Mock(name="EnemyWave")
        wave.wave_id = wave_id
        wave.enemy_count = enemy_count
        wave.enemies_spawned = 0
        wave.spawn_interval = spawn_interval
        wave.time_since_last_spawn = 0
        wave.is_active = True
        wave.is_completed = False

        # Mock methods
        wave.update = Mock(return_value=[])
        wave.spawn_enemy = Mock()
        wave.get_remaining_spawns = Mock(return_value=enemy_count)

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(wave, key, value)

        return wave


class BoardFactory:
    """Factory for creating test game boards."""

    @staticmethod
    def create(width=1200, height=800, tile_size=50, **kwargs):
        """
        Create a mock GameBoard instance.

        Args:
            width: Board width in pixels
            height: Board height in pixels
            tile_size: Size of each tile
            **kwargs: Additional properties

        Returns:
            Mock board object with specified properties.
        """
        board = Mock(name="GameBoard")
        board.width = width
        board.height = height
        board.tile_size = tile_size
        board.grid_width = width // tile_size
        board.grid_height = height // tile_size
        board.path = [(100, 100), (300, 100), (300, 300), (500, 300)]

        # Mock methods
        board.is_valid_placement = Mock(return_value=True)
        board.get_tile_at = Mock()
        board.get_tower_at = Mock(return_value=None)
        board.update = Mock()
        board.draw = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(board, key, value)

        return board


class LevelFactory:
    """Factory for creating test levels."""

    @staticmethod
    def create(
        level_id=0, wave_count=3, starting_gold=100, starting_health=20, **kwargs
    ):
        """
        Create a mock Level instance.

        Args:
            level_id: ID of the level
            wave_count: Number of waves in the level
            starting_gold: Starting gold amount
            starting_health: Starting health
            **kwargs: Additional properties

        Returns:
            Mock level object with specified properties.
        """
        level = Mock(name="Level")
        level.level_id = level_id
        level.waves = [WaveFactory.create(i) for i in range(wave_count)]
        level.active_waves = []
        level.current_wave_index = 0
        level.starting_gold = starting_gold
        level.starting_health = starting_health
        level.is_completed = False

        # Mock methods
        level.update_level = Mock(return_value=[])
        level.get_next_wave = Mock(return_value=None)
        level.start_wave = Mock()
        level.complete_wave = Mock()
        level.reset = Mock()

        # Set any additional properties
        for key, value in kwargs.items():
            setattr(level, key, value)

        return level
