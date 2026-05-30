# Balance Notes

## CP5 Targets

- First run duration: 2-5 minutes.
- First reward: around score 6.
- Boss reveal: around score 12.
- Boss durability: 3 hits.
- Hazards: readable warnings before lethal cells.

## Current Balance Read

- The loop is intentionally compact. Score 6 and score 12 are reachable quickly
  with score-focused modules.
- `Reactive Shield Core` is the safest learning module because it forgives one
  fatal hit.
- `Overclock Spine` creates a strong risk/reward pressure because speed and
  score both rise.
- `Scrap Magnet Tail` is a meta-progression hook, but scrap currently has no
  spend sink. That is acceptable for CP5 and should be solved in a later
  checkpoint.

## CP5 Balance Fix

Classic snake movement now allows moving into the tail cell when the tail will
move away that tick. This makes tight turns feel fairer and reduces accidental
deaths that read as rules friction instead of player error.

## Tuning Levers

- Raise `REWARD_INTERVAL` if rewards interrupt the run too often.
- Raise `BOSS_SCORE_THRESHOLD` if the boss appears before the player understands
  hazards.
- Increase hazard warning duration if active hazards feel cheap.
- Lower `fps_delta` on `Overclock Spine` if speed becomes too punishing.
- Add a scrap sink only after playtesting confirms module choices are fun.

