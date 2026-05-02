# ISSUE-006 - Relative Path Fragility

## Type
Bug / Reliability

## Priority
Medium

## Source
`docs/KNOWN_ISSUES.md`

## Summary
File loading/saving currently assumes process working directory equals repository root, which can break runtime behavior in alternate launch contexts.

## Problem Statement
- Multiple code paths reference relative locations such as:
  - `assets/...`
  - `src/save_data/...`
- Running from a different CWD can fail to load assets or save data.

## Expected Behavior
Paths resolve reliably regardless of process working directory (IDE, CLI, tests, packaged builds).

## Scope
- Replace fragile relative path construction with project-root-aware or module-relative path utilities.
- Centralize path resolution to one helper/config layer.
- Ensure save and asset paths are both covered.

## Suggested Technical Approach
1. Add helper(s) that resolve from stable base (e.g., repo root or module root).
2. Refactor direct string paths in managers/screens/config loaders to helper calls.
3. Keep path joins OS-safe.
4. Add fallback/error reporting when files are missing.

## Acceptance Criteria
- Game can launch from non-root working directory without asset/save path failures.
- Save/load and asset loading both function in tests and normal runtime.
- No hardcoded path assumptions remain in critical load/save flows.

## Validation / Test Plan
- Start game from at least two different CWDs and verify behavior.
- Add regression tests for path helper resolution.

## Risks / Notes
- Coordinate with any future packaging/distribution workflow so path strategy remains compatible.
