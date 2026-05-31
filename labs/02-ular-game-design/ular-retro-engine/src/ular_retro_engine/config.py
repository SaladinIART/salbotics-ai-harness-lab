from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    title: str = "Ular Retro Engine"
    width: int = 240
    height: int = 160
    fps: int = 30
    display_scale: int = 3
    content_dir: Path = Path("content")
    saves_dir: Path = Path("saves")
    profile_name: str = "profile.json"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_config(root: Path | None = None) -> AppConfig:
    base = root or project_root()
    return AppConfig(
        content_dir=base / "content",
        saves_dir=base / "saves",
    )
