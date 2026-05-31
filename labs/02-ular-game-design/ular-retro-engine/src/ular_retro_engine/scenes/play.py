from __future__ import annotations

from ..input import ActionSnapshot
from ..modules import loadout_stats, normalize_loadout
from ..profile import MAX_SPEED_FPS, MIN_SPEED_FPS, Profile, clamp_speed
from ..run_state import Direction, Hazard, RunState
from ..scene import BaseScene, Renderer


CELL_SIZE = 8
PLAYFIELD_X = 8
PLAYFIELD_Y = 18
HUD_X = 176


class PlayScene(BaseScene):
    name = "play"

    def __init__(self) -> None:
        self.run_state: RunState | None = None
        self.tick_accumulator = 0
        self.run_recorded = False

    def enter(self, context) -> None:
        super().enter(context)
        profile = self._profile()
        catalog = self.context.content_registry.module_catalog()
        profile.equipped_modules = normalize_loadout(catalog, profile.unlocked_modules, profile.equipped_modules)
        self.context.profile_store.save(profile)
        stats = loadout_stats(catalog, profile.equipped_modules)
        self.run_state = RunState(seed=profile.total_runs + 1, loadout=stats)

    def handle_input(self, actions: ActionSnapshot) -> None:
        run_state = self._run_state()
        if actions.pressed("cancel"):
            from .lab import LabScene

            self.context.replace_scene(LabScene())
            return

        if actions.pressed("speed_down"):
            self._change_speed(-1)
        elif actions.pressed("speed_up"):
            self._change_speed(1)

        if self.context.debug_console.enabled:
            self._handle_debug(actions)

        if run_state.phase == "reward":
            if actions.pressed("reward_1"):
                run_state.choose_reward(0)
            elif actions.pressed("reward_2"):
                run_state.choose_reward(1)
            elif actions.pressed("reward_3"):
                run_state.choose_reward(2)
            return

        if run_state.phase in {"game_over", "cleared"}:
            if actions.pressed("confirm"):
                self._restart_run()
            return

        if actions.pressed("move_up"):
            run_state.set_direction(Direction.UP)
        elif actions.pressed("move_down"):
            run_state.set_direction(Direction.DOWN)
        elif actions.pressed("move_left"):
            run_state.set_direction(Direction.LEFT)
        elif actions.pressed("move_right"):
            run_state.set_direction(Direction.RIGHT)

    def update(self, dt_ticks: int) -> None:
        run_state = self._run_state()
        if run_state.phase != "active":
            self._record_finished_run()
            return

        profile = self._profile()
        effective_speed = clamp_speed(profile.snake_speed_fps + run_state.loadout.speed_delta)
        self.tick_accumulator += effective_speed * dt_ticks
        while self.tick_accumulator >= 30 and run_state.phase == "active":
            self.tick_accumulator -= 30
            run_state.step()
        if run_state.phase != "active":
            self._record_finished_run()

    def draw(self, renderer: Renderer) -> None:
        run_state = self._run_state()
        profile = self._profile()
        renderer.clear(0)

        renderer.text(8, 5, "ULAR CYBER-ROGUELITE", 11)
        renderer.rectb(
            PLAYFIELD_X - 1,
            PLAYFIELD_Y - 1,
            run_state.width * CELL_SIZE + 2,
            run_state.height * CELL_SIZE + 2,
            5,
        )

        for hazard in run_state.hazards:
            self._draw_cell(renderer, hazard.cell.x, hazard.cell.y, 10 if hazard.phase == "warning" else 8)

        if run_state.food is not None:
            self._draw_cell(renderer, run_state.food.x, run_state.food.y, 9)

        if run_state.boss.active and run_state.boss.target is not None:
            self._draw_cell(renderer, run_state.boss.target.x, run_state.boss.target.y, 12)

        for index, cell in enumerate(reversed(run_state.snake)):
            color = 11 if index == len(run_state.snake) - 1 else 3
            self._draw_cell(renderer, cell.x, cell.y, color)

        renderer.rect(HUD_X - 4, 0, 68, 160, 1)
        renderer.text(HUD_X, 8, "RUN", 10)
        renderer.text(HUD_X, 21, f"Score {run_state.score}", 7)
        renderer.text(HUD_X, 32, f"Len {len(run_state.snake)}", 7)
        renderer.text(HUD_X, 43, f"Speed {profile.snake_speed_fps}", 7)
        renderer.text(HUD_X, 54, f"Heat {run_state.heat}", 10)
        renderer.text(HUD_X, 65, f"Shield {run_state.shield}", 12 if run_state.shield else 6)
        renderer.text(HUD_X, 76, f"Boss {run_state.boss.hp if run_state.boss.active else '-'}", 12)
        renderer.text(HUD_X, 87, f"Scrap {run_state.finish_scrap()}", 10)
        renderer.text(HUD_X, 99, run_state.phase[:10], 6)

        self._draw_module_names(renderer, run_state)

        if run_state.phase == "reward":
            self._draw_rewards(renderer, run_state)
        elif run_state.phase == "game_over":
            renderer.text(58, 72, "RUN ENDED", 10)
            renderer.text(42, 86, "Space/Enter restart", 7)
            renderer.text(54, 98, "Esc returns lab", 5)
        elif run_state.phase == "cleared":
            renderer.text(64, 72, "CLEARED", 11)
            renderer.text(42, 86, "Space/Enter restart", 7)

        if self.context.debug_console.enabled:
            renderer.text(4, 4, "DEV", 10)
            renderer.text(8, 150, "B boss H hazard G score R reward V shield C clear", 5)

    def _draw_cell(self, renderer: Renderer, x: int, y: int, color: int) -> None:
        renderer.rect(
            PLAYFIELD_X + x * CELL_SIZE,
            PLAYFIELD_Y + y * CELL_SIZE,
            CELL_SIZE - 1,
            CELL_SIZE - 1,
            color,
        )

    def _draw_rewards(self, renderer: Renderer, run_state: RunState) -> None:
        renderer.rect(28, 48, 140, 56, 1)
        renderer.rectb(28, 48, 140, 56, 10)
        renderer.text(58, 56, "CHOOSE REWARD", 10)
        for index, reward in enumerate(run_state.reward_choices):
            renderer.text(40, 70 + index * 10, f"{index + 1}: {reward.label}", 7)

    def _draw_module_names(self, renderer: Renderer, run_state: RunState) -> None:
        names = list(run_state.loadout.module_names.values())
        for index, name in enumerate(names[:4]):
            renderer.text(HUD_X, 116 + index * 10, name[:12], 5)

    def _handle_debug(self, actions: ActionSnapshot) -> None:
        run_state = self._run_state()
        if actions.pressed("debug_boss"):
            run_state.spawn_boss()
        if actions.pressed("debug_hazard"):
            run_state.spawn_hazard()
        if actions.pressed("debug_score"):
            run_state.score += 1
        if actions.pressed("debug_reward"):
            run_state.open_reward()
        if actions.pressed("debug_shield"):
            run_state.shield += 1
        if actions.pressed("debug_clear"):
            run_state.clear_hazards()

    def _restart_run(self) -> None:
        self._run_state().restart()
        self.run_recorded = False
        self.tick_accumulator = 0

    def _profile(self) -> Profile:
        return self.context.profile

    def _run_state(self) -> RunState:
        if self.run_state is None:
            raise RuntimeError("PlayScene entered without RunState")
        return self.run_state

    def _change_speed(self, delta: int) -> None:
        profile = self._profile()
        profile.snake_speed_fps = clamp_speed(profile.snake_speed_fps + delta)
        self.context.profile_store.save(profile)

    def _record_finished_run(self) -> None:
        if self.run_recorded:
            return
        run_state = self._run_state()
        if run_state.phase not in {"game_over", "cleared"}:
            return
        profile = self._profile()
        earned_scrap = run_state.finish_scrap()
        profile.total_runs += 1
        profile.best_score = max(profile.best_score, run_state.score)
        profile.scrap += earned_scrap
        if run_state.boss.defeated and "head_targeting_reticle" not in profile.unlocked_modules:
            profile.unlocked_modules.append("head_targeting_reticle")
        if run_state.boss.defeated:
            profile.materials["warden_capacitor"] = profile.materials.get("warden_capacitor", 0) + 1
        if profile.best_score >= 8 and "spine_overclock" not in profile.unlocked_modules:
            profile.unlocked_modules.append("spine_overclock")
        self.context.profile_store.save(profile)
        self.run_recorded = True


def speed_bounds() -> tuple[int, int]:
    return MIN_SPEED_FPS, MAX_SPEED_FPS
