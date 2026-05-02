# ISSUE-004 - Frame Timing Main Loop Double Tick

## Type
Bug / Performance Stability

## Priority
Medium

## Source
`docs/KNOWN_ISSUES.md`

## Summary
Frame timing appears to be advanced multiple times per loop iteration, which can destabilize simulation speed and UI responsiveness.

## Problem Statement
- `src/game/game.py` calls `clock.tick(FPS)` twice in one main-loop iteration.
- `update_ui()` also calls `clock.tick(FPS)`.
- Multiple ticks per frame can distort delta timing and produce inconsistent frame pacing.

## Expected Behavior
Game loop performs exactly one authoritative frame tick per iteration, and subsystems consume the same frame timing data.

## Scope
- Consolidate clock tick ownership to one location in the main loop.
- Remove or refactor secondary tick calls in UI/update helpers.
- Ensure update/draw order remains correct.

## Suggested Technical Approach
1. Keep a single `dt = clock.tick(FPS)` in main loop.
2. Pass `dt` into update subsystems that need timing.
3. Remove direct tick calls from `update_ui()` and any helpers.
4. Verify no subsystem implicitly relies on independent ticking.

## Acceptance Criteria
- Only one `clock.tick(...)` call executes per frame iteration.
- Frame pacing is stable under normal gameplay.
- UI updates remain smooth and in sync with game state.

## Validation / Test Plan
- Manual playtest with FPS overlay/logging to confirm stable cadence.
- Optional instrumentation test to assert one-tick-per-loop contract.

## Risks / Notes
- Timing changes can reveal latent update-order assumptions; validate combat and wave timing after fix.
