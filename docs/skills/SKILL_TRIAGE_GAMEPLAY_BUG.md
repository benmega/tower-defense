# Skill: Triage Gameplay Bug

## Use When

- A bug is reported in gameplay simulation, waves, collisions, or tower attacks.

## Inputs To Gather

- Exact reproduction steps.
- Current `GameState` during failure.
- Expected vs observed behavior.

## Procedure

1. Reproduce with the shortest possible action sequence.
2. Start trace at `src/game/game.py` in `Game.update()`:
   - identify which manager call first diverges from expectation.
3. Follow ownership boundaries:
   - level/waves (`src/game/level.py`, `src/managers/level_manager.py`),
   - enemies (`src/managers/enemy_manager.py`),
   - towers/projectiles (`src/managers/tower_manager.py`, `src/managers/projectile_manager.py`).
4. Validate data shapes crossing boundaries.
5. Implement narrow fix in owner module.
6. Smoke-test main gameplay loop.

## Expected Output

- One-sentence root cause.
- Minimal patch touching the smallest subsystem.
- Verification notes for reproduction and retest.
