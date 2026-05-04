# /launch Skill

Automated test-launch-debug cycle for the tower defense game, including building and testing the executable.

## Files

- **SKILL.md** - Main skill documentation with full instructions for all 7 phases
- **scripts/launch_orchestrator.py** - Main orchestrator script (entry point)
- **evals/evals.json** - Test cases for evaluating the skill
- **../../../towerDefense.spec** - PyInstaller spec file for building the executable

## How It Works

When invoked with `/launch`, this skill runs a comprehensive 7-phase validation cycle:

1. **Phase 1: Pre-flight checks** (2-3 min)
   - Syntax validation on all Python files
   - Import validation on critical modules
   - Asset file existence checks

2. **Phase 2: Unit tests** (1-2 min, if tests exist)
   - Runs pytest if test files found
   - Reports pass/fail count

3. **Phase 3: Python game launch & stability** (1-2 min)
   - Launches the game via Python
   - Monitors for crashes over 30 seconds
   - Catches import errors and runtime exceptions

4. **Phase 4: Build executable** (5-10 min)
   - Builds the game with PyInstaller
   - Uses towerDefense.spec for configuration
   - Reuses recent exe if available (>1MB)

5. **Phase 5: Test executable & stability** (1-2 min)
   - Launches the built .exe file
   - Monitors for crashes over 30 seconds  
   - Verifies executable stability

6. **Phase 6: Debug loop** (if errors, auto-fix up to 3 attempts)
   - Analyzes errors from Phases 3 or 5
   - Attempts common fixes (missing __init__, config issues, etc.)
   - Re-tests after each fix

7. **Phase 7: Final report**
   - Summary table of all phases
   - List of fixes applied
   - Clear ✓ READY TO PLAY or ✗ NEEDS ATTENTION status

## Testing the Skill

To test with the 3 provided test cases:

```bash
# Ensure you're in the game repo directory
cd /path/to/towerDefense

# Test Case 1: Clean launch (no errors)
python launch_orchestrator.py

# Test Case 2: Launch with auto-fix (simulated error)
python launch_orchestrator.py --max-attempts 3

# Test Case 3: Catch syntax error
# (First introduce a syntax error in src/game/game.py, then run)
python launch_orchestrator.py
```

## Configuration

- **--repo-path**: Path to game repository (default: current directory)
- **--max-attempts**: Maximum debug attempts (default: 3)

## Output

The skill prints colored output to console:
- ✓ Green: Success
- ✗ Red: Failure
- ⚠ Yellow: Warning
- ⊘ Gray: Skipped

Final report shows:
- Phase-by-phase status table
- Total elapsed time
- List of fixes applied (if any)
- Clear final status

## Extension Points

To enhance the skill:

1. **Better auto-fix logic** - Expand `_analyze_and_fix()` method in orchestrator
2. **Custom test suite** - Add game-specific validation in a separate script
3. **Performance benchmarking** - Add FPS/load time measurements during Phase 3
4. **Asset validation** - Check all referenced assets are present
5. **Feature verification** - Spawn game and programmatically test core features

## Limitations

Current version:
- Auto-fixes are simple (not sophisticated code changes)
- Does not modify code logic (only config/imports)
- Game must have a valid entry point (main.py)
- Requires Python 3.8+ and pygame

## Future Improvements

- [ ] Intelligent error classification and fix suggestions
- [ ] Feature validation (pause, tower placement, etc.)
- [ ] Performance profiling during launch
- [ ] Detailed asset dependency graph
- [ ] Integration with CI/CD pipeline
- [ ] Automated regression test generation
