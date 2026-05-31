# Prompt Harness: Ular Game Design

Use this prompt when continuing the current Pyxel prototype or teaching how the
project reached CP11.

```text
I want to continue the public-safe Ular Cyber-Roguelite prototype.

Current folder:
C:\Users\salbot01\Salbotics\salbotics-ai-harness-lab\labs\02-ular-game-design\ular-retro-engine

Current checkpoint:
CP11 is complete.

Current game:
- Pyxel-based Tactical Snake+ roguelite prototype.
- Title, Lab, and Play scenes.
- Body module slots: head, core, spine, tail.
- Module definitions live in content/modules.json.
- Lab lets the player cycle unlocked modules.
- Runs include food, score, length, collision, hazards, reward choices, and Circuit Warden boss target.
- Runs earn scrap, unlock modules, and persist profile data.
- Developer mode supports boss, hazard, score, reward, shield, and clear hotkeys.

Goal:
Improve the game through one clear checkpoint at a time.

Audience:
Beginners learning harness engineering through a real game-design example.

Rules:
- Preserve the current Pygame prototype as reference.
- Work in ular-retro-engine unless the task says otherwise.
- Keep changes checkpoint-sized.
- Update README.md, GEMINI.md, ROADMAP.md, and smoke notes when behavior changes.
- Add tests for deterministic systems.
- Do not add private files, generated caches, or personal save data.

Good next checkpoints:
1. Playtest and balance pass.
2. Pixel sprite and palette pass.
3. Audio cue pass.
4. Web export trial.
5. Additional biome and boss pass.

Done criteria:
- The change is playable or verifiable.
- Tests pass with python -m unittest discover -s tests.
- Docs explain what changed and how to run it.
- Existing unrelated files are not modified.
```

## Minimal Teaching Prompt

For a classroom or beginner demo, use this shorter version:

```text
We have a Pyxel snake roguelite prototype at CP11.

Please inspect the project first, then make one small improvement.
Keep the checkpoint small, update docs, add tests if the logic changes, and
explain how to verify it.
```
