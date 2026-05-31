from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ular_retro_engine.config import project_root
from ular_retro_engine.content import ContentRegistry
from ular_retro_engine.input import ActionSnapshot
from ular_retro_engine.profile import MAX_SPEED_FPS, MIN_SPEED_FPS, Profile, ProfileStore
from ular_retro_engine.run_state import Cell, Direction, RunState
from ular_retro_engine.scene import SceneContext
from ular_retro_engine.scenes.play import PlayScene


class Cp8RunStateTests(unittest.TestCase):
    def test_snake_moves_one_cell_per_step(self) -> None:
        state = RunState(seed=1)
        start = state.head

        state.step()

        self.assertEqual(state.head, Cell(start.x + 1, start.y))
        self.assertEqual(len(state.snake), state.length_target)

    def test_reversal_guard_blocks_instant_turnaround(self) -> None:
        state = RunState(seed=1)

        state.set_direction(Direction.LEFT)
        state.step()

        self.assertEqual(state.direction, Direction.RIGHT)

    def test_food_increases_score_and_length_target(self) -> None:
        state = RunState(seed=1)
        state.food = state.head.moved(Direction.RIGHT)

        state.step()

        self.assertEqual(state.score, 1)
        self.assertEqual(state.length_target, 5)
        self.assertEqual(len(state.snake), 5)
        self.assertIsNotNone(state.food)

    def test_wall_collision_ends_run(self) -> None:
        state = RunState(width=5, height=5, seed=1)
        state.snake = [Cell(4, 2), Cell(3, 2), Cell(2, 2), Cell(1, 2)]
        state.food = Cell(0, 0)

        state.step()

        self.assertEqual(state.phase, "game_over")

    def test_self_collision_ends_run(self) -> None:
        state = RunState(width=8, height=8, seed=1)
        state.snake = [Cell(4, 4), Cell(4, 5), Cell(3, 5), Cell(3, 4), Cell(3, 3)]
        state.direction = Direction.UP
        state.pending_direction = Direction.LEFT
        state.food = Cell(7, 7)
        state.length_target = len(state.snake)

        state.step()

        self.assertEqual(state.phase, "game_over")

    def test_tail_safe_movement_is_allowed(self) -> None:
        state = RunState(width=8, height=8, seed=1)
        state.snake = [Cell(4, 4), Cell(4, 5), Cell(3, 5), Cell(3, 4)]
        state.direction = Direction.UP
        state.pending_direction = Direction.LEFT
        state.food = Cell(7, 7)
        state.length_target = len(state.snake)

        state.step()

        self.assertEqual(state.phase, "active")
        self.assertEqual(state.head, Cell(3, 4))

    def test_restart_resets_score_and_advances_seed(self) -> None:
        state = RunState(seed=9)
        state.score = 3
        state.phase = "game_over"

        state.restart()

        self.assertEqual(state.phase, "active")
        self.assertEqual(state.score, 0)
        self.assertEqual(state.seed, 10)


class Cp8PlaySceneTests(unittest.TestCase):
    def test_speed_changes_are_clamped_and_saved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(Path(tmp) / "profile.json")
            profile = Profile(snake_speed_fps=MAX_SPEED_FPS)
            store.save(profile)
            scene = PlayScene()
            scene.enter(self._context(store, profile))

            scene.handle_input(ActionSnapshot(frozenset({"speed_up"}), frozenset()))
            self.assertEqual(profile.snake_speed_fps, MAX_SPEED_FPS)

            profile.snake_speed_fps = MIN_SPEED_FPS
            scene.handle_input(ActionSnapshot(frozenset({"speed_down"}), frozenset()))
            self.assertEqual(profile.snake_speed_fps, MIN_SPEED_FPS)

            saved = store.load()
            self.assertEqual(saved.snake_speed_fps, MIN_SPEED_FPS)

    def test_finished_run_updates_profile_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = ProfileStore(Path(tmp) / "profile.json")
            profile = Profile()
            store.save(profile)
            scene = PlayScene()
            scene.enter(self._context(store, profile))
            scene.run_state.score = 4
            scene.run_state.phase = "game_over"

            scene.update(1)
            scene.update(1)

            self.assertEqual(profile.total_runs, 1)
            self.assertEqual(profile.best_score, 4)

    def _context(self, store: ProfileStore, profile: Profile) -> SceneContext:
        return SceneContext(
            replace_scene=lambda scene: None,
            push_scene=lambda scene: None,
            pop_scene=lambda: None,
            quit_app=lambda: None,
            profile=profile,
            profile_store=store,
            content_registry=ContentRegistry(project_root() / "content"),
            debug_console=type("Debug", (), {"enabled": False})(),
        )


if __name__ == "__main__":
    unittest.main()
