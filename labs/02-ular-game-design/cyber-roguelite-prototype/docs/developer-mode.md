# Developer Mode

Developer mode is for fast testing while tuning the game.

## Toggle

- `F1`: turn developer mode on/off.

The HUD shows extra developer hotkeys while it is active.

## Hotkeys

- `B`: spawn Circuit Warden boss during a run.
- `H`: spawn a hazard during a run.
- `C`: clear all hazards.
- `G`: add 1 score.
- `R`: open reward choices during a run.
- `V`: add 1 shield charge.

## Speed Controls

Speed controls work even outside developer mode:

- `[` or `-`: reduce base speed.
- `]` or `+`: increase base speed.

Base speed is saved in `saves/profile.json` as `snake_speed_fps`. The value is
clamped between `5` and `18`.

## Boss Test Flow

1. Press `Space` to start.
2. Press `F1`.
3. Press `B` to spawn the boss immediately.
4. Bite the blue boss node to damage it.
5. Press `V` before testing hazards if you want one shield buffer.

