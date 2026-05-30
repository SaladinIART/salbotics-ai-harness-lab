from __future__ import annotations

import random
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ular_cyber_roguelite.config import GameConfig
from ular_cyber_roguelite.challenge import (
    BOSS_SCORE_THRESHOLD,
    HAZARD_WARNING_TICKS,
    apply_reward_choice,
    damage_boss,
    spawn_boss,
    spawn_hazard,
)
from ular_cyber_roguelite.domain import (
    BossState,
    Direction,
    GamePhase,
    GameState,
    HazardPatch,
    HazardPhase,
    RewardChoice,
    Snake,
)
from ular_cyber_roguelite.modules import (
    ModuleSlot,
    compute_run_modifiers,
    default_loadout,
    default_module_catalog,
)
from ular_cyber_roguelite.profile import (
    cycle_profile_slot,
    default_profile,
    adjust_speed,
    load_profile,
    record_run,
    save_profile,
)
from ular_cyber_roguelite.systems import (
    create_initial_state,
    current_fps,
    request_direction,
    spawn_food,
    start_or_restart,
    step,
)


class SystemTests(unittest.TestCase):
    def test_spawn_food_avoids_occupied_cells(self) -> None:
        config = GameConfig(grid_columns=3, grid_rows=2)
        occupied = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]

        food = spawn_food(config, occupied, random.Random(1))

        self.assertEqual(food, (2, 1))

    def test_spawn_food_returns_none_when_grid_full(self) -> None:
        config = GameConfig(grid_columns=2, grid_rows=2)
        occupied = [(0, 0), (1, 0), (0, 1), (1, 1)]

        self.assertIsNone(spawn_food(config, occupied, random.Random(1)))

    def test_direction_change_rejects_instant_reversal(self) -> None:
        config = GameConfig(grid_columns=6, grid_rows=6)
        state = create_initial_state(config, random.Random(1), phase=GamePhase.RUNNING)

        request_direction(state, Direction.LEFT)

        self.assertEqual(state.snake.direction, Direction.RIGHT)

    def test_step_moves_snake_without_growth(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            phase=GamePhase.RUNNING,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.snake.body, [(4, 3), (3, 3), (2, 3)])
        self.assertEqual(state.score, 0)
        self.assertEqual(state.phase, GamePhase.RUNNING)

    def test_food_increases_score_and_length(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(4, 3),
            phase=GamePhase.RUNNING,
        )

        step(state, config, random.Random(2))

        self.assertEqual(state.score, 1)
        self.assertEqual(len(state.snake.body), 4)
        self.assertNotIn(state.food, state.snake.body)

    def test_wall_collision_ends_run(self) -> None:
        config = GameConfig(grid_columns=5, grid_rows=5)
        state = GameState(
            snake=Snake(body=[(4, 2), (3, 2), (2, 2)], direction=Direction.RIGHT),
            food=(0, 0),
            phase=GamePhase.RUNNING,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.GAME_OVER)

    def test_self_collision_ends_run(self) -> None:
        config = GameConfig(grid_columns=6, grid_rows=6)
        state = GameState(
            snake=Snake(body=[(2, 2), (2, 3), (1, 3), (1, 2)], direction=Direction.DOWN),
            food=(5, 5),
            phase=GamePhase.RUNNING,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.GAME_OVER)

    def test_can_move_into_tail_cell_when_tail_will_move(self) -> None:
        config = GameConfig(grid_columns=6, grid_rows=6)
        state = GameState(
            snake=Snake(body=[(2, 2), (2, 3), (1, 3), (1, 2)], direction=Direction.LEFT),
            food=(5, 5),
            phase=GamePhase.RUNNING,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.snake.body, [(1, 2), (2, 2), (2, 3), (1, 3)])

    def test_cannot_move_into_tail_cell_when_growing(self) -> None:
        config = GameConfig(grid_columns=6, grid_rows=6)
        state = GameState(
            snake=Snake(body=[(2, 2), (2, 3), (1, 3), (1, 2)], direction=Direction.LEFT),
            food=(5, 5),
            phase=GamePhase.RUNNING,
            growth_pending=1,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.GAME_OVER)

    def test_start_or_restart_creates_running_state(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = create_initial_state(config, random.Random(1), phase=GamePhase.GAME_OVER)

        restarted = start_or_restart(config, state, random.Random(2))

        self.assertEqual(restarted.phase, GamePhase.RUNNING)
        self.assertEqual(restarted.score, 0)
        self.assertEqual(len(restarted.snake.body), 3)

    def test_module_loadout_changes_run_modifiers(self) -> None:
        catalog = default_module_catalog()
        loadout = default_loadout()
        loadout[ModuleSlot.HEAD.value] = "targeting_reticle"
        loadout[ModuleSlot.CORE.value] = "reactive_shield_core"
        loadout[ModuleSlot.SPINE.value] = "overclock_spine"
        loadout[ModuleSlot.TAIL.value] = "scrap_magnet_tail"

        modifiers = compute_run_modifiers(loadout, catalog)

        self.assertEqual(modifiers.score_per_food, 3)
        self.assertEqual(modifiers.shield_charges, 1)
        self.assertEqual(modifiers.starting_length_bonus, 1)
        self.assertEqual(modifiers.fps_delta, 3)
        self.assertEqual(modifiers.scrap_multiplier, 2)

    def test_initial_state_applies_starting_length_and_shields(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        catalog = default_module_catalog()
        loadout = default_loadout()
        loadout[ModuleSlot.CORE.value] = "reactive_shield_core"
        modifiers = compute_run_modifiers(loadout, catalog)

        state = create_initial_state(config, random.Random(1), GamePhase.RUNNING, modifiers, loadout)

        self.assertEqual(len(state.snake.body), 4)
        self.assertEqual(state.shield_charges, 1)

    def test_shield_blocks_one_wall_collision(self) -> None:
        config = GameConfig(grid_columns=5, grid_rows=5)
        catalog = default_module_catalog()
        loadout = default_loadout()
        loadout[ModuleSlot.CORE.value] = "reactive_shield_core"
        modifiers = compute_run_modifiers(loadout, catalog)
        state = GameState(
            snake=Snake(body=[(4, 2), (3, 2), (2, 2)], direction=Direction.RIGHT),
            food=(0, 0),
            phase=GamePhase.RUNNING,
            loadout=loadout,
            modifiers=modifiers,
            shield_charges=modifiers.shield_charges,
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.shield_charges, 0)
        self.assertEqual(state.snake.direction, Direction.LEFT)

    def test_module_score_and_growth_apply_when_eating(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        catalog = default_module_catalog()
        loadout = default_loadout()
        loadout[ModuleSlot.HEAD.value] = "targeting_reticle"
        modifiers = compute_run_modifiers(loadout, catalog)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(4, 3),
            phase=GamePhase.RUNNING,
            loadout=loadout,
            modifiers=modifiers,
        )

        step(state, config, random.Random(2))

        self.assertEqual(state.score, 2)
        self.assertEqual(len(state.snake.body), 4)

    def test_overclock_spine_changes_current_fps(self) -> None:
        config = GameConfig(fps=8)
        catalog = default_module_catalog()
        loadout = default_loadout()
        loadout[ModuleSlot.SPINE.value] = "overclock_spine"
        state = create_initial_state(
            config,
            random.Random(1),
            GamePhase.RUNNING,
            compute_run_modifiers(loadout, catalog),
            loadout,
        )

        self.assertEqual(current_fps(config, state), 11)

    def test_custom_speed_changes_current_fps(self) -> None:
        config = GameConfig(fps=8)
        state = create_initial_state(config, random.Random(1), GamePhase.RUNNING, speed_fps=12)

        self.assertEqual(current_fps(config, state), 12)


class ProfileTests(unittest.TestCase):
    def test_profile_round_trip(self) -> None:
        catalog = default_module_catalog()
        profile = default_profile(catalog)
        profile.scrap = 12
        profile.snake_speed_fps = 11
        profile.loadout[ModuleSlot.TAIL.value] = "scrap_magnet_tail"

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "profile.json"
            save_profile(profile, path)
            loaded = load_profile(path, catalog)

        self.assertEqual(loaded.scrap, 12)
        self.assertEqual(loaded.snake_speed_fps, 11)
        self.assertEqual(loaded.loadout[ModuleSlot.TAIL.value], "scrap_magnet_tail")

    def test_adjust_speed_clamps_to_playable_range(self) -> None:
        profile = default_profile(default_module_catalog())

        adjust_speed(profile, 99)
        self.assertEqual(profile.snake_speed_fps, 18)

        adjust_speed(profile, -99)
        self.assertEqual(profile.snake_speed_fps, 5)

    def test_cycle_profile_slot_selects_next_module(self) -> None:
        catalog = default_module_catalog()
        profile = default_profile(catalog)

        cycle_profile_slot(profile, ModuleSlot.HEAD, 1, catalog)

        self.assertEqual(profile.loadout[ModuleSlot.HEAD.value], "targeting_reticle")

    def test_record_run_awards_scrap_and_best_stats(self) -> None:
        catalog = default_module_catalog()
        profile = default_profile(catalog)
        loadout = default_loadout()
        loadout[ModuleSlot.TAIL.value] = "scrap_magnet_tail"
        modifiers = compute_run_modifiers(loadout, catalog)
        state = GameState(
            snake=Snake(body=[(2, 2), (1, 2), (0, 2), (0, 1)], direction=Direction.RIGHT),
            food=(5, 5),
            score=5,
            phase=GamePhase.GAME_OVER,
            loadout=loadout,
            modifiers=modifiers,
        )

        earned = record_run(profile, state)

        self.assertEqual(earned, 10)
        self.assertEqual(profile.scrap, 10)
        self.assertEqual(profile.total_runs, 1)
        self.assertEqual(profile.best_score, 5)
        self.assertEqual(profile.best_length, 4)


class ChallengeTests(unittest.TestCase):
    def test_warning_hazard_is_telegraphed_before_it_is_lethal(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            phase=GamePhase.RUNNING,
            hazards=[HazardPatch(cells=((4, 3),), phase=HazardPhase.WARNING, ticks_remaining=2)],
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.snake.head, (4, 3))

    def test_active_hazard_ends_run(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            phase=GamePhase.RUNNING,
            hazards=[HazardPatch(cells=((4, 3),), phase=HazardPhase.ACTIVE, ticks_remaining=3)],
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.GAME_OVER)

    def test_shield_absorbs_active_hazard(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            phase=GamePhase.RUNNING,
            shield_charges=1,
            hazards=[HazardPatch(cells=((4, 3),), phase=HazardPhase.ACTIVE, ticks_remaining=3)],
        )

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.shield_charges, 0)
        self.assertEqual(state.snake.body, [(3, 3), (2, 3), (1, 3)])

    def test_spawn_hazard_uses_warning_phase_and_avoids_occupied_cells(self) -> None:
        config = GameConfig(grid_columns=4, grid_rows=4)
        state = GameState(
            snake=Snake(body=[(0, 0), (1, 0), (2, 0)], direction=Direction.RIGHT),
            food=(3, 0),
            phase=GamePhase.RUNNING,
            heat_level=2,
        )

        hazard = spawn_hazard(state, config, random.Random(1))

        self.assertIsNotNone(hazard)
        self.assertEqual(hazard.phase, HazardPhase.WARNING)
        self.assertEqual(hazard.ticks_remaining, HAZARD_WARNING_TICKS)
        self.assertTrue(set(hazard.cells).isdisjoint({(0, 0), (1, 0), (2, 0), (3, 0)}))

    def test_milestone_score_opens_reward_choice(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(4, 3),
            score=7,
            phase=GamePhase.RUNNING,
            next_reward_score=8,
        )

        step(state, config, random.Random(2))

        self.assertEqual(state.phase, GamePhase.REWARD)
        self.assertEqual(len(state.reward_choices), 3)
        self.assertEqual(state.next_reward_score, 16)

    def test_boss_spawns_before_reward_pauses_threshold_run(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(4, 3),
            score=BOSS_SCORE_THRESHOLD - 1,
            phase=GamePhase.RUNNING,
            next_reward_score=BOSS_SCORE_THRESHOLD,
        )

        step(state, config, random.Random(2))

        self.assertEqual(state.phase, GamePhase.REWARD)
        self.assertIsNotNone(state.boss)
        self.assertEqual(state.boss.hp, 3)

    def test_reward_choice_applies_shield_and_resumes_run(self) -> None:
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            phase=GamePhase.REWARD,
            reward_choices=[
                RewardChoice(
                    reward_id="emergency_shield",
                    name="Emergency Shield",
                    summary="+1 shield charge.",
                )
            ],
        )

        apply_reward_choice(state, 0)

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.shield_charges, 1)
        self.assertEqual(state.rewards_taken, ["emergency_shield"])

    def test_boss_spawns_and_takes_damage(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(3, 3), (2, 3), (1, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            score=12,
            phase=GamePhase.RUNNING,
            next_reward_score=18,
        )

        boss = spawn_boss(state, config, random.Random(1))
        self.assertIsNotNone(boss)
        state.boss.position = (4, 3)

        step(state, config, random.Random(1))

        self.assertEqual(state.phase, GamePhase.RUNNING)
        self.assertEqual(state.boss.hp, 2)
        self.assertEqual(state.score, 14)

    def test_defeating_boss_opens_reward_choice(self) -> None:
        config = GameConfig(grid_columns=8, grid_rows=8)
        state = GameState(
            snake=Snake(body=[(4, 3), (3, 3), (2, 3)], direction=Direction.RIGHT),
            food=(7, 7),
            score=12,
            phase=GamePhase.RUNNING,
            boss=BossState(
                name="Circuit Warden",
                position=(5, 3),
                hp=1,
                max_hp=3,
            ),
        )

        damage_boss(state, config, random.Random(1))

        self.assertTrue(state.boss_defeated)
        self.assertIsNone(state.boss)
        self.assertEqual(state.phase, GamePhase.REWARD)
        self.assertEqual(len(state.reward_choices), 3)


if __name__ == "__main__":
    unittest.main()
