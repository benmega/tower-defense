# ISSUE-013 - Test Module Paths and APIs Out of Sync With Runtime

## Type
Quality / Test Reliability

## Priority
High

## Source
Codebase review (`src/tests/test_game_logic/test_tower_manager.py`)

## Summary
Some tests reference outdated module paths and constructor APIs that no longer match production code, reducing trust in test results.

## Problem Statement
- `src/tests/test_game_logic/test_tower_manager.py` imports:
  - `from src.game.tower_manager import TowerManager`
- Actual runtime module is under:
  - `src/managers/tower_manager.py`
- Test setup also instantiates `TowerManager()` with no required `player` argument, while runtime `TowerManager.__init__(self, player)` requires one.
- Similar drift indicates stale assumptions in test scaffolding.

## Expected Behavior
Tests should import current modules and construct objects using the same API contracts as runtime code.

## Scope
- Fix outdated imports and constructor usage in affected tests.
- Audit related test files for parallel module/API drift patterns.
- Ensure test scaffolds include valid fixtures/mocks for required dependencies.

## Suggested Technical Approach
1. Replace stale import paths with current package locations.
2. Introduce shared test fixtures for commonly required dependencies (e.g., mock `player`).
3. Add a lightweight smoke test to assert key managers instantiate with test doubles.

## Acceptance Criteria
- Tests import runtime modules without path errors.
- Manager/object construction in tests matches current signatures.
- Test failures (if any) are behavioral, not import/signature mismatches.

## Validation / Test Plan
- Run targeted tests for `test_tower_manager.py`.
- Run broader suite after path/signature updates.
- Add CI check to catch import errors early.

## Risks / Notes
- API churn can quickly invalidate tests; consider a fixture layer to centralize adaptation.
