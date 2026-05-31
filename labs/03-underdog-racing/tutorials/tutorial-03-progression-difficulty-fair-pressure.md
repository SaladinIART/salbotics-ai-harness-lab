# Tutorial 3: Progression, Difficulty, and Fair Pressure

## Goal

Learn how Underdog adds pressure without making the game feel random or unfair.

## Progression Stack

Underdog uses this order:

```text
car build first
driver skill second
championship structure third
sponsors and team management later
```

This matters because the player should feel that upgrades change the car, not
just numbers in a menu.

## Difficulty Should Be Explicit

Difficulty was added as a saved profile setting:

- Easy
- Normal
- Hard

Each difficulty changes rival performance. It is not hidden in the scene. It is
stored, normalized, shown in the HUD, and tested.

That is a harness lesson:

```text
If a setting changes the game, make it visible and testable.
```

## Fair Pressure

Good difficulty does not mean punishing the player blindly.

Fair pressure means:

- the rival can be understood
- the track explains mistakes
- the HUD shows useful state
- upgrades give a route forward
- the player can choose the pressure level

## What We Avoided

We did not jump into:

- full F1 seasons
- complex team management
- multiple vehicle categories
- pack AI
- weather and tire compounds

Those ideas are good, but only after the core loop is stable.

## Copy-Ready Prompt Card

```text
Add difficulty to this game in a fair and testable way.
Requirements:
- player can choose difficulty
- selected difficulty is saved
- difficulty is visible in the HUD
- difficulty changes opponent behavior or pressure
- old saves still load safely
- tests cover normalization and gameplay impact
```

## Recap

Progression gives hope. Difficulty gives pressure. The game needs both, but the
player must understand both.
