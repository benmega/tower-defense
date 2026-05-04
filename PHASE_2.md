# Phase 2 — In-Game UX

> **Prerequisite:** Phase 1 must be merged first.
> All color/spacing values come from `src/utils/constants.py`. Never hardcode RGB tuples or hex strings in new code.

## Goal

Make the in-game experience feel professional. Right now there is no pause, no placement preview, no tower management, and no fast-forward. These are the features that turn a "learning project" into a real game.

---

## 2.1 Pause System

**New state required:** Add `PAUSED` to `src/game/game_state.py` (the `GameState` enum).

**Files to modify:**
- `src/game/game_state.py` — add `PAUSED = auto()`
- `src/managers/game_state_manager.py` — add handler `open_pause_screen` in `state_handlers`; it should NOT stop music, just lower volume to 30%
- `src/managers/event_manager.py` — in `handle_playing_events`, check `event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE`; call `game.state_manager.change_state(GameState.PAUSED)` on press; if already PAUSED, resume to PLAYING
- `src/game/game.py` — in `update()`, add `elif self.current_state == GameState.PAUSED: pass` so game logic freezes
- New file `src/screens/pause_screen.py` — subclass `Screen`; use `capture_screen()` from `ui_manager` for the background; draw a semi-transparent overlay using `constants.RGB_OVERLAY`; three buttons stacked center-screen: "Resume" (→ PLAYING), "Options" (→ OPTIONS), "Quit to Menu" (→ MAIN_MENU); use `constants.SPACE_LG` for button gap; no new assets needed

**Gotcha:** `Screen.__init__` requires `ui_manager` and `game` references. Follow the same pattern as `LevelCompletionScreen` for the captured background.

**Pause button (in-game HUD):** Add a small UIButton to `src/game/player_info_panel.py` with text "||" or "PAUSE", positioned at the top-right of the panel. Pressing it fires the same state change as Escape.

---

## 2.2 Fast-Forward

**Files to modify:**
- `src/config/config.py` — add `GAME_SPEED_MULTIPLIER: float = 1.0`
- `src/game/game.py` — in `update()` PLAYING branch, multiply `time_delta` by `configuration.GAME_SPEED_MULTIPLIER` before passing to managers; also multiply enemy speed: pass `time_delta * config.GAME_SPEED_MULTIPLIER` to `enemy_manager.update()`
- `src/game/player_info_panel.py` — add a "2x" toggle UIButton next to the pause button; on click, toggle `configuration.GAME_SPEED_MULTIPLIER` between `1.0` and `2.0`; button text reflects current speed

**Gotcha:** `clock.tick()` already caps FPS; the multiplier only affects simulation advancement, not render rate. Do not touch `clock.tick()`.

---

## 2.3 Tower Placement Preview

**Files to modify:**
- `src/board/tower_selection_panel.py` — expose `self.selected_tower_type: str | None`; set it on click; add a `deselect()` method
- `src/game/game.py` — in `draw()` PLAYING branch, after drawing towers, call `self._draw_placement_preview()`; implement `_draw_placement_preview()`:
  ```
  if tower_selection_panel.selected_tower_type is not None:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      snap to nearest grid cell (use TILE_SIZE from config)
      if game_board.can_build_at(grid_x, grid_y):
          tint = (0, 200, 0, 100)  # green semi-transparent
      else:
          tint = (200, 0, 0, 100)  # red semi-transparent
      blit tower sprite at snapped position with alpha overlay
      draw range circle: pygame.draw.circle(screen, constants.RGB_GOLD_BRIGHT, center, tower.attack_range, 1)
  ```
- `src/entities/towers/tower.py` — add a classmethod or static helper `get_preview_surface(tower_type)` that returns a pre-loaded semi-transparent sprite (alpha=140)

**Gotcha:** `TILE_SIZE` in `config.py` is a tuple `(width, height)`; snap with `grid_x = mouse_x // TILE_SIZE[0]`, `grid_y = mouse_y // TILE_SIZE[1]`.

---

## 2.4 Tower Selection (click placed tower)

When the player clicks a placed tower (not during placement), show a compact info/action panel.

**Files to modify:**
- `src/managers/tower_manager.py` — add `self.selected_tower: Tower | None = None`; in a new method `handle_click(pos)`, check if `pos` is within any tower's rect; if yes, set `selected_tower`; if the click is on empty ground outside the panel, clear selection
- `src/game/game.py` — in `draw()` PLAYING branch, after drawing towers, if `tower_manager.selected_tower` is set, call `self._draw_tower_info_panel(tower)`
- New method `Game._draw_tower_info_panel(tower)` — draws a 200×160px panel (styled with `constants.RGB_BG_DARK` fill + `constants.RGB_AMBER` border, `constants.RADIUS_MD` corners) to the right of the board showing: tower name, damage, range, attack speed; "Upgrade (X gold)" button if `tower.can_upgrade()`; "Sell (X gold)" button
- Wire "Upgrade" click → `tower_manager.upgrade_tower(selected_tower, player)`; "Sell" → `tower_manager.sell_tower(selected_tower, player)` (implement sell: remove tower, refund `tower.sell_value` gold)
- Wire "Deselect" on Escape while a tower is selected (before Pause)

**Gotcha:** `upgrade_tower()` already exists in `tower_manager.py:47` but is unreachable. Wire it here. `sell_value` is calculated in `tower.py:31` but never used — use it for the refund amount.

---

## 2.5 Tower Range Circles (always visible option)

Add a toggle so players can see all tower ranges permanently.

**Files to modify:**
- `src/managers/tower_manager.py` — add `self.show_ranges: bool = False`; in a new method `toggle_ranges()`, flip the bool
- `src/game/game.py` — in `draw()` PLAYING branch, after `tower_manager.draw_towers()`, iterate towers: if `tower_manager.show_ranges`, draw a circle with `pygame.draw.circle(screen, constants.RGB_GOLD_BRIGHT + (80,), tower.center, tower.attack_range, 1)` — use alpha surface for the semi-transparent fill
- `src/game/player_info_panel.py` — add a "Ranges" toggle button; on click, call `game.tower_manager.toggle_ranges()`

---

## 2.6 Tower Tooltips on Hover

**Files to modify:**
- `src/managers/tower_manager.py` — in update or a new `handle_hover(pos)` method, check if mouse is over a tower; if yes, return that tower; if no, return None
- `src/game/game.py` — in the event loop (via event_manager), on `pygame.MOUSEMOTION`, check `tower_manager.handle_hover(event.pos)`; if a tower is returned, call `UI_manager.show_tooltip(tower)` (see below); on MOUSEBUTTONDOWN, clear tooltip
- `src/managers/ui_manager.py` — add `show_tooltip(tower)` and `hide_tooltip()` methods that create/destroy a `pygame_gui.elements.UITooltip`; the tooltip content: `f"{tower.name}\nDamage: {tower.damage}\nRange: {tower.attack_range}\nSpeed: {tower.attack_speed}\nValue: {tower.sell_value}g"`

---

## 2.7 Health Bar + Wave Info Widget

Replace the text-only player info panel with a visual-first design.

**File to modify:** `src/game/player_info_panel.py`

Current labels: Gold, Health, Score, Enemies — all plain text. Replace Health with a rendered bar:

```
def _draw_health_bar(surface, x, y, width, height, current, maximum):
    # Background track
    pygame.draw.rect(surface, constants.RGB_BG_MID, (x, y, width, height), border_radius=4)
    # Fill
    fill_w = int(width * current / maximum)
    color = constants.RGB_HEALTH_GREEN if current / maximum > 0.5 else constants.RGB_HEALTH_RED
    pygame.draw.rect(surface, color, (x, y, fill_w, height), border_radius=4)
    # Border
    pygame.draw.rect(surface, constants.RGB_AMBER, (x, y, width, height), 1, border_radius=4)
```

Add a wave progress label: `f"Wave {current_wave}/{total_waves}"` and `f"{enemies_remaining} remaining"`. These values come from `enemy_manager` which is already passed to `player_info_panel.update()`.

---

## 2.8 Wave Panel Rebuild

The current `src/board/wave_panel.py` has `panel_y = 600` hardcoded, no ruler, and no wave-detail display.

**File to modify:** `src/board/wave_panel.py`

- Replace `panel_y = 600` with `panel_y = SCREEN_HEIGHT - 40` (SCREEN_HEIGHT from config)
- Add a background track: `pygame.draw.rect(screen, constants.RGB_BG_DARK, (0, panel_y, SCREEN_WIDTH, 40))`
- Add a gold border line at the top of the panel: `pygame.draw.line(screen, constants.RGB_AMBER, (0, panel_y), (SCREEN_WIDTH, panel_y), 2)`
- Each wave button: show wave number prominently; tooltip (via pygame-gui) showing enemy types in that wave
- Display the early-wave bonus gold amount directly on the button: `f"+{bonus}g"` in `constants.GOLD_INCOME` color

---

## Sound Integration (cross-cutting)

Use `game.audio_manager.play_sound(constants.SFX_SUCCESS)` on level completion trigger in `game_state_manager.py` (`open_complete_screen`).
Use `game.audio_manager.play_sound(constants.SFX_UNLOCK)` when a new level is unlocked in `player.complete_level()`.
Use `constants.SFX_TOWER_BUILD` on tower placement (already partially wired in tower_manager.py — verify it uses the constant not a hardcoded path).

---

## Acceptance Checklist

- [ ] Pressing Escape pauses the game; pressing again resumes
- [ ] 2x button doubles game speed visibly (enemies move faster)
- [ ] Hovering mouse over board while a tower is selected shows ghost tower + green/red tint + range circle
- [ ] Clicking a placed tower opens info panel showing stats, upgrade, sell
- [ ] "Ranges" toggle shows/hides all tower coverage circles simultaneously
- [ ] Health bar renders as a colored bar, not plain text
- [ ] Wave panel is anchored to bottom of screen (not hardcoded 600px)
- [ ] Level complete plays a success sound
