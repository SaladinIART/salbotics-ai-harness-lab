# CP7 Playtest Checklist

Use this after `npm run dev` starts the Phaser prototype.

## Goal

Verify that the first campaign season is understandable and that a player can
see why each duel matters.

## Setup

```powershell
cd "C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\03-underdog-racing"
npm install
npm run dev
```

Open the local Vite URL.

## Championship Loop

- Start from Title and enter the Garage.
- Confirm the Garage HUD shows `Street Underdog Cup`.
- Confirm the current round starts at `Round 1: Backlot Shakedown`.
- Start the event and race the blue rival.
- Finish order should produce either `Won duel` or `Rival won`.
- Return to Garage and confirm the points table changes.
- Repeat races as needed to earn enough reputation for later rounds.
- Use `Left`/`Right` to select newly unlocked events.
- Complete Dockside Sprint and Club License Trial.
- Confirm the cup completion message appears after the final round.
- If the player wins the cup, confirm `Local Parts Shop` sponsor appears.
- Confirm `Crew Notebook` shows as an unlocked team facility hook.

## Handling Feel

- Steering should remain readable on the oval.
- Handbrake should slide without becoming the only fast choice.
- Rival should feel beatable after upgrades.
- Upgrade purchases should produce noticeable speed, braking, or grip changes.

## Known CP7 Boundaries

- Only one rival exists.
- The championship uses one shared test track.
- Sponsor and team systems are hooks, not full management screens.
- No real sprite/audio asset pass has happened yet.

## Automated Checks

```powershell
npm test
npm run build
```

Expected: all tests pass and the build succeeds. A Phaser bundle-size warning is
acceptable for CP7.
