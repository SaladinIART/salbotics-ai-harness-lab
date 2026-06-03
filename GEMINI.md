# GEMINI.md

## Project Summary

`salbotics-ai-harness-lab` is a public learning hub for harness engineering: a practical way to make AI-assisted work repeatable, reviewable, and less likely to drift into rabbit holes.

The first release supports a 15-20 minute talk:

**Implement Harness Engineering: A Clear Path to Minimize Rabbit Holes While Vibing**

Audience priority:

1. Never-coders and domain experts
2. Vibe coders and AI tool users
3. Technical people who want repeatable AI workflows

## Core Message

Vibing is not the problem. Unmanaged vibing is.

Harness engineering gives AI work a reusable shape:

```text
Goal + Context + Path + Checkpoints + Done Criteria
```

The phrase to preserve:

> Do not prompt harder. Harness better.

## Tone

Use casual, plain English. Keep the language practical and encouraging. Avoid heavy theory unless it is hidden behind simple examples.

Acceptable style:

- Friendly
- Beginner-safe
- Practical
- Slightly playful
- Respectful of domain experts

Avoid:

- Dense AI jargon
- Tool worship
- Making non-coders feel behind
- Overexplaining GitHub mechanics in the main learning path

## Salbotics Imprint

Use this exact imprint:

```text
Salbotics Solutions — Built for Real World, Not Textbook.
```

The imprint should feel like authorship and stewardship, not hard selling.

## Episode 1 Continuation Notes

Episode 1 teaches harness engineering through a simple app-building example. The app can be patient tracking, chemical inventory, animation asset tracking, or any repeated domain task.

When simplifying, do not replace the deck first. Add companion guides, worksheets, templates, and short examples.

## Episode 2 Continuation Notes

Episode 2 is `episodes/02-lessons-from-real-projects/`.

It shares public-safe lessons from past Salbotics work for non-technical builders. Use anonymized patterns only: fake examples, generic roles, reusable prompt cards, worksheets, and checklists.

Do not add client names, local paths, private repo names, account details, buyer data, exact operational numbers, commercial strategy, internal product design, private screenshots, or personal notes. If a lesson only works by revealing private detail, do not publish it.

Current Episode 2 files:

- `README.md`: episode index and checkpoint master list.
- `public-safety-map.md`: allowed themes, forbidden detail categories, and review checklist.
- `tutorial-template.md`: required tutorial structure.
- `tutorial-01` through `tutorial-05`: work order, context packs, checkpoint rule, testing, and public lessons.
- `worksheets/`: prompt brief, redaction checklist, checkpoint review, and handoff checklist.

## Episode 3 Continuation Notes

Episode 3 is `episodes/03-programming-language-swot/`.

It teaches programming language applications and SWOT for students planning
5-10 years ahead. Keep it public-safe and student-focused. The core message is:
do not learn every language equally; learn a practical stack first, then
specialize based on project needs.

Current Episode 3 files:

- `README.md`: module overview, language groups, sources, and exercise
  placeholder.
- `language-swot-report.md`: full student programming language applications
  and SWOT report.

Next safe work: design practical exercises that test whether learners can match
project needs to language functionality and justify choices through SWOT plus
the harness formula.

## Lab 02 Current State

Lab 02 is now implemented as a public-safe rebuild inspired by "Ular yg
Mengular" snake-game work. Do not copy private game repo files.

Current tracks:

- `labs/02-ular-game-design/cyber-roguelite-prototype`: earlier Python/Pygame
  checkpoint slice.
- `labs/02-ular-game-design/ular-retro-engine`: current Pyxel CP11 prototype
  with Lab, modules, hazards, boss, rewards, scrap economy, developer mode, and
  tests.

Use `labs/02-ular-game-design/tutorial-cp11-playtest.md` for the current
teaching/playtest walkthrough.

## Lab 03 Current State

Lab 03 is a Phaser + TypeScript track for `Underdog Racing`.

Current folder:

- `labs/03-underdog-racing`

Current state:

- Phaser + TypeScript.
- Top-down pixel racing.
- Street-to-pro drama.
- Simcade physics.
- Time trial first.
- Car build primary, driver skill passive, team management later.
- CP7 implemented: playable time-trial physics lab with one stock car, one test
  track, lap timing, DOM HUD, debug telemetry, Garage upgrades, lap payouts,
  local profile save, street-to-pro event gates, driver XP/passives, one-rival
  AI duel, Street Underdog Cup championship loop, sponsor/team hooks, and
  Vitest physics/progression/campaign/rival/championship tests.
- Post-CP7 polish implemented: Canvas rendering for stability, F1-inspired
  circuit, visible front-tire steering, floating speed readout, and
  Easy/Normal/Hard rival difficulty.
- Dedicated learning tutorials exist in
  `labs/03-underdog-racing/tutorials/`, including `wisdoms-from-underdog.md`.

Next safe work is post-CP7 deepening: better tracks, multiple rivals, sprite
and audio assets, endurance systems, tire compounds, richer sponsors, and a
fuller championship calendar.

## Checkpoint Structure

Checkpoint 1: Repo scaffold
Master list: local folder, git init, licenses, README, GEMINI, Pages shell.

Checkpoint 2: Episode 1 content
Master list: PPTX, PDF, slides.md, beginner guide, worksheet, glossary, templates.

Checkpoint 3: Public launch
Master list: public GitHub repo, Pages enabled, links tested, Salbotics imprint visible, no private files.

Checkpoint 4: Lab 02 implementation
Master list: Lab 02 docs, public-safe snake-game scope, Pyxel CP11 prototype,
prompt harness, worksheet, playtest tutorial, smoke notes.

Checkpoint 5: Lab 03 research
Master list: labs/03-underdog-racing, Phaser/TypeScript direction, Underdog
racing RFCs, physics/progression roadmap, GPL study-only cautions.

Checkpoint 6: Episode 2 public tutorial pack
Master list: episodes/02-lessons-from-real-projects, public-safety map,
tutorial template, 5 tutorials, 4 worksheets, README/GEMINI/static-site links,
privacy scan, Markdown link check.

Checkpoint 7: Lab 03 learning layer
Master list: Underdog tutorial index, 4 tutorials, wisdoms page, Lab 03 README
links, labs index link, root README link, homepage sections for current labs and
Underdog lessons.

Checkpoint 8: Episode 3 language SWOT
Master list: episodes/03-programming-language-swot, full language SWOT report,
root README link, homepage Episode 3 section, exercise placeholder for future
classroom activities.

## Recommended Model

For future major planning or rewrite work, use `gpt-5.4` with high reasoning.

Estimated token ranges:

- Repo scaffold and licensing: 3k-5k
- Beginner guide and worksheet rewrite: 6k-10k
- GitHub Pages static site: 4k-7k
- Public safety review: 3k-6k
- Future Ular lab planning: 4k-8k
- Episode 2 public tutorial pack: 25k-45k drafting, 8k-15k review
- Lab 03 learning layer: 8k-14k drafting, 3k-6k review
- Episode 3 exercise design: 8k-14k planning, 4k-8k worksheet drafting
