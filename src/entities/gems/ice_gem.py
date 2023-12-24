# ice_gem.py

from gem import Gem

class IceGem(Gem):
    def __init__(self, level, base_damage):
        super().__init__(gem_type="ice", level=level, base_damage=base_damage)
        self.slow_percentage = 0.5 - 0.05 * level  # Example: slow percentage scales with level

    def activate_effect(self, target):
        """
        Override to implement the ice-specific effect, like slowing down the target.
        """
        super().activate_effect(target)
        # Apply the slow effect to the target
        target.apply_slow(self.slow_percentage)

    def upgrade(self):
        """
        Override the upgrade method to enhance the ice gem's specific attributes.
        """
        super().upgrade()
        self.slow_percentage -= 0.05  # Increase the slow effect on upgrade

    # Additional ice gem-specific methods can be added here

# Example usage
ice_gem = IceGem(level=1, base_damage=5)
ice_gem.activate_effect(target_enemy)
ice_gem.upgrade()
