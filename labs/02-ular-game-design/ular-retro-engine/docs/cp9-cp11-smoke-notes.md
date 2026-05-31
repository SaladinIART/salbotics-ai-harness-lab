# CP9-CP11 Smoke Notes

CP9 through CP11 finish the first full Pyxel roguelite loop.

## Automated Checks

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m compileall -q src tests
```

Expected:

- CP7 and CP8 tests still pass.
- Module catalog loads from `content/modules.json`.
- Loadout effects apply to shield, scrap multiplier, speed, score, heat, and
  starting length.
- Active hazards consume shield or end the run.
- Rewards apply and resume play.
- Circuit Warden defeat opens a reward and grants bonus scrap.
- Lab skill purchase spends scrap and increases power budget.
- Finished boss runs grant scrap, unlocks, and Warden material.

## Manual Window Smoke

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine"
.\install_and_run.bat
```

Expected flow:

1. Title opens.
2. `Space` enters the Lab.
3. In Lab, `Up`/`Down` chooses body slot and `Left`/`Right` cycles unlocked
   modules.
4. `U` buys Aux Power Bus if the profile has at least 10 scrap.
5. `Space` starts a run.
6. Eat food to score; score milestones open rewards.
7. Press `1`, `2`, or `3` on reward screen.
8. At score 8, Circuit Warden can appear. Bite the blue target to damage it.
9. Yellow warning hazards become red active hazards.
10. Death or clear grants scrap back to the profile.
11. `Esc` returns to Lab.

Developer mode:

- `F1`: toggle developer mode.
- `B`: spawn boss.
- `H`: spawn hazard.
- `G`: add score.
- `R`: open reward choices.
- `V`: add shield.
- `C`: clear hazards.

## Current Scope Boundary

Implemented: body modules, Lab scene, scrap economy, one skill unlock, hazards,
boss target, reward choices, developer hotkeys, and profile persistence.

Still future: sprite art pipeline, audio, multiple biomes, multiple bosses, web
export validation, and richer module upgrading/crafting UI.
