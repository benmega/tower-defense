# In gem.py or a separate fire_gem.py

class FireGem(Gem):
    def __init__(self, level, base_damage):
        super().__init__(gem_type="fire", level=level, base_damage=base_damage)
        self.burn_damage = 2 * level  # Example: burn damage scales with level

    def activate_effect(self, target):
        """
        Override the activate_effect method to implement the burning effect.
        """
        super().activate_effect(target)
        # Implement the fire-specific effect here, like applying burn damage over time
        target.apply_burn(self.burn_damage)

    def upgrade(self):
        """
        Override the upgrade method to enhance the fire gem's specific attributes.
        """
        super().upgrade()
        self.burn_damage += 1  # Increase burn damage on upgrade

    # Additional fire gem-specific methods can be added here

# Example usage
fire_gem = FireGem(level=1, base_damage=10)
fire_gem.activate_effect(target_enemy)
fire_gem.upgrade()
