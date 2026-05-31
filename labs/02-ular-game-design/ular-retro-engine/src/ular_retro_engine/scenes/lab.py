from __future__ import annotations

from ..input import ActionSnapshot
from ..modules import SLOTS, loadout_stats, normalize_loadout, power_budget
from ..profile import Profile
from ..scene import BaseScene, Renderer
from .play import PlayScene


class LabScene(BaseScene):
    name = "lab"

    def __init__(self) -> None:
        self.slot_index = 0

    def enter(self, context) -> None:
        super().enter(context)
        self._normalize_profile()

    def handle_input(self, actions: ActionSnapshot) -> None:
        if actions.pressed("confirm"):
            self.context.replace_scene(PlayScene())
        elif actions.pressed("cancel"):
            from .title import TitleScene

            self.context.replace_scene(TitleScene())
        elif actions.pressed("move_up"):
            self.slot_index = (self.slot_index - 1) % len(SLOTS)
        elif actions.pressed("move_down"):
            self.slot_index = (self.slot_index + 1) % len(SLOTS)
        elif actions.pressed("move_left"):
            self._cycle_module(-1)
        elif actions.pressed("move_right"):
            self._cycle_module(1)
        elif actions.pressed("buy_unlock"):
            self._buy_power_skill()

    def draw(self, renderer: Renderer) -> None:
        profile = self._profile()
        catalog = self.context.content_registry.module_catalog()
        stats = loadout_stats(catalog, profile.equipped_modules)
        budget = power_budget(profile.skill_nodes)

        renderer.clear(0)
        renderer.text(8, 6, "ULAR LAB", 11)
        renderer.text(8, 18, f"Scrap {profile.scrap}", 10)
        renderer.text(74, 18, f"Power {stats.power_used}/{budget}", 7 if stats.power_used <= budget else 8)
        renderer.text(150, 18, f"Best {profile.best_score}", 7)

        for index, slot in enumerate(SLOTS):
            y = 38 + index * 18
            module = catalog.by_id[profile.equipped_modules[slot]]
            color = 10 if index == self.slot_index else 7
            renderer.text(8, y, f"{'>' if index == self.slot_index else ' '} {slot}", color)
            renderer.text(58, y, module.name[:22], color)
            renderer.text(180, y, f"P{module.power_cost}", 6)

        renderer.text(8, 118, "Up/Down slot  Left/Right module", 5)
        renderer.text(8, 130, "Space play  U buy Aux Power Bus", 5)
        renderer.text(8, 142, "Esc title", 5)

        if "lab_power_budget_01" in profile.skill_nodes:
            renderer.text(146, 130, "Aux Bus owned", 11)
        else:
            renderer.text(146, 130, "Aux Bus 10", 10)

        if self.context.debug_console.enabled:
            renderer.text(4, 4, "DEV", 10)

    def _cycle_module(self, delta: int) -> None:
        profile = self._profile()
        catalog = self.context.content_registry.module_catalog()
        slot = SLOTS[self.slot_index]
        candidates = catalog.modules_for_slot(slot, profile.unlocked_modules)
        if not candidates:
            return
        current = profile.equipped_modules.get(slot)
        current_index = next((i for i, module in enumerate(candidates) if module.id == current), 0)
        profile.equipped_modules[slot] = candidates[(current_index + delta) % len(candidates)].id
        self.context.profile_store.save(profile)

    def _buy_power_skill(self) -> None:
        profile = self._profile()
        if "lab_power_budget_01" in profile.skill_nodes or profile.scrap < 10:
            return
        profile.scrap -= 10
        profile.skill_nodes.append("lab_power_budget_01")
        self.context.profile_store.save(profile)

    def _normalize_profile(self) -> None:
        profile = self._profile()
        catalog = self.context.content_registry.module_catalog()
        profile.equipped_modules = normalize_loadout(catalog, profile.unlocked_modules, profile.equipped_modules)
        self.context.profile_store.save(profile)

    def _profile(self) -> Profile:
        return self.context.profile
