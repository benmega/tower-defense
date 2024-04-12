# power_up.py

class PowerUp:
    def __init__(self, power_up_type, duration, effect):
        self.power_up_type = power_up_type  # Type of the power-up (e.g., 'speed_boost', 'damage_boost')
        self.duration = duration            # Duration for which the power-up is active
        self.effect = effect                # The effect of the power-up
        self.active = False                 # Indicates if the power-up is currently active

    def activate(self, target):
        """
        Activate the power-up, applying its effect to the target.
        """
        if not self.active:
            self.active = True
            self.apply_effect(target)

    def apply_effect(self, target):
        """
        Apply the power-up's effect. This method should be overridden by subclasses
        to implement specific power-up effects.
        """
        # Implement effect logic here
        pass

    def deactivate(self):
        """
        Deactivate the power-up, removing its effect.
        """
        self.active = False
        # Implement deactivation logic here

    # Additional methods for power-up behavior can be added here

# Example subclass for a specific type of power-up
class SpeedBoostPowerUp(PowerUp):
    def __init__(self, duration, speed_increase):
        super().__init__("speed_boost", duration, self.apply_effect)
        self.speed_increase = speed_increase

    def apply_effect(self, target):
        # Specific logic to increase the target's speed
        target.speed += self.speed_increase

    def deactivate(self, target):
        # Revert the target's speed increase
        target.speed -= self.speed_increase
        super().deactivate()

# Example usage
#speed_boost = SpeedBoostPowerUp(duration=10, speed_increase=2)
# Assuming 'target' is an entity that can receive speed boosts
