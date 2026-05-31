# CP7 Smoke Notes

CP7 created an empty Pyxel scaffold. This note is historical; after CP11, the
same app now opens a Lab-to-run roguelite loop. Use `cp9-cp11-smoke-notes.md`
for current manual play expectations.

## Automated Checks

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
python -m pip install -e .
python -m unittest discover -s tests
```

Expected:

- Package imports.
- Config resolves `content` and `saves`.
- Scene stack supports push, replace, and pop.
- Input mapper creates action snapshots.
- Profile store creates a versioned default profile.
- `RetroApp.boot()` reaches `TitleScene` without opening a Pyxel window.

## Manual Window Smoke

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
.\install_and_run.bat
```

Expected:

- Pyxel opens a 240x160 logical window titled `Ular Retro Engine`.
- Title screen appears.
- `Space` or `Enter` switches to the empty play scene.
- `Esc` from title exits.
- `Esc` from play returns to title.
- `F1` toggles the `DEV` marker and saves the preference to
  `saves/profile.json`.

## CP7 Boundary

No snake movement, food, collision, hazards, bosses, modules, rewards, or
campaign economy should exist in this checkpoint.
