"""
Lightweight particle system for visual effects.
Spawn bursts with ParticleSystem.emit(); call update() and draw() each frame.
"""
import pygame
import math
import random
from src.utils import constants as C


class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'radius')

    def __init__(self, x, y, vx, vy, life, color, radius):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.life = self.max_life = life
        self.color = color
        self.radius = radius


class ParticleSystem:
    def __init__(self):
        self._particles = []

    def emit(self, x, y, count=12, color=None, speed=2.5, spread=math.pi * 2, radius=3, life=0.6):
        """Emit particles in a burst at (x, y)."""
        if color is None:
            color = C.RGB_GOLD_BRIGHT
        for _ in range(count):
            angle = random.uniform(0, spread)
            spd = random.uniform(speed * 0.5, speed)
            self._particles.append(Particle(
                x, y, math.cos(angle) * spd, math.sin(angle) * spd,
                life * random.uniform(0.7, 1.3), color, radius
            ))

    def update(self, dt):
        """Update all particles; remove expired ones."""
        self._particles = [p for p in self._particles if p.life > 0]
        for p in self._particles:
            p.life -= dt
            p.x += p.vx
            p.y += p.vy
            p.vy += 0.05  # gravity

    def draw(self, surface):
        """Draw all particles to the surface."""
        for p in self._particles:
            alpha = int(255 * (p.life / p.max_life))
            r = max(1, int(p.radius * (p.life / p.max_life)))
            color = (*p.color[:3], alpha)
            tmp = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(tmp, color, (r, r), r)
            surface.blit(tmp, (int(p.x) - r, int(p.y) - r))
