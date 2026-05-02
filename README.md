# Tower Defense (Foundation Docs)

This repository contains a Pygame tower defense project with a working gameplay loop, state-driven UI flow, and an evolving test suite.

This document is intentionally focused on helping new contributors and future coding agents get productive quickly.

## Current Snapshot

- **Language/runtime:** Python 3, Pygame, pygame_gui
- **Entry point:** `src/main.py`
- **Core composition root:** `src/game/game.py`
- **Level content:** `src/config/levels/LevelsAll.json`
- **Primary configuration:** `src/config/config.py`
- **Tests:** `src/tests/` (mixed quality; see `docs/KNOWN_ISSUES.md`)

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies used by the codebase:
   - `pygame`
   - `pygame_gui`
3. Run from repository root:
   - `python -m src.main`

If that import-style command fails in your environment, run:
- `python src/main.py`

## Project Layout

- `src/game/` - game loop, game state enum, level model.
- `src/managers/` - event routing, state transitions, entities/towers/projectiles/levels/audio/UI management.
- `src/entities/` - enemies, towers, projectiles, player, power-ups, gems.
- `src/screens/` - main menu, campaign map, options, skills, save/load data, level completion.
- `src/board/` - board drawing/build-logic and in-game panels.
- `src/config/` - gameplay constants, asset paths, level and theme data.
- `src/tests/` - unit/integration tests (contains stale and placeholder tests).
- `assets/` - images/audio assets.
- `docs/` - contributor/agent onboarding and workflows.

## Read This First

Before modifying code, review:

1. `docs/ARCHITECTURE.md`
2. `docs/AGENT_ONBOARDING.md`
3. `docs/WORKFLOWS.md`
4. `docs/KNOWN_ISSUES.md`

## Guardrails For Contributors

- Prefer small, isolated changes; this codebase has tightly coupled runtime paths.
- Verify behavior in-game for any simulation/UI change.
- Do not trust all tests as-is; some tests are out of sync with implementation.
- Keep working-directory assumptions in mind: several paths are relative.

## Foundation Goal

These docs establish a shared baseline so future contributors and agents can:

- onboard quickly,
- avoid rediscovering architectural hazards,
- and execute changes through repeatable workflows.
