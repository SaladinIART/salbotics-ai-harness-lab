from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .domain import GameState
from .modules import (
    ModuleDefinition,
    ModuleSlot,
    cycle_module_id,
    default_loadout,
    default_module_catalog,
    modules_for_slot,
    normalize_loadout,
)


PROFILE_VERSION = 1


@dataclass
class PlayerProfile:
    version: int = PROFILE_VERSION
    scrap: int = 0
    total_runs: int = 0
    best_score: int = 0
    best_length: int = 0
    snake_speed_fps: int = 8
    unlocked_modules: list[str] = field(default_factory=list)
    loadout: dict[str, str] = field(default_factory=default_loadout)


def default_profile(catalog: dict[str, ModuleDefinition] | None = None) -> PlayerProfile:
    catalog = catalog or default_module_catalog()
    unlocked_modules = list(catalog.keys())
    return PlayerProfile(
        unlocked_modules=unlocked_modules,
        loadout=normalize_loadout(default_loadout(), catalog, set(unlocked_modules)),
    )


def default_profile_path() -> Path:
    return Path(__file__).resolve().parents[2] / "saves" / "profile.json"


def load_profile(
    path: Path | None = None,
    catalog: dict[str, ModuleDefinition] | None = None,
) -> PlayerProfile:
    catalog = catalog or default_module_catalog()
    path = path or default_profile_path()
    if not path.exists():
        return default_profile(catalog)

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default_profile(catalog)

    unlocked = [module_id for module_id in raw.get("unlocked_modules", []) if module_id in catalog]
    if not unlocked:
        unlocked = list(catalog.keys())

    return PlayerProfile(
        version=PROFILE_VERSION,
        scrap=max(0, int(raw.get("scrap", 0))),
        total_runs=max(0, int(raw.get("total_runs", 0))),
        best_score=max(0, int(raw.get("best_score", 0))),
        best_length=max(0, int(raw.get("best_length", 0))),
        snake_speed_fps=max(5, min(18, int(raw.get("snake_speed_fps", 8)))),
        unlocked_modules=unlocked,
        loadout=normalize_loadout(raw.get("loadout", {}), catalog, set(unlocked)),
    )


def save_profile(profile: PlayerProfile, path: Path | None = None) -> None:
    path = path or default_profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")


def cycle_profile_slot(
    profile: PlayerProfile,
    slot: ModuleSlot,
    direction: int,
    catalog: dict[str, ModuleDefinition],
) -> None:
    unlocked = set(profile.unlocked_modules)
    slot_modules = modules_for_slot(catalog, slot, unlocked)
    current_module_id = profile.loadout.get(slot.value, "")
    profile.loadout[slot.value] = cycle_module_id(current_module_id, slot_modules, direction)


def record_run(profile: PlayerProfile, state: GameState) -> int:
    earned_scrap = state.score * state.modifiers.scrap_multiplier
    profile.scrap += earned_scrap
    profile.total_runs += 1
    profile.best_score = max(profile.best_score, state.score)
    profile.best_length = max(profile.best_length, len(state.snake.body))
    return earned_scrap


def adjust_speed(profile: PlayerProfile, amount: int) -> None:
    profile.snake_speed_fps = max(5, min(18, profile.snake_speed_fps + amount))
