# ISSUE-014 - Pathfinding Core Function Is Unimplemented

## Type
Bug / Missing Core Functionality

## Priority
High

## Source
Codebase review (`src/utils/pathfinding.py`)

## Summary
`find_path(...)` is a stub (`pass`) and currently provides no pathfinding behavior.

## Problem Statement
- `src/utils/pathfinding.py` defines:
  - `def find_path(start, goal, game_board):`
  - body: `pass`
- Any gameplay or tooling that relies on this utility cannot compute routes.
- This blocks expected path-based validation (e.g., board/path integrity tests).

## Expected Behavior
`find_path(...)` should return a valid path representation (or explicit no-path result) for a given board and endpoints.

## Scope
- Implement `find_path(...)` with a defined algorithm and return contract.
- Define behavior for blocked/no-path scenarios.
- Align tests and callers with one canonical path format.

## Suggested Technical Approach
1. Implement A* or BFS depending on grid weighting requirements.
2. Define return contract clearly:
   - ordered coordinate list when path exists,
   - empty list/`None` when unreachable.
3. Add unit tests for normal, blocked, and edge-case boards.

## Acceptance Criteria
- `find_path(...)` returns deterministic valid paths on traversable grids.
- No-path scenarios are handled predictably without crashes.
- Existing and new pathfinding tests pass against the declared contract.

## Validation / Test Plan
- Add focused tests for:
  - direct path,
  - obstacle detour,
  - unreachable destination.
- Run integration checks where board/path data is consumed by gameplay logic.

## Risks / Notes
- Path contract should be coordinated with board coordinate model to avoid mismatched units.
