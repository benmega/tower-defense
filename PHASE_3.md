# Phase 3 — Screen Polish

> **Prerequisite:** Phase 2 must be merged first.
> All color/spacing values come from `src/utils/constants.py`.

## Goal

Every screen in the game currently uses hardcoded pixel positions, has no transitions, and varies wildly in style. This phase standardizes the layout system, adds entry/exit transitions, and rebuilds each screen to a professional quality.

---

## 3.1 Responsive Layout Helper

Create `src/utils/layout.py`. This is the foundation that all Phase 3 screen work builds on.

```python
"""
Layout helpers. All position math lives here — never in screen files.

Usage:
    from src.utils.layout import center_rect, stack_rects, anchor

    btn_rect = center_rect(width=200, height=40, within=(SCREEN_WIDTH, SCREEN_HEIGHT))
    rects = stack_rects(count=4, item_h=40, gap=12, top=300, screen_w=SCREEN_WIDTH)
"""
import pygame
import src.config.config as cfg

def center_rect(width: int, height: int, within: tuple = None) -> pygame.Rect:
    """Return a Rect centered in `within` (defaults to full screen)."""
    w, h = within or (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    return pygame.Rect((w - width) // 2, (h - height) // 2, width, height)

def stack_rects(count: int, item_w: int, item_h: int, gap: int,
                top: int, screen_w: int = None) -> list[pygame.Rect]:
    """Return a vertical stack of `count` Rects centered horizontally."""
    sw = screen_w or cfg.SCREEN_WIDTH
    x = (sw - item_w) // 2
    return [pygame.Rect(x, top + i * (item_h + gap), item_w, item_h) for i in range(count)]

def anchor(obj_w: int, obj_h: int,
           h: str = 'center', v: str = 'center',
           margin: int = 0, within: tuple = None) -> tuple[int, int]:
    """
    Return (x, y) for an object anchored within a container.
    h: 'left' | 'center' | 'right'
    v: 'top'  | 'center' | 'bottom'
    """
    cw, ch = within or (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    x = {'left': margin, 'center': (cw - obj_w) // 2, 'right': cw - obj_w - margin}[h]
    y = {'top': margin, 'center': (ch - obj_h) // 2, 'bottom': ch - obj_h - margin}[v]
    return x, y
```

---

## 3.2 Screen Base Class — Add Lifecycle + Fade Transitions

**File to modify:** `src/screens/screen.py`

Add:
1. `on_enter(self)` — called when a screen becomes active; starts fade-in timer; subclasses override for screen-specific setup
2. `on_exit(self)` — called when leaving; starts fade-out; subclasses override for cleanup
3. `_draw_fade_overlay(surface)` — draws a black rect at the current alpha value during transitions

Implementation sketch:
```python
import src.utils.constants as C

class Screen:
    FADE_DURATION = C.ANIM_NORMAL  # seconds

    def __init__(self, ...):
        ...
        self._fade_alpha = 255       # start fully black, fade in
        self._fading_in = True
        self._fading_out = False
        self._fade_timer = 0.0

    def on_enter(self):
        self._fade_alpha = 255
        self._fading_in = True
        self._fade_timer = 0.0

    def on_exit(self):
        self._fading_out = True
        self._fade_timer = 0.0

    def update(self, time_delta):
        if self._fading_in:
            self._fade_timer += time_delta
            self._fade_alpha = max(0, int(255 * (1 - self._fade_timer / self.FADE_DURATION)))
            if self._fade_timer >= self.FADE_DURATION:
                self._fading_in = False
        elif self._fading_out:
            self._fade_timer += time_delta
            self._fade_alpha = min(255, int(255 * self._fade_timer / self.FADE_DURATION))

    def _draw_fade_overlay(self, surface):
        if self._fade_alpha > 0:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self._fade_alpha))
            surface.blit(overlay, (0, 0))
```

Call `on_enter()` inside `open_screen()` (base class) and call `_draw_fade_overlay(screen)` at the very end of `draw()` in the base class. Call `on_exit()` inside `close_screen()`.

Call `screen.on_enter()` from `GameStateTransitionHandler` in `game_state_manager.py` for each screen open method.

---

## 3.3 Main Menu

**File:** `src/screens/main_menu.py`

Current problems: button positions are magic constants from config; no indication of save file existing; no visual hierarchy.

Changes:
1. Replace `MAIN_MENU_*_BUTTON_POSITION` constants with `layout.stack_rects(count=4, item_w=220, item_h=44, gap=14, top=int(SCREEN_HEIGHT * 0.44))`
2. On init, check if any save file exists (glob `src/save_data/*.json`); if none found, set "Continue Game" button `is_enabled=False` so it renders in the disabled (grey) style — the theme already handles disabled styling
3. Update `config.py` to remove the four `MAIN_MENU_*_BUTTON_POSITION` constants (they are only used here)

---

## 3.4 Campaign Map

**File:** `src/screens/campain_map.py` (note: typo in filename — do NOT rename the file, it would break imports; leave the rename for a future PR)

Current problems: 30 level positions hardcoded as pixel coordinates; camera speed has no easing; skills button at magic offset `[SCREEN_WIDTH - 300, 10]`; `initilize_buttons` typo.

Changes:
1. Rename method `initilize_buttons` → `initialize_buttons` and update the one call site in `__init__`
2. Replace hardcoded level position list with a computed snake-path generator:
   ```python
   def _generate_level_positions(count: int, cols: int = 6) -> list[tuple]:
       """Lay out levels in a snake pattern across the map."""
       positions = []
       row_h = MAP_HEIGHT * 3 // (count // cols + 1)
       for i in range(count):
           row = i // cols
           col = i % cols if row % 2 == 0 else (cols - 1 - i % cols)
           x = int(MAP_WIDTH * 3 * (col + 0.5) / cols)
           y = int(row_h * (row + 0.5))
           positions.append((x, y))
       return positions
   ```
   Use `_generate_level_positions(30)` instead of the hand-typed list. This keeps the map maintainable as levels are added.
3. Smooth camera: replace the snap pan `camera += speed` with `camera += (target - camera) * 0.12` (exponential easing). Target is set when the mouse nears an edge.
4. Skills button: use `layout.anchor(btn_w, btn_h, h='right', v='top', margin=constants.SPACE_MD)` instead of the magic `[SCREEN_WIDTH - 300, 10]` offset.

---

## 3.5 Options Screen

**File:** `src/screens/options_screen.py`

Current problems: fullscreen toggle does nothing (just `print`); slider labels rely on background image; button positions hardcoded; no live readout of volume value.

Changes:
1. **Implement fullscreen toggle** — replace the `print` with:
   ```python
   pygame.display.toggle_fullscreen()
   ```
2. Replace hardcoded button/slider positions with layout helpers:
   ```python
   slider_positions = layout.stack_rects(count=2, item_w=300, item_h=30, gap=40, top=int(SCREEN_HEIGHT * 0.25))
   ```
3. Add a UILabel next to each slider showing the current percentage value; update it in `handle_events` when the slider fires `UI_HORIZONTAL_SLIDER_MOVED`
4. Add descriptive UILabel headers above each slider: "Music Volume" and "Sound Effects Volume" — use `constants.TEXT_LIGHT` color

---

## 3.6 Game Data Screen (Load/Save)

**File:** `src/screens/game_data_screen.py`

Current problems: load and save buttons overlap at identical coords (only visibility differs); mode toggle button hardcoded at `(50, 50)`; code cuts off mid-statement at line 146.

Changes:
1. Fix the truncated line (line ~146): read the file to find the incomplete `set_text(...)` call and complete it. The button text should read `"Switch to Load"` when in save mode and `"Switch to Save"` when in load mode.
2. Move mode toggle button to use `layout.anchor(btn_w, btn_h, h='right', v='top', margin=constants.SPACE_MD)` — away from top-left where return button lives.
3. Keep the overlapping button approach (it works), but make the visual transition between modes smoother: on mode switch, briefly hide both sets and show them after a 1-frame delay so pygame-gui doesn't flash.
4. Each save slot button should display: slot number, saved level (if any), score, and timestamp — formatted as two lines using `\n` in button text.

---

## 3.7 Skills Screen

**File:** `src/screens/skills_screen.py`

Current problems: grid layout uses magic numbers (cell size 380×50, margin 200, spacing 10); no visual distinction for maxed skills; button text overflows; `skill_points` label at `[50, 50]`.

Changes:
1. Replace magic grid constants with layout helpers:
   ```python
   CELL_W = int(SCREEN_WIDTH * 0.35)
   CELL_H = 48
   GAP = constants.SPACE_SM
   MARGIN_TOP = int(SCREEN_HEIGHT * 0.22)
   MARGIN_LEFT = int(SCREEN_WIDTH * 0.08)
   ```
2. Skill points label: use `layout.anchor(label_w, label_h, h='right', v='top', margin=constants.SPACE_MD)` — top-right corner.
3. Maxed skills: after upgrade, if `skill.level >= skill.max_level`, set button `is_enabled=False` so it renders in the disabled (gold-grey) style and cannot be clicked.
4. Button text: shorten to `"{name} (Lv {level})"` on the first line and `"Next: {cost}pts"` or `"MAX"` on the second line using `\n`.
5. Fix button text refresh on upgrade (current line ~144 only sets key, not the full formatted text).

---

## 3.8 Level Completion / Defeat Screen

**File:** `src/screens/level_completion.py`

Current problems: modal is 40% wide × 50% tall using magic fractions; buttons positioned with integer division that assumes aspect ratio; background capture stored but stale; no visual difference between win and defeat.

Changes:
1. Replace modal sizing with:
   ```python
   modal_w = int(SCREEN_WIDTH * 0.38)
   modal_h = int(SCREEN_HEIGHT * 0.48)
   modal_rect = layout.center_rect(modal_w, modal_h)
   ```
2. Stack buttons using `layout.stack_rects(count=3, item_w=modal_w - 40, item_h=44, gap=12, top=modal_rect.y + modal_h // 2)`
3. Win screen: draw 1–3 star icons (use a simple polygon or the star from `assets/`) above the buttons based on score threshold. Thresholds: 1 star = any completion, 2 stars = >60% enemies killed before base damage, 3 stars = no damage taken. (Score thresholds are approximate — tune in Phase 4.)
4. Defeat screen: use a red-tinted overlay (`(180, 0, 0, 60)` over captured background) instead of just the defeat image, to make it feel distinct and serious.
5. Remove the double `load_background()` call.

---

## Acceptance Checklist

- [ ] All screen transitions fade in/out (black overlay, ~0.3s)
- [ ] Main menu "Continue" is visually disabled when no save file exists
- [ ] Campaign map level positions are generated, not hardcoded; camera pans smoothly
- [ ] Options fullscreen button actually toggles fullscreen
- [ ] Options sliders show live percentage labels
- [ ] Game data screen toggle button is not at `(50, 50)` and code does not cut off
- [ ] Skills screen maxed-out skills are greyed and non-clickable
- [ ] Level completion shows win vs. defeat with distinct visual treatments
- [ ] No screen uses a hardcoded pixel coordinate that isn't derived from SCREEN_WIDTH/SCREEN_HEIGHT or a layout helper
