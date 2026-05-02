# Contributor Workflows

## Workflow 1: Bug Triage (Default)

1. Reproduce issue with minimal steps.
2. Identify subsystem owner:
   - events/state/UI -> `src/managers/event_manager.py`, `src/managers/game_state_manager.py`, `src/screens/`
   - simulation -> `src/game/game.py`, `src/game/level.py`, `src/managers/*_manager.py`
3. Inspect nearest boundary where data/flow can break.
4. Implement smallest safe fix.
5. Validate manually in game.
6. Add or update focused test if practical.

## Workflow 2: UI/Event Regression

1. Reproduce interaction in one screen.
2. Trace dispatch path:
   - Pygame event -> `EventManager` -> screen handler.
3. Verify method signatures and argument count across boundary.
4. Apply fix in one location first; avoid broad signature churn.
5. Smoke-test other screens that use same dispatch path.

## Workflow 3: Wave/Enemy Simulation Issue

1. Start at `Game.update()` in `PLAYING` branch.
2. Track new enemy production path:
   - `LevelManager.update_levels()` -> `Level.update_level()` -> `EnemyManager.update()`.
3. Confirm ownership:
   - decide where spawning is authoritative for the bug under investigation.
4. Fix data shape/order issue.
5. Validate:
   - expected enemy spawn cadence,
   - no duplicate spawns,
   - level-complete transition still works.

## Workflow 4: Test Rehabilitation

1. Classify failing tests into:
   - stale API import/signature mismatch,
   - behavior regression,
   - placeholder/incomplete.
2. Repair import/signature drift first.
3. Replace brittle assumptions with behavior-level assertions.
4. Prioritize tests for:
   - state transitions,
   - wave spawning completion,
   - tower/projectile/enemy interaction contracts,
   - save/load and level unlock persistence.

## Workflow 5: Asset/Path Failures

1. Confirm command run location (root vs subfolder).
2. Inspect config path constants and helper load functions.
3. Normalize path resolution near loading boundary.
4. Validate at least one image + one audio load path in runtime.

## Definition of Done (Per Task)

- Behavior fixed and manually verified.
- No obvious regressions in adjacent flow.
- Notes/test updates included when warranted.
- Scope remains narrow and comprehensible.
