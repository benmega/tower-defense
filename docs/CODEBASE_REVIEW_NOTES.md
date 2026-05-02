# Codebase Review Notes

## Scope

Review covered architecture, runtime update flow, manager/screen coupling, test posture, and data/path assumptions.

## Key Observations

- Composition is centralized in `src/game/game.py` and currently very concrete-coupled.
- State-driven UI is clear conceptually but relies on fragile method-signature alignment.
- Wave spawning logic appears split across modules, increasing duplication/regression risk.
- Test suite has useful structure but contains stale and placeholder tests.

## Strong Points

- Clear separation of directories by concern (entities/managers/screens/board/config).
- Rich content setup for towers/projectiles/enemies in config.
- Existing integration test folder provides a good anchor for future quality gates.

## Main Bottlenecks

- Ownership boundaries are not always singular (especially in spawn pipeline).
- Runtime path assumptions can cause environment-specific failures.
- Some screen interactions are likely partially implemented.

## Recommendation

Preserve current architecture for now, but prioritize boundary cleanup and test stabilization before adding major features.
