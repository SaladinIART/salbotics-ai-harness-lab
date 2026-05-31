# Ular Retro Engine

Pyxel-based retro remake of `Ular Cyber-Roguelite`.

CP6 defined the engine and game design. CP7 created the empty Pyxel scaffold.
CP8 added the first playable snake slice. CP9 through CP11 finish the first
roguelite loop: Lab, cybernetic modules, scrap economy, hazards, Circuit Warden,
rewards, developer tools, unlocks, and profile persistence.

The existing Pygame prototype in `cyber-roguelite-prototype` stays intact as the
reference build.

## Current Status

- Checkpoint: CP11, campaign roguelite loop.
- Engine base: Pyxel layer.
- Visual target: GBA-inspired pixel art with modern readability.
- Game shape: tactical snake roguelite campaign.
- Progression: body modules first, skill tree and loot second.
- Difficulty: hard-fair mastery.
- Platform target: Windows desktop first, web export later.
- Le Mans racing branch: dropped for now.

## Setup

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

```powershell
python -m ular_retro_engine
```

Or:

```powershell
.\install_and_run.bat
```

## Controls

- `Space` or `Enter`: title to Lab, Lab to run, or restart after run end.
- Lab: `Up`/`Down` selects module slot.
- Lab: `Left`/`Right` cycles unlocked modules.
- Lab: `U` buys Aux Power Bus if you have 10 scrap.
- Run: arrow keys or `WASD` turn.
- Reward screen: `1`, `2`, or `3` chooses a reward.
- `[` or `-`: reduce saved snake speed.
- `]` or `=`: increase saved snake speed.
- `Esc`: quit from title, return from run to Lab, or Lab to title.
- `F1`: toggle developer mode.

Developer mode run hotkeys:

- `B`: spawn boss.
- `H`: spawn hazard.
- `G`: add score.
- `R`: open reward choices.
- `V`: add shield.
- `C`: clear hazards.

## Test

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m compileall -q src tests
```

## Documents

- `ENGINE_RFC.md`: engine boundary and public interfaces.
- `GAME_DESIGN_RFC.md`: roguelite campaign design and difficulty contract.
- `CONTENT_SCHEMA.md`: planned content data shapes.
- `ROADMAP.md`: CP6 through CP11 checkpoint structure.
- `RESEARCH_SOURCES.md`: research links and source notes.
- `GEMINI.md`: continuation handoff.
- `docs/cp7-smoke-notes.md`: CP7 verification notes.
- `docs/cp8-smoke-notes.md`: CP8 verification notes.
- `docs/cp9-cp11-smoke-notes.md`: full loop verification notes.

## Source Attribution

- Reference repo: https://github.com/SaladinIART/Ular_yg_Mengular
- Current playable Salbotics prototype:
  `labs/02-ular-game-design/cyber-roguelite-prototype`

No source code from the reference repo or the Pygame prototype is copied here.

## Checkpoint Status

- CP6: RFC and research folder, complete.
- CP7: Pyxel engine scaffold, complete.
- CP8: Tactical Snake+ vertical slice, complete.
- CP9: Cybernetic buildcraft, complete.
- CP10: hard-fair challenge layer, complete.
- CP11: campaign roguelite loop, complete.

## Next Work

The roadmap CPs are complete for the first Pyxel full-loop prototype. Next safe
work should be a playtest/balance pass, sprite/audio pass, or web export trial.
