# Playtest Checklist

Use this checklist for a 10-15 minute CP5 playtest.

## Setup

- Install dependencies with `python -m pip install -e .`.
- Run with `python -m ular_cyber_roguelite`.
- Start with a fresh or disposable `saves/profile.json` if testing progression.

## Start And Loadout

- Start screen appears without errors.
- `Up` and `Down` select the four slots: head, core, spine, tail.
- `Left` and `Right` cycle modules in each slot.
- `[`/`]` or `-`/`+` changes saved base speed.
- Module choices persist after restarting the app.
- `Space` starts a run.

## Core Run

- Snake movement feels responsive.
- Instant reversal is blocked.
- Moving into a vacating tail cell is allowed.
- Food increases score and length.
- Wall and body collisions are clear.
- `P` pauses and resumes.

## Cybernetic Modules

- `Targeting Reticle` increases score per food.
- `Reactive Shield Core` absorbs one fatal hit.
- `Overclock Spine` makes the run faster.
- `Scrap Magnet Tail` increases scrap gained after death.

## Challenge Layer

- Yellow hazard warnings are visible before becoming active.
- Active hazards are visually distinct and lethal.
- Shield can absorb an active hazard.
- Heat rises over time or score.
- `Circuit Warden` appears at about score 8.
- Biting the boss damages it and moves it.
- Defeating the boss opens reward choices.

## Developer Mode

- `F1` toggles developer mode.
- `B` spawns the boss during a run.
- `H` spawns a hazard.
- `C` clears hazards.
- `G` adds score.
- `R` opens reward choices.
- `V` adds shield.

## Rewards And End State

- Score milestone opens a reward choice.
- `1`, `2`, and `3` select reward options.
- Rewards resume the run.
- Game over records scrap, runs, best score, and best length.
- Restart works after game over.

## Done Criteria

- One complete run reaches at least one reward.
- One complete run reaches or nearly reaches the boss.
- Death feels explainable from visible state.
- At least one module choice changes strategy.
