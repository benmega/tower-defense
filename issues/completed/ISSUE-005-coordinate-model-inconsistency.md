# ISSUE-005 - Coordinate Model Inconsistency

## Type
Technical Debt / Bug Risk

## Priority
Medium

## Source
`docs/KNOWN_ISSUES.md`

## Summary
Entity rendering and movement use mixed coordinate sources (`x/y` vs `rect`), creating drift risk and unclear spatial authority.

## Problem Statement
- Base `Entity.draw()` references `self.x` / `self.y`.
- Many concrete classes appear to use `rect` as primary position state.
- Mixed state model can cause:
  - rendering at stale positions,
  - collision mismatches,
  - fragile subclass behavior.

## Expected Behavior
Position authority is consistent across entity lifecycle (update, collision, draw), with clear synchronization rules.

## Scope
- Decide canonical coordinate authority (`rect` recommended for pygame-style collision/draw workflows).
- Align base `Entity` and subclasses to the same model.
- Remove redundant position state or enforce synchronization boundaries.

## Suggested Technical Approach
1. Audit `Entity`, enemy, tower, and projectile position reads/writes.
2. Standardize draw and collision on one coordinate source.
3. If both representations remain, add explicit sync methods and invariant checks.
4. Update docstrings/comments to codify the contract.

## Acceptance Criteria
- Draw, movement, and collision all use consistent position authority.
- No observable sprite offset/drift across moving entities.
- Position contract is documented in core entity abstractions.

## Validation / Test Plan
- Manual test: moving enemies/projectiles maintain visual-collision alignment.
- Add targeted tests for position updates and draw coordinate consistency.

## Risks / Notes
- Coordinate contract changes can affect many classes; execute after critical gameplay bugs are stabilized.
