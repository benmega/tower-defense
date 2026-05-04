# Phase 4 — Visual Flourish & Asset Cleanup

> **Prerequisite:** Phases 2 and 3 must be merged first.
> All color/spacing values come from `src/utils/constants.py`.

## Goal

The game looks and sounds polished. Particle effects, screen shake, animated tiles, and sound completeness are the difference between "nice indie game" and "asset flip". This phase adds all of it — but only what's achievable with existing assets and pygame's built-in draw primitives.

---

## 4.1 Particle System

Create `src/effects/particle_system.py`. This is a standalone, stateless effect system that any manager can call.

```python
"""
Lightweight particle system.
Spawn bursts with ParticleSystem.emit(); call update() and draw() each frame.
"""
import pygame, math, random
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
        self._particles: list[Particle] = []

    def emit(self, x, y, count=12, color=C.RGB_GOLD_BRIGHT,
             speed=2.5, spread=math.pi * 2, radius=3, life=0.6):
        for _ in range(count):
            angle = random.uniform(0, spread)
            spd = random.uniform(speed * 0.5, speed)
            self._particles.append(Particle(
                x, y, math.cos(angle) * spd, math.sin(angle) * spd,
                life * random.uniform(0.7, 1.3), color, radius
            ))

    def update(self, dt):
        self._particles = [p for p in self._particles if p.life > 0]
        for p in self._particles:
            p.life -= dt
            p.x += p.vx
            p.y += p.vy
            p.vy += 0.05  # gravity

    def draw(self, surface):
        for p in self._particles:
            alpha = int(255 * (p.life / p.max_life))
            r = max(1, int(p.radius * (p.life / p.max_life)))
            color = (*p.color[:3], alpha)
            tmp = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(tmp, color, (r, r), r)
            surface.blit(tmp, (int(p.x) - r, int(p.y) - r))
```

**Wire into `src/game/game.py`:**
1. Add `self.particles = ParticleSystem()` in `Game.__init__`
2. In `draw()` PLAYING branch, after projectiles: `self.particles.draw(self.screen)`
3. In `update()` PLAYING branch: `self.particles.update(time_delta)`
4. Pass `game.particles` to managers that need it (see below)

---

## 4.2 Enemy Death Particles

**File:** `src/managers/enemy_manager.py`

In `enemy_defeated_callback` (or wherever enemies are removed on health ≤ 0), add:
```python
game.particles.emit(enemy.rect.centerx, enemy.rect.centery,
                    count=10, color=C.RGB_HEALTH_RED, speed=2.0, life=0.5)
```

Also play `game.audio_manager.play_sound(...)` with a short death SFX. Candidate: `mixkit-lightning-whip-1508.wav` (short and punchy). Add `SFX_ENEMY_DEATH = 'assets/sounds/mixkit-lightning-whip-1508.wav'` to `constants.py`.

---

## 4.3 Gold Pickup Particles

**File:** `src/game/game.py` → `enemy_defeated_callback`

After awarding gold, emit gold sparkle particles:
```python
self.particles.emit(enemy.rect.centerx, enemy.rect.centery - 20,
                    count=6, color=C.RGB_GOLD_BRIGHT, speed=1.5, life=0.8)
```

---

## 4.4 Tower Placement Particles

**File:** `src/managers/tower_manager.py` → `add_tower_if_possible`

On successful tower placement, emit a construction burst:
```python
game.particles.emit(tower_x_center, tower_y_center,
                    count=14, color=C.RGB_AMBER, speed=3.0, spread=math.pi*2, life=0.7)
```

---

## 4.5 Screen Shake

Create `src/effects/screen_shake.py`:
```python
import random

class ScreenShake:
    def __init__(self):
        self.duration = 0.0
        self.magnitude = 0

    def trigger(self, magnitude=6, duration=0.3):
        self.magnitude = max(self.magnitude, magnitude)
        self.duration = max(self.duration, duration)

    def update(self, dt) -> tuple[int, int]:
        """Returns (offset_x, offset_y) to apply to the draw surface."""
        if self.duration <= 0:
            return 0, 0
        self.duration -= dt
        ox = random.randint(-self.magnitude, self.magnitude)
        oy = random.randint(-self.magnitude, self.magnitude)
        return ox, oy
```

**Wire into `src/game/game.py`:**
- Add `self.shake = ScreenShake()` in `__init__`
- In `draw()`, before filling the screen: `ox, oy = self.shake.update(...)` then offset the board blit by `(ox, oy)`
- Trigger `self.shake.trigger(magnitude=8, duration=0.25)` in `player_take_damage_callback`
- Trigger `self.shake.trigger(magnitude=4, duration=0.15)` on cannon/missile impacts (wire through collision_manager callback)

---

## 4.6 Path Direction Animation (animated arrow overlay)

The path tiles currently display as static sprites with no indication of direction.

**File:** `src/board/game_board.py`

Add a subtle animated scroll effect along the path by drawing semi-transparent small chevrons (▶) that drift forward along each path segment. Use a `time` accumulator in `draw_board()` that increments each frame, and offset the chevron positions by `(time * speed) % segment_length`.

Implementation:
```python
self._path_anim_time = 0.0  # add to __init__

# In draw_board():
self._path_anim_time += time_delta
# For each (a, b) segment pair in path, compute direction vector and draw a chevron
# every 32px along the segment, offset by anim_time * 20 % 32
```

Chevron: use `pygame.draw.polygon` with a small right-arrow shape (3 points), color `(*C.RGB_GOLD_BRIGHT[:3], 60)` (very low alpha so it doesn't dominate the tile art). Use a `pygame.Surface(tile_size, pygame.SRCALPHA)`.

---

## 4.7 Lava/Water Tile Animation

The existing tile set includes `lava.png`, `stone.png`, and `water.png` which are unused — only `grass.png`, `path.png`, `entrance.png`, `exit.png` are used in gameplay. Some levels might use the alternate tiles.

**File:** `src/board/game_board.py`

Add a UV-scroll simulation for lava/water tiles:
- Maintain a float offset `self._tile_anim_offset` that increments each frame
- When drawing a `LAVA` or `WATER` tile: clip the texture rect by `(offset % tile_w, 0)` to create a scrolling appearance

This is purely visual; no game logic changes.

---

## 4.8 Sound Completeness Pass

**File:** `src/managers/audio_manager.py`

Wire all the currently preloaded-but-unused Mixkit sounds:

| Event | Sound File | Call Site |
|-------|-----------|-----------|
| Level complete | `mixkit-fantasy-game-success-notification-270.wav` | `game_state_manager.open_complete_screen()` |
| Level defeat | `mixkit-retro-game-emergency-alarm-1000.wav` | `game_state_manager.open_defeat_screen()` |
| Skill unlocked | `mixkit-unlock-game-notification-253.wav` | `skills_screen.py` on successful upgrade |
| Level start | `mixkit-metal-medieval-construction-818.wav` | `game_state_manager.open_playing_scene()` |
| All levels complete / campaign won | `mixkit-magic-sweep-game-trophy-257.wav` | `game.check_game_over()` when all levels done |

Add `SFX_*` constants for each to `src/utils/constants.py`.

---

## 4.9 Asset Cleanup

These are low-risk file hygiene tasks:

1. **Fix double-extension filename:** Rename `assets/images/Players/character.png.png` → `character.png` and update any reference in config.py or entity code
2. **Deduplicate music files:** `assets/sounds/campaign_background.mp3` and `assets/sounds/campaign_map_background.mp3` are the same file. Delete `campaign_background.mp3`; the AudioManager already points to `campaign_map_background.mp3`
3. **Remove orphaned audio file:** `assets/sounds/2024-02-20-13-28-25.mp3` is an auto-named recording, not referenced in any code. Delete it.
4. **Deduplicate screen images:** `assets/images/screens/main_menu_screen.png` exists in both `screens/` and `main_menu_screen/`. Delete the `main_menu_screen/` directory; config references `screens/main_menu_screen.png`.
5. **Remove level_defeat JPGs:** `level_defeat.jpg` and `level_defeat_2.jpg` exist alongside `.png` versions. The code uses `level_defeat_2.jpg` — standardize to PNG. Convert `level_defeat_2.jpg` to PNG if possible, update the reference in `level_completion.py`.

**Before each deletion:** grep for the filename in `src/` and `assets/` to confirm nothing else references it.

---

## 4.10 Window Title & Icon

**File:** `src/game/game.py` line 38

Current: `pygame.display.set_caption("Mr. Mega's Awesome Tower Defense Game")`

Change to: `pygame.display.set_caption("Tower Defense")`

If a suitable icon exists in `assets/images/` (e.g., a tower sprite), add:
```python
icon = pygame.image.load('assets/images/towers/basic_tower.png').convert_alpha()
pygame.display.set_icon(icon)
```

---

## Acceptance Checklist

- [ ] Enemy death spawns red particle burst
- [ ] Gold pickup spawns gold sparkle
- [ ] Tower placement spawns amber construction burst
- [ ] Player taking damage triggers screen shake
- [ ] Path tiles have a subtle animated direction indicator
- [ ] Level complete plays a fanfare sound
- [ ] Level defeat plays an alarm sound
- [ ] Skill upgrade plays an unlock sound
- [ ] `character.png.png` renamed, orphan audio file removed, duplicate music file removed
- [ ] Window title is "Tower Defense" with a tower icon
