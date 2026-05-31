# Physics RFC

## Decision

Use a **simcade** top-down vehicle model.

Underdog should teach real racing concepts without becoming a strict simulator.
The player should feel acceleration, braking, lateral grip, drift, tire wear,
surface differences, and build tradeoffs, but the game should remain readable
and tunable.

## Why Not Raw Simulation First

A true racing simulator would require deep tire models, suspension, weight
transfer, drivetrain behavior, and track surface detail before the game becomes
fun. That is too much for the first harnessed checkpoints.

The better path:

```text
simple deterministic model -> playable feel -> debug metrics -> richer physics
```

Phaser handles rendering, scenes, camera, input plumbing, and browser runtime.
The game owns the simulation model so it can be tested and tuned outside Phaser
sprites.

## Core Concepts

### Velocity

Vehicle motion should be stored as a velocity vector, not just speed.

Useful values:

- Forward speed: movement along the car's facing direction.
- Lateral speed: sideways movement relative to the car.
- Angular velocity: how quickly the car rotates.

### Steering

Steering should be speed-sensitive.

Rules:

- At low speed, steering turns the car gently.
- At medium speed, steering is responsive.
- At high speed, steering should require planning and braking.
- Reverse or near-zero speed should not spin the car wildly.

### Grip

Grip reduces lateral velocity.

High grip:

- Car follows steering input.
- Less drift.
- Higher corner speed.

Low grip:

- More sliding.
- Longer braking zones.
- More dramatic correction.

Grip should be affected by tires, road surface, speed, tire wear, weather later,
and damage later.

### Braking

Braking should reduce forward speed and influence corner entry.

Later tuning hooks:

- Brake force.
- Brake bias.
- Lockup or slide tendency.
- Heat/fade for endurance events.

### Drift

Drift should be a controlled loss of lateral grip, not random sliding.

Useful early model:

- Compute lateral velocity.
- Reduce lateral velocity by grip strength each tick.
- Let low-grip tires or sharp steering preserve more lateral motion.
- Reward clean exit speed more than constant sliding.

### Tire Wear

Tire wear should matter after the first physics lab.

Tire wear sources:

- Hard braking.
- Long slides.
- High-speed cornering.
- Contact/collision.

Tire wear effects:

- Reduced grip.
- Longer braking.
- More heat.
- More risk late in race.

### Surfaces

Track surfaces should be data-driven.

Early surface types:

- Asphalt: normal grip.
- Painted curb: lower grip, good risk/reward.
- Dirt/gravel: low grip, slows car.
- Oil/wet later: very low grip, high caution.

## Upgrade Hooks

Car build stats should modify physics:

- Tires: grip, wear rate, wet/dirt behavior.
- Engine: acceleration, top speed, heat.
- Brakes: braking force, fade, control.
- Gearbox: acceleration curve, top-speed bias.
- Aero: high-speed stability, drag, cornering.
- Weight: acceleration, braking distance, collision impulse.
- Cooling: endurance consistency and heat recovery.
- Durability: damage tolerance and repair cost.

## Collision Policy

Early CP3 collision should be simple and readable.

Recommended:

- Track walls stop or bounce the car with speed loss.
- Cones/props slow the car and add small damage later.
- Checkpoints validate lap progress.
- No rival car collision until CP6.

## Debug Overlay

The first physics lab should display:

- Speed.
- Forward speed.
- Lateral speed.
- Grip scalar.
- Tire wear.
- Current surface.
- Lap time.
- Best lap.
- Reset hint.

This makes physics teachable instead of mysterious.

## Test Strategy

Physics tests should verify numbers, not visual feel:

- Acceleration increases forward speed.
- Braking reduces forward speed.
- Lateral grip reduces sideways velocity.
- Low-grip surface preserves more lateral velocity than asphalt.
- Tire wear reduces available grip.
- Reset returns car to start state.

Manual playtest still decides whether it feels fun.
