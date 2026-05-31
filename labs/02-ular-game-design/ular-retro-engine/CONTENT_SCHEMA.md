# Content Schema RFC

## Decision

Use data files for game content and balance from the beginning of the Pyxel
remake.

Initial implementation should prefer JSON because the current prototype already
uses JSON and Python can validate it easily. TOML can be reconsidered later for
designer-authored files if comments and readability become more important than
strict JSON tooling.

This document defines target shapes only. CP6 does not add real content files.

## Shared Rules

Every content record should include:

- `id`: stable machine identifier.
- `name`: display name.
- `description`: short player-facing text.
- `tags`: list of system tags for synergies and filtering.
- `tier`: integer progression tier where relevant.

Validation should fail when:

- Required fields are missing.
- IDs are duplicated.
- Numeric limits are outside documented bounds.
- Referenced IDs do not exist.
- Unknown enum values appear.

## Modules

Modules are the main progression content.

Planned fields:

```json
{
  "id": "core_reactive_shield",
  "name": "Reactive Shield Core",
  "slot": "core",
  "tier": 1,
  "rarity": "starter",
  "power_cost": 2,
  "heat_cost": 1,
  "tags": ["shield", "survival"],
  "effects": [
    {"type": "grant_shield", "amount": 1}
  ],
  "drawbacks": [
    {"type": "starting_length_delta", "amount": 1}
  ],
  "upgrade_track": ["core_reactive_shield_mk2"]
}
```

Required early slots:

- `head`
- `core`
- `spine`
- `tail`

Required early effect families:

- Score multiplier or bonus.
- Starting length delta.
- Base speed delta.
- Shield grant.
- Scrap multiplier.
- Heat generation or reduction.

## Arenas

Arenas define tile layout, spawn rules, visual palette, and challenge modifiers.

Planned fields:

```json
{
  "id": "neon_drain_01",
  "name": "Neon Drain",
  "biome": "neon_drain",
  "tier": 1,
  "size": {"w": 28, "h": 18},
  "tilemap": "neon_drain_01",
  "palette": "neon_drain",
  "spawn_rules": {
    "food_min_distance": 5,
    "hazard_safe_radius": 4
  },
  "modifiers": [
    {"type": "heat_rate_delta", "amount": 0}
  ],
  "boss_pool": ["circuit_warden"]
}
```

Arena rules must prevent unavoidable opening deaths.

## Bosses

Boss content defines readable attack patterns and rewards.

Planned fields:

```json
{
  "id": "circuit_warden",
  "name": "Circuit Warden",
  "tier": 1,
  "hp": 3,
  "weak_point": "node",
  "telegraph_ticks": 36,
  "patterns": [
    {
      "id": "lane_sweep",
      "weight": 3,
      "warning_shape": "lane",
      "active_ticks": 24,
      "cooldown_ticks": 48
    }
  ],
  "rewards": ["reward_boss_scrap", "reward_module_cache"]
}
```

Boss validation must check that pattern timing is long enough for human
reaction at the target speed range.

## Rewards

Rewards are run-time choices.

Planned fields:

```json
{
  "id": "reward_emergency_shield",
  "name": "Emergency Shield",
  "tier": 1,
  "tags": ["survival", "shield"],
  "weight": 4,
  "requirements": [],
  "effects": [
    {"type": "grant_shield", "amount": 1}
  ]
}
```

Reward pools should support:

- Milestone rewards.
- Boss rewards.
- Biome-specific rewards.
- Module-synergy rewards.

## Skill Tree Nodes

Skill nodes define permanent unlocks.

Planned fields:

```json
{
  "id": "lab_power_budget_01",
  "name": "Auxiliary Power Bus",
  "tier": 1,
  "cost": {"scrap": 50},
  "requires": [],
  "unlocks": [
    {"type": "power_budget_delta", "amount": 1}
  ]
}
```

Skill nodes should prioritize unlocking choices over flat stat inflation.

## Loot And Materials

Loot supports module crafting and upgrades.

Planned fields:

```json
{
  "id": "warden_capacitor",
  "name": "Warden Capacitor",
  "rarity": "rare",
  "tags": ["boss", "core", "shield"],
  "sources": ["circuit_warden"],
  "uses": [
    {"type": "craft_module", "target": "core_reactive_shield_mk2"}
  ]
}
```

Loot should remain secondary to module buildcraft.

## Balance Tables

Balance records keep tuning outside code.

Planned fields:

```json
{
  "id": "default_run_balance",
  "speed": {
    "min_fps": 5,
    "default_fps": 8,
    "max_fps": 18
  },
  "heat": {
    "base_rate": 1,
    "score_weight": 0.2,
    "time_weight": 0.05
  },
  "boss": {
    "first_threshold_score": 8,
    "repeat_threshold_score": 20
  }
}
```

Balance tables should be small and named. Avoid scattering constants across
systems.

## Profile Save Shape

Profile save is not content, but content IDs will appear inside it.

Planned profile fields:

```json
{
  "version": 1,
  "total_runs": 0,
  "best_score": 0,
  "scrap": 0,
  "snake_speed_fps": 8,
  "unlocked_modules": ["head_stock_sensor", "core_reactive_shield"],
  "equipped_modules": {
    "head": "head_stock_sensor",
    "core": "core_reactive_shield",
    "spine": "spine_overclock",
    "tail": "tail_scrap_magnet"
  },
  "skill_nodes": [],
  "materials": {}
}
```

Profile migrations should be explicit once shipped saves exist.
