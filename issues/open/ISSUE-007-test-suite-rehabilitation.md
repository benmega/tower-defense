# ISSUE-007 - Test Suite Rehabilitation

## Type
Quality / Test Infrastructure

## Priority
Medium

## Source
`docs/KNOWN_ISSUES.md`

## Summary
Current test suite contains stale and placeholder tests with outdated assumptions, reducing confidence and signal quality.

## Problem Statement
- Known risks include:
  - wrong import paths,
  - outdated constructor signatures,
  - behavior assertions misaligned with current architecture.
- Result: tests are partially untrusted and may block or mislead development.

## Expected Behavior
Test suite reflects current architecture, fails only for real regressions, and provides reliable guardrails for ongoing fixes.

## Scope
- Triage existing tests into:
  - valid,
  - fixable,
  - obsolete/deprecate.
- Repair highest-value integration and unit tests around active game systems.
- Establish a baseline for trusted CI-target tests.

## Suggested Technical Approach
1. Inventory failing tests and classify root causes.
2. Fix imports/signatures first (mechanical breakages).
3. Rewrite behavior assertions to match current contracts.
4. Quarantine or remove obsolete placeholder tests with clear rationale.
5. Document trusted test subsets for ongoing issue remediation.

## Acceptance Criteria
- A documented set of trusted tests passes consistently.
- Obvious stale/placeholder tests are either repaired or explicitly deprecated.
- Updated tests cover corrected behavior for high-priority issues.

## Validation / Test Plan
- Run full test suite and record pass/fail baseline.
- Run focused suites for spawn pipeline, UI events, and skills interactions after related fixes.
- Confirm deterministic local reruns.

## Risks / Notes
- Perform this work after critical behavior contracts are fixed to avoid rewriting tests against unstable interfaces.
