# Tutorial: Playtest The CP11 Ular Prototype

This tutorial is for checking the current Pyxel prototype and using it as a
harness-engineering teaching example.

## 1. Open The Prototype

Run:

```powershell
C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine\install_and_run.bat
```

The batch file creates a local virtual environment, installs Pyxel, installs the
package in editable mode, and launches the game.

## 2. Understand The Screen Flow

```text
Title -> Lab -> Run -> Reward or Run End -> Lab
```

The important teaching point: the game is not one giant prompt. It reached this
shape through checkpoints.

## 3. Try The Lab

Controls:

- `Space` or `Enter`: move from title to Lab.
- `Up`/`Down`: select head, core, spine, or tail.
- `Left`/`Right`: cycle unlocked modules for that slot.
- `U`: buy Aux Power Bus if you have 10 scrap.
- `Space` or `Enter`: start a run.

Teaching note:

The Lab demonstrates CP9 and CP11. Modules define the build. Scrap and skill
purchase make repeated runs matter.

## 4. Try A Run

Controls:

- Arrow keys or `WASD`: turn.
- `[` or `-`: reduce saved speed.
- `]` or `=`: increase saved speed.
- `Esc`: return to Lab.

During the run:

- Eat food to increase score and length.
- Yellow hazard cells are warnings.
- Red hazard cells are active danger.
- At score pressure, Circuit Warden can appear.
- Bite the blue boss target to damage the boss.
- Reward screens use `1`, `2`, or `3`.

Teaching note:

The run demonstrates CP8 and CP10. The point is hard-fair challenge: the player
should see danger before it becomes lethal.

## 5. Use Developer Mode

Press `F1` to toggle developer mode.

Developer hotkeys during a run:

- `B`: spawn boss.
- `H`: spawn hazard.
- `G`: add score.
- `R`: open reward choices.
- `V`: add shield.
- `C`: clear hazards.

Teaching note:

Developer mode is a harness tool. It lets you jump to hard-to-test moments
without replaying the whole run every time.

## 6. Verify With Tests

From the Pyxel prototype folder:

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m compileall -q src tests
```

Expected result:

```text
25 tests OK
```

## 7. Suggested Playtest Notes

Record short answers:

```text
Did Lab choices feel understandable?
Were hazards readable before they became dangerous?
Did the boss appear clearly?
Did rewards feel useful?
Did scrap make failure feel worthwhile?
Was the snake speed comfortable?
What one thing should improve next?
```

## 8. Recommended Next Checkpoint

Start with a balance pass:

- Slow or speed up heat growth.
- Make boss timing clearer.
- Improve reward usefulness.
- Tune scrap earned per run.
- Make module tradeoffs easier to understand.

Keep the next checkpoint small. The harness wins by making progress visible.
