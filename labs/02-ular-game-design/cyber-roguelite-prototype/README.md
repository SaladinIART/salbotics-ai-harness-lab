# Ular Cyber-Roguelite Prototype

Clean Python/Pygame rebuild inspired by
[SaladinIART/Ular_yg_Mengular](https://github.com/SaladinIART/Ular_yg_Mengular).

This folder is intentionally isolated from other Salbotics projects and from the
existing Lab 02 beginner-scope materials.

## Goal

Transform the current snake-game idea into a cyber-roguelite vertical slice:
short hard-but-fair runs, cybernetic module choices, escalating tactical arenas,
and persistent progress that makes each failure feel earned.

Post-CP5 gameplay upgrade adds a larger arena, slower default pacing, saved
speed customization, earlier boss appearance, and developer mode. Campaign RPG
and open-strategy layers are still parked for later work.

## Source Attribution

- Reference repo: `SaladinIART/Ular_yg_Mengular`
- License in reference repo: MIT
- CP1 approach: clean scaffold and documentation only; no source files copied.

## Checkpoints

- [x] CP1: isolated scaffold, docs, requirements, package folders
- [x] CP2: clean playable snake skeleton
- [x] CP3: cybernetic module slots and profile save
- [x] CP4: tactical challenge layer, hazards, miniboss, rewards
- [x] CP5: playtest notes, balance pass, handoff polish

## Folder Structure

```text
cyber-roguelite-prototype/
├── README.md
├── GEMINI.md
├── upgrade-notes.md
├── requirements.txt
├── pyproject.toml
├── content/
│   ├── balance_targets.json
│   ├── challenge_rules.json
│   └── starter_modules.json
├── docs/
│   ├── balance-notes.md
│   ├── developer-mode.md
│   ├── handoff.md
│   ├── known-issues.md
│   └── playtest-checklist.md
├── saves/
├── src/
│   └── ular_cyber_roguelite/
└── tests/
```

## Setup

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\cyber-roguelite-prototype"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

```powershell
python -m ular_cyber_roguelite
```

Controls:

- `Space`: start or restart
- Ready/game-over screen: `Up`/`Down` selects module slot
- Ready/game-over screen: `Left`/`Right` cycles module
- During run: arrow keys or `WASD` change direction
- Reward screen: `1`, `2`, or `3` chooses a reward
- `[` or `-`: reduce snake speed
- `]` or `+`: increase snake speed
- `F1`: toggle developer mode
- `P`: pause or resume
- `Esc`: quit

## CP3 Module Slots

- `head`: score/food identity.
- `core`: survival identity.
- `spine`: speed/risk identity.
- `tail`: scrap/progression identity.

Starter active modules:

- `Targeting Reticle`: more score per food, shorter starting body.
- `Reactive Shield Core`: blocks one fatal collision, longer starting body.
- `Overclock Spine`: more score per food, faster run speed.
- `Scrap Magnet Tail`: doubles scrap from score, longer starting body.

Profile data is saved locally to `saves/profile.json`. The `saves` folder is
ignored by Git so personal run data does not become project source.

## CP4 Challenge Layer

- Hazard cells appear as yellow warnings before turning lethal.
- Active hazards are pink/red and end the run unless a shield absorbs them.
- Heat rises with score and time, increasing pressure and run speed slightly.
- The `Circuit Warden` miniboss appears after enough score; bite the blue node
  three times to defeat it.
- Milestone rewards pause the run and let the player choose a short-term boost.

## Speed And Developer Mode

Speed is saved in `saves/profile.json`, with base speed clamped from `5` to
`18`. Module and heat effects can still modify the current run speed.

Developer mode:

- `F1`: toggle developer mode.
- `B`: spawn the boss during a run.
- `H`: spawn a hazard during a run.
- `C`: clear hazards.
- `G`: add 1 score.
- `R`: open reward choices during a run.
- `V`: add 1 shield.

## CP5 Stabilization

- Tail-safe movement now allows classic snake movement into a vacating tail
  cell.
- Balance targets are captured in `content/balance_targets.json`.
- Playtest checklist, balance notes, known issues, and continuation handoff live
  in `docs/`.

## Post-CP5 Gameplay Upgrade

- Default arena expanded to `34 x 28`.
- Default speed reduced to `8`.
- Boss threshold reduced to score `8`.
- Hazard warnings last longer and hazards spawn less aggressively.
- Boss spawn now happens before reward pause, so the boss is visible when the
  threshold is reached.

## Test

```powershell
python -m unittest discover -s tests
```

## Done Criteria For CP1

- Folder exists inside Lab 02.
- `README.md`, `GEMINI.md`, `upgrade-notes.md`, and `requirements.txt` exist.
- `src/ular_cyber_roguelite`, `tests`, `content`, and `saves` exist.
- No files outside this prototype folder are changed.

## Done Criteria For CP2

- Game opens from `python -m ular_cyber_roguelite`.
- Snake moves on a grid and turns without instant reversal.
- Food increases score and length.
- Wall or self collision ends the run.
- `Space` restarts after game over.
- Core movement, food, and collision behavior have tests.

## Done Criteria For CP3

- Four cybernetic slots exist: `head`, `core`, `spine`, `tail`.
- Player can cycle unlocked modules before starting/restarting a run.
- Loadout effects alter score, speed, starting length, shield charge, or scrap.
- Run completion saves profile stats and earned scrap.
- Module/profile behavior has tests.

## Done Criteria For CP4

- Hazards are telegraphed before becoming lethal.
- Active hazards interact with shield charges.
- Heat scaling changes pressure over time.
- Circuit Warden miniboss can spawn, take damage, and open a reward on defeat.
- Score milestones open reward choices.
- Hazard, boss, and reward behavior have tests.

## Done Criteria For CP5

- Playtest checklist exists.
- Balance targets and notes exist.
- Known issues are documented.
- Handoff doc explains current state and next safe work.
- Tests and smoke checks pass after final polish.
