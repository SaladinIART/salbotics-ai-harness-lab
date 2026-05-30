# Handoff

## Current State

CP1 through CP5 are complete for the first vertical slice.

The prototype is a clean Python/Pygame rebuild with:

- Snake movement, food, score, collision, pause, restart.
- Four cybernetic slots and starter modules.
- Local profile save.
- Telegraphed hazards, heat scaling, milestone rewards, and Circuit Warden
  miniboss.
- Saved speed customization and developer mode.
- Tests for core logic, modules, profile, hazards, boss, and rewards.

## How To Verify

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\cyber-roguelite-prototype"
python -m pip install -e .
python -m unittest discover -s tests
python -m ular_cyber_roguelite
```

## Safe Next Work

Start with playtest tuning before adding new systems:

- Tune reward pacing.
- Tune hazard warning and active durations.
- Tune boss score threshold.
- Decide whether scrap should unlock modules or reroll rewards.
- Decide whether developer mode should become a proper debug overlay.

## Expansion Boundaries

Do not add campaign RPG or open strategy systems until the current run loop is
fun for repeated 5-minute sessions.

Parked expansion path:

- CP6: scrap shop and unlock economy.
- CP7: authored arenas and boss attack patterns.
- CP8: campaign map prototype.
- CP9: open strategy layer prototype.
