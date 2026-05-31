# CP2-CP7 Smoke Notes

CP2 creates the Phaser/Vite scaffold. CP3 adds the first playable time-trial
physics lab. CP4 adds the first garage upgrade economy. CP5 adds street-to-pro
event gates and driver XP. CP6 adds the first rival duel. CP7 adds the Street
Underdog Cup championship loop.

## Automated Checks

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\03-underdog-racing"
npm install
npm test
npm run build
```

Expected:

- Vehicle physics tests pass.
- Time-trial/lap tests pass.
- Progression, upgrade, save/load, and lap payout tests pass.
- Campaign gate, license unlock, and driver-skill tests pass.
- Rival pathing, finish-order, and duel reward tests pass.
- Championship calendar, standings, campaign advancement, and save migration
  tests pass.
- TypeScript and Vite build succeeds.

## Manual Browser Smoke

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\03-underdog-racing"
npm run dev
```

Open the shown localhost URL.

Expected:

- Title scene opens with Underdog branding.
- `Space` or `Enter` opens Garage.
- Garage shows money, reputation, build rating, and upgrade categories.
- `Up`/`Down` changes selected upgrade.
- `Left`/`Right` cycles unlocked campaign events.
- `1`/`2`/`3` chooses Easy, Normal, or Hard rival difficulty.
- `U` buys selected upgrade when money is available.
- `Space` starts the test track with upgraded vehicle specs.
- Test track shows a longer F1-inspired circuit with a start/finish
  straight, esses, hairpin, stadium section, curbs, pit-wall details, and
  path-based surface physics.
- A blue rival car follows the checkpoint racing line.
- Player and rival cars show front tires that rotate with steering.
- Player car shows a floating live speed readout.
- `WASD` or arrow keys drive.
- `Shift` or `Space` acts as handbrake.
- `R` resets.
- `Esc` returns to Garage.
- `F1` toggles debug telemetry in the HUD.
- HUD shows lap time, best lap, speed, surface, tire wear, and next gate.
- Finished laps award money/reputation and save the profile.
- Event results grant driver XP and can unlock club license.
- Duel results compare player and rival finish order.
- Garage HUD shows the Street Underdog Cup round and player/rival standings.
- Championship wins unlock sponsor/team hooks.

## CP3 Boundary

Implemented:

- One stock car.
- One test track.
- Acceleration, braking, steering, lateral grip, drift, surface drag, tire wear.
- Lap checkpoints and best lap.
- DOM HUD and debug telemetry.
- Money/reputation profile.
- Upgrade categories: tires, engine, brakes, gearbox, aero, weight.
- Upgrade purchase UI.
- Local profile save.
- Street-to-pro events.
- License and reputation gates.
- Driver XP/passive skills.
- One AI rival.
- Racing line/checkpoint path.
- Finish order and duel rewards.
- Street Underdog Cup calendar.
- Championship points table.
- Sponsor and team-management hooks.
- Canvas renderer selected for crash-resistant 2D pixel rendering.
- F1-inspired circuit map replacing the early oval.
- Visible front-tire steering and live speed readout.
- Player-selectable Easy/Normal/Hard rival difficulty.

Still future:

- Real art/audio assets.
- Multiple rivals and richer championship seasons.
