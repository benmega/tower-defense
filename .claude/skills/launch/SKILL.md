---
name: launch
description: |
  Run a complete test-launch-debug cycle for the tower defense game. Syntax checks → unit tests → game launch → runtime monitoring → automated debugging → iterate until solid.
  
  Use this whenever the user types `/launch`, wants to verify the game works after changes, or needs a comprehensive validation cycle. This skill runs the full pipeline: pre-flight checks for syntax errors and missing dependencies, unit tests if they exist, launches the actual game, monitors for crashes during initial startup, and if issues occur, automatically debugs and attempts fixes up to 3 times before reporting back.
  
  The skill handles both import errors (missing modules, circular dependencies) and runtime errors (missing files, configuration issues). It's designed for iterative development — each fix cycles back through the test suite, so you can confidently make changes and validate them end-to-end.

compatibility: |
  Requires: Python 3.8+, pygame, pytest (optional but recommended)
  Platform: Windows (tested on tower defense game repo structure)
  
---

# /launch Skill: Automated Test-Launch-Debug Cycle

## Overview

This skill automates the full validation pipeline for the tower defense game, including building and testing the executable:

```
Phase 1: Pre-flight checks (syntax, imports, assets)
    ↓
Phase 2: Unit tests (pytest if available)
    ↓
Phase 3: Python game launch & 30-second stability test
    ↓
Phase 4: Build executable with PyInstaller
    ↓
Phase 5: Test built executable & stability monitor
    ↓
Phase 6: Debug loop (if errors, attempt auto-fix, max 3 cycles)
    ↓
Phase 7: Final report (summary, builds, fixes applied, remaining issues)
```

Each phase reports success/failure before moving to the next. If any phase fails, the skill either attempts an automated fix or stops and reports the issue.

---

## How to Invoke

Type or ask for `/launch` in any context where you want to validate the game. The skill will:
1. Run the full pipeline
2. Fix issues automatically when possible
3. Report results with clear pass/fail status for each phase
4. Return a "ready to play" status or list of issues needing attention

---

## Phase Details

### Phase 1: Pre-flight Checks (2-3 minutes)

**What it does:**
- Scans all `.py` files in `src/` for syntax errors (compile check)
- Validates imports on critical modules (game.py, game_state.py, managers/*, etc.)
- Checks for missing asset files referenced in code
- Reports file count and any issues

**Pass criteria:** No syntax errors, all imports valid, critical assets present

**Example output:**
```
✓ Syntax check: 42 Python files, no errors
✓ Import validation: game.py, managers, entities, screens all import successfully
✓ Asset check: 95 sprites, 18 sounds, all present
```

---

### Phase 2: Unit Tests (1-2 minutes if tests exist)

**What it does:**
- Looks for `tests/` or `test_*.py` files
- If found, runs pytest with summary output
- If not found, notes this and continues (not a failure)
- Reports pass/fail count

**Pass criteria:** All tests pass (or skip if none exist)

**Example output:**
```
✓ Tests: 12 passed in 1.2s
```

---

### Phase 3: Game Launch & Stability Monitor (1-2 minutes)

**What it does:**
- Attempts to launch the game with a 30-second timeout
- Monitors stderr/stdout for exceptions and crashes
- Catches both import-time errors (missing dependencies) and runtime errors (file not found, config issues)
- If the game survives 30 seconds without crashing, this phase passes

**Pass criteria:** Game launches and runs for 30 seconds without uncaught exceptions

**Example output:**
```
✓ Game launched successfully
✓ Stability test: 30 seconds, no exceptions
✓ Core imports: pygame, config, managers all loaded
```

**Fail example:**
```
✗ Game launch failed
  Error: ModuleNotFoundError: No module named 'src.utils.constants'
  Location: src/game/game.py line 45
```

---

### Phase 4: Debug Loop (Automatic, up to 3 iterations)

**What it does if Phase 3 fails:**
1. Analyzes the error message
2. Attempts automated fixes:
   - **Missing module**: Check if file exists, verify import path, check for circular dependencies
   - **Missing file/asset**: Locate file or suggest alternative
   - **Config error**: Review config.py for syntax or missing keys
   - **Import error**: Check for typos in import statements
3. After each fix attempt, re-runs Phase 1-3 to verify
4. If it works, reports the fix and moves to Phase 5
5. If still broken after 3 attempts, stops and reports what was tried

**Example output (successful fix):**
```
✗ First attempt failed: from src.utils.constants import RGB_OVERLAY
  Issue: constants.py file exists but module not in __init__.py

  Attempting fix #1: Verify __init__.py in src/utils/
  ✓ __init__.py exists, adding 'from . import constants'

  Re-testing...
  ✓ Phase 1-3 passed after fix
```

**Example output (unable to auto-fix):**
```
Attempted 3 fixes:
  1. Added missing import to __init__.py — still failed
  2. Checked circular dependency — not the issue  
  3. Validated all file paths — all correct

Unable to auto-resolve. Need manual review.
Issue: pygame.error: No available video mode for (1067, 800)
Recommendation: Check pygame/SDL initialization or display settings
```

---

### Phase 5: Final Report

**What it outputs:**
- Summary: ✓ or ✗ for each phase
- Total time elapsed
- Fixes applied (if any)
- Remaining issues (if any)
- Clear "Ready to play" or "Needs attention" status

**Example (all green):**
```
═══════════════════════════════════════════
LAUNCH REPORT — Tower Defense Game
═══════════════════════════════════════════

Phase 1: Pre-flight checks          ✓ PASS
Phase 2: Unit tests                 ✓ PASS (12/12)
Phase 3: Game launch & stability    ✓ PASS (30s)
Phase 4: Debug loop                 ✓ N/A (no issues)

Total time: 4m 32s
Fixes applied: 0
Final status: ✓ READY TO PLAY

Game is stable and ready for testing.
```

**Example (with fixes):**
```
═══════════════════════════════════════════
LAUNCH REPORT — Tower Defense Game
═══════════════════════════════════════════

Phase 1: Pre-flight checks          ✓ PASS
Phase 2: Unit tests                 ✓ PASS (12/12)
Phase 3: Game launch & stability    ✗ FAIL → Auto-fixed
Phase 4: Debug loop                 ✓ RESOLVED (1/3 attempts)

Total time: 6m 14s
Fixes applied:
  • Added 'from . import constants' to src/utils/__init__.py
  • Re-verified imports after fix: ✓ all pass

Final status: ✓ READY TO PLAY

Game is now stable. The issue was a missing __init__.py reference.
```

---

## Key Behaviors

### Auto-fix Strategy

The skill attempts fixes for **common, recoverable errors only**:
- ✓ Missing `__init__.py` imports
- ✓ Typos in import paths
- ✓ Missing config keys (can add defaults)
- ✓ Path issues (absolute vs relative)

It **does NOT** attempt:
- ✗ Logic changes to the game code
- ✗ Installing new packages (requires user decision)
- ✗ Refactoring code structure

### Error Categories

The skill categorizes errors and handles them differently:

| Error Type | Auto-fixable? | Behavior |
|-----------|---------------|----------|
| Syntax error | No | Report immediately, stop |
| Import error | Yes* | Try up to 3 fixes, then report |
| Missing asset | Partial | Check for file, suggest location |
| Config missing | Yes | Add sensible default, retest |
| Runtime crash | No | Report with traceback |

*Some import errors are fixable (missing __init__.py reference); others require code changes.

### Timeout & Safety

- Game launch timeout: 30 seconds
- Each debug attempt: 2 minutes max
- Total skill runtime: ~15 minutes max (hard limit)
- If anything hangs, the skill exits cleanly and reports

---

## What to Do With Results

### If Status = ✓ READY TO PLAY

The game is validated and stable. You can:
- Play/test the game manually
- Deploy to itch.io
- Commit changes confidently

### If Status = ✗ NEEDS ATTENTION

The skill will report:
1. What it tried to fix
2. What still isn't working
3. Suggested next steps

Common scenarios:
- **"Unable to fix after 3 attempts"** → Problem requires code changes; skill shows you the error and location
- **"Syntax error in X.py"** → Fix the Python syntax directly; re-run `/launch`
- **"Missing asset: sprites/tower.png"** → Find/add the asset; re-run `/launch`

---

## Running the Skill

When you invoke `/launch`:

1. **The agent will:**
   - Run all 5 phases in order
   - Print status updates as each phase completes
   - Attempt auto-fixes if Phase 3 fails
   - Provide a final report

2. **You can:**
   - Let it run (most automation is hands-off)
   - Stop early if you see a known issue
   - Ask the agent to skip a phase (e.g., "skip tests, just launch")

3. **After the report:**
   - Review the final status
   - If issues remain, the report will guide your next action
   - Re-run `/launch` after making fixes

---

## Technical Notes

### File Locations
- Game entry point: `src/main.py` or `src/game/game.py`
- Config: `src/config/config.py`
- Tests: `tests/` or `test_*.py` (if they exist)
- Assets: `assets/`

### Monitored Directories
- `src/` — all `.py` files scanned for syntax
- `src/game/`, `src/managers/`, `src/entities/`, `src/screens/` — import validation
- `assets/images/`, `assets/sounds/` — asset presence check

### Error Monitoring
The skill watches for:
- Python exceptions (uncaught during startup)
- Missing modules (ModuleNotFoundError, ImportError)
- File not found (FileNotFoundError, IOError)
- Config errors (KeyError, missing required settings)
- SDL/pygame init failures (video mode, audio init)

---

## Troubleshooting

**Q: The skill says "Game launched but test failed" — what does that mean?**
A: The game window opened, but something crashed during the 30-second stability test. The error details will be in the report. Usually this is a logic bug (not a setup/import issue), so you'll need to review the code.

**Q: Can I run `/launch` repeatedly without issues?**
A: Yes. Each run is independent. You can run it after every change, and it won't leave behind temp files or stuck processes.

**Q: The skill stopped at Phase 1 with a syntax error. Now what?**
A: Fix the syntax in the file it reported. Then run `/launch` again — it'll pick up where it left off.

**Q: I want to skip tests and just launch the game. Can I do that?**
A: Yes, tell the agent: "Run `/launch` but skip Phase 2 (tests)." The skill is flexible.

---

## Success Indicators

You'll know `/launch` worked when:
- ✓ Final report shows all phases passing
- ✓ Status line says "READY TO PLAY"
- ✓ No outstanding issues listed
- ✓ Total time is under 10 minutes (indicates smooth run)

If you see yellow/red anywhere, the report will guide you on next steps.
