from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .modules import STARTER_MODULES, STARTER_UNLOCKS


MIN_SPEED_FPS = 5
MAX_SPEED_FPS = 18
DEFAULT_SPEED_FPS = 8


def clamp_speed(value: int) -> int:
    return max(MIN_SPEED_FPS, min(MAX_SPEED_FPS, value))


@dataclass
class Profile:
    version: int = 1
    total_runs: int = 0
    best_score: int = 0
    scrap: int = 0
    snake_speed_fps: int = DEFAULT_SPEED_FPS
    unlocked_modules: list[str] = field(default_factory=lambda: list(STARTER_UNLOCKS))
    equipped_modules: dict[str, str] = field(default_factory=lambda: dict(STARTER_MODULES))
    skill_nodes: list[str] = field(default_factory=list)
    materials: dict[str, int] = field(default_factory=dict)
    developer_mode: bool = False


class ProfileStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def default_profile(self) -> Profile:
        return Profile()

    def load(self) -> Profile:
        if not self.path.exists():
            profile = self.default_profile()
            self.save(profile)
            return profile

        data = json.loads(self.path.read_text(encoding="utf-8"))
        return Profile(
            version=int(data.get("version", 1)),
            total_runs=int(data.get("total_runs", 0)),
            best_score=int(data.get("best_score", 0)),
            scrap=int(data.get("scrap", 0)),
            snake_speed_fps=clamp_speed(int(data.get("snake_speed_fps", DEFAULT_SPEED_FPS))),
            unlocked_modules=list(data.get("unlocked_modules", STARTER_UNLOCKS)),
            equipped_modules=dict(data.get("equipped_modules", STARTER_MODULES)),
            skill_nodes=list(data.get("skill_nodes", [])),
            materials=dict(data.get("materials", {})),
            developer_mode=bool(data.get("developer_mode", False)),
        )

    def save(self, profile: Profile) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(asdict(profile), indent=2, sort_keys=True),
            encoding="utf-8",
        )
