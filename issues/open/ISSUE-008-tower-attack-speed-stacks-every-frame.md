# ISSUE-008 - Tower Attack Speed Stacks Every Frame

## Type
Bug / Gameplay Balance

## Priority
High

## Source
Codebase review (`src/managers/tower_manager.py`)

## Summary
Tower attack speed is permanently increased every update tick, causing runaway firing-rate behavior over time.

## Problem Statement
- `src/managers/tower_manager.py` applies player `attack_speed` skill in `update(...)`:
  - `tower.attack_speed += attack_speed_increase`
- Because this executes every frame, attack speed grows without bound instead of representing a stable per-level modifier.
- Side effects include:
  - exponential combat pacing drift,
  - invalid balancing versus intended skill progression,
  - non-deterministic tower behavior after long runs.

## Expected Behavior
Attack-speed skill modifies tower cadence in a bounded, deterministic way (e.g., one-time stat application or derived value each frame without mutating the base stat repeatedly).

## Scope
- Correct the tower attack-speed skill application path in `TowerManager.update(...)`.
- Ensure tower attack cadence remains stable for identical inputs over time.
- Clarify whether skill effects are additive, multiplicative, or computed from a base stat.

## Suggested Technical Approach
1. Store immutable/base tower attack speed separately from current runtime cadence.
2. Compute effective attack speed from base + skill level, without cumulative mutation each frame.
3. Apply skill changes on tower creation/upgrade or via a recompute step when skill level changes.
4. Add a guard test that simulates many frames and asserts bounded attack-speed value.

## Acceptance Criteria
- Tower attack speed does not increase continuously across frames at a fixed skill level.
- Long-running sessions preserve consistent tower cadence.
- Skill-based attack-speed bonus still affects gameplay as designed.

## Validation / Test Plan
- Run a fixed-length simulation and compare tower cadence at frame 1 vs frame N.
- Add unit/integration regression test for `TowerManager.update(...)` stat stability.
- Manual gameplay check: tower fire rate remains consistent over time.

## Risks / Notes
- Any change to attack cadence impacts difficulty and economy tuning; retune related balance if needed.
