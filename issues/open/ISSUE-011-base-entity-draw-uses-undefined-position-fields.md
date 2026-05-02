# ISSUE-011 - Base Entity Draw Uses Undefined Position Fields

## Type
Bug / Rendering Contract

## Priority
High

## Source
Codebase review (`src/entities/entity.py`)

## Summary
Base `Entity.draw()` blits using `self.x` / `self.y`, but base entity initialization defines `rect` and does not guarantee `x/y` attributes.

## Problem Statement
- `src/entities/entity.py` sets position via `self.rect = self.image.get_rect(...)`.
- `draw()` uses:
  - `screen.blit(self.image, (self.x, self.y))`
- Many entities are `pygame.sprite.Sprite`-style and use `rect` as their position source.
- If an entity subclass does not define `self.x` and `self.y`, draw path can raise `AttributeError`.

## Expected Behavior
Base entity rendering should use the canonical, guaranteed position model (typically `self.rect.topleft`) unless an explicit alternate contract exists.

## Scope
- Align base `Entity.draw()` with entity position authority.
- Verify subclasses do not rely on mixed/implicit coordinate fields.
- Document draw-position contract for entity subclasses.

## Suggested Technical Approach
1. Update base draw to use `self.rect` (`screen.blit(self.image, self.rect)` or `self.rect.topleft`).
2. If x/y are needed for specific subclasses, define sync rules explicitly.
3. Add a minimal unit test for drawing an `Entity` subclass that only defines `rect`.

## Acceptance Criteria
- Base `Entity.draw()` does not require undeclared `x/y` fields.
- Rendering works for rect-based entities without subclass-specific hacks.
- Position contract is consistent between update/collision/draw paths.

## Validation / Test Plan
- Instantiate and draw a rect-only entity subclass.
- Manual smoke test for enemy/tower rendering alignment.
- Run targeted tests touching entity drawing behavior.

## Risks / Notes
- Coordinate contract changes may affect collision/draw assumptions in older subclasses; audit impacted classes.
