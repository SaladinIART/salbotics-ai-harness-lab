# Upgrade Notes

## Reference Repo

- Repo: [SaladinIART/Ular_yg_Mengular](https://github.com/SaladinIART/Ular_yg_Mengular)
- Current observed shape: small Python/Pygame snake project with versioned
  scripts, local high scores, menu states, power-ups, obstacles, and
  troubleshooting files.
- Important mismatch: the README references `Ular_yang_Mengular.v2.0.py`, but
  the inspected repository contains files up to `Ular_yang_Mengular.v1.3.py`.
  The latest script caption says `v2.0`.

## SWOT Analysis

### Strengths

- Working Python/Pygame snake foundation.
- Existing menu, pause, difficulty, high-score, power-up, and obstacle ideas.
- Small codebase that is easy to inspect and rebuild.
- MIT-licensed public reference repo.
- Earlier versions show useful gameplay experiments such as levels, ghosting,
  shields, and obstacle patterns.

### Weaknesses

- Main gameplay is concentrated in large single-file scripts.
- Rendering, input, persistence, tuning, and game logic are tightly coupled.
- Troubleshooting files are not reusable modules and rely on undefined globals.
- No tests, packaging, requirements file, or stable save-data strategy.
- Difficulty leans on speed and random placement rather than tactical mastery.
- Version naming and README state are inconsistent.

### Opportunities

- Reframe power-ups as cybernetic buildcraft.
- Add slots, module tradeoffs, unlocks, run rewards, and persistent profile
  progress.
- Use content files for modules, arenas, hazards, and tuning.
- Create hard-but-fair tactical pressure through telegraphs, escalating heat,
  and handcrafted arenas.
- Use the lab as a harness-engineering example: checkpoints, done criteria,
  playtest notes, and handoff docs.

### Threats

- Scope creep from RPG, roguelite, and open strategy ideas can delay a playable
  first slice.
- Pygame UI can become cumbersome if inventory and strategy systems grow too
  quickly.
- Random challenge without readable warnings can make failure feel cheap.
- Copying the old single-file structure forward would make future upgrades
  fragile.

## V2 Roadmap

### CP1: Isolated Scaffold

Status: complete.

Master list:

- Prototype folder.
- Python package skeleton.
- `README.md`.
- `GEMINI.md`.
- `upgrade-notes.md`.
- `requirements.txt`.
- Source attribution.

### CP2: Clean Playable Skeleton

Status: complete.

Build a small modular Pygame snake loop:

- Window, clock, input, snake movement.
- Food, score, collision, restart.
- Basic tests around movement, spawn safety, and collision.
- No cybernetic modules yet.

### CP3: Cybernetic Modules

Status: complete.

Add RPG-style customization:

- Slots: head, core, spine, tail.
- Starter modules with benefits and costs.
- Loadout screen.
- Persistent profile save.

Implemented starter modules:

- Targeting Reticle: score bonus with shorter starting body.
- Reactive Shield Core: one collision block with longer starting body.
- Overclock Spine: score bonus with higher run speed.
- Scrap Magnet Tail: doubled scrap with longer starting body.

### CP4: Tactical Challenge Layer

Status: complete.

Make suffering feel earned:

- Telegraphed hazards.
- Arena modifiers.
- Escalating heat.
- Miniboss encounter.
- Reward choices after milestones.

Implemented challenge pieces:

- Yellow warning hazard cells arm before becoming active lethal cells.
- Shields can absorb active hazards.
- Heat rises from score/time and slightly increases run speed.
- Circuit Warden miniboss appears after score pressure and grants a reward on
  defeat.
- Milestone rewards pause the run and offer three choices.

### CP5: Playtest And Handoff

Status: complete.

Stabilize the first vertical slice:

- Playtest checklist.
- Balance notes.
- Bug list.
- Final handoff docs.
- Parked roadmap for campaign RPG and open strategy systems.

Implemented CP5 polish:

- Tail-safe movement allows entering the vacating tail cell, matching expected
  snake rules.
- Added playtest checklist, balance notes, known issues, and handoff docs.
- Added balance targets as structured content.
- Re-ran tests, compile check, and headless Pygame smoke.

## Parked Ideas

Campaign RPG:

- Story map with regions and bosses.
- NPC faction contracts.
- Named cybernetic relics.
- Quest rewards and narrative consequences.

Open strategy:

- Territory map between runs.
- Resource allocation before missions.
- Facility upgrades.
- Enemy pressure that reacts to player progress.

These ideas should stay documented until the cyber-roguelite loop is playable.
