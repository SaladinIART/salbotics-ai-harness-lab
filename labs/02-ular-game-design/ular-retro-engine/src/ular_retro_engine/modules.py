from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


SLOTS = ("head", "core", "spine", "tail")
STARTER_MODULES = {
    "head": "head_stock_sensor",
    "core": "core_light_battery",
    "spine": "spine_stabilizer",
    "tail": "tail_heat_sink",
}
STARTER_UNLOCKS = [
    "head_stock_sensor",
    "core_light_battery",
    "spine_stabilizer",
    "tail_heat_sink",
    "core_reactive_shield",
    "tail_scrap_magnet",
]
BASE_POWER_BUDGET = 6


@dataclass(frozen=True)
class ModuleEffect:
    type: str
    amount: int


@dataclass(frozen=True)
class ModuleDef:
    id: str
    name: str
    slot: str
    tier: int
    power_cost: int
    heat_cost: int
    tags: tuple[str, ...] = ()
    effects: tuple[ModuleEffect, ...] = ()


@dataclass
class LoadoutStats:
    starting_length: int = 4
    score_per_food: int = 1
    shield: int = 0
    speed_delta: int = 0
    heat_rate_delta: int = 0
    scrap_multiplier: int = 1
    power_used: int = 0
    heat_cost: int = 0
    module_names: dict[str, str] = field(default_factory=dict)


class ModuleCatalog:
    def __init__(self, modules: list[ModuleDef]) -> None:
        self.modules = modules
        self.by_id = {module.id: module for module in modules}

    @classmethod
    def load(cls, path: Path) -> "ModuleCatalog":
        data = json.loads(path.read_text(encoding="utf-8"))
        modules = []
        for item in data:
            effects = tuple(ModuleEffect(type=e["type"], amount=int(e["amount"])) for e in item.get("effects", []))
            modules.append(
                ModuleDef(
                    id=item["id"],
                    name=item["name"],
                    slot=item["slot"],
                    tier=int(item.get("tier", 1)),
                    power_cost=int(item.get("power_cost", 0)),
                    heat_cost=int(item.get("heat_cost", 0)),
                    tags=tuple(item.get("tags", [])),
                    effects=effects,
                )
            )
        catalog = cls(modules)
        catalog.validate()
        return catalog

    def validate(self) -> None:
        ids = set()
        for module in self.modules:
            if module.id in ids:
                raise ValueError(f"Duplicate module id: {module.id}")
            ids.add(module.id)
            if module.slot not in SLOTS:
                raise ValueError(f"Invalid slot for {module.id}: {module.slot}")

    def modules_for_slot(self, slot: str, unlocked: list[str]) -> list[ModuleDef]:
        unlocked_set = set(unlocked)
        return [module for module in self.modules if module.slot == slot and module.id in unlocked_set]

    def first_for_slot(self, slot: str, unlocked: list[str]) -> ModuleDef:
        candidates = self.modules_for_slot(slot, unlocked)
        if not candidates:
            return self.by_id[STARTER_MODULES[slot]]
        return candidates[0]


def power_budget(skill_nodes: list[str]) -> int:
    return BASE_POWER_BUDGET + (1 if "lab_power_budget_01" in skill_nodes else 0)


def normalize_loadout(catalog: ModuleCatalog, unlocked: list[str], equipped: dict[str, str]) -> dict[str, str]:
    unlocked_set = set(unlocked) or set(STARTER_UNLOCKS)
    normalized: dict[str, str] = {}
    for slot in SLOTS:
        module_id = equipped.get(slot, STARTER_MODULES[slot])
        module = catalog.by_id.get(module_id)
        if module is None or module.slot != slot or module_id not in unlocked_set:
            module = catalog.first_for_slot(slot, list(unlocked_set))
        normalized[slot] = module.id
    return normalized


def loadout_stats(catalog: ModuleCatalog, equipped: dict[str, str]) -> LoadoutStats:
    stats = LoadoutStats()
    for slot in SLOTS:
        module = catalog.by_id[equipped[slot]]
        stats.power_used += module.power_cost
        stats.heat_cost += module.heat_cost
        stats.module_names[slot] = module.name
        for effect in module.effects:
            if effect.type == "starting_length_delta":
                stats.starting_length += effect.amount
            elif effect.type == "score_per_food_delta":
                stats.score_per_food += effect.amount
            elif effect.type == "shield_delta":
                stats.shield += effect.amount
            elif effect.type == "speed_delta":
                stats.speed_delta += effect.amount
            elif effect.type == "heat_rate_delta":
                stats.heat_rate_delta += effect.amount
            elif effect.type == "scrap_multiplier_delta":
                stats.scrap_multiplier += effect.amount
    stats.starting_length = max(2, stats.starting_length)
    stats.score_per_food = max(1, stats.score_per_food)
    stats.scrap_multiplier = max(1, stats.scrap_multiplier)
    return stats
