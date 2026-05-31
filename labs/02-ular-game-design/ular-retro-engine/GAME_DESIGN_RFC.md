# Game Design RFC

## Product Direction

`Ular Retro Engine` exists to ship a deeper version of Ular: a tactical,
cybernetic snake roguelite with GBA-inspired pixel presentation and permanent
RPG progression.

The player should feel that every run teaches something, every death was
readable, and every upgrade changes how the snake is built.

## Design Pillars

- Tactical Snake+: preserve classic snake pressure while adding cybernetic
  modules, body positioning, hazards, boss telegraphs, terrain, and build
  combos.
- Hard-fair mastery: danger is sharp, but it is signaled before it becomes
  lethal.
- Body as build: the snake is customized through visible body modules, not just
  abstract stats.
- Suffering with return: failed runs still produce scrap, unlock knowledge, and
  better planning.
- Retro discipline: GBA-inspired constraints guide camera, color, sprites, and
  animation without sacrificing readability.

## Core Loop

1. Return to the Lab after a run.
2. Spend scrap, inspect loot, unlock skill tree nodes, and configure body
   modules.
3. Pick a biome or mission tier.
4. Enter a short tactical run.
5. Grow, dodge, route, trigger rewards, survive hazards, and defeat or escape
   boss pressure.
6. Die, clear, or retreat.
7. Convert run outcome into persistent progress.

Early targets:

- One run should become interesting in under 30 seconds.
- A normal run should fit 3 to 7 minutes.
- Boss pressure should be visible early during testing.
- Developer mode should let the designer jump directly to challenge moments.

## Moment-To-Moment Play

The snake remains grid-based or strongly grid-readable. Turning, body length,
self-collision, and routing stay central.

New layers:

- Dash or burst movement as a module-driven ability, not a default action at
  first.
- Hazards with warning and active phases.
- Terrain cells that alter movement, heat, scoring, or boss attacks.
- Boss attack patterns that create routing puzzles.
- Module synergies that change food value, shield behavior, body growth, heat,
  tail effects, pickup magnetism, or risk/reward scoring.

The player should not need twitch reflexes alone. Good routing, anticipation,
loadout planning, and reading telegraphs should matter.

## Progression Hierarchy

### Primary: Body Modules

Modules define build identity.

Planned early slots:

- Head: targeting, sensing, scoring, food interaction.
- Core: shield, health proxy, power, heat safety.
- Spine: speed, turning, dash, length behavior.
- Tail: scrap, pickup, trail, hazard interaction.

Later slots can be added only after the first four are meaningful.

Module properties:

- Rarity or tier.
- Power cost.
- Heat cost or heat behavior.
- Primary effect.
- Drawback.
- Synergy tags.
- Upgrade level.
- Visual identity.

### Secondary: Skill Tree

The skill tree should unlock new strategic options rather than replace module
buildcraft.

Good skill nodes:

- Unlock a new module family.
- Increase loadout power budget slightly.
- Add a new reward type to the run pool.
- Add a new biome route.
- Improve lab services such as rerolling, crafting, or analysis.

Avoid flat stat-only trees until the module system has enough personality.

### Secondary: Loot And Materials

Loot supports crafting and module variation.

Good loot jobs:

- Craft a module.
- Upgrade a module.
- Add a modifier to a module.
- Open a boss-specific tech branch.
- Feed a lab experiment.

Loot should not bury the game in random numbers before the core run loop is fun.

## Difficulty Contract

The target is hard-fair mastery.

Rules:

- Lethal events need warning, pattern language, or clear precedent.
- Bosses should test routing and build choices, not hidden knowledge.
- Randomness can surprise, but it should not spawn unavoidable death.
- Permanent progress should soften repeated failure without deleting challenge.
- Developer mode must support fast balance checks for boss timing, speed, heat,
  hazard density, and reward pacing.

Pain is welcome. Cheapness is not.

## Boss Direction

The first serious boss family can evolve from the Pygame prototype's Circuit
Warden.

Desired boss traits:

- Clear weak point or bite target.
- Telegraph before area denial.
- Phase changes tied to HP or heat.
- Arena pressure that interacts with the snake body.
- Reward choice or module unlock after defeat.

Bosses should appear as learnable exams for the current biome and loadout, not
random bullet storms.

## Campaign Structure

The roguelite campaign should start simple:

- Biome ladder rather than open world.
- Lab upgrades between runs.
- Boss gates after biome tiers.
- Module unlocks through scrap, bosses, and skill nodes.
- Later strategy-map ideas stay parked until repeated runs are fun.

Possible biome direction:

- Neon Drain: tutorial scrapyard, simple hazards.
- Signal Mangrove: sensor interference, delayed telegraphs.
- Foundry Spine: heat pressure, molten lanes.
- Black Relay: boss-heavy signal corruption.

Names are placeholders, not final lore.

## Visual Direction

GBA-inspired means:

- Small internal canvas.
- Chunky readable sprites.
- Tile-first environments.
- Limited palettes by biome.
- Strong silhouette for snake parts and hazards.
- Crisp scaling, no blurry filters.
- UI that reads on a modern monitor.

It does not mean exact GBA hardware emulation.

## Developer Mode

Developer mode is part of the design, not a cheat afterthought.

Required design jobs:

- Spawn boss.
- Force reward selection.
- Grant scrap or module.
- Change heat and speed.
- Toggle hazard/boss telegraph overlays.
- Display RNG seed and active run state.
- Reload content once content loading exists.

This is needed because hard-fair difficulty cannot be tuned from full runs only.

## Out Of Scope

- Le Mans racing game.
- Open strategy map.
- Continuous action RPG world.
- Online progression.
- Multiplayer.
- Full asset editor.

These can be reconsidered only after CP10 or CP11 proves Ular has a strong
repeatable run loop.
