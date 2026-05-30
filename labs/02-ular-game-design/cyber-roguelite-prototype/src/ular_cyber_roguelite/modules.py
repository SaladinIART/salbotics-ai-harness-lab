from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModuleSlot(Enum):
    HEAD = "head"
    CORE = "core"
    SPINE = "spine"
    TAIL = "tail"


SLOT_ORDER = (
    ModuleSlot.HEAD,
    ModuleSlot.CORE,
    ModuleSlot.SPINE,
    ModuleSlot.TAIL,
)


@dataclass(frozen=True)
class ModuleEffects:
    score_per_food_delta: int = 0
    growth_per_food_delta: int = 0
    shield_charges_delta: int = 0
    starting_length_delta: int = 0
    fps_delta: int = 0
    scrap_multiplier_delta: int = 0


@dataclass(frozen=True)
class RunModifiers:
    score_per_food: int = 1
    growth_per_food: int = 1
    shield_charges: int = 0
    starting_length_bonus: int = 0
    fps_delta: int = 0
    scrap_multiplier: int = 1


@dataclass(frozen=True)
class ModuleDefinition:
    module_id: str
    slot: ModuleSlot
    name: str
    summary: str
    tradeoff: str
    effects: ModuleEffects


STARTER_MODULES: tuple[ModuleDefinition, ...] = (
    ModuleDefinition(
        module_id="stock_head",
        slot=ModuleSlot.HEAD,
        name="Stock Sensor",
        summary="Baseline steering optics.",
        tradeoff="No bonus.",
        effects=ModuleEffects(),
    ),
    ModuleDefinition(
        module_id="targeting_reticle",
        slot=ModuleSlot.HEAD,
        name="Targeting Reticle",
        summary="+1 score per food.",
        tradeoff="Shorter starting body.",
        effects=ModuleEffects(score_per_food_delta=1, starting_length_delta=-1),
    ),
    ModuleDefinition(
        module_id="stock_core",
        slot=ModuleSlot.CORE,
        name="Stock Core",
        summary="Reliable base reactor.",
        tradeoff="No shield.",
        effects=ModuleEffects(),
    ),
    ModuleDefinition(
        module_id="reactive_shield_core",
        slot=ModuleSlot.CORE,
        name="Reactive Shield Core",
        summary="Blocks one fatal collision per run.",
        tradeoff="Starts longer and harder to steer.",
        effects=ModuleEffects(shield_charges_delta=1, starting_length_delta=1),
    ),
    ModuleDefinition(
        module_id="stock_spine",
        slot=ModuleSlot.SPINE,
        name="Stock Spine",
        summary="Stable movement cadence.",
        tradeoff="No speed bonus.",
        effects=ModuleEffects(),
    ),
    ModuleDefinition(
        module_id="overclock_spine",
        slot=ModuleSlot.SPINE,
        name="Overclock Spine",
        summary="+1 score per food.",
        tradeoff="Run speed increases.",
        effects=ModuleEffects(score_per_food_delta=1, fps_delta=3),
    ),
    ModuleDefinition(
        module_id="stock_tail",
        slot=ModuleSlot.TAIL,
        name="Stock Tail",
        summary="Plain tail assembly.",
        tradeoff="No scrap bonus.",
        effects=ModuleEffects(),
    ),
    ModuleDefinition(
        module_id="scrap_magnet_tail",
        slot=ModuleSlot.TAIL,
        name="Scrap Magnet Tail",
        summary="Doubles scrap earned from score.",
        tradeoff="Starts one segment longer.",
        effects=ModuleEffects(scrap_multiplier_delta=1, starting_length_delta=1),
    ),
)


def default_module_catalog() -> dict[str, ModuleDefinition]:
    return {module.module_id: module for module in STARTER_MODULES}


def default_loadout() -> dict[str, str]:
    return {
        ModuleSlot.HEAD.value: "stock_head",
        ModuleSlot.CORE.value: "stock_core",
        ModuleSlot.SPINE.value: "stock_spine",
        ModuleSlot.TAIL.value: "stock_tail",
    }


def modules_for_slot(
    catalog: dict[str, ModuleDefinition],
    slot: ModuleSlot,
    unlocked_module_ids: set[str] | None = None,
) -> list[ModuleDefinition]:
    unlocked = unlocked_module_ids or set(catalog)
    return [
        module
        for module in catalog.values()
        if module.slot == slot and module.module_id in unlocked
    ]


def normalize_loadout(
    loadout: dict[str, str],
    catalog: dict[str, ModuleDefinition],
    unlocked_module_ids: set[str] | None = None,
) -> dict[str, str]:
    normalized = default_loadout()
    unlocked = unlocked_module_ids or set(catalog)
    for slot in SLOT_ORDER:
        selected_id = loadout.get(slot.value)
        selected = catalog.get(selected_id) if selected_id else None
        if selected and selected.slot == slot and selected.module_id in unlocked:
            normalized[slot.value] = selected.module_id
    return normalized


def compute_run_modifiers(
    loadout: dict[str, str],
    catalog: dict[str, ModuleDefinition],
) -> RunModifiers:
    score_per_food = 1
    growth_per_food = 1
    shield_charges = 0
    starting_length_bonus = 0
    fps_delta = 0
    scrap_multiplier = 1

    for module_id in loadout.values():
        module = catalog[module_id]
        score_per_food += module.effects.score_per_food_delta
        growth_per_food += module.effects.growth_per_food_delta
        shield_charges += module.effects.shield_charges_delta
        starting_length_bonus += module.effects.starting_length_delta
        fps_delta += module.effects.fps_delta
        scrap_multiplier += module.effects.scrap_multiplier_delta

    return RunModifiers(
        score_per_food=max(1, score_per_food),
        growth_per_food=max(1, growth_per_food),
        shield_charges=max(0, shield_charges),
        starting_length_bonus=starting_length_bonus,
        fps_delta=fps_delta,
        scrap_multiplier=max(1, scrap_multiplier),
    )


def cycle_module_id(
    current_module_id: str,
    slot_modules: list[ModuleDefinition],
    direction: int,
) -> str:
    if not slot_modules:
        return current_module_id

    module_ids = [module.module_id for module in slot_modules]
    if current_module_id not in module_ids:
        return module_ids[0]

    current_index = module_ids.index(current_module_id)
    return module_ids[(current_index + direction) % len(module_ids)]

