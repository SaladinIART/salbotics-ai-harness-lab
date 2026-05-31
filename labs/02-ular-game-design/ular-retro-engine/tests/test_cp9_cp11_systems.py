from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ular_retro_engine.config import project_root
from ular_retro_engine.content import ContentRegistry
from ular_retro_engine.input import ActionSnapshot
from ular_retro_engine.modules import STARTER_MODULES, loadout_stats, normalize_loadout, power_budget
from ular_retro_engine.profile import Profile, ProfileStore
from ular_retro_engine.run_state import Cell, Hazard, RunState
from ular_retro_engine.scene import SceneContext
from ular_retro_engine.scenes.lab import LabScene
from ular_retro_engine.scenes.play import PlayScene


def content_registry() -> ContentRegistry:
    return ContentRegistry(project_root() / "content")


class Cp9ModuleTests(unittest.TestCase):
    def test_module_catalog_loads_and_validates_content(self) -> None:
        catalog = content_registry().module_catalog()

        self.assertIn("core_reactive_shield", catalog.by_id)
        self.assertEqual(catalog.by_id["tail_scrap_magnet"].slot, "tail")

    def test_loadout_stats_apply_module_effects(self) -> None:
        catalog = content_registry().module_catalog()
        equipped = dict(STARTER_MODULES)
        equipped["core"] = "core_reactive_shield"
        equipped["tail"] = "tail_scrap_magnet"

        stats = loadout_stats(catalog, equipped)

        self.assertEqual(stats.shield, 1)
        self.assertEqual(stats.scrap_multiplier, 2)
        self.assertGreaterEqual(stats.starting_length, 4)

    def test_normalize_loadout_replaces_locked_or_wrong_slot_module(self) -> None:
        catalog = content_registry().module_catalog()
        equipped = dict(STARTER_MODULES)
        equipped["head"] = "spine_overclock"

        normalized = normalize_loadout(catalog, ["head_stock_sensor"], equipped)

        self.assertEqual(normalized["head"], "head_stock_sensor")


class Cp10ChallengeTests(unittest.TestCase):
    def test_active_hazard_consumes_shield_before_game_over(self) -> None:
        state = RunState(seed=1)
        state.shield = 1
        target = state.head.moved(state.direction)
        state.hazards = [Hazard(cell=target, phase="active", ticks=3)]

        state.step()

        self.assertEqual(state.phase, "active")
        self.assertEqual(state.shield, 0)

    def test_active_hazard_ends_run_without_shield(self) -> None:
        state = RunState(seed=1)
        target = state.head.moved(state.direction)
        state.hazards = [Hazard(cell=target, phase="active", ticks=3)]

        state.step()

        self.assertEqual(state.phase, "game_over")

    def test_reward_choice_applies_effect_and_resumes_run(self) -> None:
        state = RunState(seed=1)
        state.open_reward()

        state.choose_reward(0)

        self.assertEqual(state.phase, "active")
        self.assertEqual(state.reward_choices, [])

    def test_boss_defeat_opens_reward_and_grants_scrap_bonus(self) -> None:
        state = RunState(seed=1)
        state.spawn_boss()
        state.boss.hp = 1
        state.boss.target = state.head.moved(state.direction)

        state.step()

        self.assertTrue(state.boss.defeated)
        self.assertEqual(state.phase, "reward")
        self.assertGreaterEqual(state.bonus_scrap, 10)


class Cp11CampaignTests(unittest.TestCase):
    def test_lab_purchase_adds_power_budget_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = Profile(scrap=10)
            store = ProfileStore(Path(tmp) / "profile.json")
            store.save(profile)
            scene = LabScene()
            scene.enter(make_context(store, profile))

            scene.handle_input(ActionSnapshot(frozenset({"buy_unlock"}), frozenset()))

            self.assertIn("lab_power_budget_01", profile.skill_nodes)
            self.assertEqual(profile.scrap, 0)
            self.assertEqual(power_budget(profile.skill_nodes), 7)

    def test_finished_boss_run_adds_scrap_unlock_and_material(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = Profile()
            store = ProfileStore(Path(tmp) / "profile.json")
            store.save(profile)
            scene = PlayScene()
            scene.enter(make_context(store, profile))
            scene.run_state.score = 8
            scene.run_state.bonus_scrap = 10
            scene.run_state.boss.defeated = True
            scene.run_state.phase = "game_over"

            scene.update(1)

            self.assertGreaterEqual(profile.scrap, 18)
            self.assertIn("head_targeting_reticle", profile.unlocked_modules)
            self.assertIn("spine_overclock", profile.unlocked_modules)
            self.assertEqual(profile.materials["warden_capacitor"], 1)


def make_context(store: ProfileStore, profile: Profile) -> SceneContext:
    return SceneContext(
        replace_scene=lambda scene: None,
        push_scene=lambda scene: None,
        pop_scene=lambda: None,
        quit_app=lambda: None,
        profile=profile,
        profile_store=store,
        content_registry=content_registry(),
        debug_console=type("Debug", (), {"enabled": False})(),
    )


if __name__ == "__main__":
    unittest.main()
