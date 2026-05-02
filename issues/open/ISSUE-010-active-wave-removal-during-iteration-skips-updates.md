# ISSUE-010 - Active Wave Removal During Iteration Skips Updates

## Type
Bug / Wave Processing

## Priority
High

## Source
Codebase review (`src/game/level.py`)

## Summary
`Level.update_level(...)` mutates `active_waves` while iterating, which can skip wave updates and produce inconsistent spawn behavior.

## Problem Statement
- In `src/game/level.py`, `update_level(...)` loops over `self.active_waves`.
- Inside that loop, finished waves are removed with `self.active_waves.remove(wave)`.
- Removing from a list during iteration can shift indices and skip processing of subsequent entries in the same frame.
- This can distort:
  - spawn cadence,
  - wave-finished handling,
  - progression timing when multiple waves are active.

## Expected Behavior
Wave iteration should be stable and process each active wave exactly once per frame, without side effects from in-loop list mutation.

## Scope
- Refactor `Level.update_level(...)` to avoid mutating `self.active_waves` during direct iteration.
- Preserve spawn/update semantics for concurrent active waves.
- Re-validate wave completion and `current_wave_index` updates.

## Suggested Technical Approach
1. Iterate over a shallow copy (`for wave in list(self.active_waves):`) or collect finished waves and remove after loop.
2. Keep spawn aggregation logic unchanged except for iteration safety.
3. Add regression test with multiple active waves finishing near the same frame.

## Acceptance Criteria
- No skipped wave updates when multiple waves are active.
- Completed waves are removed deterministically.
- Spawn behavior remains consistent across repeated runs.

## Validation / Test Plan
- Instrument wave update counts per frame in a multi-wave scenario.
- Add test where two active waves can finish in the same update window.
- Verify expected enemy spawn counts and progression timing.

## Risks / Notes
- This issue compounds with broader spawn-pipeline concerns; validate alongside spawn ownership fixes.
