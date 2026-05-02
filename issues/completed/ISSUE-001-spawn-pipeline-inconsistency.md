# ISSUE-001 - Spawn Pipeline Inconsistency

## Type
Bug

## Priority
Critical

## Source
`docs/KNOWN_ISSUES.md`

## Summary
Enemy spawning responsibilities are split across multiple systems, creating inconsistent data flow and risk of duplicate or malformed enemy spawns.

## Problem Statement
- `src/managers/level_manager.py` appends the result of `current_level.update_level(...)` into `new_enemies`.
- `src/game/game.py` iterates `new_enemies` and adds each item into `EnemyManager`.
- `src/managers/enemy_manager.py` also calls `wave.update(...)`, suggesting a second spawn path.
- Current behavior risks:
  - duplicate spawns,
  - nested list shapes in `new_enemies`,
  - ownership confusion between level and enemy systems.

## Expected Behavior
There is a single authoritative owner for enemy spawn generation, and the downstream API consumes one consistent enemy collection shape.

## Scope
- Clarify spawn ownership between:
  - `Level`/`LevelManager`,
  - `Game` loop,
  - `EnemyManager`/wave logic.
- Normalize return type for spawn output.
- Remove duplicate spawning call path.

## Suggested Technical Approach
1. Define contract:
   - `Level.update_level(...) -> list[Enemy]` (flat list, empty if no spawn).
2. Ensure only one subsystem calls wave update logic.
3. Update `Game` loop to consume normalized output exactly once.
4. Add defensive assertion/logging for unexpected spawn payload types during transition.

## Acceptance Criteria
- No duplicate enemy spawns from a single wave event.
- Spawn output entering `EnemyManager` is always a flat list of enemy instances.
- Exactly one call path triggers wave spawn update per frame.
- Existing gameplay still progresses waves normally.

## Validation / Test Plan
- Run a gameplay scenario with multiple waves and verify spawn counts per wave.
- Add or update tests around:
  - spawn output shape contract,
  - single-spawn-path behavior,
  - wave progression integration.

## Risks / Notes
- This issue is foundational; resolve before other gameplay fixes that depend on spawn timing.
