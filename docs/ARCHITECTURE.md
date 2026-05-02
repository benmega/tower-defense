# Architecture Reference

## Runtime Flow

1. `src/main.py` creates `Game` and calls `Game.run()`.
2. `Game.__init__` constructs the composition graph:
   - managers (`EventManager`, `GameStateManager`, `LevelManager`, etc.),
   - domain objects (`Player`, `GameBoard`, `TowerSelectionPanel`),
   - UI (`UIManager` and screens).
3. `Game.run()` sets state to `MAIN_MENU`, then loops:
   - process events,
   - update state/simulation,
   - draw frame.
4. `Game.update()` branches on `GameState` and drives either screen updates or gameplay simulation.
5. `Game.draw()` renders gameplay first (when playing), then UI, then flips the display.

## Module Responsibilities

### `src/game/`

- `game.py`: top-level orchestrator and loop.
- `game_state.py`: enum-like state model.
- `level.py`: wave scheduling and spawn progression inside a level.

### `src/managers/`

- `event_manager.py`: dispatches Pygame + pygame_gui events based on state.
- `game_state_manager.py`: transitions states and opens/closes corresponding UI screens.
- `level_manager.py`: loads levels, starts/resets level, updates waves, owns `WavePanel`.
- `enemy_manager.py`: stores/updates enemies and applies defeat/reach-end callbacks.
- `tower_manager.py`: tower placement, tower updates, and skill/stat modifiers.
- `projectile_manager.py`: projectile lifecycle.
- `collision_manager.py`: group collision handling.
- `audio_manager.py`: music and sound control.
- `ui_manager.py`: pygame_gui root and screen registry.

### `src/entities/`

- `enemies/`: enemy types + wave spawning (`enemy_wave.py`).
- `towers/`: base tower and specialized tower types.
- `projectiles/`: projectile base/specialized classes.
- `Player.py`: player resources, progression, skills.

### `src/screens/`

- Independent UI screens for menu/navigation flows.
- State transitions are tightly integrated with these classes.

### `src/board/`

- `game_board.py`: tile/path rendering and buildability checks.
- `tower_selection_panel.py`: tower selection panel interactions.
- `wave_panel.py`: wave start controls.

## Coupling Map (Important)

- `Game` directly composes nearly all concrete classes.
- `EventManager` directly maps states to specific screen handlers.
- `LevelManager` links simulation with UI (`WavePanel`).
- `TowerManager` and `Player.skills` are tightly coupled.
- `Projectile` logic assumes specific enemy methods/effects.

## Data Flow

- Config constants in `src/config/config.py`.
- Level definitions in `src/config/levels/LevelsAll.json`.
- Theme in `src/config/theme.json`.
- Save slots in `src/save_data/savegame_slot*.json`.

## Architectural Risks

- Spawn ownership split across `Level`, `LevelManager`, and `EnemyManager`.
- Inconsistent coordinate conventions (`rect` vs `x/y`) across entities.
- Event handler signature drift in UI interactions.
- Relative path assumptions can fail if launched from non-root CWD.
