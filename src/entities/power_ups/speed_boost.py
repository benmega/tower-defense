# speed_boost.py

from power_up import PowerUp

class SpeedBoostPowerUp(PowerUp):
    def __init__(self, duration, speed_increase):
        super().__init__("speed_boost", duration, self.apply_effect)
        self.speed_increase = speed_increase

    def apply_effect(self, target):
        """
        Apply the speed boost effect to the target.
        Increase the target's speed attribute by the specified amount.
        """
        target.speed += self.speed_increase
        # You might want to add a timer here to handle the duration of the effect

    def deactivate(self):
        """
        Deactivate the speed boost, reverting the target's speed to its original state.
        """
        # Assuming target maintains its original speed in another attribute
        target.speed -= self.speed_increase
        super().deactivate()

# Example usage
# Assuming 'target' is an entity that has a 'speed' attribute
target = SomeEntity(speed=5)
speed_boost = SpeedBoostPowerUp(duration=10, speed_increase=2)
speed_boost.activate(target)

# After duration, deactivate the power-up
speed_boost.deactivate()
