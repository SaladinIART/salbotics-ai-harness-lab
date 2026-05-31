# CP8 Smoke Notes

CP8 added the first playable Tactical Snake+ baseline in the Pyxel scaffold.
This note is historical; after CP11, use `cp9-cp11-smoke-notes.md` for current
manual play expectations.

## Automated Checks

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m compileall -q src tests
```

Expected:

- CP7 scaffold tests still pass.
- `RunState` moves the snake deterministically.
- Instant reversal is blocked.
- Food increases score and target length.
- Wall and self collisions end the run.
- Moving into the vacating tail cell is allowed.
- Restart resets run state.
- Speed preference clamps between 5 and 18 FPS and saves to profile.
- Finished runs update profile stats only once.

## Manual Window Smoke

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
.\install_and_run.bat
```

Expected:

- Title screen opens.
- `Space` or `Enter` starts the playable CP8 snake run.
- Arrow keys or `WASD` turn the snake.
- Food increases score and length.
- Wall or self collision shows `RUN ENDED`.
- `Space` or `Enter` restarts after run end.
- `[` or `-` lowers speed, `]` or `=` raises speed.
- Speed is saved to `saves/profile.json`.
- `Esc` returns from play to title.

## CP8 Boundary

Still intentionally absent:

- Cybernetic modules.
- Skill tree.
- Loot/materials.
- Hazards.
- Bosses.
- Rewards.
- Campaign lab.
- Web export.
