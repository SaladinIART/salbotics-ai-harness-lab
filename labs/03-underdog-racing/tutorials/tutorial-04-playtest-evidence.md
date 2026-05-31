# Tutorial 4: Playtest Evidence Beats Vibes

## Goal

Learn why Underdog uses both automated tests and browser smoke tests.

## The Crash Lesson

The automated tests passed, but the browser still showed a black screen in one
test environment.

The cause was rendering-related: Phaser selected WebGL, and the environment
reported a framebuffer problem.

The fix was to force Canvas rendering for this 2D pixel prototype.

## The Lesson

```text
Unit tests can prove rules.
Browser smoke tests prove the player can see and use the game.
```

Both are needed.

## Evidence We Captured

The project now keeps screenshots in `docs/`:

- `circuit-smoke.png`
- `vehicle-difficulty-smoke.png`

These are not just decoration. They are evidence that the game boots, renders,
and reaches the intended scene.

## What To Test Manually

When playtesting, ask:

- Can I start the game?
- Can I reach the Garage?
- Can I choose difficulty?
- Can I start a race?
- Is the car visible?
- Do the front tires turn?
- Does speed update?
- Does the rival move?
- Does the HUD explain enough without blocking the playfield?

## Copy-Ready Prompt Card

```text
Run a browser smoke test for this game.
Verify:
- title screen loads
- garage opens
- difficulty can be changed
- race starts
- no console/page errors
- screenshot proves the playfield renders
- HUD text matches the current state
Summarize failures with reproduction steps.
```

## Recap

"It builds" is not the same as "a player can play it."

The screenshot is part of the harness.
