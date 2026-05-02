# ISSUE-015 - Collision Manager Uses Inconsistent Position Contract

## Type
Bug Risk / Architecture Consistency

## Priority
Medium

## Source
Codebase review (`src/managers/collision_manager.py`, `src/entities/enemies/enemy.py`, `src/entities/entity.py`)

## Summary
`CollisionManager.check_collision(...)` assumes `x/y/width/height` attributes, while core entities are primarily rect-based sprites.

## Problem Statement
- `src/managers/collision_manager.py` builds rects from:
  - `entity.x`, `entity.y`, `entity.width`, `entity.height`
- Several runtime entities (e.g., enemies) expose `rect` as authoritative position and may not define `x/y`.
- This mismatch creates fragile collision behavior and potential `AttributeError` if `check_collision(...)` is used with rect-only entities.

## Expected Behavior
Collision helpers should use one consistent spatial contract across the entity model (prefer `pygame.sprite.Sprite.rect` for sprite-based systems).

## Scope
- Align collision helper methods with sprite `rect` contract.
- Ensure both pairwise and group collision paths operate on compatible entity data.
- Document expected entity interface for collision utilities.

## Suggested Technical Approach
1. Update `check_collision(...)` to use existing `rect` attributes when available.
2. Add compatibility fallback only if needed for non-sprite objects.
3. Add tests covering both sprite-based and legacy entity representations.

## Acceptance Criteria
- Collision checks work for rect-based entities without requiring `x/y` duplication.
- No attribute errors from collision helpers under normal gameplay objects.
- Collision behavior remains consistent between helper methods.

## Validation / Test Plan
- Add unit tests for pairwise collisions using sprite entities.
- Compare outcomes from `check_collision(...)` and `handle_group_collisions(...)` on equivalent inputs.
- Manual smoke test for projectile-enemy collision flow.

## Risks / Notes
- This overlaps with broader coordinate-model consistency work; resolve contracts in tandem to avoid partial fixes.
