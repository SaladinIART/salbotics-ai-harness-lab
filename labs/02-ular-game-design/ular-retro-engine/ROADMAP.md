# Roadmap

## Recommended Model

Use `gpt-5.4` with high reasoning for substantial future checkpoints.

## Checkpoint Policy

- Keep each checkpoint reviewable and playable or verifiable.
- End each checkpoint with tests, smoke notes, and a `GEMINI.md` update.
- The Pygame prototype remains the reference build, but the Pyxel track is now
  the full-loop remake prototype.

## CP6: RFC And Research Folder

Status: complete.

Master list:

- New sibling folder.
- `README.md`.
- `GEMINI.md`.
- `ENGINE_RFC.md`.
- `GAME_DESIGN_RFC.md`.
- `CONTENT_SCHEMA.md`.
- `ROADMAP.md`.
- `RESEARCH_SOURCES.md`.
- Source links.
- No gameplay code.

## CP7: Pyxel Engine Scaffold

Status: complete.

Master list:

- Python package scaffold.
- Pyxel dependency.
- App boot through `python -m ular_retro_engine`.
- `RetroApp` shell.
- Scene stack.
- Title scene.
- Empty play scene.
- Input mapper.
- Profile default file.
- Developer-mode flag stub.
- Windows run script.
- Unit tests and smoke notes.

## CP8: Tactical Snake+ Vertical Slice

Status: complete.

Master list:

- Deterministic `RunState`.
- Snake movement.
- Direction/reversal guard.
- Food spawn.
- Score and length.
- Wall and self collision.
- Run restart.
- HUD.
- Speed preference.
- Renderer for snake, food, grid, and basic UI.
- Tests for movement, food, collision, restart.

## CP9: Cybernetic Buildcraft

Status: complete.

Master list:

- Body slots: head, core, spine, tail.
- Module content loader.
- Power budget.
- Heat budget.
- Starter modules.
- Module effects and drawbacks.
- Lab loadout screen.
- Profile persistence.
- Skill unlock draft.
- Loot/material draft.
- Tests for module effects and profile behavior.

## CP10: Hard-Fair Challenge Layer

Status: complete.

Master list:

- Hazard telegraph system.
- Heat scaling.
- First boss: Circuit Warden target.
- Milestone rewards.
- Boss rewards.
- Developer mode controls.
- Tests for hazards, rewards, boss state, and debug-supporting systems.

## CP11: Campaign Roguelite Loop

Status: complete.

Master list:

- Lab scene.
- Scrap economy.
- Skill tree unlock: Aux Power Bus.
- Boss-gated unlocks.
- Score-gated unlocks.
- Run summary through HUD/profile persistence.
- Warden Capacitor material.
- Save persistence.
- End-to-end smoke checklist.

## Post-CP11 Recommended Work

- Manual playtest and balance pass.
- Pixel sprite and palette pass.
- Audio cue pass.
- Web export trial.
- Additional biomes.
- Additional bosses.
- Richer module upgrade/crafting UI.

## Parked Ideas

- Le Mans top-down endurance racing.
- Open strategy map.
- Action RPG overworld.
- Online accounts.
- Multiplayer.
