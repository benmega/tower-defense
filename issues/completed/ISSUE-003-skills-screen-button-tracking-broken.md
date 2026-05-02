# ISSUE-003 - Skills Screen Button Tracking Broken

## Type
Bug

## Priority
Medium

## Source
`docs/KNOWN_ISSUES.md`

## Summary
Skills screen creates UI buttons but likely fails to track them in the collection used by upgrade-processing logic.

## Problem Statement
- `src/screens/skills_screen.py` creates buttons.
- Buttons are not appended to `self.skill_buttons`.
- Upgrade flow iterates `self.skill_buttons`, so user actions may never map to upgrade execution.

## Expected Behavior
All interactable skill buttons are registered in the same collection consumed by click/upgrade processing logic.

## Scope
- Fix button registration lifecycle in skills screen.
- Verify button list reflects rendered buttons.
- Confirm upgrade callback path is triggered from UI interactions.

## Suggested Technical Approach
1. Ensure every created skill button is appended to `self.skill_buttons`.
2. Reset/rebuild `self.skill_buttons` safely when screen refreshes to avoid stale references.
3. Validate mapping between button metadata and upgrade target.

## Acceptance Criteria
- Clicking a skill button triggers corresponding upgrade logic.
- `self.skill_buttons` count matches displayed skill buttons.
- No duplicate button references after screen re-entry/rebuild.

## Validation / Test Plan
- Manual test: open skills screen, click upgrades, verify stat/resource changes.
- Add or update tests for:
  - button registration count,
  - click-to-upgrade path execution.

## Risks / Notes
- Ensure this does not regress other UI lists using similar create-and-track patterns.
