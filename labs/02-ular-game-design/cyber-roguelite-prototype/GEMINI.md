# GEMINI.md

## Project Summary

This folder contains the Python/Pygame prototype for `Ular Cyber-Roguelite`.

The project is inspired by the public GitHub repo
`SaladinIART/Ular_yg_Mengular`, but it is a clean rebuild. No gameplay source
files have been copied into this folder.

## Current Checkpoint

CP5 implemented:

- Clean playable Python/Pygame snake skeleton.
- Pure domain logic and systems separated from rendering.
- Four cybernetic slots: head, core, spine, tail.
- Starter active modules: Targeting Reticle, Reactive Shield Core, Overclock
  Spine, Scrap Magnet Tail.
- Local profile save at `saves/profile.json`.
- Telegraphed hazards: warning cells become active lethal cells after a delay.
- Heat scaling: pressure rises with score/time and slightly increases speed.
- Circuit Warden miniboss: blue target node, 3 HP, reward on defeat.
- Milestone reward screen: choose with `1`, `2`, or `3`.
- Tail-safe movement polish: moving into a vacating tail cell is allowed.
- Playtest and handoff docs are in `docs/`.
- Balance targets are in `content/balance_targets.json`.
- Standard-library tests cover movement, food, reversal guard, restart,
  collision behavior, module modifiers, shield behavior, profile persistence,
  hazards, boss damage, and reward choices.
- No campaign RPG, territory strategy, online services, or asset pipeline yet.

## Design Spine

Primary direction: cyber-roguelite snake.

Core feel:

- Short runs.
- Hard-but-fair challenge.
- Tactical hazards with readable warnings.
- Cybernetic modules with tradeoffs.
- Persistent progression that makes repeated failure worthwhile.

## Terminology

- Ular: the player-controlled snake.
- Run: one attempt from start to death or clear.
- Cybernetic module: an upgrade installed into a body slot.
- Slot: planned module location such as head, core, spine, or tail.
- Heat: planned difficulty pressure that rises during a run.
- Scrap: planned upgrade currency.

## Parked Expansion Branches

Campaign RPG branch:

- World map, quests, bosses, characters, narrative progression.
- Not part of CP1.

Open strategy branch:

- Resource map, territory control, base planning, longer strategic decisions.
- Not part of CP1.

## Continuation Notes

The checkpoint series CP1-CP5 is complete for this vertical slice. Next safe
work should be either manual playtest tuning or a new planned checkpoint, not a
silent expansion into campaign or strategy systems.

## Next Guardrail

Do not add big new systems without a new checkpoint plan. Tune the current loop
first: hazard readability, reward pacing, boss timing, and module tradeoffs.

Recommended model for next substantial checkpoint: `gpt-5.4` with high
reasoning.
