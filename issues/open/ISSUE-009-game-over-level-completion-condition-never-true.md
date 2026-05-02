# ISSUE-009 - Game Over Level Completion Condition Never True

## Type
Bug / State Logic

## Priority
High

## Source
Codebase review (`src/game/game.py`)

## Summary
The game-over completion branch compares incompatible types, preventing the final-level completion condition from evaluating correctly.

## Problem Statement
- `src/game/game.py` in `check_game_over()` contains:
  - `if self.level_manager.get_current_level() == len(self.level_manager.levels):`
- `get_current_level()` returns a `Level` object or `None`, while `len(...)` is an integer.
- This condition is effectively always false, so the intended completion path cannot trigger via this branch.

## Expected Behavior
End-of-campaign logic should compare compatible values (e.g., current level index vs total level count) and reliably detect completion.

## Scope
- Fix completion comparison logic in `Game.check_game_over()`.
- Ensure completion state transitions occur when the final level and waves are actually finished.
- Align completion checks with existing `LevelManager` indexing semantics.

## Suggested Technical Approach
1. Replace object-vs-int comparison with index-based check:
   - `current_level_index == len(levels) - 1` (or equivalent).
2. Pair index check with wave/enemy completion conditions already used elsewhere.
3. Add test coverage for final-level completion path.

## Acceptance Criteria
- Completion check evaluates true when the final level is fully complete.
- No false positives mid-campaign.
- State transition to completion flow is reachable through normal gameplay.

## Validation / Test Plan
- Simulate completion of last configured level and verify transition behavior.
- Add regression test for `check_game_over()` completion branch.
- Confirm non-final levels do not trigger completion.

## Risks / Notes
- Completion logic currently exists in multiple places; consolidate criteria to avoid future divergence.
