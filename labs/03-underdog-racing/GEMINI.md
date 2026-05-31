# GEMINI.md

## Project Summary

`03-underdog-racing` is a new harness-engineering lab for a top-down pixel
racing game called **Underdog**.

Unlike Ular, this project should use Phaser + TypeScript and browser-first
tooling. The design emphasis is racing feel, simcade vehicle physics, upgrade
economy, and a street-to-pro campaign ladder.

## Current Checkpoint

CP7 implemented:

- Vite + TypeScript scaffold.
- Phaser dependency.
- Boot, Title, Garage, and TestTrack scenes.
- DOM HUD.
- Input action map.
- Pure simulation modules for vehicle physics and time trial state.
- One stock car.
- One oval test track.
- Acceleration, braking, steering, lateral grip, drift, surface drag, tire wear.
- Lap checkpoints, current lap, best lap, reset.
- Debug telemetry toggle.
- Vitest unit tests for physics and lap behavior.
- Money and reputation campaign profile.
- Upgrade categories: tires, engine, brakes, gearbox, aero, weight.
- Derived vehicle specs from car build.
- Garage upgrade purchase UI.
- Lap payouts and best-lap persistence.
- Local storage profile save.
- Vitest coverage for upgrades, purchases, save/load, and lap payouts.
- Street-to-pro campaign events.
- Reputation and license gates.
- Event selection from Garage.
- Event result rewards.
- Driver XP and passive skill unlocks.
- Club license unlock through license trial.
- Old-save normalization for CP4 profiles.
- One blue AI rival.
- Rival checkpoint racing line.
- Simple AI throttle/steering.
- Finish order.
- Duel rewards.
- Rival/duel tests.
- Street Underdog Cup championship calendar.
- Player/rival points table.
- Round-by-round championship advancement.
- Local Parts Shop sponsor hook.
- Crew Notebook team-management hook.
- Garage HUD championship panel.
- Championship-loop tests.
- Post-CP7 polish: Canvas renderer, F1-inspired circuit, visible steering tires,
  floating speed readout, and Easy/Normal/Hard rival difficulty.

Still absent:

- Real sprite/audio assets.
- Multi-rival grids.
- Richer championship calendar.

## Locked Decisions

- Engine: Phaser + TypeScript.
- Genre: top-down pixel racing.
- Visual style: top-down pixel, not angled 2.5D.
- Campaign fantasy: street-to-pro drama.
- Physics target: simcade.
- First playable after docs: time trial first.
- Progression hierarchy: car build primary, driver skill passive XP
  achievements, team management hooks after CP7.
- GPL racing projects can be studied but not copied into this repo.

## Terminology

- Underdog: the working title and player fantasy.
- Street-to-pro: campaign arc from informal racing into licensed competition.
- Simcade: physics feel between arcade and strict simulator.
- Time trial: first playable format; one vehicle, lap timing, no AI pack.
- Car build: upgradeable specs such as tires, engine, brakes, gearbox, aero,
  weight, cooling, and durability.
- Driver skill: passive achievement/XP unlocks earned by driving well.
- Team management: later layer for sponsors, crew, logistics, and events.
- Grip budget: how much tire force is available before sliding.
- Lateral velocity: sideways motion that must be reduced by tire grip.
- Racing line: path that balances turn-in, apex, exit speed, and risk.

## Guardrails

- Do not implement gameplay in CP1.
- Do not place this project inside Lab 02 or Ular folders.
- Do not copy GPL code from Dust Racing 2D, Speed Dreams, or other references.
- Keep simulation separate from Phaser rendering when implementation starts.
- Time trial comes before rival AI or championship pack racing.

## Continuation Notes

Next safe work is a post-CP7 deepening pass: better tracks, multiple rivals,
sprite/audio assets, tire compounds, endurance pressure, and fuller sponsor/team
management.

Recommended model for the next major design pass: `gpt-5.4`, high reasoning.
