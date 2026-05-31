# Game Design RFC

## Product Direction

**Underdog** is a top-down pixel racing game about climbing from street racing
into professional competition.

The emotional arc:

```text
scrap car -> local respect -> risky street events -> license chance -> club
racing -> endurance/pro events -> formula-inspired top tier
```

The game should make the player feel that better driving and smarter upgrades
matter more than raw grinding.

## Design Pillars

- Handling feel first: the car must be satisfying before the campaign gets big.
- Street-to-pro drama: early races feel improvised and risky; later races feel
  structured, licensed, and competitive.
- Build the machine: car upgrades are the main expression of progression.
- Earn the driver: passive skills unlock from demonstrated driving habits.
- Readable top-down racing: track, grip, speed, braking, and collision state
  should be easy to inspect.
- Harnessed ambition: every checkpoint must stay playable or verifiable.

## Core Loop

1. Start in the garage.
2. Choose event or test session.
3. Tune or upgrade the vehicle.
4. Drive a short race/time-trial/challenge.
5. Earn money, parts, reputation, XP, or license progress.
6. Repair, upgrade, unlock, and try harder events.

Early playable loop should be smaller:

```text
Garage -> Time Trial -> Result -> Upgrade -> Time Trial
```

AI rivals and championship tables should wait until the vehicle feel is strong.

## Campaign Ladder

The campaign should be street-to-pro, not all vehicles everywhere at once.

Planned ladder:

- Backlot Bicycle Runs: optional tutorial-like handling school.
- Moped Alley: low-speed vehicle control and traffic-cone routes.
- Street Compact: first real car, money pressure, illegal events.
- Club License: transition into sanctioned competition.
- Touring Underdog: proper circuits, tire wear, brakes, endurance.
- Prototype/Formula Gate: high aero, high speed, high precision.

The bicycle/motorcycle ideas are useful as low-speed teaching tiers, but they
should not distract from the main car-build fantasy. The primary campaign should
be about becoming a racer, not collecting every vehicle type equally.

## First Playable Target

Time trial first.

Required early experience:

- One car.
- One small test track.
- Start/finish line.
- Lap timer.
- Reset car.
- Basic acceleration, braking, steering, drift/grip behavior.
- Debug overlay for speed, lateral velocity, grip, and lap timing.

No AI opponent in the first playable slice. The player should be able to feel
whether the car is good before the game asks them to race someone.

## Race Formats

Future formats:

- Time trial: learn track and tune build.
- License test: prove braking, racing line, and clean driving.
- Rival duel: one opponent with a strong identity.
- Street sprint: short point-to-point race.
- Club circuit: multi-lap legal race.
- Endurance run: durability, tire wear, fuel/cooling later.
- Championship: event calendar, points, sponsors, advancement.

## Failure And Progress

Failure should produce learning and some progress, but not free victory.

Possible outcomes:

- Clean lap bonus.
- Damage cost.
- Reputation gain/loss.
- Money prize.
- Part drop or sponsor interest.
- Driver XP for repeated behaviors.
- License progress if requirements are met.

The game should reward both speed and craft: clean braking, good exits, low
damage, consistent laps, and smart upgrades.

## Camera And Visual Style

Use top-down pixel art.

Reason:

- Strong track readability.
- Clear vehicle orientation.
- Easier collision and physics debugging.
- Better fit for Phaser.
- Better teaching surface for racing-line and grip concepts.

Avoid angled 2.5D for the first track because it complicates asset production,
track readability, and collision alignment.

## Out Of Scope For Early Checkpoints

- Full open world.
- Police systems.
- Online multiplayer.
- Deep crew management.
- Dozens of vehicles.
- Full F1 simulation.
- Licensed real brands, teams, tracks, or logos.
