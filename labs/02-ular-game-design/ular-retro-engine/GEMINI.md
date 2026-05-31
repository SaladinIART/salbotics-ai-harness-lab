# GEMINI.md

## Project Summary

`ular-retro-engine` is the Pyxel-based remake track for `Ular
Cyber-Roguelite`.

The current playable Pygame prototype lives in the sibling folder
`cyber-roguelite-prototype`. This folder is now the newer Pyxel full-loop
prototype and does not modify that reference build.

## Current Checkpoint

CP11 implemented:

- Python package scaffold and Pyxel app boot.
- Title, Lab, and Play scenes.
- Scene stack, input mapper, profile store, and developer-mode flag.
- Deterministic `RunState`.
- Grid movement, reversal guard, food, score, length, collision, restart.
- Tail-safe movement into a vacating tail cell.
- Saved snake speed preference.
- Module catalog loaded from `content/modules.json`.
- Body slots: head, core, spine, tail.
- Lab loadout cycling.
- Scrap economy.
- Aux Power Bus skill unlock.
- Telegraphed hazards.
- Circuit Warden boss target.
- Reward choices.
- Developer hotkeys for boss, hazard, score, reward, shield, and hazard clear.
- Boss defeat unlocks Targeting Reticle and grants Warden Capacitor material.
- Score progression unlocks Overclock Spine.
- Unit tests and smoke notes through CP11.

Still intentionally absent:

- Generated sprite assets.
- Audio.
- Multiple biomes.
- Multiple bosses.
- Web export validation.
- Rich crafting/module upgrade UI.

## Locked Decisions

- Build a Pyxel-backed Salbotics Retro Engine layer, not a raw engine from
  scratch.
- Keep the game GBA-inspired, not strict hardware-accurate.
- Make Ular the flagship game; the Le Mans top-down racing idea is dropped for
  now.
- Preserve the identity as Tactical Snake+.
- Use a roguelite campaign structure.
- Make body modules the primary RPG/customization system.
- Use skill tree unlocks and loot/materials as supporting systems.
- Tune for hard-fair mastery.
- Optimize for Windows desktop first while avoiding choices that block later
  Pyxel web export.

## Terminology

- Ular: the cybernetic snake controlled by the player.
- Tactical Snake+: classic snake pressure expanded with modules, hazards, boss
  telegraphs, terrain, and build choices.
- Run: one mission attempt from launch to death, retreat, or clear.
- Lab: between-run hub for modules and upgrades.
- Body module: cybernetic part installed into a slot.
- Slot: head, core, spine, or tail.
- Power budget: loadout limit used by modules.
- Heat: run pressure that spawns hazards over time.
- Scrap: persistent currency earned from runs.
- Warden Capacitor: first boss material.
- Developer mode: built-in tuning/debug layer.

## Continuation Notes

Next safe work: playtest and balance pass. Focus on reward pacing, hazard
warning readability, boss visibility, module power pressure, scrap rewards, and
whether repeated failure feels worthwhile.

Recommended model for the next substantial pass: `gpt-5.4`, high reasoning.
