# Agent Onboarding Guide

## Mission

Preserve gameplay stability while iterating toward cleaner architecture and reliable tests.

## First 30 Minutes Checklist

1. Read:
   - `README.md`
   - `docs/ARCHITECTURE.md`
   - `docs/KNOWN_ISSUES.md`
2. Open core runtime files:
   - `src/game/game.py`
   - `src/managers/event_manager.py`
   - `src/managers/level_manager.py`
   - `src/managers/enemy_manager.py`
   - `src/game/level.py`
3. Validate game starts from repo root:
   - `python -m src.main` (or `python src/main.py`)
4. Pick one focused scope (simulation, UI state, tests, or data paths).

## Working Rules

- Avoid broad refactors unless requested.
- Keep changes localized to one subsystem when possible.
- Pair code changes with validation steps (manual and/or tests).
- Assume some existing tests are stale; inspect failures before fixing.
- Never remove unrelated existing work in a dirty tree.

## High-Value Debugging Sequence

1. Reproduce in-game with the smallest sequence possible.
2. Add temporary prints only if necessary and remove before finalizing.
3. Trace state and ownership boundaries:
   - state transition (`GameStateManager`),
   - event dispatch (`EventManager`),
   - simulation update ordering (`Game.update`).
4. Confirm data shape at boundaries (e.g., enemy list vs enemy object).
5. Add/update focused tests after behavior is stable.

## Risk Zones

- Wave spawning and enemy lifecycle.
- UI event routing signatures.
- Skill screen controls and skill button wiring.
- Path/asset loading behavior when working directory differs.

## What Good Changes Look Like

- Small patch, clear intent, and direct verification.
- No behavior regressions in main menu -> campaign map -> level play loop.
- Improved docs/tests for changed behavior.
