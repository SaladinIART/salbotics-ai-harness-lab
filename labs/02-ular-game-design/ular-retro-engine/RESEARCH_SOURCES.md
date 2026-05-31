# Research Sources

CP6 uses external projects as research references, not copied source.

## Chosen Base

### Pyxel

Link: https://github.com/kitao/pyxel

Why it fits:

- Python-first retro game engine.
- Strong constraints: limited palette, simple audio, small-game feel.
- Good match for a GBA-inspired Ular remake and the current Python workflow.
- Lets Salbotics build a game-specific engine layer without rebuilding low-level
  runtime systems.

Tradeoff:

- Dense RPG UI may need careful layout because the retro frame is small.

## Alternatives Considered

### Godot

Link: https://docs.godotengine.org/en/stable/

Why it is attractive:

- Mature open-source 2D/3D engine.
- Strong editor, scenes, animation, input, import, UI, and packaging tools.
- Best option if the main priority becomes full-scale production speed.

Why not chosen for this path:

- It reduces the need to build a Salbotics-specific retro engine layer.
- It moves the project away from the current Python prototype lineage.

### TIC-80

Link: https://github.com/nesbox/TIC-80

Why it is attractive:

- Fantasy computer with built-in code, sprite, map, and sound tools.
- Strong tiny-cartridge retro identity.

Why not chosen:

- Better for small fantasy-console games than a larger RPG roguelite campaign.

### raylib

Link: https://github.com/raysan5/raylib

Why it is attractive:

- Lightweight C library for games and tools.
- More low-level control than Pyxel.

Why not chosen:

- Higher engineering cost for the current project.
- Less direct continuity with the Python/Pygame prototype.

### Phaser

Link: https://phaser.io/phaser4

Why it is attractive:

- Open-source HTML5 game framework.
- Strong option for browser-first games.

Why not chosen:

- The current priority is Python-first Windows desktop with later web export,
  not web-first development.

### MonoGame And HaxeFlixel

Links:

- https://monogame.net/
- https://haxeflixel.com/

Why they are attractive:

- Proven open-source 2D game frameworks.
- Useful references for state management, cameras, content, and platform builds.

Why not chosen:

- They require larger language/toolchain shifts than Pyxel.

## Visual Reference

### Tonc GBA Graphics Notes

Link: https://www.coranac.com/tonc/text/video.htm

Useful lessons:

- GBA screen reference: 240x160.
- Tile-first backgrounds and sprites are a practical mental model.
- Palettes, layers, and readable sprite shapes should guide the art pipeline.

Important boundary:

- Ular Retro Engine should be GBA-inspired, not hardware-authentic.

## Parked Reference

### Dust Racing 2D

Link: https://github.com/juzzlin/DustRacing2D

Why it was considered:

- Open-source top-down racing reference with a level editor.
- Useful if the Le Mans endurance racing idea returns later.

Why it is parked:

- The user chose to drop Le Mans for now and focus on Ular.
- It is GPL-3.0 licensed, so it should be studied carefully and not copied into
  this project without accepting GPL obligations.
