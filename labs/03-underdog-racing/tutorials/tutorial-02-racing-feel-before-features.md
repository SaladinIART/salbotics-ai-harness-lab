# Tutorial 2: Racing Feel Before Racing Features

## Goal

Understand why the driving feel had to come before campaign systems.

## The Rule

```text
Handling feel first. Tournament drama second.
```

If the car does not feel readable, no amount of money, upgrades, sponsors, or
championship points can save the game.

## What We Built

The physics lab started with:

- acceleration
- braking
- steering
- lateral grip
- drift/slide behavior
- tire wear
- road, curb, and grass surfaces
- checkpoint lap timing

Only after that did we add garage upgrades and rivals.

## Why Front Tires Matter

The first vehicle was just a rectangle. It moved, but it did not explain itself.

Adding visible front tires made steering readable:

- the player can see input direction
- the car feels more mechanical
- screenshots communicate racing better
- debugging handling becomes easier

The floating speed readout helped for the same reason. It turns feel into
evidence.

## Why We Changed the Track

The early oval was useful for CP3, but boring later. A better circuit needed:

- a start/finish straight
- braking zones
- esses
- a hairpin
- a final technical section
- curbs and grass that match physics

The lesson is simple:

```text
A test map is allowed to be boring.
A racing map is not.
```

## Copy-Ready Prompt Card

```text
Improve the playfeel of this vehicle game.
Do not add campaign features yet.
Focus on readable movement:
- steering feedback
- speed feedback
- surface feedback
- track shape
- player recovery after mistakes
Add tests where the simulation changes.
Use browser smoke tests where rendering changes.
```

## Recap

Racing games are built from feedback loops. The player presses, the car
responds, the screen explains what happened.
