# Engine RFC

## Decision

Build `Ular Retro Engine` as a small game-specific engine layer on top of
Pyxel.

Pyxel supplies the low-level runtime: window, frame callbacks, keyboard input,
basic drawing, image banks, tilemaps, and audio primitives. The Salbotics layer
owns the game architecture: scene flow, deterministic simulation state, content
loading, save/profile handling, debug tools, pixel rules, and testable gameplay
contracts.

## Goals

- Keep the project Python-first and approachable from VS Code.
- Preserve a strong retro constraint without locking the design to exact GBA
  hardware limits.
- Make game logic testable without a live Pyxel window.
- Separate simulation, content data, rendering, and persistence.
- Support hard-fair roguelite tuning through developer tools and repeatable
  tests.
- Leave a later path to Pyxel web export.

## Non-Goals

- No raw renderer, operating-system window layer, audio mixer, asset compiler, or
  physics engine in CP7.
- No entity-component framework unless actual Ular complexity demands it.
- No multiplayer, online services, mod loader, or native level editor in the
  first production path.
- No Le Mans racing support in the Ular roadmap.

## Runtime Shape

The runtime should be small and explicit:

1. `RetroApp` initializes Pyxel, loads configuration, creates service objects,
   and pushes the first scene.
2. Pyxel calls app-level `update` and `draw` callbacks.
3. `RetroApp` captures input into an action snapshot each frame.
4. The active `Scene` handles input and advances its own state.
5. Game scenes update deterministic `RunState` through pure or mostly pure
   systems.
6. Renderers read state snapshots and draw to the pixel canvas.
7. Saves happen only through a profile/save service, never directly from
   simulation systems.

The target should feel like a console loop: clear ticks, fixed rules, predictable
state transitions, and no hidden cross-module mutation.

## Public Interface Contracts

### RetroApp

Owner of the Pyxel boot lifecycle.

Responsibilities:

- Read project configuration.
- Initialize the Pyxel window at the chosen logical resolution.
- Hold scene stack, input mapper, content registry, profile store, audio service,
  and debug console.
- Route `update` and `draw` calls to the active scene.
- Provide scene transitions such as push, pop, replace, and quit.
- Expose a controlled service context to scenes.

CP7 acceptance:

- Can boot to an empty title scene.
- Can switch to an empty play scene.
- Can exit cleanly.
- Can run a smoke test without gameplay systems.

### Scene

Base contract for screens and modes.

Required lifecycle:

- `enter(context)`: receive shared services and optional transition payload.
- `handle_input(actions)`: react to one-frame and held actions.
- `update(dt_ticks)`: advance state.
- `draw(renderer)`: draw current scene.
- `exit()`: release transient state if needed.

Expected first scenes:

- `TitleScene`: future main menu placeholder.
- `PlayScene`: future run placeholder.
- `PauseScene`: later overlay.
- `RewardScene`: later modal run choice.
- `LabScene`: later campaign upgrade hub.

### InputMapper

Converts raw Pyxel keys into game actions.

Core actions:

- `move_up`, `move_down`, `move_left`, `move_right`
- `confirm`, `cancel`, `pause`
- `cycle_left`, `cycle_right`
- `speed_down`, `speed_up`
- `debug_toggle`

Developer actions should exist behind a developer-mode flag so normal play does
not accidentally trigger test hooks.

### ContentRegistry

Loads and validates data definitions.

First planned content families:

- Modules.
- Arenas.
- Bosses.
- Rewards.
- Skill tree nodes.
- Loot and materials.
- Balance tables.

The registry should return typed records or validated dictionaries. Invalid
content should fail early with clear file and field names.

### RunState

Deterministic state for a single run.

It should include:

- Snake body, direction, pending direction, length target.
- Food, pickups, hazards, warning cells.
- Boss state and active attack pattern.
- Heat, score, scrap preview, current biome/arena.
- Equipped module effects.
- Run phase: ready, active, paused, reward, boss, game over, cleared.
- Random seed or RNG object controlled by the run setup.

Renderers read `RunState`; they do not own gameplay decisions.

### Profile

Persistent player state outside a single run.

Planned fields:

- Total runs, best score, total scrap.
- Unlocked modules, module levels, known loot.
- Skill tree unlocks.
- Speed and accessibility preferences.
- Last selected loadout.
- Version number for future migration.

Profile saves should be local files first. Cloud saves or account identity are
out of scope.

### DebugConsole

Developer mode must be designed early, not bolted on after bugs appear.

Planned capabilities:

- Toggle hitboxes and hazard warning overlays.
- Spawn boss or force a boss phase.
- Grant scrap, shield, heat, score, module, or loot.
- Reload content definitions.
- Dump current run state to a readable debug file later.
- Show FPS/tick, scene name, RNG seed, heat, active boss pattern, and module
  effects.

## Rendering Rules

Use a GBA-inspired internal frame:

- Logical resolution target: 240x160 or a close Pyxel-friendly equivalent.
- Tiles: prefer 8x8 for floor and UI details, 16x16 for major actors when
  readability wins.
- Scaling: crisp integer scaling where possible.
- Layers: background, terrain, hazard telegraphs, snake/body, boss/actors,
  effects, HUD, debug overlay.
- Palette discipline: limited palettes per biome and module family, but not
  strict hardware-authentic palette banking.

The HUD should protect the playfield. Important danger telegraphs must not hide
under UI text.

## Data Flow

Suggested dependency direction:

`Pyxel -> RetroApp -> Scene -> Game Systems -> RunState`

`ContentRegistry`, `ProfileStore`, `AudioService`, and `DebugConsole` are
services passed through the app context. Game systems can read content records
and profile-derived loadouts but should not mutate the profile directly during a
run.

## CP7 Acceptance Tests

CP7 should prove the engine scaffold before gameplay:

- Import test for the package.
- Config/content path resolution test.
- Scene stack push/pop/replace behavior test.
- Input mapper action snapshot test.
- Profile default creation and version field test.
- Smoke boot script or documented manual smoke test for the Pyxel window.

## Risks

- Pyxel's retro constraints may make dense RPG UI hard to read. Mitigation:
  design lab/menu screens with larger text regions and keep combat HUD minimal.
- Web export may impose packaging constraints. Mitigation: avoid absolute paths
  in runtime content loading and keep saves abstracted behind `ProfileStore`.
- Engine work can swallow game work. Mitigation: every engine feature must map
  to a CP8-CP11 Ular requirement.
