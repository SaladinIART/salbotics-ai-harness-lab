# Lab 03: Underdog Racing

Phaser + TypeScript prototype for **Underdog**, a top-down pixel racing game
about climbing from street racing into legitimate professional competition.

This lab intentionally uses a different stack from the Ular project. Ular tests
Pyxel and Python; Underdog tests Phaser, TypeScript, browser deployment, racing
physics, and a different kind of progression design.

## Current Status

- Checkpoint: CP7, championship loop.
- Engine: Phaser + TypeScript.
- Genre: top-down pixel racing.
- Campaign fantasy: street-to-pro drama.
- Physics target: simcade.
- First playable later: time trial first.
- Progression: car build primary, driver skill passive XP achievements, team
  management hooks.

CP1 created research/RFC docs. CP2 created the Phaser/Vite scaffold. CP3 added
the first playable time-trial physics lab. CP4 connected the Garage to car-build
upgrades, money, reputation, lap payouts, and profile persistence. CP5 adds the
street-to-pro campaign shell with event selection, license gates, driver XP, and
passive skill unlocks. CP6 adds a blue AI rival, checkpoint pathing, finish
order, and duel rewards. CP7 connects duel results into the Street Underdog Cup
with a calendar, points table, campaign advancement reward, sponsor hook, and
team facility hook. The first post-CP7 polish pass forces Canvas rendering for
stability, replaces the early oval with an F1-inspired technical circuit, adds
visible front-tire steering, adds an in-world speed readout, and lets players
choose Easy/Normal/Hard rival difficulty.

## Goal

Use harness engineering to learn racing-game design without jumping straight
into a giant championship simulator.

The first principle:

```text
Handling feel first. Tournament drama second.
```

The car must feel good in a time trial before rival AI, pack racing, sponsors,
or championships are allowed to carry the design.

## Documents

- `GEMINI.md`: handoff context, terminology, locked decisions, parked ideas.
- `GAME_DESIGN_RFC.md`: street-to-pro fantasy, race loop, tournament loop,
  campaign structure.
- `PHYSICS_RFC.md`: simcade vehicle model and physics concepts.
- `PROGRESSION_RFC.md`: car build, driver skill, resources, sponsors, and team
  management boundaries.
- `ROADMAP.md`: CP1 through CP7 checkpoint structure.
- `RESEARCH_SOURCES.md`: research links and licensing cautions.
- `docs/cp2-cp3-smoke-notes.md`: run, build, test, and playtest notes through
  CP7.
- `docs/cp7-playtest-checklist.md`: focused championship-loop playtest script.
- `tutorials/README.md`: dedicated learning path from this exercise.
- `tutorials/wisdoms-from-underdog.md`: reusable lessons and working wisdoms.

## Run

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\03-underdog-racing"
npm install
npm run dev
```

## Test

```powershell
npm test
npm run build
```

## Current Controls

- `Space` or `Enter`: title to Garage, Garage to test track.
- Garage: `Up`/`Down` selects upgrade category.
- Garage: `Left`/`Right` cycles unlocked events.
- Garage: `1`/`2`/`3` selects Easy/Normal/Hard difficulty.
- Garage: `U` buys selected upgrade.
- `WASD` or arrow keys: throttle, brake, steer.
- `Shift` or `Space`: handbrake during test track.
- `R`: reset car.
- `Esc`: return to Garage.
- `F1`: toggle debug telemetry.

## Architecture

The CP2+ implementation should separate rules from rendering:

```text
src/
  simulation/   deterministic vehicle physics, lap timing, race rules, economy
  phaser/       scenes, sprites, camera, track rendering, effects
  ui/           DOM overlays for garage, upgrades, tournaments, settings
  content/      vehicle classes, parts, tracks, events, sponsors, licenses
  saves/        local campaign profile
```

## CP1 Done Criteria

- Folder exists under `labs/03-underdog-racing`.
- Required RFC docs exist.
- Docs clearly choose Phaser + TypeScript.
- Docs explain the simcade physics target.
- Docs warn that GPL racing projects are study-only, not copied.
- No gameplay code exists yet.

## CP2 Done Criteria

- Vite + TypeScript scaffold exists.
- Phaser dependency exists.
- Boot, Title, Garage, and TestTrack scenes exist.
- DOM HUD exists.
- Input action map exists.

## CP3 Done Criteria

- One stock car can drive on a top-down test track.
- Vehicle simulation is separate from Phaser scenes.
- Acceleration, braking, steering, lateral grip, surface drag, and tire wear
  exist.
- Lap timing and checkpoints exist.
- Debug telemetry exists.
- Unit tests cover vehicle physics and lap progress.

## CP4 Done Criteria

- Money and reputation profile exists.
- Upgrade categories exist: tires, engine, brakes, gearbox, aero, weight.
- Upgrade purchases modify derived vehicle specs.
- Garage UI shows build state and purchase feedback.
- Completed laps award money and reputation.
- Profile saves to local storage.
- Tests cover upgrade effects, purchase rules, save/load, and lap payouts.

## CP5 Done Criteria

- Street events and license-trial events exist.
- Events are gated by reputation and license tier.
- Garage can cycle unlocked events.
- Event results grant money, reputation, and driver XP.
- License trial can unlock club license.
- Driver XP unlocks passive skill bonuses.
- Old CP4 saves normalize into campaign-ready profiles.
- Tests cover gates, rewards, license unlocks, driver skills, and profile
  migration defaults.

## CP6 Done Criteria

- One AI rival exists.
- Rival follows a checkpoint racing line.
- Race state tracks player and rival finish.
- Finish order resolves player-vs-rival result.
- Duel rewards add money, reputation, and driver XP.
- Tests cover rival pathing, finish order, race updates, and duel rewards.

## CP7 Done Criteria

- Street Underdog Cup event calendar exists.
- Duel results award championship points.
- Garage HUD shows current round and player/rival points table.
- Campaign advancement awards sponsor and team-management hooks.
- Save migration preserves old profiles with championship defaults.
- Tests cover championship recording, standings, hook rewards, and migration.
- Tutorial/playtest docs exist.

## Next Work

Post-CP7 should deepen the game instead of adding another broad scaffold:
multiple rivals, better tracks, sprite/audio assets, endurance systems,
weather, tire compounds, and a richer championship calendar.

## Tutorials And Lessons

Use the [Underdog tutorial path](tutorials/README.md) to teach what this lab
revealed about harness engineering, racing feel, progression, difficulty, and
playtest evidence.

Recommended order:

1. [Harness a Big Game Idea Without Drowning](tutorials/tutorial-01-harness-a-big-game-idea.md)
2. [Racing Feel Before Racing Features](tutorials/tutorial-02-racing-feel-before-features.md)
3. [Progression, Difficulty, and Fair Pressure](tutorials/tutorial-03-progression-difficulty-fair-pressure.md)
4. [Playtest Evidence Beats Vibes](tutorials/tutorial-04-playtest-evidence.md)
5. [Wisdoms From Underdog](tutorials/wisdoms-from-underdog.md)
