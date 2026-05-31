# Lab 02: Ular Game Design

This lab shows how to use harness engineering to grow a small snake-game idea
without losing control of scope.

It is inspired by the public repo
[SaladinIART/Ular_yg_Mengular](https://github.com/SaladinIART/Ular_yg_Mengular),
but the lab prototypes are public-safe rebuilds. No private project files are
copied here.

## Current Progress

Lab 02 now has two implementation tracks:

- [cyber-roguelite-prototype](cyber-roguelite-prototype/README.md): earlier
  Python/Pygame vertical slice with cybernetic slots, hazards, boss, rewards,
  speed customization, and developer mode.
- [ular-retro-engine](ular-retro-engine/README.md): newer Pyxel remake through
  CP11 with Lab, module loadouts, scrap economy, skill purchase, hazards,
  Circuit Warden, reward choices, unlocks, materials, profile persistence, and
  tests.

The Pyxel `ular-retro-engine` is the current forward path.

## Learning Goal

Use harness engineering to transform an exciting game idea into visible,
reviewable checkpoints:

```text
Goal + Context + Path + Checkpoints + Done Criteria
```

The main lesson is not only "build snake." The lesson is how to keep a creative
idea from becoming an endless feature spiral.

## How To Run The Current Prototype

```powershell
C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine\install_and_run.bat
```

Or from the folder:

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
python -m ular_retro_engine
```

## Current Controls

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

## Checkpoint Timeline

- CP1: isolated scaffold and source attribution.
- CP2: clean playable snake skeleton.
- CP3: cybernetic modules in the Pygame prototype.
- CP4: hazards, heat, boss, and rewards in the Pygame prototype.
- CP5: playtest notes, balance pass, and handoff polish.
- CP6: Pyxel engine RFC and research folder.
- CP7: Pyxel engine scaffold.
- CP8: Pyxel Tactical Snake+ vertical slice.
- CP9: cybernetic buildcraft.
- CP10: hard-fair challenge layer.
- CP11: campaign roguelite loop.

## Tutorial Files

- [Prompt harness](prompt-harness.md)
- [Design worksheet](design-worksheet.md)
- [CP11 playtest tutorial](tutorial-cp11-playtest.md)
- [Pyxel prototype README](ular-retro-engine/README.md)
- [Pyxel handoff notes](ular-retro-engine/GEMINI.md)

## What Is Still Future Work

- Pixel sprite and palette pass.
- Audio cues.
- Multiple biomes.
- Multiple bosses.
- Richer module upgrading/crafting UI.
- Web export validation.
