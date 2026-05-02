# Skill: Test Rehabilitation

## Use When

- Existing tests fail due to drift, placeholders, or fragile assumptions.

## Procedure

1. Run targeted subset of tests for touched subsystem.
2. Classify each failure:
   - stale import/signature,
   - true regression,
   - incomplete placeholder.
3. Fix stale wiring first so meaningful failures surface.
4. Replace implementation-coupled assertions with behavior-level expectations.
5. Keep tests deterministic and minimal.
6. Document gaps that remain intentionally deferred.

## Prioritized Areas

- State transitions (`main menu`, `campaign map`, `playing`, `level end`).
- Wave spawn and completion flow.
- Tower/projectile/enemy interaction contract.
- Save/load and unlock progression.

## Expected Output

- Reduced false-failure noise.
- Reliable tests around changed behavior.
- Clear note of unresolved test debt.
