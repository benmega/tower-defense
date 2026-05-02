# Skill: UI Event Routing Debug

## Use When

- Buttons/sliders/dialogs do nothing or crash.
- Behavior differs between screens.

## Procedure

1. Identify triggering UI element and active state.
2. Trace event path:
   - `pygame` event -> `src/managers/event_manager.py` -> target screen method.
3. Validate:
   - handler mapping for current `GameState`,
   - method signature alignment,
   - visibility/open/close state of screen elements.
4. Apply smallest fix (dispatch map or target handler).
5. Retest one neighboring screen that shares dispatch branch.

## Common Failure Patterns

- Argument mismatch between dispatch and handler.
- Screen method exists but is unreachable from current state map.
- Hidden/inactive controls receiving no effective events.

## Expected Output

- Event path summary.
- Corrected mapping/signature.
- Manual verification steps and result.
