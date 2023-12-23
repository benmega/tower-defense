class EnemyWave:
    def __init__(self, enemy_type, count, spawn_interval, path):
        """
        Initialize an enemy wave.

        :param enemy_type: The type of enemy in this wave.
        :param count: The number of enemies in this wave.
        :param spawn_interval: Time interval between enemy spawns.
        :param path: Walking path. TODO Make this part of level or path_manager class
        """
        self.enemy_type = enemy_type
        self.count = count
        self.spawn_interval = spawn_interval
        self.spawned_count = 0
        self.last_spawn_time = 0
        self.path = path

    def update(self, current_time):
        """
        Update the wave, spawning enemies at the defined interval.

        :param current_time: Current time in the game.
        :return: An enemy instance if it's time to spawn, else None.
        """
        if self.spawned_count < self.count and current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawned_count += 1
            self.last_spawn_time = current_time
            print(f"Spawning enemy {self.spawned_count}/{self.count}")
            return self.enemy_type(self.path)  # Assumes enemy_type creates an enemy instance
        return None
