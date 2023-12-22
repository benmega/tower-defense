# gem.py

class Gem:
    def __init__(self, gem_type, level, base_damage, special_effect=None):
        self.gem_type = gem_type       # Type of the gem (e.g., fire, ice, poison)
        self.level = level             # Level of the gem, affecting its potency
        self.base_damage = base_damage # Base damage dealt by the gem
        self.special_effect = special_effect # Special effect (e.g., slowing, splash damage)

    def upgrade(self):
        """
        Upgrade the gem, increasing its level and stats.
        """
        self.level += 1
        self.base_damage *= 1.2  # Example: Increase damage by 20% upon upgrade
        # You can add more upgrade logic here

    def activate_effect(self, target):
        """
        Activate the gem's special effect on a target.
        """
        if self.special_effect:
            # Implement the effect logic here
            pass

    # Additional methods for gem functionality can be added here

# Example usage
fire_gem = Gem(gem_type="fire", level=1, base_damage=10)
fire_gem.upgrade()
