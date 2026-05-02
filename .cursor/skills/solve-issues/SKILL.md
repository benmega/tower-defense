---
name: solve-issues
description: Resolve tracked repository issues end-to-end with a reproducible workflow. Use when the user asks to solve/fix/triage an issue, references `issues/open/ISSUE-*.md`, or invokes /solve-issues.
---

# Solve Issues

## Goal

Close one issue at a time with a minimal, verified patch that matches this codebase's architecture and issue contracts.

## Inputs

Collect these before coding:
- Target issue file in `issues/open/` (or ask user to choose one).
- Reproduction steps from the issue and/or user.
- Expected behavior, acceptance criteria, and test plan from the issue.

## Repo-Specific Orientation

Use these as primary references:
- Runtime ownership: `docs/ARCHITECTURE.md`
- Triage flows: `docs/WORKFLOWS.md`
- Known risk areas: `docs/KNOWN_ISSUES.md`

Core execution path to trace first:
- `src/game/game.py` (`Game.update`)
- `src/managers/event_manager.py`
- `src/managers/level_manager.py`
- `src/game/level.py`
- `src/managers/enemy_manager.py`

## Workflow

Copy and execute this checklist:

- [ ] 1) Read the issue file and restate root symptom + expected behavior in 1-2 sentences.
- [ ] 2) Reproduce with the shortest sequence possible (manual gameplay and/or test).
- [ ] 3) Trace the nearest ownership boundary where behavior diverges:
      - UI/event bugs: `pygame event -> EventManager -> screen handler`
      - Simulation bugs: `Game.update -> LevelManager -> Level -> EnemyManager`
      - Data/path bugs: config constants and loading boundaries
- [ ] 4) Apply the smallest fix in the authoritative owner module (avoid broad refactors).
- [ ] 5) Validate acceptance criteria from the issue:
      - direct reproduction now passes,
      - adjacent flow smoke test passes,
      - no shape/signature regressions at touched boundaries.
- [ ] 6) Add or update focused tests when practical (especially contracts and regressions).
- [ ] 7) Move the resolved issue file from `issues/open/` to `issues/completed/` once you are satisfied the fix is correct.
- [ ] 8) Summarize: root cause, fix, verification evidence, and residual risks.

## Fix Rules

- Keep scope narrow and local to one subsystem when possible.
- Standardize contracts at boundaries (list shape, callback signature, coordinate model).
- If issue and runtime disagree, align to current runtime behavior unless user requests a breaking change.
- After successful validation, move the issue markdown file from `issues/open/` to `issues/completed/` in the same change set.
- Do not clean unrelated files in dirty trees.

## Validation Standard

Run targeted validation first, then broaden only as needed:

1. Focused test(s) for changed behavior.
2. Relevant integration path (e.g., wave progression, options sliders).
3. Manual smoke flow: main menu -> campaign map -> level play loop.

If full suite is noisy/stale, report exactly what was run and why.

## Output Format

Return results in this structure:

```markdown
Issue: ISSUE-###

Root cause
- ...

Changes made
- `path/to/file.py`: ...

Verification
- Command/manual step: result

Acceptance criteria status
- [x] ...
- [ ] ... (if blocked, explain)

Risks / follow-ups
- ...
```

## Escalation Triggers

Stop and ask before continuing when:
- Multiple issues are coupled and require architectural refactor.
- Reproduction is impossible without missing assets/data/user action.
- Fix would intentionally change gameplay balance or save-data format.
