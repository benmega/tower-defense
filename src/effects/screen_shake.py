"""Screen shake effect system."""
import random


class ScreenShake:
    """Simple screen shake effect."""

    def __init__(self):
        self.duration = 0.0
        self.magnitude = 0

    def trigger(self, magnitude=6, duration=0.3):
        """Trigger a shake effect."""
        self.magnitude = max(self.magnitude, magnitude)
        self.duration = max(self.duration, duration)

    def update(self, dt):
        """Update shake and return (offset_x, offset_y) to apply to the draw surface."""
        if self.duration <= 0:
            return 0, 0
        self.duration -= dt
        ox = random.randint(-self.magnitude, self.magnitude)
        oy = random.randint(-self.magnitude, self.magnitude)
        return ox, oy
