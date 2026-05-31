# Research Sources

CP1 records research sources only. Do not copy code from references into this
repo unless the license and attribution obligations are explicitly accepted.

## Chosen Engine

### Phaser

Links:

- https://phaser.io/
- https://docs.phaser.io/phaser/concepts/physics/matter
- https://phaser.io/examples/v3.55.0/physics/matterjs/view/top-down-car-body

Why it fits:

- Browser-first.
- Strong 2D sprite/tile workflow.
- Good scene, camera, and input primitives.
- Matter physics is available when rigid bodies help.
- Works well with TypeScript and DOM overlays.

Decision:

Use Phaser for scenes/rendering/input. Keep racing simulation rules in a
separate TypeScript module so physics can be tested without Phaser.

## Physics References

### Box2D Top-Down Car Physics

Link: https://phaser.io/tutorials/box2d-tutorials/top-down-car-physics

Useful ideas:

- Split forward and lateral velocity.
- Reduce lateral velocity through tire grip.
- Use impulses/forces to model traction.
- Treat top-down car handling as a controlled sliding problem.

### Godot 4 Top-Down Car Steering

Link: https://kidscancode.org/godot_recipes/4.x/2d/car_steering/

Useful ideas:

- Arcade-friendly steering can still use velocity and acceleration.
- Steering behavior should change with speed.
- A compact top-down model is enough for a fun first slice.

## Open-Source Racing References

### Dust Racing 2D

Link: https://github.com/juzzlin/DustRacing2D

Why it is useful:

- Top-down racing reference.
- Track editor ideas.
- AI/pathing and race flow inspiration.

License caution:

- GPL-licensed. Study design ideas only. Do not copy source into this MIT/CC
  learning repo without accepting GPL obligations.

### Speed Dreams

Link: https://www.speed-dreams.net/

Why it is useful:

- Open-source racing simulator project.
- Useful for terminology around cars, tracks, race formats, and simulation
  ambition.

License caution:

- GPL-oriented project. Study concepts and terminology only for this lab.

## Game Design Topics To Study

- Racing line: braking point, turn-in, apex, exit.
- Car setup tradeoffs: tires, aero, gear ratio, weight, brakes.
- Skill progression: reward player behavior, not only grinding.
- Event ladder: street races, license tests, club events, pro tiers.
- Time trial UX: lap timer, best lap, delta, reset, ghost later.

## Licensing Rule

Research links are references. CP1 copies no code, art, tracks, car data,
brands, logos, or assets.
