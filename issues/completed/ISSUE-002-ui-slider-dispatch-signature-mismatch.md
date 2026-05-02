# ISSUE-002 - UI Slider Dispatch Signature Mismatch

## Type
Bug

## Priority
High

## Source
`docs/KNOWN_ISSUES.md`

## Summary
The event dispatch system sends a different argument signature than the options screen handler expects for slider events.

## Problem Statement
- `src/managers/event_manager.py` dispatches slider callbacks as:
  - `on_slider_moved(ui_element, value, game)`
- `src/screens/options_screen.py` defines:
  - `on_slider_moved(self, ui_element, value)`
- Mismatch can trigger runtime exceptions or silently break settings updates.

## Expected Behavior
Slider event dispatch and handler signatures are aligned across the UI event routing path.

## Scope
- Resolve method-signature mismatch between event dispatch and options screen handlers.
- Verify all slider listeners across screens use the same contract.
- Confirm audio/settings updates still apply.

## Suggested Technical Approach
1. Choose a canonical slider handler signature (with or without `game`).
2. Update dispatcher and all subscribers to match.
3. If `game` context is required, standardize an event object or context wrapper instead of ad-hoc positional args.

## Acceptance Criteria
- No exceptions when moving sliders in options UI.
- Slider values apply immediately and persist as designed.
- All slider callback implementations match dispatcher signature.

## Validation / Test Plan
- Manually move each slider in options screen and verify effect.
- Add regression tests for event manager dispatch signature compatibility.
- Run UI smoke test for settings screen interactions.

## Risks / Notes
- Closely related to UI event routing reliability; ensure no similar mismatches in button/toggle handlers.
