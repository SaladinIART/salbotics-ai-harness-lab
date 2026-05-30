# Known Issues

## Current Rough Edges

- Profile save is local JSON only. There is no migration system beyond version
  normalization.
- Scrap accumulates but cannot yet be spent.
- The reward pool is small and can repeat similar run shapes.
- Boss movement is random after each hit; it is readable but not yet expressive.
- Hazard placement is random and not authored into arenas.
- UI is serviceable Pygame text, not final art direction.
- There is no sound, animation polish, or accessibility settings.
- Developer mode is intentionally simple and does not have an in-game menu yet.

## Not Bugs For CP5

- Campaign RPG systems are intentionally not implemented.
- Open strategy/base systems are intentionally not implemented.
- Online leaderboard and accounts are intentionally not implemented.
- Asset pipeline and sprite art are intentionally not implemented.

## Next Fix Candidates

- Add a small scrap shop for permanent unlocks.
- Add authored arena patterns instead of purely random hazard cells.
- Add a clearer boss telegraph and attack rhythm.
- Add visual/audio feedback for shield burn, reward install, and boss hit.
