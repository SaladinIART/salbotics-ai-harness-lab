# Roadmap

## Recommended Model

Use `gpt-5.4` with high reasoning for major Underdog checkpoints.

## CP1: Research RFC Folder

Status: complete.

Master list:

- Folder.
- `README.md`.
- `GEMINI.md`.
- `GAME_DESIGN_RFC.md`.
- `PHYSICS_RFC.md`.
- `PROGRESSION_RFC.md`.
- `ROADMAP.md`.
- `RESEARCH_SOURCES.md`.
- No gameplay code.

Estimated tokens: 8k-12k.

## CP2: Phaser Scaffold

Status: complete.

Goal: create the browser-game shell without racing physics.

Master list:

- Vite + TypeScript app.
- Phaser dependency.
- Phaser boot.
- Empty Title scene.
- Empty Garage scene.
- Empty TestTrack scene.
- Input action map.
- DOM overlay policy.
- Smoke test.
- README/GEMINI update.

Estimated tokens: 10k-16k.

## CP3: Time-Trial Physics Lab

Status: complete.

Goal: make one car feel testable.

Master list:

- Deterministic vehicle state.
- Acceleration.
- Braking.
- Steering.
- Lateral grip.
- Drift tuning.
- One test track.
- Lap timer.
- Reset.
- Debug overlay.
- Unit tests for physics numbers.

Estimated tokens: 18k-30k.

## CP4: Garage And Car Build

Status: complete.

Goal: connect upgrades to vehicle behavior.

Master list:

- Money/resource profile.
- Tires.
- Engine.
- Brakes.
- Gearbox.
- Aero.
- Weight.
- Upgrade purchase UI.
- Save profile.
- Tests for upgrade effects and save/load.

Estimated tokens: 16k-28k.

## CP5: Street-To-Pro Campaign Shell

Status: complete.

Goal: make the ladder visible.

Master list:

- Street events.
- License gates.
- Reputation.
- Driver XP/passives.
- Tournament results.
- Unlock next tier.
- Event selection UI.
- Tests for gates and rewards.

Estimated tokens: 18k-30k.

## CP6: Rival/AI Race Prototype

Status: complete.

Goal: add one rival after time trial is good.

Master list:

- One AI rival.
- Racing line/checkpoint path.
- Simple AI throttle/steering.
- Collision policy.
- Finish order.
- Duel result rewards.
- Tests for checkpoint progress and finish ranking.

Estimated tokens: 20k-35k.

## CP7: Championship Loop

Status: complete.

Goal: connect events into a season-like structure.

Master list:

- Event calendar.
- Points table.
- Campaign advancement.
- Sponsor hooks.
- Team management hooks.
- Tutorial docs.
- Playtest checklist.

Estimated tokens: 20k-35k.

Implemented notes:

- Street Underdog Cup calendar uses Backlot Shakedown, Dockside Sprint, and
  Club License Trial.
- Duel results award championship points.
- Garage HUD shows current round, points table, sponsor state, and team
  facility hooks.
- Winning the cup unlocks the Local Parts Shop sponsor hook and Crew Notebook
  facility hook.
- Tests cover round recording, standings, hook unlocks, and save migration.

## Post-CP7 Ideas

- Multiple vehicle classes.
- Endurance fuel/cooling.
- Tire compounds.
- Weather.
- Track editor.
- Ghost replay.
- Web publishing.
