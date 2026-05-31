from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .modules import ModuleCatalog

@dataclass(frozen=True)
class ContentRegistry:
    root: Path

    def resolve(self, relative_path: str) -> Path:
        return self.root / relative_path

    def exists(self) -> bool:
        return self.root.exists()

    def module_catalog(self) -> ModuleCatalog:
        return ModuleCatalog.load(self.resolve("modules.json"))
